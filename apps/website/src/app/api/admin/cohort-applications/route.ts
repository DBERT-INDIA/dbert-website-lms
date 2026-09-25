import { NextResponse } from 'next/server';
import { cookies } from 'next/headers';
import jwt from 'jsonwebtoken';
import db from '@/lib/db';
import { getJwtSecret } from '@/lib/env';
import { callCohortEmailApi, CohortDecisionType } from '@/lib/email';

async function verifyAdmin(): Promise<{ ok: boolean; username?: string }> {
  const cookieStore = await cookies();
  const token = cookieStore.get('admin_token')?.value;

  if (!token) return { ok: false };

  try {
    const decoded = jwt.verify(token, getJwtSecret()) as { username?: string };
    return { ok: true, username: decoded.username || 'admin' };
  } catch {
    return { ok: false };
  }
}

export async function GET(request: Request) {
  const auth = await verifyAdmin();
  if (!auth.ok) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  try {
    const { searchParams } = new URL(request.url);
    const status = searchParams.get('status');
    const domain = searchParams.get('domain');
    const search = searchParams.get('search')?.trim().toLowerCase();

    const where: any = { cohortSlug: 'aivara' };
    if (status && status !== 'all') {
      where.status = status;
    }
    if (domain && domain !== 'all') {
      where.domain = domain;
    }

    let applications = await db.cohortApplication.findMany({
      where,
      orderBy: { createdAt: 'desc' },
    });

    if (search) {
      applications = applications.filter(app =>
        app.fullName.toLowerCase().includes(search) ||
        app.email.toLowerCase().includes(search) ||
        app.college.toLowerCase().includes(search) ||
        app.city.toLowerCase().includes(search)
      );
    }

    return NextResponse.json({ applications, total: applications.length }, { status: 200 });
  } catch (err) {
    console.error('Failed to fetch cohort applications:', err);
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }
}

export async function PATCH(request: Request) {
  const auth = await verifyAdmin();
  if (!auth.ok) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  try {
    const body = await request.json();
    const { id, decision, adminNotes } = body;

    if (!id || !decision) {
      return NextResponse.json({ error: 'Missing application ID or decision' }, { status: 400 });
    }

    const validDecisions: CohortDecisionType[] = ['approved', 'approved_certified', 'rejected'];
    if (!validDecisions.includes(decision)) {
      return NextResponse.json({
        error: 'Invalid decision. Must be "approved", "approved_certified", or "rejected".',
      }, { status: 400 });
    }

    const application = await db.cohortApplication.findUnique({
      where: { id },
    });

    if (!application) {
      return NextResponse.json({ error: 'Cohort application not found.' }, { status: 404 });
    }

    // 1. Dispatch Email (or trigger placeholder API)
    const emailResult = await callCohortEmailApi({
      to: application.email,
      applicantName: application.fullName,
      decision,
      domain: application.domain,
      adminNotes: adminNotes?.trim() || undefined,
      cohortName: 'Aivara Technologies Hiring Cohort',
    });

    // 2. Persist Decision & Email audit trail to database
    const updated = await db.cohortApplication.update({
      where: { id },
      data: {
        status: decision,
        adminNotes: adminNotes ? adminNotes.trim() : null,
        reviewedAt: new Date(),
        reviewedBy: auth.username,
        emailSent: emailResult.success,
        emailSentAt: emailResult.dispatchedAt,
        emailTypeSent: decision,
        emailResponseLog: emailResult.log,
      },
    });

    return NextResponse.json({
      success: true,
      application: updated,
      emailResult,
    }, { status: 200 });
  } catch (err) {
    console.error('Cohort admin decision error:', err);
    return NextResponse.json({ error: 'Failed to record cohort decision.' }, { status: 500 });
  }
}
