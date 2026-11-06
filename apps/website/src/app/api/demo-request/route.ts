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

    const { name, email, phone, companyName, productName, message } = body;

    if (!name || typeof name !== 'string' || name.trim().length < 2 || name.trim().length > 150) {
      return NextResponse.json({ error: 'Please enter a valid full name (2-150 characters).' }, { status: 400 });
    }

    if (!email || typeof email !== 'string' || !isValidEmail(email) || email.trim().length > 254) {
      return NextResponse.json({ error: 'Please enter a valid business email address.' }, { status: 400 });
    }

    if (!productName || typeof productName !== 'string' || productName.trim().length < 2 || productName.trim().length > 150) {
      return NextResponse.json({ error: 'Please select a valid product.' }, { status: 400 });
    }

    const cleanCompany = (typeof companyName === 'string' && companyName.trim()) ? companyName.trim().slice(0, 200) : null;
    const cleanPhone = (typeof phone === 'string' && phone.trim()) ? phone.trim().slice(0, 30) : null;
    const cleanMessage = (typeof message === 'string' && message.trim()) ? message.trim().slice(0, 4000) : null;

    const demoReq = await db.demoRequest.create({
      data: {
        name: name.trim(),
        email: email.trim().toLowerCase(),
        phone: cleanPhone,
        companyName: cleanCompany,
        productName: productName.trim(),
        message: cleanMessage,
      }
    });

    return NextResponse.json({ success: true, id: demoReq.id }, { status: 201 });
  } catch (err) {
    console.error('Demo request error:', err);
    return NextResponse.json({ error: 'Failed to process demo request. Please try again later.' }, { status: 500 });
  }
}
