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

    const { name, email, phone, subject, message, sourcePage } = body;

    if (!name || typeof name !== 'string' || name.trim().length < 2 || name.trim().length > 150) {
      return NextResponse.json({ error: 'Please enter a valid name (2-150 characters).' }, { status: 400 });
    }

    if (!email || typeof email !== 'string' || !isValidEmail(email) || email.trim().length > 254) {
      return NextResponse.json({ error: 'Please enter a valid email address.' }, { status: 400 });
    }

    if (!subject || typeof subject !== 'string' || subject.trim().length < 2 || subject.trim().length > 200) {
      return NextResponse.json({ error: 'Please enter a valid subject (2-200 characters).' }, { status: 400 });
    }

    if (!message || typeof message !== 'string' || message.trim().length < 5 || message.trim().length > 5000) {
      return NextResponse.json({ error: 'Message must be between 5 and 5,000 characters.' }, { status: 400 });
    }

    const cleanSource = (typeof sourcePage === 'string' && sourcePage.trim()) ? sourcePage.trim().slice(0, 100) : 'contact';
    const cleanPhone = (typeof phone === 'string' && phone.trim()) ? phone.trim().slice(0, 30) : null;

    const submission = await db.contactSubmission.create({
      data: {
        name: name.trim(),
        email: email.trim().toLowerCase(),
        phone: cleanPhone,
        subject: subject.trim(),
        message: message.trim(),
        sourcePage: cleanSource,
      }
    });

    return NextResponse.json({ success: true, id: submission.id }, { status: 201 });
  } catch (err) {
    console.error('Contact submission error:', err);
    return NextResponse.json({ error: 'Unable to process your request at this time. Please try again later.' }, { status: 500 });
  }
}
