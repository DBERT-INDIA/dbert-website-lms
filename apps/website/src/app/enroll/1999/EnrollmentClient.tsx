'use client';

import React, { useState, useEffect, useSyncExternalStore } from 'react';
import { useSearchParams } from 'next/navigation';
import Link from 'next/link';
import s from './enroll.module.css';
import { PRICING_CONFIG, formatINR } from '@/config/pricing.config';
import { getNextCohortStandup } from '@/lib/cohortCalendar';
import { trackEvent } from '@/lib/analytics';
import AITrustBanner from '@/components/common/AITrustBanner';

interface CandidateData {
  certId: string;
  internId?: string;
  holderName: string;
  email?: string;
  phone?: string;
  college?: string;
  domain?: string;
  project?: string;
  batch?: string;
  isProvisional?: boolean;
  utrNumber?: string;
  amountPaid?: number;
  submissionId?: string;
}

interface SubmissionResponse {
  submissionId: string;
  submittedAt: string;
  candidateName: string;
  certId?: string;
  domain: string;
  utrNumber: string;
  amount: number;
  claimStatus?: 'pending' | 'verified' | 'rejected';
}

interface ApprovedRecord {
  submissionId: string;
  candidateName: string;
  email: string;
  phone?: string;
  college?: string;
  domain: string;
  certId?: string;
  internId?: string;
  utrNumber: string;
  amountPaid: number;
  batchStartDate: string;
  batchStartDisplay: string;
}

const DOMAIN_OPTIONS = [
  'Data Analyst',
  'Artificial Intelligence (AI) & Machine Learning (ML)',
  'Full Stack Web Development',
  'Python Automation & Scripting',
  'Mobile App Development (Android/iOS)',
  'Cybersecurity & Ethical Hacking',
  'Cloud Computing & DevOps',
  'Digital Marketing & Business Branding',
  'Embedded Systems & IoT'
];
const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const balanceAmount = formatINR(PRICING_CONFIG.balancePayable);

export default function EnrollmentClient() {
  const searchParams = useSearchParams();

  // URL Query Parameters
  const paramCertId = searchParams.get('certid') || searchParams.get('certId') || '';
  const paramEmail = searchParams.get('email') || '';
  const paramName = searchParams.get('name') || '';
  const paramPhone = searchParams.get('phone') || '';
  const paramCollege = searchParams.get('college') || '';
  const paramDomain = searchParams.get('domain') || '';
  const paramInternId = searchParams.get('intern_id') || '';
  const isRejoin = searchParams.get('rejoin') === '1';
  const paramQuery = searchParams.get('q') || paramCertId || paramEmail || '';
  const isLegacyRedirect = Boolean(paramCertId) && !isRejoin;

  const resolvedInitialDomain =
    DOMAIN_OPTIONS.find(d => d.toLowerCase() === paramDomain.toLowerCase()) ||
    paramDomain ||
    'Data Analyst';

  // Lookup State
  const [lookupQuery, setLookupQuery] = useState(paramQuery);
  const [lookupLoading, setLookupLoading] = useState(Boolean(paramQuery) && !isRejoin);
  const [lookupAlert, setLookupAlert] = useState<{ type: 'success' | 'error'; text: string } | null>(
    isRejoin && (paramName || paramEmail)
      ? {
          type: 'success',
          text: `Your LMS profile is prefilled. Submit your ${balanceAmount} balance payment for review.`
        }
      : null
  );

  // Approved Candidate State & Countdown
  const [approvedRecord, setApprovedRecord] = useState<ApprovedRecord | null>(null);
  const [countdown, setCountdown] = useState({
    days: 0,
    hours: 0,
    minutes: 0,
    seconds: 0,
    isStarted: false
  });

  // Form Fields
  const [fullName, setFullName] = useState(paramName);
  const [email, setEmail] = useState(paramEmail.includes('***') ? '' : paramEmail);
  const [phone, setPhone] = useState(paramPhone.includes('***') ? '' : paramPhone);
  const [college, setCollege] = useState(paramCollege);
  const [domain, setDomain] = useState(resolvedInitialDomain);
  const [certId, setCertId] = useState(paramCertId);
  const [internId, setInternId] = useState(paramInternId);
  const [utrNumber, setUtrNumber] = useState('');
  const [remarks, setRemarks] = useState(isRejoin ? 'REJOIN_COHORT' : '');

  // UI / Payment State
  const [copiedVpa, setCopiedVpa] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [submissionResult, setSubmissionResult] = useState<SubmissionResponse | null>(null);

  // Detect device platform
  const deviceType = useSyncExternalStore(
    () => () => {},
    () => {
      const ua = typeof navigator !== 'undefined' ? (navigator.userAgent || '') : '';
      if (/android/i.test(ua)) return 'android';
      if (/iphone|ipad|ipod/i.test(ua)) return 'ios';
      return 'desktop';
    },
    () => 'desktop' as const
  );

  const applyCandidateRecord = (data: any, q: string) => {
    if (data.found && data.candidate) {
      const c: CandidateData = data.candidate;
      trackEvent('enrollment_candidate_lookup', { found: true, domain: c.domain || 'Unknown' });

      // Check if candidate already has an approved enrollment (skip when re-joining a new cohort)
      if (!isRejoin && (data.isApproved || data.enrollmentStatus === 'APPROVED')) {
        const defaultCohort = getNextCohortStandup();
        const startDate = data.batchStartDate || defaultCohort.batchStartDate;
        const displayDate = data.batchStartDisplay || defaultCohort.batchStartDisplay;

        setApprovedRecord({
          submissionId: c.submissionId || 'DBERT-ENR-CONFIRMED',
          candidateName: c.holderName,
          email: c.email || '',
          phone: c.phone || '',
          college: c.college || '',
          domain: c.domain || 'Full Stack Web Development',
          certId: c.certId,
          internId: c.internId,
          utrNumber: c.utrNumber || '',
          amountPaid: c.amountPaid || PRICING_CONFIG.balancePayable,
          batchStartDate: startDate,
          batchStartDisplay: displayDate
        });
        setLookupAlert({
          type: 'success',
          text: `Enrollment approved. Batch commences ${displayDate}.`
        });
        return;
      }

      // Check if candidate has submitted but pending review (skip when re-joining a new cohort)
      if (!isRejoin && data.enrollmentStatus === 'SUBMITTED') {
        setSubmissionResult({
          submissionId: c.submissionId || 'DBERT-ENR-RECORDED',
          submittedAt: new Date().toISOString(),
          candidateName: c.holderName,
          certId: c.certId,
          domain: c.domain || 'Data Analyst',
          utrNumber: c.utrNumber || '',
          amount: c.amountPaid || PRICING_CONFIG.balancePayable
        });
        return;
      }

      setApprovedRecord(null);
      setSubmissionResult(null);
      setFullName(c.holderName || '');
      const returnedEmail = c.email?.includes('***') ? '' : c.email;
      const lookupEmail = EMAIL_PATTERN.test(q) && !q.includes('***') ? q : '';
      setEmail(returnedEmail || lookupEmail);
      setPhone(c.phone && !c.phone.includes('***') ? c.phone : '');
      setCollege(c.college || '');
      if (c.domain) {
        const matchOpt = DOMAIN_OPTIONS.find(d => d.toLowerCase() === c.domain?.toLowerCase());
        setDomain(matchOpt || c.domain);
      }
      setCertId(c.certId || '');
      setInternId(c.internId || '');
      setLookupAlert(data.enrollmentStatus === 'REJECTED'
        ? {
            type: 'error',
            text: 'The earlier payment claim was rejected. If you have a valid payment reference, enter it with your registration details.',
          }
        : {
            type: 'success',
            text: 'Candidate record found. Complete the remaining fields with your registration details.',
          });
    } else {
      setApprovedRecord(null);
      setLookupAlert({
        type: 'error',
        text: 'No matching candidate record found. You can still manually complete the form below.'
      });
    }
  };

  // Lookup function
  const handleLookup = async (queryVal?: string) => {
    const q = (queryVal || lookupQuery).trim();
    if (!q) {
      setLookupAlert({ type: 'error', text: 'Please enter a Certificate ID, Intern ID, or Registered Email.' });
      return;
    }

    setLookupLoading(true);
    setLookupAlert(null);

    try {
      const res = await fetch(`/api/enroll/lookup?q=${encodeURIComponent(q)}`);
      const data = await res.json();
      applyCandidateRecord(data, q);
    } catch (err: any) {
      setLookupAlert({
        type: 'error',
        text: `Lookup connection error: ${err.message}. Please enter details manually.`
      });
    } finally {
      setLookupLoading(false);
    }
  };

  // Autofill on initial mount if param is provided (skip lookup when prefilled via rejoin=1)
  useEffect(() => {
    if (!paramQuery || isRejoin) return;
    let ignore = false;
    fetch(`/api/enroll/lookup?q=${encodeURIComponent(paramQuery.trim())}`)
      .then(res => res.json())
      .then(data => {
        if (!ignore) {
          applyCandidateRecord(data, paramQuery.trim());
        }
      })
      .catch((err: any) => {
        if (!ignore) {
          setLookupAlert({
            type: 'error',
            text: `Lookup connection error: ${err.message}. Please enter details manually.`
          });
        }
      })
      .finally(() => {
        if (!ignore) {
          setLookupLoading(false);
        }
      });

    return () => {
      ignore = true;
    };
  }, [paramQuery, isRejoin]);

  // Countdown timer hook when approvedRecord is set
  useEffect(() => {
    if (!approvedRecord) return;
    const defaultCohort = getNextCohortStandup();
    const targetTime = new Date(approvedRecord.batchStartDate || defaultCohort.batchStartDate).getTime();

    const tick = () => {
      const now = Date.now();
      const diff = targetTime - now;
      if (diff <= 0) {
        setCountdown({ days: 0, hours: 0, minutes: 0, seconds: 0, isStarted: true });
      } else {
        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
        const minutes = Math.floor((diff / (1000 * 60)) % 60);
        const seconds = Math.floor((diff / 1000) % 60);
        setCountdown({ days, hours, minutes, seconds, isStarted: false });
      }
    };

    tick();
    const interval = setInterval(tick, 1000);
    return () => clearInterval(interval);
  }, [approvedRecord]);

  // Copy Merchant VPA
  const merchantVpa = PRICING_CONFIG.merchantVpa;
  const handleCopyVpa = () => {
    navigator.clipboard.writeText(merchantVpa);
    setCopiedVpa(true);
    setTimeout(() => setCopiedVpa(false), 3000);
  };

  // Download QR Code (Mobile + Desktop friendly blob download)
  const [downloadingQr, setDownloadingQr] = useState(false);
  const handleDownloadQr = async () => {
    setDownloadingQr(true);
    trackEvent('qr_code_download', { certId: certId || 'UNKNOWN' });
    try {
      const res = await fetch(PRICING_CONFIG.qrCodePath);
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `DBERT-Payment-QR-${certId || PRICING_CONFIG.balancePayable}.jpeg`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      setTimeout(() => window.URL.revokeObjectURL(url), 1000);
    } catch {
      window.open(PRICING_CONFIG.qrCodePath, '_blank');
    } finally {
      setDownloadingQr(false);
    }
  };

  // UPI deep links
  const noteParam = certId ? `DBERT-${certId}` : `DBERT-BALANCE-${PRICING_CONFIG.balancePayable}`;
  const upiQuery = `pa=${merchantVpa}&pn=${encodeURIComponent(PRICING_CONFIG.merchantName)}&am=${PRICING_CONFIG.balancePayable}&cu=INR&tn=${encodeURIComponent(noteParam)}`;
  const genericUpiUri = `upi://pay?${upiQuery}`;

  const gpayUri = deviceType === 'android'
    ? `intent://pay?${upiQuery}#Intent;scheme=upi;package=com.google.android.apps.nbu.paisa.user;end`
    : `gpay://upi/pay?${upiQuery}`;

  const phonepeUri = deviceType === 'android'
    ? `intent://pay?${upiQuery}#Intent;scheme=upi;package=com.phonepe.app;end`
    : `phonepe://pay?${upiQuery}`;

  const paytmUri = deviceType === 'android'
    ? `intent://pay?${upiQuery}#Intent;scheme=upi;package=net.one97.paytm;end`
    : `paytmmp://pay?${upiQuery}`;

  // Form Submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitError(null);

    // Validate
    if (!fullName.trim()) {
      setSubmitError('Please enter your full legal name.');
      return;
    }
    if (!EMAIL_PATTERN.test(email.trim()) || email.includes('***')) {
      setSubmitError('Please enter a valid registered email address.');
      return;
    }
    if (!phone.trim() || phone.trim().replace(/\D/g, '').length < 10) {
      setSubmitError('Please enter a valid 10-digit WhatsApp/contact number.');
      return;
    }
    if (!utrNumber.trim() || utrNumber.trim().length < 6) {
      setSubmitError('Please enter your 12-digit UPI UTR / Transaction Reference number.');
      return;
    }

    setSubmitting(true);

    try {
      const res = await fetch('/api/enroll/balance', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          fullName: fullName.trim(),
          email: email.trim(),
          phone: phone.trim(),
          college: college.trim(),
          domain,
          certId: certId.trim(),
          internId: internId.trim(),
          utrNumber: utrNumber.trim(),
          remarks: remarks.trim()
        })
      });

      const data = await res.json();
      if (data.success) {
        trackEvent('balance_utr_submitted', {
          amount: data.amount,
          domain
        });
        setSubmissionResult({
          submissionId: data.submissionId,
          submittedAt: data.submittedAt || new Date().toISOString(),
          candidateName: fullName.trim(),
          certId: certId.trim(),
          domain,
          utrNumber: utrNumber.trim().toUpperCase(),
          amount: data.amount,
          claimStatus: data.claimStatus
        });
      } else {
        setSubmitError(data.error || 'Submission failed. Please verify your details and try again.');
      }
    } catch (err: any) {
      setSubmitError(`Network error: ${err.message}. Please try again.`);
    } finally {
      setSubmitting(false);
    }
  };

  // WhatsApp screenshot proof link for pending submissions
  const generateWhatsAppProofUrl = () => {
    if (!submissionResult) return '#';
    const text = [
      `*DBERT Incubation Balance Payment Claim*`,
      ``,
      `Hello DBERT Admissions, I am sharing payment proof for my incubation balance claim.`,
      ``,
      ...(submissionResult.candidateName ? [`• *Candidate Name:* ${submissionResult.candidateName}`] : []),
      `• *Certificate ID:* ${submissionResult.certId || 'N/A'}`,
      `• *Domain Track:* ${submissionResult.domain}`,
      ...(submissionResult.utrNumber ? [`• *Transaction Reference:* ${submissionResult.utrNumber}`] : []),
      `• *Submission Ref:* ${submissionResult.submissionId}`,
      `• *Claimed Amount:* ${formatINR(submissionResult.amount)}`,
      ``,
      `I am attaching my payment transaction screenshot for review.`
    ].join('\n');

    return `https://wa.me/${PRICING_CONFIG.admissionsWhatsApp}?text=${encodeURIComponent(text)}`;
  };

  // ── Render: APPROVED ENROLLMENT & LIVE COUNTDOWN VIEW ─────────────────────────
  if (approvedRecord) {
    const whatsappApprovedUrl = `https://wa.me/${PRICING_CONFIG.admissionsWhatsApp}?text=${encodeURIComponent(
      `*DBERT Approved Incubation Enrollment Confirmation*\n\n` +
      `Hello DBERT Admissions, I checked my enrollment (Ref: ${approvedRecord.submissionId}).\n\n` +
      `• Domain Track: ${approvedRecord.domain}\n` +
      `• Batch Kickoff: ${approvedRecord.batchStartDisplay} (06:00 PM IST)\n\n` +
      `I see my enrollment is officially approved with seat confirmed. Ready for induction sprints!`
    )}`;

    return (
      <div className={s.container}>
        <Link href="/verify" className={s.breadcrumb}>
          ← Back to Verification Engine
        </Link>

        <div className={s.approvedCard}>
          <div className={s.approvedBadge}>
            <span className={s.approvedPulseDot} />
            <span>✓ OFFICIAL ENROLLMENT APPROVED & SEAT CONFIRMED</span>
          </div>

          <h1 className={s.approvedTitle}>
            Your DBERT Technical Incubation enrollment is approved
          </h1>
          <p className={s.approvedSubtitle}>
            Your balance payment has been verified and your seat is confirmed in the{' '}
            <strong style={{ color: '#F0F4F8' }}>{approvedRecord.domain}</strong> production engineering cohort.
          </p>

          {/* Live Countdown Box */}
          <div className={s.countdownBox}>
            <div className={s.countdownHeader}>
              <span>⏳</span>
              <span>BATCH INDUCTION COUNTDOWN</span>
            </div>
            <div className={s.countdownKickoffDate}>
              Orientation & Sprint Kickoff:{' '}
              <span style={{ color: '#E2B96F' }}>
                {approvedRecord.batchStartDisplay} · 06:00 PM IST
              </span>
            </div>

            <div className={s.countdownGrid}>
              <div className={s.countdownTile}>
                <span className={s.countdownNumber}>{String(countdown.days).padStart(2, '0')}</span>
                <span className={s.countdownLabel}>DAYS</span>
              </div>
              <div className={s.countdownTile}>
                <span className={s.countdownNumber}>{String(countdown.hours).padStart(2, '0')}</span>
                <span className={s.countdownLabel}>HOURS</span>
              </div>
              <div className={s.countdownTile}>
                <span className={s.countdownNumber}>{String(countdown.minutes).padStart(2, '0')}</span>
                <span className={s.countdownLabel}>MINUTES</span>
              </div>
              <div className={s.countdownTile}>
                <span className={s.countdownNumber}>{String(countdown.seconds).padStart(2, '0')}</span>
                <span className={s.countdownLabel}>SECONDS</span>
              </div>
            </div>
          </div>

          {/* Authenticated Dossier Table */}
          <div className={s.receiptDetails}>
            <div className={s.receiptRow}>
              <span className={s.receiptLabel}>Enrollment Status</span>
              <span className={s.receiptVal} style={{ color: '#10B981', fontWeight: 700 }}>
                APPROVED & SEAT CONFIRMED
              </span>
            </div>
            {approvedRecord.candidateName && (
              <div className={s.receiptRow}>
                <span className={s.receiptLabel}>Candidate Name</span>
                <span className={s.receiptVal}>{approvedRecord.candidateName}</span>
              </div>
            )}
            {approvedRecord.email && (
              <div className={s.receiptRow}>
                <span className={s.receiptLabel}>Registered Email</span>
                <span className={s.receiptVal} style={{ color: '#38BDF8' }}>{approvedRecord.email}</span>
              </div>
            )}
            {approvedRecord.phone && (
              <div className={s.receiptRow}>
                <span className={s.receiptLabel}>WhatsApp Phone</span>
                <span className={s.receiptVal}>{approvedRecord.phone}</span>
              </div>
            )}
            <div className={s.receiptRow}>
              <span className={s.receiptLabel}>Domain Track</span>
              <span className={s.receiptVal}>{approvedRecord.domain}</span>
            </div>
            <div className={s.receiptRow}>
              <span className={s.receiptLabel}>Program Fee Settlement</span>
              <span className={s.receiptVal} style={{ color: '#10B981' }}>
                Balance payment verified
              </span>
            </div>
            {approvedRecord.utrNumber && (
              <div className={s.receiptRow}>
                <span className={s.receiptLabel}>Verified Transaction Reference</span>
                <span className={s.receiptVal} style={{ fontFamily: 'monospace', color: '#E2B96F' }}>
                  {approvedRecord.utrNumber}
                </span>
              </div>
            )}
            {approvedRecord.internId && (
              <div className={s.receiptRow}>
                <span className={s.receiptLabel}>Permanent Intern ID</span>
                <span className={s.receiptVal} style={{ fontFamily: 'monospace', color: '#38BDF8' }}>
                  {approvedRecord.internId}
                </span>
              </div>
            )}
            {approvedRecord.certId && (
              <div className={s.receiptRow}>
                <span className={s.receiptLabel}>Certificate Identifier</span>
                <span className={s.receiptVal} style={{ fontFamily: 'monospace', color: '#38BDF8' }}>
                  {approvedRecord.certId}
                </span>
              </div>
            )}
            <div className={s.receiptRow}>
              <span className={s.receiptLabel}>Official Batch Kickoff</span>
              <span className={s.receiptVal} style={{ color: '#F0F4F8', fontWeight: 700 }}>
                {approvedRecord.batchStartDisplay} (06:00 PM IST)
              </span>
            </div>
          </div>

          {/* Induction Roadmap */}
          <div className={s.roadmapBox}>
            <div className={s.roadmapHeader}>
              <span>🚀</span>
              <span>Induction Sprint Preparation Roadmap</span>
            </div>
            <div className={s.roadmapTimeline}>
              <div className={s.roadmapStep}>
                <span className={s.stepBadge}>STEP 01</span>
                <div className={s.stepContent}>
                  <div className={s.stepTitle}>Live Orientation & Induction Kickoff</div>
                  <div className={s.stepDesc}>
                    Commences <strong>Monday, 9 Nov 2026 at 06:00 PM IST</strong> via Google Meet. Program Head Mr. Abhinav Sharma will outline sprint milestones and project architectures.
                  </div>
                </div>
              </div>
              <div className={s.roadmapStep}>
                <span className={s.stepBadge}>STEP 02</span>
                <div className={s.stepContent}>
                  <div className={s.stepTitle}>Cloud Workspace & Repository Provisioning</div>
                  <div className={s.stepDesc}>
                    Your production GitHub branch, Discord developer channel, and LMS credentials will be dispatched to your registered email.
                  </div>
                </div>
              </div>
              <div className={s.roadmapStep}>
                <span className={s.stepBadge}>STEP 03</span>
                <div className={s.stepContent}>
                  <div className={s.stepTitle}>Production Sprint Deliverables</div>
                  <div className={s.stepDesc}>
                    Engage in 2-week agile sprint cycles delivering production features with live code review, unit testing, and architectural benchmarking.
                  </div>
                </div>
              </div>
            </div>
          </div>

          <a
            href={whatsappApprovedUrl}
            target="_blank"
            rel="noopener noreferrer"
            className={s.approvedWhatsAppBtn}
          >
            <span>📲 Contact Admissions Concierge on WhatsApp</span>
          </a>

          <div>
            <button
              type="button"
              className={s.btnResetCheck}
              onClick={() => {
                setApprovedRecord(null);
                setLookupQuery('');
              }}
            >
              ← Check Another Candidate or Certificate ID
            </button>
          </div>
        </div>
      </div>
    );
  }

  // ── Render: Post-Submission Success State (Pending) ──────────────────────────
  if (submissionResult) {
    const reviewStatus = submissionResult.claimStatus || 'pending';
    const verified = reviewStatus === 'verified';
    return (
      <div className={s.container}>
        <div className={s.successCard}>
          <div className={s.successIcon}>✓</div>
          <h1 className={s.successTitle}>
            {verified ? 'Balance payment verified'
              : reviewStatus === 'rejected' ? 'Balance payment claim rejected' : 'Balance payment claim received'}
          </h1>
          <p className={s.successDesc}>
            {verified ? 'Admissions matched the payment to your enrollment.'
              : reviewStatus === 'rejected' ? 'Contact admissions with your receipt reference if you believe this claim should be verified.'
                : 'Admissions will match your transaction reference and amount against the settlement ledger.'}
          </p>

          <div className={s.receiptDetails}>
            <div className={s.receiptRow}>
              <span className={s.receiptLabel}>Submission Reference</span>
              <span className={s.receiptVal} style={{ color: '#E2B96F' }}>{submissionResult.submissionId}</span>
            </div>
            {submissionResult.candidateName && (
              <div className={s.receiptRow}>
                <span className={s.receiptLabel}>Candidate Name</span>
                <span className={s.receiptVal}>{submissionResult.candidateName}</span>
              </div>
            )}
            {submissionResult.certId && (
              <div className={s.receiptRow}>
                <span className={s.receiptLabel}>Certificate Identifier</span>
                <span className={s.receiptVal} style={{ color: '#38BDF8' }}>{submissionResult.certId}</span>
              </div>
            )}
            <div className={s.receiptRow}>
              <span className={s.receiptLabel}>Domain Track</span>
              <span className={s.receiptVal}>{submissionResult.domain}</span>
            </div>
            <div className={s.receiptRow}>
              <span className={s.receiptLabel}>{verified ? 'Verified balance payment' : 'Claimed balance amount'}</span>
              <span className={s.receiptVal}>{formatINR(submissionResult.amount)}</span>
            </div>
            <div className={s.receiptRow}>
              <span className={s.receiptLabel}>12-Digit UTR / Ref ID</span>
              <span className={s.receiptVal}>{submissionResult.utrNumber}</span>
            </div>
            <div className={s.receiptRow}>
              <span className={s.receiptLabel}>Status</span>
              <span className={s.receiptVal}>{verified ? 'Verified' : reviewStatus === 'rejected' ? 'Rejected' : 'Pending verification'}</span>
            </div>
          </div>

          <a href="https://lms.dbert.in/portal/payment-claims" className={s.backVerifyLink}>
            View payment status in LMS
          </a>

          {!verified && <a
            href={generateWhatsAppProofUrl()}
            target="_blank"
            rel="noopener noreferrer"
            className={s.whatsappProofBtn}
            onClick={() => trackEvent('whatsapp_proof_routing_click', { source: 'balance_claim' })}
          >
            <span>📲 Send Payment Screenshot via WhatsApp to Admissions</span>
          </a>}

          <div>
            {submissionResult.certId ? (
              <Link href={`/verify/${submissionResult.certId}`} className={s.backVerifyLink}>
                ← Return to Credential Verification Page ({submissionResult.certId})
              </Link>
            ) : (
              <Link href="/verify" className={s.backVerifyLink}>
                ← Go to DBERT Credential Verification Engine
              </Link>
            )}
          </div>
        </div>
      </div>
    );
  }

  // ── Render: Active Enrollment Form ───────────────────────────────────────────
  return (
    <div className={s.container}>
      {/* Breadcrumb */}
      <Link href="/verify" className={s.breadcrumb}>
        ← Back to Verification Engine
      </Link>

      <AITrustBanner />

      {isRejoin && (
        <div style={{
          background: '#fffbeb',
          border: '1px solid #fcd34d',
          borderRadius: '10px',
          padding: '14px 18px',
          marginBottom: '20px',
          color: '#92400e',
          fontSize: '13.5px',
          lineHeight: '1.6'
        }}>
          <strong>Re-Joining New Cohort:</strong> Your LMS profile details have been prefilled below. Submit your {balanceAmount} balance payment for review after your {formatINR(PRICING_CONFIG.cautionDeposit)} caution deposit is confirmed.
        </div>
      )}

      {isLegacyRedirect && (
        <div style={{
          background: '#ecfdf5',
          border: '1px solid #6ee7b7',
          borderRadius: '10px',
          padding: '14px 18px',
          marginBottom: '20px',
          color: '#065f46',
          fontSize: '13.5px',
          lineHeight: '1.6'
        }}>
          <strong>Notice:</strong> Standalone ₹299 verification fees have been discontinued. Verified credentials, Turnitin evaluation rubrics, and letters of recommendation are fully included in the official Fellowship (₹1,999 all-inclusive).
        </div>
      )}

      {/* Main Header & Ledger */}
      <div className={s.headerCard}>
        <div className={s.badgeRow}>
          <span className={s.portalBadge}>Official Admissions Portal</span>
          <span className={s.sovereignBadge}>DBERT Sovereign Incubation · dbert.in</span>
        </div>

        <h1 className={s.pageTitle}>
          Technical Incubation & Fellowship Balance Payment
        </h1>
        <p className={s.pageSubtitle}>
          Complete your final admission enrollment to unlock official credentials, institutional LOR, production GitHub repository access, and placement sprint onboarding.
        </p>

        {/* Financial Transparency Ledger */}
        <div className={s.ledgerBox}>
          <div className={s.ledgerItem}>
            <span className={s.ledgerLabel}>Fellowship Program Total:</span>
            <span className={s.ledgerValue}>{formatINR(PRICING_CONFIG.totalProgramFee)}</span>
          </div>
          <div className={s.ledgerItem}>
            <span className={s.ledgerLabel}>Balance due after your confirmed caution deposit:</span>
            <span className={`${s.ledgerValue} ${s.ledgerPayable}`}>{balanceAmount}</span>
          </div>
          <div className={s.ledgerItem}>
            <span className={s.ledgerLabel}>Screening &amp; Assessment Fees:</span>
            <span className={s.ledgerValue}>100% Free (Zero Fees)</span>
          </div>
          <p className={s.ledgerNote}>
            💡 <strong>Committed Program Enrollment:</strong> Covers 2 months of intensive engineering sprints, client repository assignments, 1:1 mentor code reviews, Turnitin originality evaluation, and verified credential issuance.
          </p>
        </div>
      </div>

      {/* Instant Profile Lookup Bar */}
      <div className={s.lookupSection}>
        <div className={s.lookupTitle}>Already Registered? Check Enrollment Status & Auto-Fill</div>
        <p className={s.lookupSubtitle}>
          Enter your Registered Email, Certificate ID, or Intern ID to instantly check your enrollment status or autofill your candidate profile.
        </p>
        <div className={s.lookupRow}>
          <input
            type="text"
            className={s.lookupInput}
            placeholder="e.g. learner@example.com or your certificate ID"
            value={lookupQuery}
            onChange={(e) => setLookupQuery(e.target.value)}
            onKeyDown={(e) => { if (e.key === 'Enter') handleLookup(); }}
          />
          <button
            type="button"
            className={s.btnLookup}
            disabled={lookupLoading}
            onClick={() => handleLookup()}
          >
            {lookupLoading ? 'Checking...' : 'Check Status / Auto-Fill'}
          </button>
        </div>
        {lookupAlert && (
          <div className={`${s.lookupAlert} ${lookupAlert.type === 'success' ? s.lookupAlertSuccess : s.lookupAlertError}`}>
            {lookupAlert.text}
          </div>
        )}
      </div>

      {/* Main Form & Payment Grid */}
      <div className={s.contentGrid}>
        {/* Left Column: Candidate & Admission Form */}
        <div className={s.sectionCard}>
          <div className={s.sectionHeader}>
            <div className={`${s.sectionIcon} ${s.iconCyan}`}>01</div>
            <div>
              <div className={s.sectionTitle}>Candidate Profile & Verification</div>
              <div className={s.sectionSubtitle}>Confirm your legal academic details for official records</div>
            </div>
          </div>

          <form onSubmit={handleSubmit}>
            <div className={s.formGroup}>
              <label className={s.formLabel}>
                Full Legal Name <span className={s.requiredAsterisk}>*</span>
              </label>
              <input
                type="text"
                className={s.formInput}
                placeholder="Full Name as per official ID"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                required
              />
            </div>

            <div className={s.formGroup}>
              <label className={s.formLabel}>
                Registered Email Address <span className={s.requiredAsterisk}>*</span>
              </label>
              <input
                type="email"
                className={s.formInput}
                placeholder="candidate@gmail.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
              <span className={s.formHint}>Must match your original registration email</span>
            </div>

            <div className={s.formGroup}>
              <label className={s.formLabel}>
                WhatsApp / Contact Number <span className={s.requiredAsterisk}>*</span>
              </label>
              <input
                type="tel"
                className={s.formInput}
                placeholder="10-digit mobile number"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                required
              />
            </div>

            <div className={s.formGroup}>
              <label className={s.formLabel}>College / Institutional Name</label>
              <input
                type="text"
                className={s.formInput}
                placeholder="Your University or Engineering College"
                value={college}
                onChange={(e) => setCollege(e.target.value)}
              />
            </div>

            <div className={s.formGroup}>
              <label className={s.formLabel}>
                Technical Incubation Domain Track <span className={s.requiredAsterisk}>*</span>
              </label>
              <select
                className={s.formSelect}
                value={domain}
                onChange={(e) => setDomain(e.target.value)}
                required
              >
                {DOMAIN_OPTIONS.map((opt) => (
                  <option key={opt} value={opt}>
                    {opt}
                  </option>
                ))}
              </select>
            </div>

            <div className={s.formGroup}>
              <label className={s.formLabel}>DBERT Certificate Identifier (If assigned)</label>
              <input
                type="text"
                className={s.formInput}
                placeholder="e.g. CERT-DBERT-2026-DA-057"
                value={certId}
                onChange={(e) => setCertId(e.target.value)}
              />
              <span className={s.formHint}>Leave blank if enrolling directly for the upcoming cohort</span>
            </div>

            {/* UPI UTR Input Field */}
            <div className={s.utrBox}>
              <div className={s.utrTitle}>Payment Confirmation · 12-Digit UPI UTR</div>
              <p className={s.utrDesc}>
                Pay the {balanceAmount} balance using the QR code or UPI link. Enter your payment transaction reference below.
              </p>
              <div className={s.formGroup} style={{ marginBottom: 0 }}>
                <label className={s.formLabel}>
                  12-Digit UPI UTR / Transaction Reference <span className={s.requiredAsterisk}>*</span>
                </label>
                <input
                  type="text"
                  className={s.formInput}
                  placeholder="e.g. 679862090077 (12 numeric digits)"
                  value={utrNumber}
                  maxLength={20}
                  onChange={(e) => setUtrNumber(e.target.value)}
                  required
                />
              </div>
            </div>

            <div className={s.formGroup} style={{ marginTop: '16px' }}>
              <label className={s.formLabel}>Additional Notes / Payment App Used</label>
              <textarea
                className={s.formTextarea}
                placeholder="e.g. Paid via GPay / PhonePe / Paytm..."
                value={remarks}
                onChange={(e) => setRemarks(e.target.value)}
              />
            </div>

            {submitError && (
              <div className={`${s.lookupAlert} ${s.lookupAlertError}`} style={{ marginBottom: '16px' }}>
                {submitError}
              </div>
            )}

            <button
              type="submit"
              className={s.btnSubmit}
              disabled={submitting}
            >
              {submitting ? 'Recording Submission...' : `Submit ${balanceAmount} Balance Claim →`}
            </button>
          </form>
        </div>

        {/* Right Column: Payment Gateway, QR Code, and 1-Tap Launchers */}
        <div className={s.sectionCard}>
          <div className={s.sectionHeader}>
            <div className={`${s.sectionIcon} ${s.iconAmber}`}>02</div>
            <div>
              <div className={s.sectionTitle}>Pay the {balanceAmount} Balance</div>
              <div className={s.sectionSubtitle}>Official DBERT UPI Merchant QR & Direct Deep-Launchers</div>
            </div>
          </div>

          <div className={s.qrCard}>
            {/* Embedded High-Res QR Code */}
            <div className={s.qrImageWrapper}>
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src={PRICING_CONFIG.qrCodePath}
                alt="DBERT Official UPI Payment QR Code"
                className={s.qrImage}
                onError={(e) => {
                  // Fallback if primary path fails
                  (e.target as HTMLImageElement).src = PRICING_CONFIG.qrCodeFallback;
                }}
              />
            </div>

            <div className={s.vpaBadge}>
              <code>{merchantVpa}</code>
              <button
                type="button"
                className={s.copyVpaBtn}
                onClick={handleCopyVpa}
              >
                {copiedVpa ? '✓ Copied' : 'Copy UPI ID'}
              </button>
            </div>

            <button
              type="button"
              className={s.btnDownloadQr}
              onClick={handleDownloadQr}
              disabled={downloadingQr}
            >
              {downloadingQr ? 'Preparing QR...' : '📥 Download High-Res Payment QR'}
            </button>

            {/* Mobile 1-Tap UPI Launchers */}
            <div className={s.intentTitle}>
              {deviceType === 'desktop' ? 'Mobile UPI Deep Launchers' : `1-Tap UPI Balance Payment (${balanceAmount})`}
            </div>

            <div className={s.intentGrid}>
              <a
                href={gpayUri}
                className={`${s.intentBtn} ${s.intentGpay}`}
                onClick={() => trackEvent('upi_launcher_click', { provider: 'gpay', amount: PRICING_CONFIG.balancePayable })}
              >
                Google Pay
              </a>
              <a
                href={phonepeUri}
                className={`${s.intentBtn} ${s.intentPhonePe}`}
                onClick={() => trackEvent('upi_launcher_click', { provider: 'phonepe', amount: PRICING_CONFIG.balancePayable })}
              >
                PhonePe
              </a>
              <a
                href={paytmUri}
                className={`${s.intentBtn} ${s.intentPaytm}`}
                onClick={() => trackEvent('upi_launcher_click', { provider: 'paytm', amount: PRICING_CONFIG.balancePayable })}
              >
                Paytm
              </a>
              <a
                href={genericUpiUri}
                className={`${s.intentBtn} ${s.intentGeneric}`}
                onClick={() => trackEvent('upi_launcher_click', { provider: 'default_upi', amount: PRICING_CONFIG.balancePayable })}
              >
                Default UPI
              </a>
            </div>
          </div>
        </div>
      </div>

      {/* Secondary Admissions Verification Support */}
      <div className={s.fallbackSection}>
        <div className={s.fallbackTitle}>Prefer WhatsApp Verification Support?</div>
        <p className={s.fallbackDesc}>
          If your bank app requires manual screenshot submission or you need immediate admissions assistance, you can submit your transaction proof directly to our admissions desk.
        </p>
        <a
          href={`https://wa.me/918192911360?text=Hi%20Admissions%20Team%2C%20I%20am%20submitting%20my%20%E2%82%B91%2C999%20incubation%20enrollment%20proof%20manually%20(Email%3A%20${encodeURIComponent(email || 'candidate')}).`}
          target="_blank"
          rel="noopener noreferrer"
          className={s.fallbackBtn}
        >
          Submit Proof to Admissions (+91 81929 11360) ↗
        </a>
      </div>

      {/* Program Guides & Transparency Links */}
      <div style={{ marginTop: '24px', padding: '18px 20px', borderRadius: '14px', border: '1px solid rgba(255,255,255,0.08)', background: 'rgba(15,23,42,0.55)' }}>
        <div style={{ fontSize: '0.78rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.07em', color: '#E2B96F', marginBottom: '10px' }}>
          Program Guides &amp; Transparency
        </div>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px 18px', fontSize: '0.88rem' }}>
          <Link
            href="/blog/dbert-1999-program-non-refundable-value-breakdown"
            onClick={() => trackEvent('enroll_guide_click', { slug: 'dbert-1999-program-non-refundable-value-breakdown' })}
            style={{ color: '#93C5FD', textDecoration: 'underline' }}
          >
            ₹1,999 Fee &amp; Non-Refundable Policy Breakdown →
          </Link>
          <Link
            href="/blog/dbert-unpaid-internship-vs-paid-corporate-vs-self-learning"
            onClick={() => trackEvent('enroll_guide_click', { slug: 'dbert-unpaid-internship-vs-paid-corporate-vs-self-learning' })}
            style={{ color: '#93C5FD', textDecoration: 'underline' }}
          >
            DBERT vs. Paid Corporate vs. Self-Learning →
          </Link>
          <Link
            href="/blog/inside-dbert-engineering-sprints-rag-saas-security-qa-ocr-bots"
            onClick={() => trackEvent('enroll_guide_click', { slug: 'inside-dbert-engineering-sprints-rag-saas-security-qa-ocr-bots' })}
            style={{ color: '#93C5FD', textDecoration: 'underline' }}
          >
            Real Sprint Tracks (RAG, SaaS, Security, QA, OCR, Bots) →
          </Link>
          <Link
            href="/blog/how-to-verify-dbert-internship-and-get-hired"
            onClick={() => trackEvent('enroll_guide_click', { slug: 'how-to-verify-dbert-internship-and-get-hired' })}
            style={{ color: '#93C5FD', textDecoration: 'underline' }}
          >
            How to Verify Credentials &amp; Get Hired →
          </Link>
        </div>
      </div>
    </div>
  );
}
