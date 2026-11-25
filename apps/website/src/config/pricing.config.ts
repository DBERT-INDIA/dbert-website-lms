/**
 * pricing.config.ts - Centralized Financial & Payment Ledger Configuration
 * 
 * Single source of truth for all fee structures, caution deposits,
 * merchant UPI coordinates, and contact hotlines across the DBERT Next.js website.
 */

export const PRICING_CONFIG = {
  // Canonical 3-Program Tuition Schedule (INR) — All Programs Unified to 2 Months (8 Weeks)
  launchpadFee: 7999,
  accelerateFee: 4999,
  fellowshipFee: 1999,
  programDurationLabel: '2 Months (8 Weeks)',

  // Fellowship (₹1,999) internal 2-step ledger & statutory verification
  cautionDeposit: 499,
  balancePayable: 1500,
  totalProgramFee: 1999,
  verificationFee: 299,

  programs: {
    launchpad: {
      name: 'DBERT Launchpad',
      level: 'Beginner · 0-to-1 Foundations',
      duration: '2 Months (8 Weeks)',
      fee: 7999,
      href: '/learners/launchpad',
    },
    accelerate: {
      name: 'DBERT Accelerate',
      level: 'Intermediate · Applied Industrial Sprints',
      duration: '2 Months (8 Weeks)',
      fee: 4999,
      href: '/learners/accelerate',
    },
    fellowship: {
      name: 'DBERT Fellowship',
      level: 'Production · Live Client Repo Internship',
      duration: '2 Months (8 Weeks)',
      fee: 1999,
      href: '/learners/courses',
    },
  },

  // Payment coordinates
  merchantVpa: process.env.NEXT_PUBLIC_MERCHANT_VPA || 'Q652429146@ybl',
  merchantName: process.env.NEXT_PUBLIC_MERCHANT_NAME || 'DBERT Admissions',
  qrCodePath: '/images/qrcode.jpeg',
  qrCodeFallback: '/qrcode.jpeg',

  // Admissions & Support Concierge
  admissionsPhone: '+91 81929 11360',
  admissionsWhatsApp: '918192911360',
  supportEmail: 'admissions@dbert.in',
} as const;

/**
 * Format a number as Indian Rupee string (e.g. 1500 -> "₹1,500").
 */
export function formatINR(amount: number): string {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(amount);
}

/**
 * Generates standard UPI payment URL for 1-tap mobile checkout.
 */
export function buildUpiUri(params: {
  amount?: number;
  note?: string;
  vpa?: string;
  payeeName?: string;
}): string {
  const vpa = params.vpa || PRICING_CONFIG.merchantVpa;
  const name = params.payeeName || PRICING_CONFIG.merchantName;
  const amount = params.amount ?? PRICING_CONFIG.balancePayable;
  const note = params.note || 'DBERT-BALANCE-1500';

  const query = new URLSearchParams({
    pa: vpa,
    pn: name,
    am: amount.toString(),
    cu: 'INR',
    tn: note,
  });

  return `upi://pay?${query.toString()}`;
}
