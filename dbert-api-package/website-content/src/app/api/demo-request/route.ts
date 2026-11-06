import { NextResponse } from 'next/server';
import db from '@/lib/db';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { name, email, phone, companyName, productName, message } = body;

    if (!name || !email || !productName) {
      return NextResponse.json({ error: 'Missing required parameters' }, { status: 400 });
    }

    const demoReq = await db.demoRequest.create({
      data: {
        name,
        email,
        phone: phone || null,
        companyName: companyName || null,
        productName,
        message: message || null,
      }
    });

    return NextResponse.json({ success: true, id: demoReq.id }, { status: 201 });
  } catch (err) {
    console.error('Demo request error:', err);
    return NextResponse.json({ error: 'Failed to request demo' }, { status: 500 });
  }
}
