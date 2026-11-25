import { getDb } from '@/lib/db';
import {
  validateWebsiteCapture,
  WebsitePaymentError,
  type WebsiteOrder,
} from '@/lib/website-payment-contract';

const orderFields = {
  id: true, email: true, amount: true, status: true, razorpayOrderId: true, razorpayPaymentId: true,
} as const;

export async function loadWebsiteOrder(orderId: string): Promise<WebsiteOrder> {
  const candidates = await getDb().enrollmentInquiry.findMany({
    where: { razorpayOrderId: orderId },
    select: orderFields,
    take: 2,
  });
  if (!candidates.length) throw new WebsitePaymentError('The payment order could not be found.', 404);
  if (candidates.length !== 1) throw new WebsitePaymentError('The order requires manual reconciliation.', 409);
  return candidates[0];
}

export async function reconcileWebsiteCapture(order: WebsiteOrder, paymentId: string, raw: unknown) {
  validateWebsiteCapture(order, paymentId, raw);
  const settled = await getDb().enrollmentInquiry.updateMany({
    where: {
      id: order.id, amount: order.amount, razorpayOrderId: order.razorpayOrderId,
      status: { in: ['payment_pending', 'failed'] }, razorpayPaymentId: null,
    },
    data: { status: 'paid', razorpayPaymentId: paymentId },
  });
  if (settled.count === 1) return;
  const latest = await getDb().enrollmentInquiry.findUnique({ where: { id: order.id }, select: orderFields });
  if (latest?.status === 'paid' && latest.razorpayPaymentId === paymentId) return;
  throw new WebsitePaymentError('The order requires manual reconciliation.', 409);
}
