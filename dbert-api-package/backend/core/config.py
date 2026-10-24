import os
from typing import List, Optional
try:
    from pydantic_settings import BaseSettings
    from pydantic import Field
except ImportError:
    from pydantic import BaseModel as BaseSettings, Field

class Settings(BaseSettings):
    # Core
    PROJECT_NAME: str = "DBERT API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = os.environ.get("ENVIRONMENT", "development")
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "dbert-secure-default-secret-key-change-in-prod-32chars")
    
    # Database
    DATABASE_URL: str = os.environ.get(
        "DATABASE_URL", 
        "postgresql+asyncpg://dbert:dbert_pass@localhost:5432/dbert_db"
    )
    SQLITE_SOURCE_PATH: str = os.environ.get("SQLITE_SOURCE_PATH", "databases/internship.db")
    
    # Auth & Tokens
    ACCESS_TOKEN_TTL: int = int(os.environ.get("ACCESS_TOKEN_TTL", "3600"))        # 1 hour
    REFRESH_TOKEN_TTL: int = int(os.environ.get("REFRESH_TOKEN_TTL", "5184000"))   # 60 days
    SESSION_DAYS: int = int(os.environ.get("SESSION_DAYS", "7"))
    ADMIN_USERNAME: str = os.environ.get("ADMIN_USERNAME", "dbert_admin")
    ADMIN_PASSWORD: str = os.environ.get("ADMIN_PASSWORD", "dbert_admin_2026")
    ADMIN_KEY: str = os.environ.get("ADMIN_KEY", "dbert_admin_2026")
    
    # CORS
    CORS_ORIGINS: str = os.environ.get("CORS_ORIGINS", "*")
    
    @property
    def cors_origins_list(self) -> List[str]:
        if not self.CORS_ORIGINS or self.CORS_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    # Payments & Razorpay
    RAZORPAY_KEY_ID: str = os.environ.get("RAZORPAY_KEY_ID", "")
    RAZORPAY_KEY_SECRET: str = os.environ.get("RAZORPAY_KEY_SECRET", "")
    UPI_ID: str = os.environ.get("UPI_ID", "Q681021429@ybl")
    UPI_AMOUNT: int = int(os.environ.get("UPI_AMOUNT", "499"))
    PAID_PROGRAM_AMOUNT: int = int(os.environ.get("PAID_PROGRAM_AMOUNT", "1599"))
    
    # Google Gemini AI
    GEMINI_API_KEY: str = os.environ.get("GEMINI_API_KEY", "")
    GEMINI_API_KEYS: str = os.environ.get("GEMINI_API_KEYS", "")
    GEMINI_MODEL: str = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash-lite")
    GEMINI_TIMEOUT: int = int(os.environ.get("GEMINI_TIMEOUT", "8"))
    GEMINI_TOTAL_BUDGET: int = int(os.environ.get("GEMINI_TOTAL_BUDGET", "30"))
    INTERVIEW_ENABLED: bool = os.environ.get("INTERVIEW_ENABLED", "true").lower() == "true"
    INTERVIEW_NUM_QUESTIONS: int = int(os.environ.get("INTERVIEW_NUM_QUESTIONS", "4"))
    INTERVIEW_MAX_ATTEMPTS: int = int(os.environ.get("INTERVIEW_MAX_ATTEMPTS", "2"))
    INTERVIEW_COOLING_HOURS: int = int(os.environ.get("INTERVIEW_COOLING_HOURS", "24"))
    
    # OneSignal Push
    ONESIGNAL_APP_ID: str = os.environ.get("ONESIGNAL_APP_ID", "1b181bc1-46b8-4359-ac7a-e87ecab91be4")
    ONESIGNAL_REST_API_KEY: str = os.environ.get("ONESIGNAL_REST_API_KEY", "")
    
    # Email
    EMAIL_PROVIDER: str = os.environ.get("EMAIL_PROVIDER", "smtp")
    SMTP_HOST: str = os.environ.get("SMTP_HOST", "dbert.online")
    SMTP_PORT: int = int(os.environ.get("SMTP_PORT", "465"))
    SMTP_USER: str = os.environ.get("SMTP_USER", "contactus@dbert.online")
    SMTP_PASS: str = os.environ.get("SMTP_PASS", "")
    FROM_EMAIL: str = os.environ.get("FROM_EMAIL", "contactus@dbert.online")
    FROM_NAME: str = os.environ.get("FROM_NAME", "DBERT Support")
    SMTP_BACKUP_HOST: str = os.environ.get("SMTP_BACKUP_HOST", "dbert.info")
    SMTP_BACKUP_PORT: int = int(os.environ.get("SMTP_BACKUP_PORT", "465"))
    SMTP_BACKUP_USER: str = os.environ.get("SMTP_BACKUP_USER", "contactus@dbert.info")
    SMTP_BACKUP_PASS: str = os.environ.get("SMTP_BACKUP_PASS", "")
    EMAILS_ENABLED: bool = os.environ.get("EMAILS_ENABLED", "true").lower() == "true"
    CPANEL_EMAIL_API_URL: str = os.environ.get("CPANEL_EMAIL_API_URL", "https://mailer.aivaratech.online/send")
    CPANEL_EMAIL_API_KEY: str = os.environ.get("CPANEL_EMAIL_API_KEY", "")
    AWS_SES_REGION: str = os.environ.get("AWS_SES_REGION", "us-east-1")
    
    # Cron & Background Jobs
    CRON_SECRET: str = os.environ.get("CRON_SECRET", "dbert_cron_secret_2026")
    
    # GitHub Integration
    GITHUB_TOKEN: str = os.environ.get("GITHUB_TOKEN", "")
    GITHUB_TIMEOUT: int = int(os.environ.get("GITHUB_TIMEOUT", "6"))
    
    # Security & Financial Encryption
    FERNET_KEY: str = os.environ.get("FERNET_KEY", "")
    AMBASSADOR_ENABLED: bool = os.environ.get("AMBASSADOR_ENABLED", "0") == "1"
    
    # File Storage
    UPLOAD_FOLDER: str = os.environ.get("UPLOAD_FOLDER", "uploads")
    MAX_UPLOAD_SIZE_MB: int = int(os.environ.get("MAX_UPLOAD_SIZE_MB", "6"))
    
    # Rate Limiting
    DISABLE_RATE_LIMIT: bool = os.environ.get("DISABLE_RATE_LIMIT", "0") == "1"
    RL_LOGIN_EMAIL_LIMIT: int = int(os.environ.get("RL_LOGIN_EMAIL_LIMIT", "5"))
    RL_LOGIN_EMAIL_WINDOW: int = int(os.environ.get("RL_LOGIN_EMAIL_WINDOW", "900"))
    RL_LOGIN_IP_LIMIT: int = int(os.environ.get("RL_LOGIN_IP_LIMIT", "20"))
    RL_LOGIN_IP_WINDOW: int = int(os.environ.get("RL_LOGIN_IP_WINDOW", "900"))
    RL_APPLY_IP_LIMIT: int = int(os.environ.get("RL_APPLY_IP_LIMIT", "30"))
    RL_APPLY_IP_WINDOW: int = int(os.environ.get("RL_APPLY_IP_WINDOW", "3600"))
    
    # SEO & Analytics
    GA4_ID: str = os.environ.get("GA4_ID", "G-GZ17KZ7MDW")
    GA4_API_SECRET: str = os.environ.get("GA4_API_SECRET", "")
    SITE_ORIGIN: str = os.environ.get("SITE_ORIGIN", "https://internship.dbert.online")
    ADSENSE_PUB_ID: str = os.environ.get("ADSENSE_PUB_ID", "pub-1320532532258767")
    OG_IMAGE_URL: str = os.environ.get("OG_IMAGE_URL", "")
    LOGO_URL: str = os.environ.get("LOGO_URL", "")
    
    # Business Rules
    ENROLLMENT_DEADLINE: str = os.environ.get("ENROLLMENT_DEADLINE", "2026-12-31")
    MAX_APPLICATIONS_PER_PERSON: int = int(os.environ.get("MAX_APPLICATIONS_PER_PERSON", "3"))

settings = Settings()
