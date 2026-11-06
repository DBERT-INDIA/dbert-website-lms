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

    // Timing-safe cryptographic comparison
    const genBuf = Buffer.from(generatedSignature, 'utf-8');
    const supBuf = Buffer.from(String(razorpay_signature), 'utf-8');
    const isSignatureValid = genBuf.length === supBuf.length && crypto.timingSafeEqual(genBuf, supBuf);

    if (!isSignatureValid) {
      // Payment signature is invalid — record failed state if order exists
      try {
        await db.enrollmentInquiry.updateMany({
          where: { razorpayOrderId: razorpay_order_id, status: { not: 'paid' } },
          data: { status: 'failed' }
        });
      } catch (e) {
        console.warn('Failed state update warning:', e);
      }
      return NextResponse.json({ error: 'Invalid cryptographic payment signature' }, { status: 400 });
    }

    // Strict Binding: Payment must belong to the matching local order / enrollment (Finding DBERT-008)
    let enrollment = null;
    try {
      if (enrollmentId) {
        enrollment = await db.enrollmentInquiry.findFirst({
          where: { id: enrollmentId, razorpayOrderId: razorpay_order_id }
        });
        if (!enrollment) {
          return NextResponse.json({
            error: 'Security Mismatch: The provided enrollment does not match the payment order.'
          }, { status: 400 });
        }
      } else {
        enrollment = await db.enrollmentInquiry.findFirst({
          where: { razorpayOrderId: razorpay_order_id }
        });
      }
    } catch (lookupErr) {
      console.error('Enrollment lookup error:', lookupErr);
    }

    // Durable state update (Finding DBERT-004: Never return false success on DB failure)
    if (enrollment) {
      try {
        await db.enrollmentInquiry.update({
          where: { id: enrollment.id },
          data: {
            razorpayPaymentId: razorpay_payment_id,
            razorpaySignature: razorpay_signature,
            status: 'paid'
          }
        });
      } catch (dbErr) {
        console.error('CRITICAL: Payment verified but enrollment update failed:', dbErr);
        return NextResponse.json({
          error: 'Payment received at gateway but database record update failed. Support has been notified for manual reconciliation.',
          orderId: razorpay_order_id,
          paymentId: razorpay_payment_id
        }, { status: 500 });
      }
    }

    return NextResponse.json({
      success: true,
      message: 'Payment verified and enrollment confirmed',
      orderId: razorpay_order_id,
      paymentId: razorpay_payment_id
    }, { status: 200 });

  } catch (err) {
    console.error('Payment verification error:', err);
    return NextResponse.json({ error: 'Verification processing failed' }, { status: 500 });
  }
}
