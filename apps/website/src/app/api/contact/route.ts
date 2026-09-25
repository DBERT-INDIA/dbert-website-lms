import { NextResponse } from 'next/server';
import db from '@/lib/db';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { name, email, phone, subject, message, sourcePage } = body;

    if (!name || !email || !subject || !message || !sourcePage) {
      return NextResponse.json({ error: 'Missing required parameters' }, { status: 400 });
    }

    const submission = await db.contactSubmission.create({
      data: {
        name,
        email,
        phone: phone || null,
        subject,
        message,
        sourcePage,
      }
    });

    return NextResponse.json({ success: true, id: submission.id }, { status: 201 });
  } catch (err) {
    console.error('Contact submission error:', err);
    return NextResponse.json({ error: 'Failed to send message' }, { status: 500 });
  }
}
