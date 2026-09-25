import { NextResponse } from 'next/server';
import db from '@/lib/db';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { name, email, phone, companyName, companySize, serviceType, description, preferredDate } = body;

    if (!name || !email || !phone || !serviceType) {
      return NextResponse.json({ error: 'Missing required parameters' }, { status: 400 });
    }

    const booking = await db.consultationBooking.create({
      data: {
        name,
        email,
        phone,
        companyName: companyName || null,
        companySize: companySize || null,
        serviceType,
        description: description || null,
        preferredDate: preferredDate || null,
      }
    });

    return NextResponse.json({ success: true, id: booking.id }, { status: 201 });
  } catch (err) {
    console.error('Consultation booking error:', err);
    return NextResponse.json({ error: 'Failed to request consultation' }, { status: 500 });
  }
}
