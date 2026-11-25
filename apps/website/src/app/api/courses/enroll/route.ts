import { NextRequest, NextResponse } from 'next/server';
import {
  PaymentClaimSubmissionError,
  submitEnrollmentPaymentClaim,
} from '@/lib/enrollment-payment-claim';
import { PRICING_CONFIG } from '@/config/pricing.config';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json().catch(() => null);
    const receipt = await submitEnrollmentPaymentClaim(body, 'deposit', PRICING_CONFIG.cautionDeposit);
    return NextResponse.json({
      ...receipt,
      redirectUrl: 'https://lms.dbert.in/portal/payment-claims',
      message: receipt.claimStatus === 'pending'
        ? 'Your payment claim is pending verification.'
        : 'This payment claim has already been reviewed.',
    }, { status: receipt.alreadySubmitted ? 200 : 201 });
  } catch (error) {
    if (error instanceof PaymentClaimSubmissionError) {
      return NextResponse.json({ success: false, error: error.message }, { status: error.status });
    }
    return NextResponse.json({
      success: false,
      error: 'Payment submission is temporarily unavailable. Please try again shortly.',
    }, { status: 503 });
  }
}
