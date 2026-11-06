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

    const { name, email, phone, companyName, companySize, serviceType, description, preferredDate } = body;

    if (!name || typeof name !== 'string' || name.trim().length < 2 || name.trim().length > 150) {
      return NextResponse.json({ error: 'Please enter a valid contact name (2-150 characters).' }, { status: 400 });
    }

    if (!email || typeof email !== 'string' || !isValidEmail(email) || email.trim().length > 254) {
      return NextResponse.json({ error: 'Please enter a valid business email address.' }, { status: 400 });
    }

    if (!phone || typeof phone !== 'string' || phone.trim().replace(/\D/g, '').length < 10) {
      return NextResponse.json({ error: 'Please enter a valid contact phone number.' }, { status: 400 });
    }

    if (!serviceType || typeof serviceType !== 'string' || serviceType.trim().length < 2) {
      return NextResponse.json({ error: 'Please select an architectural service type.' }, { status: 400 });
    }

    const cleanCompany = (typeof companyName === 'string' && companyName.trim()) ? companyName.trim().slice(0, 200) : null;
    const cleanSize = (typeof companySize === 'string' && companySize.trim()) ? companySize.trim().slice(0, 50) : null;
    const cleanDesc = (typeof description === 'string' && description.trim()) ? description.trim().slice(0, 4000) : null;
    const cleanDate = (typeof preferredDate === 'string' && preferredDate.trim()) ? preferredDate.trim().slice(0, 50) : null;

    const booking = await db.consultationBooking.create({
      data: {
        name: name.trim(),
        email: email.trim().toLowerCase(),
        phone: phone.trim(),
        companyName: cleanCompany,
        companySize: cleanSize,
        serviceType: serviceType.trim(),
        description: cleanDesc,
        preferredDate: cleanDate,
      }
    });

    return NextResponse.json({ success: true, id: booking.id }, { status: 201 });
  } catch (err) {
    console.error('Consultation booking error:', err);
    return NextResponse.json({ error: 'Failed to request consultation. Please try again later.' }, { status: 500 });
  }
}
