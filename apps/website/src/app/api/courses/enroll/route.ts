import { NextRequest, NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

interface CourseDepositSubmission {
  id: string;
  submittedAt: string;
  fullName: string;
  email: string;
  phone: string;
  college?: string;
  domain: string;
  courseTitle?: string;
  programType?: string;
  amountExpected: number;
  amountPaid: number;
  utrNumber: string;
  status: 'SUBMITTED' | 'VERIFIED';
  ipAddress?: string;
  userAgent?: string;
}

function resolveAuthoritativeCourseAmount(programType?: string, requestedAmount?: number): {
  programType: string;
  amount: number;
  paymentType: string;
} {
  const key = (programType || '').toLowerCase().trim();
  if (key === 'launchpad') {
    return { programType: 'launchpad', amount: 7999, paymentType: 'launchpad' };
  }
  if (key === 'accelerate') {
    return { programType: 'accelerate', amount: 4999, paymentType: 'accelerate' };
  }
  if (key === 'fellowship' && Number(requestedAmount) === 1999) {
    return { programType: 'fellowship', amount: 1999, paymentType: 'paid_program' };
  }
  return { programType: key || 'fellowship_deposit', amount: 499, paymentType: 'deposit' };
}

function resolveCourseDataFilePath(): string {
  const dataDir = path.join(process.cwd(), 'data');
  if (!fs.existsSync(dataDir)) {
    try {
      fs.mkdirSync(dataDir, { recursive: true });
    } catch {
      // ignore
    }
  }
  return path.join(dataDir, 'course_enrollments_499.json');
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const {
      name,
      fullName,
      email,
      phone,
      college,
      domain,
      track,
      courseTitle,
      programType,
      amountInr,
      utrNumber,
      utr
    } = body;

    const resolvedFee = resolveAuthoritativeCourseAmount(programType, amountInr);

    const candidateName = (fullName || name || '').trim();
    const candidateEmail = (email || '').trim().toLowerCase();
    const candidatePhone = (phone || '').trim();
    const candidateDomain = (domain || track || 'Full Stack Web Development').trim();
    const cleanUtr = (utrNumber || utr || '').trim().toUpperCase();

    if (!candidateName) {
      return NextResponse.json({ success: false, error: 'Full Legal Name is required.' }, { status: 400 });
    }
    if (!candidateEmail || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(candidateEmail)) {
      return NextResponse.json({ success: false, error: 'A valid email address is required.' }, { status: 400 });
    }
    if (!candidatePhone || candidatePhone.replace(/\D/g, '').length < 10) {
      return NextResponse.json({ success: false, error: 'A valid 10-digit contact / WhatsApp number is required.' }, { status: 400 });
    }
    if (!cleanUtr || cleanUtr.length < 6) {
      return NextResponse.json({ success: false, error: 'A valid 12-digit UPI UTR / Transaction Reference number is required.' }, { status: 400 });
    }

    const timestamp = new Date().toISOString();
    const randomHex = Math.random().toString(36).substring(2, 6).toUpperCase();
    const submissionId = `DBERT-CRS-${Date.now().toString().slice(-6)}-${randomHex}`;

    const submissionRecord: CourseDepositSubmission = {
      id: submissionId,
      submittedAt: timestamp,
      fullName: candidateName,
      email: candidateEmail,
      phone: candidatePhone,
      college: (college || '').trim(),
      domain: candidateDomain,
      courseTitle: (courseTitle || '').trim() || undefined,
      programType: resolvedFee.programType,
      amountExpected: resolvedFee.amount,
      amountPaid: resolvedFee.amount,
      utrNumber: cleanUtr,
      status: 'SUBMITTED',
      ipAddress: request.headers.get('x-forwarded-for') || request.headers.get('x-real-ip') || undefined,
      userAgent: request.headers.get('user-agent') || undefined
    };

    // Save to persistent storage
    const targetFile = resolveCourseDataFilePath();
    let existing: CourseDepositSubmission[] = [];
    if (fs.existsSync(targetFile)) {
      try {
        const raw = fs.readFileSync(targetFile, 'utf-8');
        existing = JSON.parse(raw);
        if (!Array.isArray(existing)) existing = [];
      } catch {
        existing = [];
      }
    }

    // Check duplicate UTR
    const duplicate = existing.find(e => e.utrNumber === cleanUtr);
    if (duplicate) {
      return NextResponse.json({
        success: true,
        alreadySubmitted: true,
        submissionId: duplicate.id,
        redirectUrl: 'https://lms.dbert.in/portal',
        message: 'This UTR has already been recorded and is currently in verification queue.'
      });
    }

    existing.unshift(submissionRecord);

    const tempFile = `${targetFile}.tmp.${Date.now()}`;
    fs.writeFileSync(tempFile, JSON.stringify(existing, null, 2), 'utf-8');
    fs.renameSync(tempFile, targetFile);

    // Synchronize to LMS PostgreSQL
    try {
      const syncEndpoint = process.env.INTERNAL_LMS_SYNC_URL || 'https://lms.dbert.in/api/internal/enrollment-sync';
      const syncSecret = process.env.INTERNAL_SYNC_SECRET || 'dbert-secure-sync-token-2026';
      
      await fetch(syncEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-DBERT-Internal-Secret': syncSecret
        },
        body: JSON.stringify({
          name: candidateName,
          email: candidateEmail,
          phone: candidatePhone,
          college: (college || '').trim(),
          domain: candidateDomain,
          amount: resolvedFee.amount,
          payment_type: resolvedFee.paymentType,
          utr: cleanUtr,
          submission_id: submissionId
        }),
        signal: AbortSignal.timeout(4000)
      });
    } catch (syncErr) {
      console.error('[Course Deposit Sync Warning - Handled]', syncErr instanceof Error ? syncErr.message : syncErr);
    }

    return NextResponse.json({
      success: true,
      submissionId,
      submittedAt: timestamp,
      candidateName,
      domain: candidateDomain,
      utrNumber: cleanUtr,
      amount: resolvedFee.amount,
      redirectUrl: 'https://lms.dbert.in/portal',
      message: 'Enrollment & UTR recorded! Your LMS account confirmation is queued.'
    });
  } catch (err: any) {
    return NextResponse.json({ success: false, error: err.message || 'Internal server error' }, { status: 500 });
  }
}
