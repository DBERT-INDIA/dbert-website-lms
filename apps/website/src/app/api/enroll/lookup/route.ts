import { NextRequest, NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';
import raw409 from '@/data/all_409_provisional_registry.json';
import raw56 from '@/data/certificates_registry.json';
import raw1593 from '@/data/sheet_1593_provisional_registry.json';

interface CandidateRecord {
  certId: string;
  internId?: string;
  holderName: string;
  email?: string;
  phone?: string;
  college?: string;
  domain?: string;
  project?: string;
  batch?: string;
  isProvisional?: boolean;
}

interface BalanceEnrollment {
  id: string;
  submittedAt: string;
  fullName: string;
  email: string;
  phone: string;
  college?: string;
  domain: string;
  certId?: string;
  internId?: string;
  amountExpected: number;
  amountPaid: number;
  utrNumber: string;
  remarks?: string;
  status: 'SUBMITTED' | 'UNDER_REVIEW' | 'VERIFIED' | 'APPROVED' | 'REJECTED';
  approvedAt?: string;
  batchStartDate?: string;
  batchStartDisplay?: string;
}

function getBalanceEnrollments(): BalanceEnrollment[] {
  const possiblePaths = [
    path.join(process.cwd(), 'data', 'balance_enrollments_1500.json'),
    path.join(process.cwd(), '..', '..', 'data', 'balance_enrollments_1500.json'),
    '/var/www/dbert-website-lms/data/balance_enrollments_1500.json'
  ];

  for (const p of possiblePaths) {
    if (fs.existsSync(/*turbopackIgnore: true*/ p)) {
      try {
        const raw = fs.readFileSync(/*turbopackIgnore: true*/ p, 'utf-8');
        const parsed = JSON.parse(raw);
        if (Array.isArray(parsed)) return parsed;
      } catch {
        // continue
      }
    }
  }
  return [];
}

function getVerificationSubmissions(): any[] {
  const possiblePaths = [
    path.join(process.cwd(), 'data', 'verification_submissions_299.json'),
    path.join(process.cwd(), '..', '..', 'data', 'verification_submissions_299.json'),
    '/var/www/dbert-website-lms/data/verification_submissions_299.json'
  ];

  for (const p of possiblePaths) {
    if (fs.existsSync(/*turbopackIgnore: true*/ p)) {
      try {
        const raw = fs.readFileSync(/*turbopackIgnore: true*/ p, 'utf-8');
        const parsed = JSON.parse(raw);
        if (Array.isArray(parsed)) return parsed;
      } catch {
        // continue
      }
    }
  }
  return [];
}

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const query = (
      searchParams.get('q') ||
      searchParams.get('certid') ||
      searchParams.get('email') ||
      ''
    ).trim().toLowerCase();

    if (!query) {
      return NextResponse.json({ found: false, error: 'Query parameter required' }, { status: 400 });
    }

    // 1. Primary Check: Approved or submitted records in balance_enrollments_1500.json
    const balanceRecords = getBalanceEnrollments();
    const balanceMatch = balanceRecords.find((b) => {
      const bEmail = (b.email || '').toLowerCase().trim();
      const bPhone = (b.phone || '').replace(/\D/g, '');
      const bUtr = (b.utrNumber || '').toLowerCase().trim();
      const bId = (b.id || '').toLowerCase().trim();
      const bCert = (b.certId || '').toLowerCase().trim();
      const bIntern = (b.internId || '').toLowerCase().trim();
      const cleanQ = query.replace(/\D/g, '');

      return (
        bEmail === query ||
        bUtr === query ||
        bId === query ||
        bCert === query ||
        bIntern === query ||
        (cleanQ.length >= 10 && bPhone === cleanQ)
      );
    });

    if (balanceMatch) {
      const isApproved = balanceMatch.status === 'APPROVED' || balanceMatch.status === 'VERIFIED';
      // Mask PII for public lookup (Finding DBERT-014)
      const rawEmail = balanceMatch.email || '';
      const maskedEmail = rawEmail.includes('@')
        ? `${rawEmail.split('@')[0].slice(0, 3)}***@${rawEmail.split('@')[1]}`
        : '';
      const rawPhone = (balanceMatch.phone || '').replace(/\D/g, '');
      const maskedPhone = rawPhone.length >= 4
        ? `+91 ******${rawPhone.slice(-4)}`
        : '';

      return NextResponse.json({
        found: true,
        enrollmentStatus: balanceMatch.status || 'SUBMITTED',
        isApproved,
        rejectionReason: (balanceMatch as any).rejectionReason || null,
        batchStartDate: balanceMatch.batchStartDate || '2026-11-09T18:00:00+05:30',
        batchStartDisplay: balanceMatch.batchStartDisplay || 'Monday, 9 Nov 2026',
        candidate: {
          // Never fabricate fake IDs (Finding DBERT-015)
          certId: balanceMatch.certId || null,
          internId: balanceMatch.internId || null,
          holderName: balanceMatch.fullName,
          email: maskedEmail,
          phone: maskedPhone,
          college: balanceMatch.college || 'Full Stack Incubation Scholar',
          domain: balanceMatch.domain,
          project: balanceMatch.domain + ' Production Architecture',
          batch: balanceMatch.batchStartDisplay || 'Monday, 9 Nov 2026',
          isProvisional: !isApproved,
          submissionId: balanceMatch.id,
          status: balanceMatch.status,
          rejectionReason: (balanceMatch as any).rejectionReason || null
        }
      });
    }

    // 1.5 Check if submitted in verification_submissions_299.json
    const verSubmissions = getVerificationSubmissions();
    const verMatch = verSubmissions.find((v) => {
      const vEmail = (v.email || '').toLowerCase().trim();
      const vPhone = (v.phone || '').replace(/\D/g, '');
      const vCert = (v.certId || '').toLowerCase().trim();
      const cleanQ = query.replace(/\D/g, '');
      return vEmail === query || vCert === query || (cleanQ.length >= 10 && vPhone === cleanQ);
    });

    // 2. Secondary Check: Search in 409 provisional registry
    const provCandidates: CandidateRecord[] = raw409 as any[];
    let match = provCandidates.find((c) => {
      const cId = (c.certId || '').toLowerCase();
      const iId = (c.internId || '').toLowerCase();
      const em = (c.email || '').toLowerCase();
      return cId === query || iId === query || em === query;
    });

    // 3. Tertiary Check: Search in master certificates registry
    if (!match) {
      const masterRegistry: Record<string, any> = raw56 as Record<string, any>;
      const masterEntries = Object.values(masterRegistry);
      const foundMaster = masterEntries.find((c: any) => {
        const cId = (c.certId || '').toLowerCase();
        const iId = (c.internId || '').toLowerCase();
        const em = (c.email || '').toLowerCase();
        return cId === query || iId === query || em === query;
      });

      if (foundMaster) {
        match = {
          certId: foundMaster.certId,
          internId: foundMaster.internId,
          holderName: foundMaster.holderName,
          email: foundMaster.email,
          phone: foundMaster.phone || '',
          college: foundMaster.college || '',
          domain: foundMaster.domain || '',
          project: foundMaster.project || '',
          batch: foundMaster.batch || '',
          isProvisional: false
        };
      }
    }

    // 4. Quaternary Check: Search in 1593 sheet provisional registry
    if (!match) {
      const sheetList: CandidateRecord[] = raw1593 as any[];
      const foundSheet = sheetList.find((c: any) => {
        const cId = (c.certId || '').toLowerCase();
        const iId = (c.internId || '').toLowerCase();
        const em = (c.email || '').toLowerCase();
        return cId === query || iId === query || em === query;
      });

      if (foundSheet) {
        match = {
          certId: foundSheet.certId,
          internId: foundSheet.internId,
          holderName: foundSheet.holderName,
          email: foundSheet.email,
          phone: foundSheet.phone || '',
          college: foundSheet.college || '',
          domain: foundSheet.domain || '',
          project: foundSheet.project || '',
          batch: foundSheet.batch || '',
          isProvisional: true
        };
      }
    }

    if (match) {
      return NextResponse.json({
        found: true,
        enrollmentStatus: 'UNENROLLED',
        isApproved: false,
        verificationStatus: verMatch ? verMatch.status : (match.isProvisional ? 'UNVERIFIED' : 'VERIFIED'),
        verificationSubmission: verMatch || null,
        candidate: {
          certId: match.certId,
          internId: match.internId || '',
          holderName: match.holderName,
          email: match.email || '',
          phone: match.phone || '',
          college: match.college || '',
          domain: match.domain || '',
          project: match.project || '',
          batch: match.batch || '',
          isProvisional: match.isProvisional ?? true
        }
      });
    }

    return NextResponse.json({ found: false, message: 'Candidate record not found' }, { status: 404 });
  } catch (err: any) {
    return NextResponse.json({ found: false, error: err.message }, { status: 500 });
  }
}
