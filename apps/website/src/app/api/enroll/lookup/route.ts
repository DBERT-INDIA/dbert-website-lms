import { NextRequest, NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';
import raw409 from '@/data/all_409_provisional_registry.json';
import raw56 from '@/data/certificates_registry.json';

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
  status: 'SUBMITTED' | 'APPROVED' | 'REJECTED';
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
    if (fs.existsSync(p)) {
      try {
        const raw = fs.readFileSync(p, 'utf-8');
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
      const isApproved = balanceMatch.status === 'APPROVED';
      return NextResponse.json({
        found: true,
        enrollmentStatus: balanceMatch.status || 'APPROVED',
        isApproved,
        batchStartDate: balanceMatch.batchStartDate || '2026-11-09T18:00:00+05:30',
        batchStartDisplay: balanceMatch.batchStartDisplay || 'Monday, 9 Nov 2026',
        candidate: {
          certId: balanceMatch.certId || 'CERT-DBERT-2026-FSD-156',
          internId: balanceMatch.internId || 'DBERT-2026-INT-1412',
          holderName: balanceMatch.fullName,
          email: balanceMatch.email,
          phone: balanceMatch.phone,
          college: balanceMatch.college || 'Full Stack Incubation Scholar',
          domain: balanceMatch.domain,
          project: balanceMatch.domain + ' Production Architecture',
          batch: balanceMatch.batchStartDisplay || 'Monday, 9 Nov 2026',
          isProvisional: false,
          amountPaid: balanceMatch.amountPaid,
          utrNumber: balanceMatch.utrNumber,
          submissionId: balanceMatch.id,
          status: balanceMatch.status
        }
      });
    }

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

    if (match) {
      return NextResponse.json({
        found: true,
        enrollmentStatus: 'UNENROLLED',
        isApproved: false,
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
