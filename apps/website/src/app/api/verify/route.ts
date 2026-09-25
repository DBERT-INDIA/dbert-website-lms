import { NextResponse } from 'next/server';
import db from '@/lib/db';

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const certId = searchParams.get('certId');

    if (!certId) {
      return NextResponse.json({ error: 'Missing certificate ID parameters' }, { status: 400 });
    }

    const certificate = await db.certificate.findUnique({
      where: { certificateId: certId }
    });

    if (!certificate) {
      return NextResponse.json({ verified: false }, { status: 404 });
    }

    return NextResponse.json({
      holderName: certificate.holderName,
      programName: certificate.programName,
      domain: certificate.domain,
      issueDate: certificate.issueDate,
      verified: certificate.verified
    }, { status: 200 });
  } catch (err) {
    console.error('Certificate verification API error:', err);
    return NextResponse.json({ error: 'Failed to verify certificate' }, { status: 500 });
  }
}
