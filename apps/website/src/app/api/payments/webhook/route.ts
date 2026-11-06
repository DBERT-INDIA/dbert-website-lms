import { NextResponse } from 'next/server';
import crypto from 'crypto';
import db from '@/lib/db';

export async function POST(request: Request) {
  try {
    const rawBody = await request.text();
    const signature = request.headers.get('x-razorpay-signature');
    
    if (!signature) {
      return NextResponse.json({ error: 'Missing signature' }, { status: 400 });
    }

    const webhookSecret = process.env.RAZORPAY_WEBHOOK_SECRET;
    if (!webhookSecret) {
      return NextResponse.json({ error: 'Server misconfiguration: Webhook secret not found' }, { status: 500 });
    }

    const expectedSignature = crypto
      .createHmac('sha256', webhookSecret)
      .update(rawBody)
      .digest('hex');

    // Timing-safe HMAC verification
    const expBuf = Buffer.from(expectedSignature, 'utf-8');
    const sigBuf = Buffer.from(signature, 'utf-8');
    if (expBuf.length !== sigBuf.length || !crypto.timingSafeEqual(expBuf, sigBuf)) {
      return NextResponse.json({ error: 'Invalid webhook signature' }, { status: 400 });
    }

    const event = JSON.parse(rawBody);

    if (event.event === 'payment.captured' || event.event === 'order.paid') {
      const paymentEntity = event.payload?.payment?.entity;
      const orderId = paymentEntity?.order_id || event.payload?.order?.entity?.id;
      
      if (orderId) {
        await db.enrollmentInquiry.updateMany({
          where: { razorpayOrderId: orderId },
          data: { status: 'paid', razorpayPaymentId: paymentEntity?.id }
        });
      }
    } else if (event.event === 'payment.failed') {
      const paymentEntity = event.payload?.payment?.entity;
      const orderId = paymentEntity?.order_id;
      
      // State Guard: Stale payment.failed callback MUST NOT downgrade an already paid order
      if (orderId) {
        await db.enrollmentInquiry.updateMany({
          where: { razorpayOrderId: orderId, status: { not: 'paid' } },
          data: { status: 'failed' }
        });
      }
    }

    return NextResponse.json({ status: 'ok' }, { status: 200 });
  } catch (err) {
    console.error('Webhook processing error:', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
