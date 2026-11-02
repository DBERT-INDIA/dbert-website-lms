import { NextResponse } from 'next/server';
import db from '@/lib/db';

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const certId = searchParams.get('certId') || searchParams.get('id');

    if (!certId) {
      return NextResponse.json({ error: 'Missing certificate ID parameters' }, { status: 400 });
    }

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
        holderName: certificate.holderName,
        programName: certificate.programName,
        domain: certificate.domain,
        issueDate: certificate.issueDate,
        verified: certificate.verified
      }, { status: 200 });
    }

    // Fallback: Query LMS database /api/verify
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

    return NextResponse.json({ verified: false }, { status: 404 });
  } catch (err) {
    console.error('Certificate verification API error:', err);
    return NextResponse.json({ error: 'Failed to verify certificate' }, { status: 500 });
  }
}
