import { NextRequest, NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

interface BalanceSubmission {
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
  status: 'SUBMITTED' | 'VERIFIED' | 'REJECTED';
  ipAddress?: string;
  userAgent?: string;
}

function resolveDataFilePath(): string {
  // Statically scoped to data folder within cwd
  const dataDir = path.join(process.cwd(), 'data');
  if (!fs.existsSync(dataDir)) {
    try {
      fs.mkdirSync(dataDir, { recursive: true });
    } catch {
      // ignore
    }
  }
  return path.join(dataDir, 'balance_enrollments_1500.json');
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
      return NextResponse.json({ success: false, error: 'A valid 10-digit contact / WhatsApp number is required.' }, { status: 400 });
    }
    if (!domain || typeof domain !== 'string' || !domain.trim()) {
      return NextResponse.json({ success: false, error: 'Domain Track selection is required.' }, { status: 400 });
    }
    if (!utrNumber || typeof utrNumber !== 'string' || utrNumber.trim().length < 6) {
      return NextResponse.json({ success: false, error: 'A valid 12-digit UPI UTR / Transaction Reference number is required.' }, { status: 400 });
    }

    const cleanUtr = utrNumber.trim().toUpperCase();
    const cleanCertId = (certId || '').trim();
    const cleanInternId = (internId || '').trim();

    // Unique submission reference
    const timestamp = new Date().toISOString();
    const randomHex = Math.random().toString(36).substring(2, 6).toUpperCase();
    const submissionId = `DBERT-ENR-${Date.now().toString().slice(-6)}-${randomHex}`;

    const submissionRecord: BalanceSubmission = {
      id: submissionId,
      submittedAt: timestamp,
      fullName: fullName.trim(),
      email: email.trim().toLowerCase(),
      phone: phone.trim(),
      college: (college || '').trim(),
      domain: domain.trim(),
      certId: cleanCertId || undefined,
      internId: cleanInternId || undefined,
      amountExpected: 1500,
      amountPaid: 1500,
      utrNumber: cleanUtr,
      remarks: (remarks || '').trim() || undefined,
      status: 'SUBMITTED',
      ipAddress: request.headers.get('x-forwarded-for') || request.headers.get('x-real-ip') || undefined,
      userAgent: request.headers.get('user-agent') || undefined
    };

    // Save to persistent storage
    const targetFile = resolveDataFilePath();
    let existing: BalanceSubmission[] = [];
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
        message: 'This UTR has already been recorded and is currently in verification queue.'
      });
    }

    existing.unshift(submissionRecord);

    // Write back atomically
    const tempFile = `${targetFile}.tmp.${Date.now()}`;
    fs.writeFileSync(tempFile, JSON.stringify(existing, null, 2), 'utf-8');
    fs.renameSync(tempFile, targetFile);

    // Also write to log file for easy auditing
    const logFile = path.join(path.dirname(targetFile), 'balance_enrollments.log');
    const logLine = `[${timestamp}] SUBMISSION_RECEIVED: ID=${submissionId} CANDIDATE="${fullName}" EMAIL="${email}" PHONE="${phone}" UTR="${cleanUtr}" CERT="${cleanCertId}"\n`;
    try {
      fs.appendFileSync(logFile, logLine, 'utf-8');
    } catch {
      // non-blocking
    }

    return NextResponse.json({
      success: true,
      submissionId,
      submittedAt: timestamp,
      candidateName: fullName.trim(),
      certId: cleanCertId,
      domain: domain.trim(),
      utrNumber: cleanUtr,
      amount: 1500
    });
  } catch (err: any) {
    return NextResponse.json({ success: false, error: err.message || 'Internal server error' }, { status: 500 });
  }
}
