import { NextRequest, NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

interface VerificationSubmission {
  id: string;
  submittedAt: string;
  fullName: string;
  email: string;
  phone: string;
  college: string;
  domain: string;
  certId?: string;
  internId?: string;
  amountExpected: number;
  amountPaid: number;
  utrNumber: string;
  remarks?: string;
  status: 'SUBMITTED' | 'UNDER_REVIEW' | 'VERIFIED' | 'APPROVED' | 'REJECTED';
  ipAddress?: string;
  userAgent?: string;
}

function resolveDataFilePath(): string {
  const possiblePaths = [
    path.join(process.cwd(), 'data'),
    path.join(process.cwd(), '..', '..', 'data'),
    '/var/www/dbert-website-lms/data'
  ];

  for (const dir of possiblePaths) {
    if (fs.existsSync(/*turbopackIgnore: true*/ dir)) {
      return path.join(dir, 'verification_submissions_299.json');
    }
  }

  const defaultDir = path.join(process.cwd(), 'data');
  if (!fs.existsSync(/*turbopackIgnore: true*/ defaultDir)) {
    try {
      fs.mkdirSync(defaultDir, { recursive: true });
    } catch {
      // ignore
    }
  }
  return path.join(defaultDir, 'verification_submissions_299.json');
}

function getStoredSubmissions(): VerificationSubmission[] {
  const filePath = resolveDataFilePath();
  if (fs.existsSync(/*turbopackIgnore: true*/ filePath)) {
    try {
      const raw = fs.readFileSync(/*turbopackIgnore: true*/ filePath, 'utf-8');
      const parsed = JSON.parse(raw);
      if (Array.isArray(parsed)) return parsed;
    } catch {
      return [];
    }
  }
  return [];
}

function saveSubmissions(submissions: VerificationSubmission[]): void {
  const filePath = resolveDataFilePath();
  fs.writeFileSync(filePath, JSON.stringify(submissions, null, 2), 'utf-8');
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const {
      fullName,
      email,
      phone,
      college,
      domain,
      certId,
      internId,
      utrNumber,
      remarks
    } = body;

    // Validation
    if (!fullName || typeof fullName !== 'string' || !fullName.trim()) {
      return NextResponse.json({ success: false, error: 'Full Legal Name is required.' }, { status: 400 });
    }
    if (!email || typeof email !== 'string' || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())) {
      return NextResponse.json({ success: false, error: 'A valid email address is required.' }, { status: 400 });
    }
    if (!phone || typeof phone !== 'string' || phone.trim().replace(/\D/g, '').length < 10) {
      return NextResponse.json({ success: false, error: 'A valid 10-digit WhatsApp phone number is required.' }, { status: 400 });
    }
    if (!utrNumber || typeof utrNumber !== 'string') {
      return NextResponse.json({ success: false, error: '12-digit UPI UTR transaction reference is required.' }, { status: 400 });
    }

    const cleanUtr = utrNumber.trim().replace(/\s+/g, '');
    if (!/^\d{12}$/.test(cleanUtr)) {
      return NextResponse.json({
        success: false,
        error: 'Invalid UTR format. Please provide the exact 12-digit numerical reference found in your UPI transaction receipt.'
      }, { status: 400 });
    }

    const submissions = getStoredSubmissions();

    // Check duplicate UTR
    const existingSubmission = submissions.find(s => s.utrNumber === cleanUtr);
    if (existingSubmission) {
      if (existingSubmission.email.toLowerCase() === email.trim().toLowerCase()) {
        return NextResponse.json({
          success: true,
          alreadySubmitted: true,
          submissionId: existingSubmission.id,
          message: 'Your verification submission for this UTR reference has already been received and is currently under admissions review.',
          data: existingSubmission
        });
      } else {
        return NextResponse.json({
          success: false,
          error: 'This 12-digit UTR reference has already been claimed by another candidate. If this is an error, please reach out directly to Admissions (+91 81929 11360).'
        }, { status: 409 });
      }
    }

    const submissionId = `DBERT-VER-${Math.floor(100000 + Math.random() * 900000)}-${Date.now().toString(36).slice(-4).toUpperCase()}`;
    const newEntry: VerificationSubmission = {
      id: submissionId,
      submittedAt: new Date().toISOString(),
      fullName: fullName.trim(),
      email: email.trim().toLowerCase(),
      phone: phone.trim(),
      college: college ? college.trim() : 'Verified Candidate',
      domain: domain ? domain.trim() : 'Engineering Track',
      certId: certId ? certId.trim() : undefined,
      internId: internId ? internId.trim() : undefined,
      amountExpected: 299,
      amountPaid: 299,
      utrNumber: cleanUtr,
      remarks: remarks ? remarks.trim() : undefined,
      status: 'SUBMITTED',
      ipAddress: request.headers.get('x-forwarded-for') || request.headers.get('x-real-ip') || 'unknown',
      userAgent: request.headers.get('user-agent') || 'unknown'
    };

    submissions.push(newEntry);
    saveSubmissions(submissions);

    // Real-Time Convergence: Synchronize atomically to LMS PostgreSQL (BUG-P1-06)
    let lmsSynced = false;
    try {
      const syncEndpoint = process.env.INTERNAL_LMS_SYNC_URL || 'https://lms.dbert.in/api/internal/enrollment-sync';
      const syncSecret = process.env.INTERNAL_SYNC_SECRET || 'dbert-secure-sync-token-2026';

      const syncRes = await fetch(syncEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-DBERT-Internal-Secret': syncSecret
        },
        body: JSON.stringify({
          name: fullName.trim(),
          email: email.trim().toLowerCase(),
          phone: phone.trim(),
          college: college ? college.trim() : 'Verified Candidate',
          domain: domain ? domain.trim() : 'Engineering Track',
          amount: 299,
          payment_type: 'verification_299',
          utr: cleanUtr,
          submission_id: submissionId,
          cert_id: certId ? certId.trim() : undefined
        }),
        signal: AbortSignal.timeout(5000)
      });

      if (syncRes.ok) {
        lmsSynced = true;
      } else {
        console.warn(`[LMS Sync Warning] Status: ${syncRes.status}`);
      }
    } catch (syncErr: unknown) {
      console.warn('[LMS Sync Network]', syncErr instanceof Error ? syncErr.message : syncErr);
    }

    return NextResponse.json({
      success: true,
      alreadySubmitted: false,
      submissionId,
      amountPaid: 299,
      lmsSynced,
      message: '₹299 Project Verification submission successfully recorded. Credential issuance and evaluation dossier review initiated.',
      data: newEntry
    });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : 'Unknown server error';
    return NextResponse.json({ success: false, error: 'Internal Server Error: ' + message }, { status: 500 });
  }
}
