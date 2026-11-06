import { NextResponse } from 'next/server';
import db from '@/lib/db';

function isValidEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim());
}

export async function POST(request: Request) {
  try {
    let body: any;
    try {
      body = await request.json();
    } catch {
      return NextResponse.json({ error: 'Invalid JSON payload' }, { status: 400 });
    }

    if (!body || typeof body !== 'object' || Array.isArray(body)) {
      return NextResponse.json({ error: 'Request body must be a valid JSON object' }, { status: 400 });
    }

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

    if (!startupName || typeof startupName !== 'string' || startupName.trim().length < 2) {
      return NextResponse.json({ error: 'Please enter a valid startup name.' }, { status: 400 });
    }

    if (!founderName || typeof founderName !== 'string' || founderName.trim().length < 2) {
      return NextResponse.json({ error: 'Please enter founder / contact person name.' }, { status: 400 });
    }

    if (!email || typeof email !== 'string' || !isValidEmail(email)) {
      return NextResponse.json({ error: 'Please enter a valid work email address.' }, { status: 400 });
    }

    if (!phone || typeof phone !== 'string' || phone.trim().replace(/\D/g, '').length < 10) {
      return NextResponse.json({ error: 'Please enter a valid contact phone number.' }, { status: 400 });
    }

    if (!city || typeof city !== 'string' || !city.trim()) {
      return NextResponse.json({ error: 'Please enter your headquarters city.' }, { status: 400 });
    }

    if (!description || typeof description !== 'string' || description.trim().length < 10) {
      return NextResponse.json({ error: 'Please provide a brief description of what your startup does.' }, { status: 400 });
    }

    if (!challengeStmt || typeof challengeStmt !== 'string' || challengeStmt.trim().length < 10) {
      return NextResponse.json({ error: 'Please describe the engineering challenge or collaboration opportunity.' }, { status: 400 });
    }

    const cleanServices = Array.isArray(servicesNeeded) ? servicesNeeded.filter(s => typeof s === 'string').slice(0, 20) : [];

    const registration = await db.startupRegistration.create({
      data: {
        startupName: startupName.trim().slice(0, 150),
        founderName: founderName.trim().slice(0, 150),
        email: email.trim().toLowerCase(),
        phone: phone.trim().slice(0, 30),
        city: city.trim().slice(0, 100),
        stage: (typeof stage === 'string' && stage.trim()) ? stage.trim().slice(0, 50) : 'Early Stage',
        domain: (typeof domain === 'string' && domain.trim()) ? domain.trim().slice(0, 100) : 'Technology',
        teamSize: (typeof teamSize === 'string' && teamSize.trim()) ? teamSize.trim().slice(0, 50) : '1-10',
        currentFunding: (typeof currentFunding === 'string' && currentFunding.trim()) ? currentFunding.trim().slice(0, 100) : null,
        servicesNeeded: cleanServices,
        description: description.trim().slice(0, 5000),
        challengeStmt: challengeStmt.trim().slice(0, 5000),
        consent: Boolean(consent)
      }
    });

    return NextResponse.json({ success: true, id: registration.id }, { status: 201 });
  } catch (err) {
    console.error('Startup registration error:', err);
    return NextResponse.json({ error: 'Failed to register startup. Please try again later.' }, { status: 500 });
  }
}
