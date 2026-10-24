import { NextResponse } from 'next/server';
import crypto from 'crypto';
import db from '@/lib/db';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { razorpay_order_id, razorpay_payment_id, razorpay_signature, enrollmentId } = body;

    // Require all payment fields
    if (!razorpay_order_id || !razorpay_payment_id || !razorpay_signature) {
      return NextResponse.json({ error: 'Missing payment fields: razorpay_order_id, razorpay_payment_id, razorpay_signature' }, { status: 400 });
    }

    const secret = process.env.RAZORPAY_KEY_SECRET;
    if (!secret) {
      return NextResponse.json({ error: 'Server misconfiguration: Secret not found' }, { status: 500 });
    }

    // HMAC-SHA256 over "order_id|payment_id"
    const signaturePayload = `${String(razorpay_order_id)}|${String(razorpay_payment_id)}`;
    const generatedSignature = crypto
      .createHmac('sha256', secret)
      .update(signaturePayload)
      .digest('hex');

    if (generatedSignature === razorpay_signature) {
      // Payment is valid — update enrollment to paid
      if (enrollmentId) {
        try {
          await db.enrollmentInquiry.update({
            where: { id: enrollmentId },
            data: {
              razorpayPaymentId: razorpay_payment_id,
              razorpaySignature: razorpay_signature,
              status: 'paid'
            }
          });
        } catch (dbErr) {
          console.warn('Enrollment DB update skipped (DB may be unreachable):', dbErr);
        }
      }
      return NextResponse.json({ success: true, message: 'Payment verified successfully' }, { status: 200 });
    } else {
      // Payment is invalid — do NOT mark as paid
      if (enrollmentId) {
        try {
          await db.enrollmentInquiry.update({
            where: { id: enrollmentId },
            data: {
              status: 'failed'
            }
          });
        } catch (dbErr) {
          console.warn('Enrollment DB update skipped (DB may be unreachable):', dbErr);
        }
      }
      return NextResponse.json({ error: 'Invalid signature' }, { status: 400 });
    }
  } catch (err) {
    console.error('Payment verification error:', err);
    return NextResponse.json({ error: 'Verification failed' }, { status: 500 });
  }
}
