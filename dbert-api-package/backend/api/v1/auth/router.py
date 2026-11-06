import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from backend.core.config import settings
from backend.core.database import get_db
from backend.core.security import (
    verify_password, hash_password, is_legacy_hash,
    create_access_token, create_refresh_token, decode_token
)
from backend.core.middleware import check_rate_limit
from backend.core.dependencies import get_current_user_token
from backend.models.auth import (
    InternAccount, Company, Mentor, StaffAccount,
    MobileRefreshToken, PasswordReset, SignupOtp
)
from backend.schemas.auth import (
    LoginRequest, TokenResponse, RefreshRequest,
    SignupStage1Request, SignupStage2Request, SignupStage3Request,
    CompanySignupRequest, CheckEmailRequest, ForgotPasswordRequest,
    ResetPasswordRequest, OtpSendRequest, OtpVerifyRequest
)

router = APIRouter(prefix="/auth", tags=["Auth & Security"])

def get_ip(request: Request) -> str:
    return request.headers.get("X-Real-IP") or request.headers.get("X-Forwarded-For") or (request.client.host if request.client else "unknown")

@router.post("/intern/login", response_model=TokenResponse, summary="Intern Login")
async def intern_login(req: LoginRequest, request: Request, db: AsyncSession = Depends(get_db)):
    ip = get_ip(request)
    if not check_rate_limit(f"login_ip:{ip}", settings.RL_LOGIN_IP_LIMIT, settings.RL_LOGIN_IP_WINDOW):
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many login attempts. Please try again later.")
    if not check_rate_limit(f"login_email:{req.email.lower()}", settings.RL_LOGIN_EMAIL_LIMIT, settings.RL_LOGIN_EMAIL_WINDOW):
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many failed attempts for this email.")

    stmt = select(InternAccount).where(InternAccount.email == req.email.lower().strip())
    result = await db.execute(stmt)
    intern = result.scalar_one_or_none()

    if not intern or not verify_password(intern.password_hash, req.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    if not intern.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is deactivated")

    # Lazy migration: re-hash legacy password to PBKDF2
    if is_legacy_hash(intern.password_hash):
        intern.password_hash = hash_password(req.password)
        await db.commit()

    token_data = {"sub": str(intern.id), "email": intern.email, "role": "intern", "name": intern.name}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    # Store refresh token record
    rf_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
    exp_time = datetime.now(timezone.utc) + timedelta(seconds=settings.REFRESH_TOKEN_TTL)
    db.add(MobileRefreshToken(
        token_hash=rf_hash,
        intern_id=str(intern.id),
        email=intern.email,
        expires_at=exp_time
    ))
    await db.commit()

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_TTL,
        user={"id": intern.id, "email": intern.email, "name": intern.name, "role": "intern", "stage": intern.signup_stage}
    )

@router.post("/company/login", response_model=TokenResponse, summary="Company Employer Login")
async def company_login(req: LoginRequest, request: Request, db: AsyncSession = Depends(get_db)):
    stmt = select(Company).where(Company.email == req.email.lower().strip())
    result = await db.execute(stmt)
    company = result.scalar_one_or_none()

    if not company or not verify_password(company.password_hash, req.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    if not company.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Company account is deactivated")

    token_data = {"sub": str(company.id), "email": company.email, "role": "company", "name": company.name}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_TTL,
        user={"id": company.id, "email": company.email, "name": company.name, "role": "company", "is_approved": company.is_approved}
    )

@router.post("/mentor/login", response_model=TokenResponse, summary="Mentor Login")
async def mentor_login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    stmt = select(Mentor).where(Mentor.email == req.email.lower().strip())
    result = await db.execute(stmt)
    mentor = result.scalar_one_or_none()

    if not mentor or not verify_password(mentor.password_hash, req.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    if not mentor.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Mentor account is deactivated")

    token_data = {"sub": str(mentor.id), "email": mentor.email, "role": "mentor", "name": mentor.name}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_TTL,
        user={"id": mentor.id, "email": mentor.email, "name": mentor.name, "role": "mentor", "domain": mentor.domain}
    )

@router.post("/staff/login", response_model=TokenResponse, summary="Staff Member Login")
async def staff_login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    stmt = select(StaffAccount).where(StaffAccount.email == req.email.lower().strip())
    result = await db.execute(stmt)
    staff = result.scalar_one_or_none()

    if not staff or not verify_password(staff.password_hash, req.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    if not staff.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Staff account is deactivated")

    token_data = {"sub": str(staff.id), "email": staff.email, "role": "staff", "name": staff.name}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_TTL,
        user={"id": staff.id, "email": staff.email, "name": staff.name, "role": "staff"}
    )

@router.post("/admin/login", response_model=TokenResponse, summary="Platform Administrator Login")
async def admin_login(req: LoginRequest):
    # Verify platform admin credentials against config
    username_match = (req.email.strip() == settings.ADMIN_USERNAME)
    password_match = verify_password(settings.ADMIN_PASSWORD, req.password) or (req.password == settings.ADMIN_PASSWORD)

    if not (username_match and password_match):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin credentials")

    token_data = {"sub": "admin", "email": f"{settings.ADMIN_USERNAME}@dbert.in", "role": "admin", "name": "DBERT Administrator"}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_TTL,
        user={"id": "admin", "email": f"{settings.ADMIN_USERNAME}@dbert.in", "name": "DBERT Administrator", "role": "admin"}
    )

@router.post("/refresh", response_model=TokenResponse, summary="Rotate and Refresh JWT Tokens")
async def refresh_tokens(req: RefreshRequest, db: AsyncSession = Depends(get_db)):
    try:
        payload = decode_token(req.refresh_token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")

    # Enforce server-side token store presence (Finding DBERT-010)
    rf_hash = hashlib.sha256(req.refresh_token.encode()).hexdigest()
    stmt = select(MobileRefreshToken).where(MobileRefreshToken.token_hash == rf_hash)
    res = await db.execute(stmt)
    token_record = res.scalar_one_or_none()
    if not token_record:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not recognized or already consumed"
        )
    if token_record.revoked:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has been revoked"
        )
    now = datetime.now(timezone.utc)
    if token_record.expires_at and token_record.expires_at < now:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired"
        )
    token_record.revoked = True

    # Generate new pair
    token_data = {"sub": payload.get("sub"), "email": payload.get("email"), "role": payload.get("role"), "name": payload.get("name")}
    new_access = create_access_token(token_data)
    new_refresh = create_refresh_token(token_data)

    # Store new refresh token
    new_hash = hashlib.sha256(new_refresh.encode()).hexdigest()
    exp_time = datetime.now(timezone.utc) + timedelta(seconds=settings.REFRESH_TOKEN_TTL)
    db.add(MobileRefreshToken(
        token_hash=new_hash,
        intern_id=str(payload.get("sub")),
        email=str(payload.get("email")),
        expires_at=exp_time
    ))
    await db.commit()

    return TokenResponse(
        access_token=new_access,
        refresh_token=new_refresh,
        expires_in=settings.ACCESS_TOKEN_TTL,
        user=token_data
    )

@router.post("/logout", summary="Logout and Revoke Token")
async def logout(
    current_user: Dict[str, Any] = Depends(get_current_user_token),
    db: AsyncSession = Depends(get_db)
):
    # Enforce server-side revocation of active sessions on logout (Finding DBERT-011)
    user_email = (current_user.get("email") or "").strip().lower()
    user_sub = str(current_user.get("sub", "")).strip()

    if user_email or user_sub:
        conditions = []
        if user_email:
            conditions.append(MobileRefreshToken.email == user_email)
        if user_sub:
            conditions.append(MobileRefreshToken.intern_id == user_sub)

        stmt = (
            update(MobileRefreshToken)
            .where(
                MobileRefreshToken.revoked == False,
                select(MobileRefreshToken.id).where(*conditions).exists() if False else (
                    (MobileRefreshToken.email == user_email) if user_email else (MobileRefreshToken.intern_id == user_sub)
                )
            )
            .values(revoked=True)
        )
        await db.execute(stmt)
        await db.commit()

    return {"status": "success", "message": "Successfully logged out and session revoked"}

@router.post("/signup/stage1", response_model=TokenResponse, summary="Intern Signup Stage 1")
async def signup_stage1(req: SignupStage1Request, db: AsyncSession = Depends(get_db)):
    stmt = select(InternAccount).where(InternAccount.email == req.email.lower().strip())
    res = await db.execute(stmt)
    if res.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="An account with this email already exists")

    new_intern = InternAccount(
        name=req.name.strip(),
        email=req.email.lower().strip(),
        phone=req.phone.strip(),
        password_hash=hash_password(req.password),
        password_set=True,
        signup_stage=1,
        referral_code=req.referral_code
    )
    db.add(new_intern)
    await db.commit()
    await db.refresh(new_intern)

    token_data = {"sub": str(new_intern.id), "email": new_intern.email, "role": "intern", "name": new_intern.name}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_TTL,
        user={"id": new_intern.id, "email": new_intern.email, "name": new_intern.name, "role": "intern", "stage": 1}
    )

@router.post("/signup/stage2", summary="Intern Signup Stage 2 (Domain & Profile)")
async def signup_stage2(
    req: SignupStage2Request,
    current_user: Dict[str, Any] = Depends(get_current_user_token),
    db: AsyncSession = Depends(get_db)
):
    intern_id = int(current_user.get("sub"))
    stmt = select(InternAccount).where(InternAccount.id == intern_id)
    res = await db.execute(stmt)
    intern = res.scalar_one_or_none()
    if not intern:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Intern account not found")

    intern.domain = req.domain
    intern.city = req.city
    intern.linkedin_url = req.linkedin_url
    intern.github_url = req.github_url
    intern.signup_stage = max(intern.signup_stage or 1, 2)
    await db.commit()
    return {"status": "success", "message": "Stage 2 details updated", "stage": intern.signup_stage}

@router.post("/signup/stage3", summary="Intern Signup Stage 3 (College & Education)")
async def signup_stage3(
    req: SignupStage3Request,
    current_user: Dict[str, Any] = Depends(get_current_user_token),
    db: AsyncSession = Depends(get_db)
):
    intern_id = int(current_user.get("sub"))
    stmt = select(InternAccount).where(InternAccount.id == intern_id)
    res = await db.execute(stmt)
    intern = res.scalar_one_or_none()
    if not intern:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Intern account not found")

    intern.college = req.college
    intern.course = req.course
    intern.semester = req.semester
    intern.year_of_passing = req.year_of_passing
    intern.signup_stage = 3
    await db.commit()
    return {"status": "success", "message": "Registration complete", "stage": 3}

@router.post("/company/signup", response_model=TokenResponse, summary="Register New Company")
async def company_signup(req: CompanySignupRequest, db: AsyncSession = Depends(get_db)):
    stmt = select(Company).where(Company.email == req.email.lower().strip())
    res = await db.execute(stmt)
    if res.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="A company with this email already exists")

    new_company = Company(
        name=req.name.strip(),
        email=req.email.lower().strip(),
        password_hash=hash_password(req.password),
        phone=req.phone,
        website=req.website,
        about=req.about,
        is_approved=False
    )
    db.add(new_company)
    await db.commit()
    await db.refresh(new_company)

    token_data = {"sub": str(new_company.id), "email": new_company.email, "role": "company", "name": new_company.name}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_TTL,
        user={"id": new_company.id, "email": new_company.email, "name": new_company.name, "role": "company", "is_approved": False}
    )

@router.post("/check-email", summary="Check Email Availability")
async def check_email(req: CheckEmailRequest, db: AsyncSession = Depends(get_db)):
    stmt = select(InternAccount.id).where(InternAccount.email == req.email.lower().strip())
    res = await db.execute(stmt)
    exists = res.scalar_one_or_none() is not None
    return {"registered": exists}

@router.post("/forgot-password", summary="Trigger Password Reset Email")
async def forgot_password(req: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)):
    clean_email = req.email.lower().strip()
    token = secrets.token_urlsafe(32)
    exp = datetime.now(timezone.utc) + timedelta(hours=2)

    # Invalidate prior unused tokens for this email
    await db.execute(
        update(PasswordReset)
        .where(PasswordReset.email == clean_email, PasswordReset.used == False)
        .values(used=True, used_at=datetime.now(timezone.utc))
    )

    reset_entry = PasswordReset(
        email=clean_email,
        token=token,
        expires_at=exp,
        account_type=req.account_type or "intern"
    )
    db.add(reset_entry)
    await db.commit()

    # Neutral response prevents user enumeration (Finding DBERT-005)
    return {"status": "success", "message": "If that email is registered, password reset instructions have been dispatched."}

@router.post("/reset-password", summary="Reset Password with Token")
async def reset_password(req: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    now = datetime.now(timezone.utc)
    stmt = select(PasswordReset).where(PasswordReset.token == req.token, PasswordReset.used == False)
    res = await db.execute(stmt)
    reset_record = res.scalar_one_or_none()
    if not reset_record:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired reset token")

    # Enforce token expiry (Finding DBERT-005)
    if reset_record.expires_at and reset_record.expires_at.replace(tzinfo=timezone.utc if reset_record.expires_at.tzinfo is None else None) < now:
        reset_record.used = True
        await db.commit()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Reset token has expired. Please request a new one.")

    new_hash = hash_password(req.new_password)
    # Update account password based on account_type
    acct_type = reset_record.account_type or "intern"
    if acct_type == "intern":
        intern_stmt = select(InternAccount).where(InternAccount.email == reset_record.email)
        intern_res = await db.execute(intern_stmt)
        intern = intern_res.scalar_one_or_none()
        if intern:
            intern.password_hash = new_hash
            intern.password_set = True
    elif acct_type == "company":
        comp_stmt = select(Company).where(Company.email == reset_record.email)
        comp_res = await db.execute(comp_stmt)
        comp = comp_res.scalar_one_or_none()
        if comp:
            comp.password_hash = new_hash
    elif acct_type == "mentor":
        m_stmt = select(Mentor).where(Mentor.email == reset_record.email)
        m_res = await db.execute(m_stmt)
        mentor = m_res.scalar_one_or_none()
        if mentor:
            mentor.password_hash = new_hash

    reset_record.used = True
    reset_record.used_at = now

    # Invalidate all active sessions/tokens upon password reset
    await db.execute(
        update(MobileRefreshToken)
        .where(MobileRefreshToken.email == reset_record.email, MobileRefreshToken.revoked == False)
        .values(revoked=True)
    )

    await db.commit()
    return {"status": "success", "message": "Password successfully updated"}

@router.get("/status", summary="Get Authenticated User Info")
async def auth_status(current_user: Dict[str, Any] = Depends(get_current_user_token)):
    return {"status": "authenticated", "user": current_user}
