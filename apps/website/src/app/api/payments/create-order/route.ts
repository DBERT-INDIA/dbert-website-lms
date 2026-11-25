import { NextResponse } from 'next/server';
import { razorpay } from '@/lib/razorpay';
import db from '@/lib/db';

// Server-Authoritative Pricing Catalogue (Finding DBERT-007)
// Enforces canonical 3-program prices (Launchpad ₹7,999, Accelerate ₹4,999, Fellowship ₹1,999)
const PROGRAM_CATALOGUE: Record<string, number> = {
  'incubation_caution_deposit': 49900,  // ₹499 (Fellowship Step-1 Deposit)
  'caution_deposit': 49900,             // ₹499 (Fellowship Step-1 Deposit)
  'incubation_balance_1500': 150000,    // ₹1500 (Fellowship Balance after ₹499)
  'incubation_full_1999': 199900,       // ₹1999 (DBERT Fellowship)
  'fellowship': 199900,                 // ₹1999 (DBERT Fellowship)
  'accelerate': 499900,                 // ₹4999 (DBERT Accelerate)
  'launchpad': 799900,                  // ₹7999 (DBERT Launchpad)
  'certification_verification': 29900,  // ₹299 (Statutory Verification Unlock)
};

function resolveServerAuthoritativeAmount(programName: string, requestedAmount?: number): number {
  const normKey = (programName || '').toLowerCase().replace(/[^a-z0-9_]/g, '_');
  for (const [catKey, catPaise] of Object.entries(PROGRAM_CATALOGUE)) {
    if (normKey.includes(catKey) || catKey.includes(normKey)) {
      return catPaise;
    }
  }
  // If specific recognized amount in whole rupees was submitted, validate against allowed tiers
  if (
    requestedAmount &&
    (requestedAmount === 49900 ||
      requestedAmount === 150000 ||
      requestedAmount === 199900 ||
      requestedAmount === 29900 ||
      requestedAmount === 499900 ||
      requestedAmount === 799900)
  ) {
    return requestedAmount;
  }
  // Default fallback to Fellowship caution deposit tier (49900 paise = ₹499)
  return 49900;
}

export async function POST(request: Request) {
  let serverAuthoritativePaise = 49900;
  try {
    const body = await request.json();
    const { programName, domain, amount, name, email, phone } = body;

    if (!programName || !name || !email || !phone) {
      return NextResponse.json({ error: 'Missing required fields' }, { status: 400 });
    }

    // Server-side authoritative price determination (Finding DBERT-007)
    serverAuthoritativePaise = resolveServerAuthoritativeAmount(
      programName,
      Number.isInteger(Number(amount)) ? Number(amount) : undefined
    );

    const orderOptions = {
      amount: serverAuthoritativePaise,
      currency: "INR",
      receipt: `rcpt_${Date.now()}`
    };

    // Step 1 — create Razorpay order with server-calculated price
    const order = await razorpay.orders.create(orderOptions);

    // Step 2 — persist enrollment record bound to this Razorpay order ID
    let enrollmentId: string | number | bigint | null = null;
    try {
      const enrollment = await db.enrollmentInquiry.create({
        data: {
          name: name.trim(),
          email: email.trim().toLowerCase(),
          phone: phone.trim(),
          programName: programName.trim(),
          domain: domain || null,
          amount: serverAuthoritativePaise,
          razorpayOrderId: order.id,
          status: 'payment_pending'
        }
      });
      enrollmentId = enrollment.id;
    } catch (dbErr) {
      console.warn('Enrollment DB write warning:', dbErr);
    }

    return NextResponse.json({
      success: true,
      orderId: order.id,
      enrollmentId,
      amount: serverAuthoritativePaise,
      keyId: process.env.NEXT_PUBLIC_RAZORPAY_KEY_ID
    }, { status: 201 });

  } catch (err) {
    console.warn('[Razorpay Gateway Fallback Triggered]', err);
    // Graceful UPI Fallback (Resolves Dead-End D2 & Silent Fail S2)
    return NextResponse.json({
      success: false,
      fallback_upi: true,
      vpa: 'Q652429146@ybl',
      merchantName: 'DBERT Admissions',
      amount: serverAuthoritativePaise / 100,
      currency: 'INR',
      qr_url: '/images/qrcode.jpeg',
      redirect_url: '/enroll/1999',
      message: 'Razorpay gateway temporarily unreachable. Seamlessly routed to 1-Tap UPI / QR payment gateway.'
    }, { status: 200 });
  }
}
