import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';
import db from '@/lib/db';
import { getProjectRepoInfo, MENTOR_PROFILE } from '@/lib/verification';

interface RegistryRecord {
  certId: string;
  internId?: string;
  holderName: string;
  college?: string;
  domain?: string;
  project?: string;
  batch?: string;
  duration?: string;
  startDate?: string;
  endDate?: string;
  issueDate?: string;
  evalDate?: string;
  score?: number;
  grade?: string;
  signatory?: string;
  signatoryTitle?: string;
  organization?: string;
  verificationUrl?: string;
  previewUrl?: string;
  verified?: boolean;
  isProvisional?: boolean;
  status?: string;
}

function getLocalRegistry(): Record<string, RegistryRecord> {
  try {
    const regPath = path.join(process.cwd(), 'src', 'data', 'certificates_registry.json');
    if (fs.existsSync(regPath)) {
      const raw = fs.readFileSync(regPath, 'utf8');
      return JSON.parse(raw);
    }
  } catch (err) {
    console.error('Error reading certificates_registry.json:', err);
  }
  return {};
}

function getProvisionalRegistry(): RegistryRecord[] {
  try {
    const pPath = path.join(process.cwd(), 'src', 'data', 'all_409_provisional_registry.json');
    if (fs.existsSync(pPath)) {
      const raw = fs.readFileSync(pPath, 'utf8');
      return JSON.parse(raw);
    }
  } catch (err) {
    console.error('Error reading all_409_provisional_registry.json:', err);
  }
  return [];
}

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const certId = (
      searchParams.get('certid') ||
      searchParams.get('certId') ||
      searchParams.get('id') ||
      ''
    ).trim();

    const internIdParam = (
      searchParams.get('internid') ||
      searchParams.get('internId') ||
      ''
    ).trim();

    if (!certId && !internIdParam) {
      return NextResponse.json({ error: 'Missing certificate ID parameter' }, { status: 400 });
    }

    // 0. High-speed lookup by internId if provided
    if (internIdParam) {
      const provList = getProvisionalRegistry();
      const pMatch = provList.find(
        (p) => p.internId?.toLowerCase() === internIdParam.toLowerCase()
      );
      if (pMatch) {
        return NextResponse.json({
          verified: true,
          certId: pMatch.certId,
          internId: pMatch.internId,
          holderName: pMatch.holderName,
          college: pMatch.college,
          domain: pMatch.domain,
          programName: `DBERT Technical Incubation — ${pMatch.domain}`,
          project: pMatch.project,
          duration: pMatch.duration,
          startDate: pMatch.startDate,
          endDate: pMatch.endDate,
          issueDate: pMatch.issueDate || '2026-11-04',
          evalDate: pMatch.evalDate,
          score: pMatch.score,
          grade: pMatch.grade,
          signatory: pMatch.signatory || 'Mr. Abhinav Sharma',
          signatoryTitle: pMatch.signatoryTitle || 'Program Head & Project Mentor',
          organization: pMatch.organization || 'DBERT',
          verificationUrl: pMatch.verificationUrl || `https://dbert.in/verify?certid=${pMatch.certId}`,
          previewUrl: pMatch.previewUrl,
          isProvisional: !!pMatch.isProvisional,
          status: pMatch.status || 'ACTIVE',
          repoInfo: getProjectRepoInfo(pMatch.project),
          mentorProfile: {
            name: pMatch.signatory || MENTOR_PROFILE.name,
            title: pMatch.signatoryTitle || MENTOR_PROFILE.title,
            githubUrl: MENTOR_PROFILE.githubUrl,
            githubHandle: MENTOR_PROFILE.githubHandle,
          }
        }, { status: 200 });
      }
    }

    // 1. High-speed lookup in local verified registry
    const registry = getLocalRegistry();
    const matchKey = Object.keys(registry).find(
      (k) => k.toLowerCase() === certId.toLowerCase()
    );

    if (matchKey) {
      const c = registry[matchKey];
      return NextResponse.json({
        verified: true,
        certId: c.certId,
        internId: c.internId,
        holderName: c.holderName,
        college: c.college,
        domain: c.domain,
        programName: `DBERT Technical Incubation — ${c.domain}`,
        project: c.project,
        duration: c.duration,
        startDate: c.startDate,
        endDate: c.endDate,
        issueDate: c.issueDate || '2026-11-04',
        evalDate: c.evalDate,
        score: c.score,
        grade: c.grade,
        signatory: c.signatory || 'Mr. Abhinav Sharma',
        signatoryTitle: c.signatoryTitle || 'Program Head & Project Mentor',
        organization: c.organization || 'DBERT',
        verificationUrl: c.verificationUrl || `https://dbert.in/verify?certid=${c.certId}`,
        previewUrl: c.previewUrl,
        isProvisional: !!c.isProvisional,
        status: c.status || 'ACTIVE',
        repoInfo: getProjectRepoInfo(c.project),
        mentorProfile: {
          name: c.signatory || MENTOR_PROFILE.name,
          title: c.signatoryTitle || MENTOR_PROFILE.title,
          githubUrl: MENTOR_PROFILE.githubUrl,
          githubHandle: MENTOR_PROFILE.githubHandle,
        }
      }, { status: 200 });
    }

    // 1b. Check provisional list by certId
    const provList = getProvisionalRegistry();
    const pMatchCert = provList.find(
      (p) => p.certId.toLowerCase() === certId.toLowerCase()
    );
    if (pMatchCert) {
      return NextResponse.json({
        verified: true,
        certId: pMatchCert.certId,
        internId: pMatchCert.internId,
        holderName: pMatchCert.holderName,
        college: pMatchCert.college,
        domain: pMatchCert.domain,
        programName: `DBERT Technical Incubation — ${pMatchCert.domain}`,
        project: pMatchCert.project,
        duration: pMatchCert.duration,
        startDate: pMatchCert.startDate,
        endDate: pMatchCert.endDate,
        issueDate: pMatchCert.issueDate || '2026-11-04',
        evalDate: pMatchCert.evalDate,
        score: pMatchCert.score,
        grade: pMatchCert.grade,
        signatory: pMatchCert.signatory || 'Mr. Abhinav Sharma',
        signatoryTitle: pMatchCert.signatoryTitle || 'Program Head & Project Mentor',
        organization: pMatchCert.organization || 'DBERT',
        verificationUrl: pMatchCert.verificationUrl || `https://dbert.in/verify?certid=${pMatchCert.certId}`,
        previewUrl: pMatchCert.previewUrl,
        isProvisional: !!pMatchCert.isProvisional,
        status: pMatchCert.status || 'ACTIVE',
        repoInfo: getProjectRepoInfo(pMatchCert.project),
        mentorProfile: {
          name: pMatchCert.signatory || MENTOR_PROFILE.name,
          title: pMatchCert.signatoryTitle || MENTOR_PROFILE.title,
          githubUrl: MENTOR_PROFILE.githubUrl,
          githubHandle: MENTOR_PROFILE.githubHandle,
        }
      }, { status: 200 });
    }

    // 2. Fallback to Prisma database
    let certificate = null;
    try {
      certificate = await db.certificate.findUnique({
        where: { certificateId: certId }
      });
    } catch {
      // Prisma error fallback
    }

    if (certificate) {
      return NextResponse.json({
        verified: certificate.verified,
        certId: certificate.certificateId,
        holderName: certificate.holderName,
        programName: certificate.programName,
        domain: certificate.domain,
        issueDate: certificate.issueDate,
      }, { status: 200 });
    }

    // 3. Fallback: Query LMS portal database /api/verify
    const lmsUrl = process.env.NEXT_PUBLIC_LMS_URL || 'https://lms.dbert.in';
    try {
      const lmsRes = await fetch(`${lmsUrl}/api/verify?certId=${encodeURIComponent(certId)}`, {
        next: { revalidate: 60 }
      });
      if (lmsRes.ok) {
        const lmsData = await lmsRes.json();
        if (lmsData.verified) {
          return NextResponse.json(lmsData, { status: 200 });
        }
      }
    } catch {
      // LMS fetch fallback failed
    }

    return NextResponse.json({ verified: false, error: 'Certificate ID not found' }, { status: 404 });
  } catch (err) {
    console.error('Certificate verification API error:', err);
    return NextResponse.json({ error: 'Failed to verify certificate' }, { status: 500 });
  }
}
