import { NextResponse } from 'next/server';
import db from '@/lib/db';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const {
      startupName,
      founderName,
      email,
      phone,
      city,
      stage,
      domain,
      teamSize,
      currentFunding,
      servicesNeeded,
      description,
      challengeStmt,
      consent
    } = body;

    if (!startupName || !founderName || !email || !phone || !city || !description || !challengeStmt) {
      return NextResponse.json({ error: 'Missing required parameters' }, { status: 400 });
    }

    const registration = await db.startupRegistration.create({
      data: {
        startupName,
        founderName,
        email,
        phone,
        city,
        stage,
        domain,
        teamSize,
        currentFunding,
        servicesNeeded,
        description,
        challengeStmt,
        consent
      }
    });

    return NextResponse.json({ success: true, id: registration.id }, { status: 201 });
  } catch (err) {
    console.error('Startup registration error:', err);
    return NextResponse.json({ error: 'Failed to register startup' }, { status: 500 });
  }
}
