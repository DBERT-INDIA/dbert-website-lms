'use client';

import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import Link from 'next/link';
import s from './enroll.module.css';

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

export default function EnrollmentClient() {
  const searchParams = useSearchParams();

  // URL Query Parameters
  const paramCertId = searchParams.get('certid') || searchParams.get('certId') || '';
  const paramEmail = searchParams.get('email') || '';
  const paramQuery = searchParams.get('q') || paramCertId || paramEmail || '';

  // Lookup State
  const [lookupQuery, setLookupQuery] = useState(paramQuery);
  const [lookupLoading, setLookupLoading] = useState(false);
  const [lookupAlert, setLookupAlert] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [isAutofilled, setIsAutofilled] = useState(false);

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
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [college, setCollege] = useState('');
  const [domain, setDomain] = useState('Data Analyst');
  const [certId, setCertId] = useState('');
  const [internId, setInternId] = useState('');
  const [utrNumber, setUtrNumber] = useState('');
  const [remarks, setRemarks] = useState('');

  // UI / Payment State
  const [copiedVpa, setCopiedVpa] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [submissionResult, setSubmissionResult] = useState<SubmissionResponse | null>(null);
  const [deviceType, setDeviceType] = useState<'desktop' | 'android' | 'ios'>('desktop');

  // Detect device platform
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const ua = navigator.userAgent || '';
      if (/android/i.test(ua)) setDeviceType('android');
      else if (/iphone|ipad|ipod/i.test(ua)) setDeviceType('ios');
      else setDeviceType('desktop');
    }
  }, []);

  // Autofill on initial mount if param is provided
  useEffect(() => {
    if (paramQuery) {
      handleLookup(paramQuery);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [paramQuery]);

  // Countdown timer hook when approvedRecord is set
  useEffect(() => {
    if (!approvedRecord) return;
    const targetTime = new Date(approvedRecord.batchStartDate || '2026-11-09T18:00:00+05:30').getTime();

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

      if (data.found && data.candidate) {
        const c: CandidateData = data.candidate;

        // Check if candidate already has an approved enrollment
        if (data.isApproved || data.enrollmentStatus === 'APPROVED') {
          setApprovedRecord({
            submissionId: c.submissionId || 'DBERT-ENR-CONFIRMED',
            candidateName: c.holderName,
            email: c.email || q,
            phone: c.phone || '',
            college: c.college || '',
            domain: c.domain || 'Full Stack Web Development',
            certId: c.certId,
            internId: c.internId,
            utrNumber: c.utrNumber || 'VERIFIED-UPI',
            amountPaid: c.amountPaid || 1500,
            batchStartDate: data.batchStartDate || '2026-11-09T18:00:00+05:30',
            batchStartDisplay: data.batchStartDisplay || 'Monday, 9 Nov 2026'
          });
          setLookupAlert({
            type: 'success',
            text: `✓ Official Enrollment Approved for ${c.holderName}! Batch commences Monday, 9 Nov 2026.`
          });
          return;
        }

        // Check if candidate has submitted but pending review
        if (data.enrollmentStatus === 'SUBMITTED') {
          setSubmissionResult({
            submissionId: c.submissionId || 'DBERT-ENR-RECORDED',
            submittedAt: new Date().toISOString(),
            candidateName: c.holderName,
            certId: c.certId,
            domain: c.domain || 'Data Analyst',
            utrNumber: c.utrNumber || '',
            amount: c.amountPaid || 1500
          });
          return;
        }

        // Unenrolled candidate: autofill form
        setApprovedRecord(null);
        setFullName(c.holderName || '');
        if (c.email) setEmail(c.email);
        if (c.phone) setPhone(c.phone);
        if (c.college) setCollege(c.college);
        if (c.domain) {
          const matchOpt = DOMAIN_OPTIONS.find(d => d.toLowerCase() === c.domain?.toLowerCase());
          setDomain(matchOpt || c.domain);
        }
        setCertId(c.certId || '');
        setInternId(c.internId || '');
        setIsAutofilled(true);
        setLookupAlert({
          type: 'success',
          text: `✓ Verified record loaded for ${c.holderName} (${c.certId}). Remaining balance: ₹1,500.`
        });
      } else {
        setIsAutofilled(false);
        setApprovedRecord(null);
        setLookupAlert({
          type: 'error',
          text: 'No matching candidate record found. You can still manually complete the form below.'
        });
      }
    } catch (err: any) {
      setLookupAlert({
        type: 'error',
        text: `Lookup connection error: ${err.message}. Please enter details manually.`
      });
    } finally {
      setLookupLoading(false);
    }
  };

  // Copy Merchant VPA
  const merchantVpa = 'Q652429146@ybl';
  const handleCopyVpa = () => {
    navigator.clipboard.writeText(merchantVpa);
    setCopiedVpa(true);
    setTimeout(() => setCopiedVpa(false), 3000);
  };

  // Download QR Code (Mobile + Desktop friendly blob download)
  const [downloadingQr, setDownloadingQr] = useState(false);
  const handleDownloadQr = async () => {
    setDownloadingQr(true);
    try {
      const res = await fetch('/images/qrcode.jpeg');
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `DBERT-Payment-QR-${certId || '1500'}.jpeg`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      setTimeout(() => window.URL.revokeObjectURL(url), 1000);
    } catch {
      window.open('/images/qrcode.jpeg', '_blank');
    } finally {
      setDownloadingQr(false);
    }
  };

  // UPI deep links
  const noteParam = certId ? `DBERT-${certId}` : 'DBERT-BALANCE-1500';
  const upiQuery = `pa=${merchantVpa}&pn=DBERT%20Admissions&am=1500&cu=INR&tn=${encodeURIComponent(noteParam)}`;
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
    if (!email.trim() || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
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
        setSubmissionResult({
          submissionId: data.submissionId,
          submittedAt: data.submittedAt || new Date().toISOString(),
          candidateName: fullName.trim(),
          certId: certId.trim(),
          domain,
          utrNumber: utrNumber.trim().toUpperCase(),
          amount: 1500
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
      `*Official DBERT Balance Payment Proof (₹1,500)*`,
      ``,
      `Hello DBERT Admissions, I have completed the remaining balance payment of *₹1,500* for my technical internship & incubation program:`,
      ``,
      `• *Candidate Name:* ${submissionResult.candidateName}`,
      `• *Certificate ID:* ${submissionResult.certId || 'N/A'}`,
      `• *Domain Track:* ${submissionResult.domain}`,
      `• *12-Digit UTR:* ${submissionResult.utrNumber}`,
      `• *Submission Ref:* ${submissionResult.submissionId}`,
      `• *Amount Paid:* ₹1,500 (Balance of ₹1,999 Total Program)`,
      ``,
      `I am attaching my payment transaction screenshot below for instant verification & credential unlock.`
    ].join('\n');

    return `https://wa.me/918192911360?text=${encodeURIComponent(text)}`;
  };

  // ── Render: APPROVED ENROLLMENT & LIVE COUNTDOWN VIEW ─────────────────────────
  if (approvedRecord) {
    const whatsappApprovedUrl = `https://wa.me/918192911360?text=${encodeURIComponent(
      `*DBERT Approved Incubation Enrollment Confirmation*\n\n` +
      `Hello DBERT Admissions, I checked my enrollment for *${approvedRecord.candidateName}* (Ref: ${approvedRecord.submissionId}).\n\n` +
      `• Candidate: ${approvedRecord.candidateName}\n` +
      `• Registered Email: ${approvedRecord.email}\n` +
      `• Domain Track: ${approvedRecord.domain}\n` +
      `• Batch Kickoff: ${approvedRecord.batchStartDisplay} (06:00 PM IST)\n` +
      `• Verified UTR: ${approvedRecord.utrNumber}\n\n` +
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
            Welcome to DBERT Technical Incubation, {approvedRecord.candidateName}!
          </h1>
          <p className={s.approvedSubtitle}>
            Your ₹1,500 balance payment has been verified and your seat is officially confirmed in the{' '}
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
            <div className={s.receiptRow}>
              <span className={s.receiptLabel}>Candidate Name</span>
              <span className={s.receiptVal}>{approvedRecord.candidateName}</span>
            </div>
            <div className={s.receiptRow}>
              <span className={s.receiptLabel}>Registered Email</span>
              <span className={s.receiptVal} style={{ color: '#38BDF8' }}>{approvedRecord.email}</span>
            </div>
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
                ₹1,999 Paid in Full (₹499 Deposit + ₹1,500 Balance Cleared)
              </span>
            </div>
            <div className={s.receiptRow}>
              <span className={s.receiptLabel}>Verified 12-Digit UTR</span>
              <span className={s.receiptVal} style={{ fontFamily: 'monospace', color: '#E2B96F' }}>
                {approvedRecord.utrNumber}
              </span>
            </div>
            <div className={s.receiptRow}>
              <span className={s.receiptLabel}>Permanent Intern ID</span>
              <span className={s.receiptVal} style={{ fontFamily: 'monospace', color: '#38BDF8' }}>
                {approvedRecord.internId || 'DBERT-2026-INT-1412'}
              </span>
            </div>
            <div className={s.receiptRow}>
              <span className={s.receiptLabel}>Certificate Identifier</span>
              <span className={s.receiptVal} style={{ fontFamily: 'monospace', color: '#38BDF8' }}>
                {approvedRecord.certId || 'CERT-DBERT-2026-FSD-156'}
              </span>
            </div>
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
                setIsAutofilled(false);
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
    return (
      <div className={s.container}>
        <div className={s.successCard}>
          <div className={s.successIcon}>✓</div>
          <h1 className={s.successTitle}>Balance Payment Submitted Successfully</h1>
          <p className={s.successDesc}>
            Your ₹1,500 balance payment submission has been securely recorded. The admissions council is validating your 12-digit UTR with bank records.
          </p>

          <div className={s.receiptDetails}>
            <div className={s.receiptRow}>
              <span className={s.receiptLabel}>Submission Reference</span>
              <span className={s.receiptVal} style={{ color: '#E2B96F' }}>{submissionResult.submissionId}</span>
            </div>
            <div className={s.receiptRow}>
              <span className={s.receiptLabel}>Candidate Name</span>
              <span className={s.receiptVal}>{submissionResult.candidateName}</span>
            </div>
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
              <span className={s.receiptLabel}>Amount Paid (Balance)</span>
              <span className={s.receiptVal} style={{ color: '#10B981' }}>₹1,500 (₹1,999 Total Program)</span>
            </div>
            <div className={s.receiptRow}>
              <span className={s.receiptLabel}>12-Digit UTR / Ref ID</span>
              <span className={s.receiptVal}>{submissionResult.utrNumber}</span>
            </div>
            <div className={s.receiptRow}>
              <span className={s.receiptLabel}>Status</span>
              <span className={s.receiptVal} style={{ color: '#F59E0B' }}>PENDING VERIFICATION (2-4 hrs)</span>
            </div>
          </div>

          <a
            href={generateWhatsAppProofUrl()}
            target="_blank"
            rel="noopener noreferrer"
            className={s.whatsappProofBtn}
          >
            <span>📲 Send Payment Screenshot via WhatsApp to Admissions</span>
          </a>

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

      {/* Main Header & Ledger */}
      <div className={s.headerCard}>
        <div className={s.badgeRow}>
          <span className={s.portalBadge}>Official Admissions Portal</span>
          <span className={s.sovereignBadge}>DBERT Sovereign Incubation · dbert.in</span>
        </div>

        <h1 className={s.pageTitle}>
          Technical Incubation & Fellowship Enrollment (₹1,999 Program)
        </h1>
        <p className={s.pageSubtitle}>
          Complete your final admission enrollment to unlock official credentials, institutional LOR, production GitHub repository access, and placement sprint onboarding.
        </p>

        {/* Financial Transparency Ledger */}
        <div className={s.ledgerBox}>
          <div className={s.ledgerItem}>
            <span className={s.ledgerLabel}>Total Incubation Fee:</span>
            <span className={s.ledgerValue}>₹1,999</span>
          </div>
          <div className={s.ledgerItem}>
            <span className={s.ledgerLabel}>Caution Deposit Paid:</span>
            <span className={`${s.ledgerValue} ${s.ledgerDeduction}`}>- ₹499 (Credited in Full)</span>
          </div>
          <div className={s.ledgerItem}>
            <span className={s.ledgerLabel}>Net Remaining Balance Payable:</span>
            <span className={`${s.ledgerValue} ${s.ledgerPayable}`}>₹1,500</span>
          </div>
          <p className={s.ledgerNote}>
            💡 <strong>Notice for Registered Candidates:</strong> If you have already paid the initial ₹499 caution deposit, your advance is credited in full. You only need to pay the remaining <strong>₹1,500 balance</strong> to finalize your production enrollment and unlock your official credentials.
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
            placeholder="e.g. bhargavi13032007@gmail.com, CERT-DBERT-2026-DA-057"
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
                Complete the ₹1,500 balance payment using the QR code or 1-tap launchers on the right, then enter the 12-digit UTR transaction reference number below.
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
              {submitting ? 'Recording Submission...' : 'Complete Enrollment & Verify Balance Payment (₹1,500) →'}
            </button>
          </form>
        </div>

        {/* Right Column: Payment Gateway, QR Code, and 1-Tap Launchers */}
        <div className={s.sectionCard}>
          <div className={s.sectionHeader}>
            <div className={`${s.sectionIcon} ${s.iconAmber}`}>02</div>
            <div>
              <div className={s.sectionTitle}>Balance Settlement Gateway (₹1,500)</div>
              <div className={s.sectionSubtitle}>Official DBERT UPI Merchant QR & Direct Deep-Launchers</div>
            </div>
          </div>

          <div className={s.qrCard}>
            {/* Embedded High-Res QR Code */}
            <div className={s.qrImageWrapper}>
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src="/images/qrcode.jpeg"
                alt="DBERT Official UPI Payment QR Code"
                className={s.qrImage}
                onError={(e) => {
                  // Fallback to root path if /images/ fails
                  (e.target as HTMLImageElement).src = '/qrcode.jpeg';
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
              {deviceType === 'desktop' ? 'Mobile UPI Deep Launchers' : '1-Tap Mobile UPI Payment (₹1,500 Pre-Filled)'}
            </div>

            <div className={s.intentGrid}>
              <a href={gpayUri} className={`${s.intentBtn} ${s.intentGpay}`}>
                Google Pay
              </a>
              <a href={phonepeUri} className={`${s.intentBtn} ${s.intentPhonePe}`}>
                PhonePe
              </a>
              <a href={paytmUri} className={`${s.intentBtn} ${s.intentPaytm}`}>
                Paytm
              </a>
              <a href={genericUpiUri} className={`${s.intentBtn} ${s.intentGeneric}`}>
                Default UPI
              </a>
            </div>
          </div>
        </div>
      </div>

      {/* Secondary Google Form Link */}
      <div className={s.fallbackSection}>
        <div className={s.fallbackTitle}>Prefer Google Forms Alternative?</div>
        <p className={s.fallbackDesc}>
          If your bank app requires desktop screenshot uploads, you may also complete the standard Google Form alternative.
        </p>
        <a
          href="https://docs.google.com/forms/d/e/1FAIpQLSeHCTK_HO5ZbNHNcPiyW-04Y4bBeZ0RvQP7I4koQnW91d6phA/viewform?usp=header"
          target="_blank"
          rel="noopener noreferrer"
          className={s.fallbackBtn}
        >
          Open Google Form Alternative ↗
        </a>
      </div>
    </div>
  );
}
