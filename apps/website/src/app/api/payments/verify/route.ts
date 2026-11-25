import { NextResponse } from 'next/server';
import { razorpay } from '@/lib/razorpay';
import { loadWebsiteOrder, reconcileWebsiteCapture } from '@/lib/website-payment-ledger';
import { matchesPaymentSignature, WebsitePaymentError, websiteReceiptPayload } from '@/lib/website-payment-contract';

export async function POST(request: Request) {
  const secret = process.env.RAZORPAY_KEY_SECRET?.trim();
  if (!secret) return NextResponse.json({ error: 'The payment gateway is unavailable.' }, { status: 503 });

  const body = await request.json().catch(() => null);
  if (!body || typeof body !== 'object' || Array.isArray(body)) {
    return NextResponse.json({ error: 'Invalid payment details.' }, { status: 400 });
  }
  const { razorpay_order_id: orderId, razorpay_payment_id: paymentId, razorpay_signature, checkoutToken } = body;
  if (
    typeof orderId !== 'string' || !/^order_[A-Za-z0-9_-]{1,80}$/.test(orderId)
    || typeof paymentId !== 'string' || !/^pay_[A-Za-z0-9_-]{1,80}$/.test(paymentId)
    || !matchesPaymentSignature(orderId + '|' + paymentId, razorpay_signature, secret)
  ) {
    return NextResponse.json({ error: 'The payment signature could not be verified.' }, { status: 400 });
  }

  try {
    const enrollment = await loadWebsiteOrder(orderId);
    if (!matchesPaymentSignature(websiteReceiptPayload(enrollment), checkoutToken, secret)) {
      return NextResponse.json({ error: 'This checkout could not be matched to your payment.' }, { status: 403 });
    }
    if (enrollment.status !== 'paid' || enrollment.razorpayPaymentId !== paymentId) {
      const capture = await razorpay.payments.fetch(paymentId);
      await reconcileWebsiteCapture(enrollment, paymentId, capture);
    }
    return NextResponse.json({ success: true, message: 'Payment verified.', orderId, paymentId });
  } catch (error) {
    if (error instanceof WebsitePaymentError) {
      return NextResponse.json({ error: error.message }, { status: error.status });
    }
    return NextResponse.json({ error: 'Payment could not be verified. Try again shortly.' }, { status: 503 });
  }
}
