import { NextResponse } from 'next/server';
import { razorpay } from '@/lib/razorpay';
import db from '@/lib/db';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { programName, domain, amount, name, email, phone } = body;

    if (!programName || !name || !email || !phone) {
      return NextResponse.json({ error: 'Missing required fields' }, { status: 400 });
    }

    // amount must be a finite integer in paise, and at least the Razorpay minimum (100 paise = ₹1)
    const numericAmount = Number(amount);
    if (!Number.isFinite(numericAmount) || !Number.isInteger(numericAmount)) {
      return NextResponse.json({ error: 'Invalid amount: must be an integer in paise' }, { status: 400 });
    }
    if (numericAmount < 100) {
      return NextResponse.json({ error: 'Amount must be at least 100 paise (₹1)' }, { status: 400 });
    }

    const orderOptions = {
      amount: numericAmount,
      currency: "INR",
      receipt: `receipt_${Date.now()}`
    };

    // Step 1 — create the Razorpay order first (critical path)
    const order = await razorpay.orders.create(orderOptions);

    // Step 2 — try to persist enrollment (non-critical: payment still works without it)
    let enrollmentId: string | number | bigint | null = null;
    try {
      const enrollment = await db.enrollmentInquiry.create({
        data: {
          name,
          email,
          phone,
          programName,
          domain: domain || null,
          amount: numericAmount,
          razorpayOrderId: order.id,
          status: 'payment_pending'
        }
      });
      enrollmentId = enrollment.id;
    } catch (dbErr) {
      console.warn('Enrollment DB write skipped (DB may be unreachable):', dbErr);
    }

    return NextResponse.json({
      success: true,
      orderId: order.id,
      enrollmentId,
      keyId: process.env.NEXT_PUBLIC_RAZORPAY_KEY_ID
    }, { status: 201 });

  } catch (err) {
    console.error('Order creation error:', err);
    return NextResponse.json({ error: 'Failed to create order' }, { status: 500 });
  }
}
