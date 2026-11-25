import { randomUUID } from 'node:crypto';

type PaymentType = 'deposit' | 'balance';
type ClaimStatus = 'pending' | 'verified' | 'rejected';

export class PaymentClaimSubmissionError extends Error {
  readonly status: number;

  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

function field(body: Record<string, unknown>, keys: string[], maxLength: number): string {
  for (const key of keys) {
    const rawValue = body[key];
    if (rawValue == null) continue;
    if (typeof rawValue !== 'string' || rawValue.trim().length > maxLength) {
      throw new PaymentClaimSubmissionError('Check the payment form fields and try again.', 400);
    }
    if (rawValue.trim()) return rawValue.trim();
  }
  return '';
}

export async function submitEnrollmentPaymentClaim(
  rawBody: unknown,
  paymentType: PaymentType,
  amount: number,
) {
  if (!rawBody || typeof rawBody !== 'object' || Array.isArray(rawBody)) {
    throw new PaymentClaimSubmissionError('Send a valid payment form.', 400);
  }
  const body = rawBody as Record<string, unknown>;
  const name = field(body, ['fullName', 'name'], 120);
  const email = field(body, ['email'], 254).toLowerCase();
  const phone = field(body, ['phone', 'whatsapp'], 32);
  const college = field(body, ['college'], 160);
  const domain = field(body, ['domain', 'track'], 100);
  const utr = field(body, ['utrNumber', 'utr'], 64).toUpperCase();
  const certId = field(body, ['certId'], 80);
  const internId = field(body, ['internId'], 80);
  const remarks = field(body, ['remarks'], 400);
  if (!name) throw new PaymentClaimSubmissionError('Enter your full name.', 400);
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    throw new PaymentClaimSubmissionError('Enter a valid email address.', 400);
  }
  if (phone.replace(/\D/g, '').length < 10) {
    throw new PaymentClaimSubmissionError('Enter a valid phone number.', 400);
  }
  if (!domain) throw new PaymentClaimSubmissionError('Select an enrollment track.', 400);
  if (!/^[A-Z0-9]{6,64}$/.test(utr)) {
    throw new PaymentClaimSubmissionError('Enter a valid UPI transaction reference.', 400);
  }

  const endpoint = process.env.INTERNAL_LMS_SYNC_URL?.trim()
    || (process.env.NODE_ENV === 'production' ? 'https://lms.dbert.in/api/internal/enrollment-sync' : '');
  const secret = process.env.INTERNAL_SYNC_SECRET?.trim();
  if (!endpoint || !secret) {
    throw new PaymentClaimSubmissionError('Payment submission is temporarily unavailable. Please try again shortly.', 503);
  }
  let response: Response;
  try {
    response = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-DBERT-Internal-Secret': secret },
      body: JSON.stringify({
        name, email, phone, college, domain, utr, amount,
        cert_id: certId, intern_reference: internId, remarks,
        payment_type: paymentType,
        submission_id: `DBERT-${randomUUID()}`,
      }),
      redirect: 'error',
      cache: 'no-store',
      signal: AbortSignal.timeout(5000),
    });
  } catch {
    throw new PaymentClaimSubmissionError(
      'We could not confirm that your claim was received. Retry with the same transaction reference.',
      503,
    );
  }
  if (response.status === 409) {
    throw new PaymentClaimSubmissionError('This payment reference is already associated with a different claim.', 409);
  }
  if (response.status === 400) {
    throw new PaymentClaimSubmissionError('Check your enrollment track and payment details and try again.', 400);
  }

  const receipt = await response.json().catch(() => null);
  const claimStatus: ClaimStatus = receipt?.claim_status;
  if (
    !response.ok || receipt?.status !== 'success' || typeof receipt.submission_id !== 'string'
    || typeof receipt.submitted_at !== 'string' || receipt.amount !== amount
    || !['pending', 'verified', 'rejected'].includes(claimStatus)
  ) {
    throw new PaymentClaimSubmissionError(
      'We could not confirm that your claim was received. Retry with the same transaction reference.',
      503,
    );
  }
  return {
    success: true,
    alreadySubmitted: receipt.duplicate === true,
    submissionId: receipt.submission_id,
    submittedAt: receipt.submitted_at,
    candidateName: name,
    certId,
    domain,
    utrNumber: utr,
    amount,
    claimStatus,
  };
}
