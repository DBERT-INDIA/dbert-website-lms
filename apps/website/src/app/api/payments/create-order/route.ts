import { randomUUID } from 'node:crypto';
import { NextResponse } from 'next/server';
import { razorpay } from '@/lib/razorpay';
import { getDb } from '@/lib/db';
import { signWebsitePayment, websiteProgramAmount, websiteReceiptPayload } from '@/lib/website-payment-contract';

export async function POST(request: Request) {
  const secret = process.env.RAZORPAY_KEY_SECRET?.trim();
  if (!secret) return NextResponse.json({ error: 'The payment gateway is unavailable.' }, { status: 503 });

  const body = await request.json().catch(() => null);
  if (!body || typeof body !== 'object' || Array.isArray(body)) {
    return NextResponse.json({ error: 'Invalid payment details.' }, { status: 400 });
  }
  const { programName, domain, amount, name, email, phone } = body;
  const expected = typeof programName === 'string' ? websiteProgramAmount(programName) : 0;
  if (
    !expected || (amount != null && Number(amount) !== expected)
    || typeof name !== 'string' || !name.trim() || name.trim().length > 120
    || typeof email !== 'string' || email.trim().length > 254 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())
    || typeof phone !== 'string' || phone.trim().length > 32 || phone.replace(/\D/g, '').length < 10
    || (domain != null && (typeof domain !== 'string' || domain.length > 100))
  ) {
    return NextResponse.json({ error: 'Check the program and contact fields.' }, { status: 400 });
  }

  try {
    const order = await razorpay.orders.create({
      amount: expected,
      currency: 'INR',
      receipt: 'db_' + randomUUID(),
    });
    if (!order.id || order.amount !== expected || order.currency !== 'INR') {
      return NextResponse.json({ error: 'The payment gateway returned an invalid order.' }, { status: 503 });
    }

    const enrollment = await getDb().enrollmentInquiry.create({
      data: {
        name: name.trim(), email: email.trim().toLowerCase(), phone: phone.trim(),
        programName: programName.trim(), domain: domain?.trim() || null, amount: expected,
        razorpayOrderId: order.id, status: 'payment_pending',
      },
    });
    return NextResponse.json({
      success: true,
      orderId: order.id,
      enrollmentId: enrollment.id,
      checkoutToken: signWebsitePayment(websiteReceiptPayload(enrollment), secret),
      amount: expected,
      currency: 'INR',
      keyId: process.env.NEXT_PUBLIC_RAZORPAY_KEY_ID,
    }, { status: 201 });
  } catch {
    return NextResponse.json({ error: 'The payment order could not be saved. Try again shortly.' }, { status: 503 });
  }
}
