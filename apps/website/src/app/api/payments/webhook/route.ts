import { NextResponse } from 'next/server';
import { loadWebsiteOrder, reconcileWebsiteCapture } from '@/lib/website-payment-ledger';
import { matchesPaymentSignature, WebsitePaymentError } from '@/lib/website-payment-contract';

export async function POST(request: Request) {
  const secret = process.env.RAZORPAY_WEBHOOK_SECRET?.trim();
  if (!secret) return NextResponse.json({ error: 'The payment webhook is unavailable.' }, { status: 503 });

  const body = Buffer.from(await request.arrayBuffer());
  if (!matchesPaymentSignature(body, request.headers.get('x-razorpay-signature'), secret)) {
    return NextResponse.json({ error: 'Invalid webhook signature.' }, { status: 400 });
  }
  let event;
  try {
    event = JSON.parse(body.toString('utf8'));
  } catch {
    return NextResponse.json({ error: 'Invalid webhook payload.' }, { status: 400 });
  }
  if (!event || typeof event !== 'object' || Array.isArray(event)) {
    return NextResponse.json({ error: 'Invalid webhook payload.' }, { status: 400 });
  }
  if (event.event !== 'payment.captured' && event.event !== 'order.paid') {
    return NextResponse.json({ status: 'ignored' });
  }

  const capture = event.payload?.payment?.entity;
  if (!capture || typeof capture.id !== 'string' || typeof capture.order_id !== 'string') {
    return NextResponse.json({ error: 'Captured payment details are missing.' }, { status: 400 });
  }

  try {
    const order = await loadWebsiteOrder(capture.order_id);
    await reconcileWebsiteCapture(order, capture.id, capture);
    return NextResponse.json({ status: 'processed' });
  } catch (error) {
    if (error instanceof WebsitePaymentError && error.status === 404) {
      // Accounts can deliver events for portal purchases to the website webhook.
      return NextResponse.json({ status: 'unmatched' });
    }
    if (error instanceof WebsitePaymentError) {
      return NextResponse.json({ error: error.message }, { status: error.status });
    }
    return NextResponse.json({ error: 'Payment could not be reconciled. Try again shortly.' }, { status: 503 });
  }
}
