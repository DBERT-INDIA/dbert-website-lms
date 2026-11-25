import { createHmac, timingSafeEqual } from 'node:crypto';

const PROGRAM_AMOUNTS = {
  incubation_caution_deposit: 49900,
  caution_deposit: 49900,
  incubation_balance_1500: 150000,
  incubation_full_1999: 199900,
  certification_verification: 29900,
  fellowship: 49900,
  launchpad: 49900,
};

export class WebsitePaymentError extends Error {
  readonly status: number;

  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

export function websiteProgramAmount(programName: string): number {
  const key = programName.trim().toLowerCase().replace(/[^a-z0-9]+/g, '_');
  return Object.hasOwn(PROGRAM_AMOUNTS, key) ? PROGRAM_AMOUNTS[key as keyof typeof PROGRAM_AMOUNTS] : 0;
}

export function signWebsitePayment(payload: string | Buffer, secret: string): string {
  return createHmac('sha256', secret).update(payload).digest('hex');
}

export function matchesPaymentSignature(payload: string | Buffer, signature: unknown, secret: string): boolean {
  if (!secret || typeof signature !== 'string' || !/^[0-9a-f]{64}$/i.test(signature)) return false;
  const expected = Buffer.from(signWebsitePayment(payload, secret), 'hex');
  const supplied = Buffer.from(signature, 'hex');
  return timingSafeEqual(expected, supplied);
}

export type WebsiteOrder = {
  id: string;
  email: string;
  amount: number | null;
  status: string;
  razorpayOrderId: string | null;
  razorpayPaymentId: string | null;
};

export function websiteReceiptPayload(order: WebsiteOrder): string {
  return JSON.stringify(['db-website-checkout-v1', order.id, order.razorpayOrderId, order.email]);
}

export function validateWebsiteCapture(order: WebsiteOrder, paymentId: string, raw: unknown) {
  if (!raw || typeof raw !== 'object' || !order.amount || !order.razorpayOrderId) {
    throw new WebsitePaymentError('The payment order could not be confirmed.', 409);
  }
  const capture = raw as Record<string, unknown>;
  if (
    capture.id !== paymentId || capture.order_id !== order.razorpayOrderId
    || capture.amount !== order.amount || capture.currency !== 'INR'
    || capture.status !== 'captured'
  ) {
    throw new WebsitePaymentError('The captured payment does not match the expected order.', 409);
  }
}
