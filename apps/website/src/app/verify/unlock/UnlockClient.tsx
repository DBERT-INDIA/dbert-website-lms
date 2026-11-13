'use client';

import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import Link from 'next/link';
import Image from 'next/image';
import s from './unlock.module.css';

interface CandidateProfile {
  certId?: string;
  internId?: string;
  holderName: string;
  email?: string;
  phone?: string;
  college?: string;
  domain?: string;
  project?: string;
  isProvisional?: boolean;
}

interface SubmissionResult {
  submissionId: string;
  utrNumber: string;
  amountPaid: number;
  fullName: string;
  email: string;
  phone: string;
  domain: string;
  certId?: string;
  submittedAt: string;
  alreadySubmitted?: boolean;
}


interface FeaturedEngineer {
  name: string;
  domain: string;
  college: string;
  score: number;
  stack: string[];
  certId: string;
}

const FEATURED_ENGINEERS: FeaturedEngineer[] = [
  {
    name: 'Smit Shah',
    domain: 'Data Analyst',
    college: 'Vishwakarma University',
    score: 87,
    stack: ['Python', 'SQL', 'Tableau', 'Power BI'],
    certId: 'CERT-DBERT-2026-DA-053'
  },
  {
    name: 'N Deekshitha',
    domain: 'AI & Machine Learning',
    college: 'Sreenidhi Inst of Science & Tech',
    score: 92,
    stack: ['PyTorch', 'TensorFlow', 'Scikit-Learn', 'OpenCV'],
    certId: 'CERT-DBERT-2026-AIML-092'
  },
  {
    name: 'Ankit Saini',
    domain: 'Full Stack Web Dev',
    college: 'Maharshi Dayanand University',
    score: 91,
    stack: ['Next.js', 'Node.js', 'PostgreSQL', 'Docker'],
    certId: 'CERT-DBERT-2026-FSD-070'
  },
  {
    name: 'M Brahmani',
    domain: 'Data Analyst',
    college: 'G. Pulla Reddy Engineering College',
    score: 90,
    stack: ['Pandas', 'NumPy', 'EDA', 'Business Intelligence'],
    certId: 'CERT-DBERT-2026-DA-117'
  }
];

export default function UnlockClient() {
  const searchParams = useSearchParams();

  // Search / Lookup state
  const [lookupQuery, setLookupQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const [candidate, setCandidate] = useState<CandidateProfile | null>(null);

  // Form inputs
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [college, setCollege] = useState('');
  const [domain, setDomain] = useState('Full Stack Web Development');
  const [certId, setCertId] = useState('');
  const [utrNumber, setUtrNumber] = useState('');
  const [remarks, setRemarks] = useState('');

  // UI state
  const [submitting, setSubmitting] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [copiedVpa, setCopiedVpa] = useState(false);
  const [submittedResult, setSubmittedResult] = useState<SubmissionResult | null>(null);

  const VPA = 'Q652429146@ybl';
  const MERCHANT_NAME = 'DBERT Admissions';
  const VERIFY_AMOUNT = 299;

  // Read initial query params from URL
  useEffect(() => {
    const q = searchParams.get('certid') || searchParams.get('email') || searchParams.get('q') || '';
    if (q) {
      setLookupQuery(q);
      executeLookup(q);
    }
  }, [searchParams]);

  const executeLookup = async (queryText: string) => {
    const clean = queryText.trim();
    if (!clean) return;

    setIsSearching(true);
    setErrorMsg('');

    try {
      const res = await fetch(`/api/enroll/lookup?q=${encodeURIComponent(clean)}`);
      const data = await res.json();

      if (data.found && data.candidate) {
        const c = data.candidate;
        setCandidate(c);
        if (c.holderName) setFullName(c.holderName);
        if (c.email && !c.email.includes('***')) setEmail(c.email);
        if (c.phone && !c.phone.includes('***')) setPhone(c.phone);
        if (c.college) setCollege(c.college);
        if (c.domain) setDomain(c.domain);
        if (c.certId) setCertId(c.certId);

        // Check if already submitted
        if (data.verificationSubmission) {
          const vs = data.verificationSubmission;
          setSubmittedResult({
            submissionId: vs.id,
            utrNumber: vs.utrNumber,
            amountPaid: vs.amountPaid || 299,
            fullName: vs.fullName,
            email: vs.email,
            phone: vs.phone,
            domain: vs.domain,
            certId: vs.certId,
            submittedAt: vs.submittedAt,
            alreadySubmitted: true
          });
        }
      } else {
        // Fallback: if query looks like a Cert ID, set it
        if (clean.toUpperCase().startsWith('CERT-')) {
          setCertId(clean.toUpperCase());
        } else if (clean.includes('@')) {
          setEmail(clean.toLowerCase());
        }
      }
    } catch {
      // ignore network lookup error
    } finally {
      setIsSearching(false);
    }
  };

  const handleCopyVpa = () => {
    if (navigator?.clipboard) {
      navigator.clipboard.writeText(VPA);
      setCopiedVpa(true);
      setTimeout(() => setCopiedVpa(false), 2000);
    }
  };

  const handleDownloadQr = () => {
    const link = document.createElement('a');
    link.href = '/qrcode.jpeg';
    link.download = 'DBERT_UPI_Verification_QR_299.jpeg';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg('');

    if (!fullName.trim()) {
      setErrorMsg('Please enter your full legal name.');
      return;
    }
    if (!email.trim() || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      setErrorMsg('Please enter a valid email address.');
      return;
    }
    const cleanPhone = phone.replace(/\D/g, '');
    if (cleanPhone.length < 10) {
      setErrorMsg('Please enter a valid 10-digit WhatsApp phone number.');
      return;
    }
    const cleanUtr = utrNumber.trim().replace(/\s+/g, '');
    if (!/^\d{12}$/.test(cleanUtr)) {
      setErrorMsg('Invalid UTR format. Please provide the exact 12-digit numeric reference number from your UPI receipt.');
      return;
    }

    setSubmitting(true);

    try {
      const res = await fetch('/api/verify/unlock', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          fullName: fullName.trim(),
          email: email.trim().toLowerCase(),
          phone: cleanPhone,
          college: college.trim() || 'Verified Candidate',
          domain: domain.trim(),
          certId: certId.trim() || undefined,
          utrNumber: cleanUtr,
          remarks: remarks.trim() || undefined
        })
      });

      const data = await res.json();

      if (!res.ok || !data.success) {
        setErrorMsg(data.error || 'Failed to submit verification payment. Please contact admissions.');
        setSubmitting(false);
        return;
      }

      setSubmittedResult({
        submissionId: data.submissionId,
        utrNumber: cleanUtr,
        amountPaid: VERIFY_AMOUNT,
        fullName: fullName.trim(),
        email: email.trim().toLowerCase(),
        phone: cleanPhone,
        domain: domain.trim(),
        certId: certId.trim() || undefined,
        submittedAt: new Date().toISOString(),
        alreadySubmitted: data.alreadySubmitted
      });
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Network error';
      setErrorMsg('Network error: ' + msg);
    } finally {
      setSubmitting(false);
    }
  };

  const upiTxNote = encodeURIComponent(`DBERT-CERT-VERIFY-${certId || '2026'}`);
  const upiGenericUrl = `upi://pay?pa=${VPA}&pn=${encodeURIComponent(MERCHANT_NAME)}&am=${VERIFY_AMOUNT}&cu=INR&tn=${upiTxNote}`;
  const upiGPayUrl = `gpay://upi/pay?pa=${VPA}&pn=${encodeURIComponent(MERCHANT_NAME)}&am=${VERIFY_AMOUNT}&cu=INR&tn=${upiTxNote}`;
  const upiPhonePeUrl = `phonepe://pay?pa=${VPA}&pn=${encodeURIComponent(MERCHANT_NAME)}&am=${VERIFY_AMOUNT}&cu=INR&tn=${upiTxNote}`;
  const upiPaytmUrl = `paytmmp://pay?pa=${VPA}&pn=${encodeURIComponent(MERCHANT_NAME)}&am=${VERIFY_AMOUNT}&cu=INR&tn=${upiTxNote}`;

  const whatsAppProofUrl = submittedResult
    ? `https://wa.me/918192911360?text=${encodeURIComponent(
        `*Official DBERT Project Verification Proof (₹299)*\n\n` +
        `Hello DBERT Admissions, I have completed the ₹299 project verification payment to unlock my official credentials.\n\n` +
        `• *Candidate Name:* ${submittedResult.fullName}\n` +
        `• *Certificate ID:* ${submittedResult.certId || 'N/A'}\n` +
        `• *Domain Track:* ${submittedResult.domain}\n` +
        `• *Amount Paid:* ₹299\n` +
        `• *12-Digit UTR:* ${submittedResult.utrNumber}\n` +
        `• *Submission Ref:* ${submittedResult.submissionId}\n\n` +
        `Please verify and activate my official 3-document credential packet.`
      )}`
    : '';

  return (
    <div className={s.container}>
      {/* Breadcrumb Navigation */}
      <Link href="/verify" className={s.breadcrumb}>
        &larr; Return to Credential Verification
      </Link>

      {/* Header Announcement Card */}
      <div className={s.headerCard}>
        <div className={s.badgeRow}>
          <span className={s.portalBadge}>Official Verification Desk</span>
          <span className={s.sovereignBadge}>DBERT Sovereign Registry · dbert.in</span>
        </div>

        <h1 className={s.pageTitle}>
          Credential Authentication &amp; Final Project Verification
        </h1>
        <p className={s.pageSubtitle}>
          Complete final project verification to unlock your official cryptographic certificate of completion, 9-dimension academic evaluation rubric, Turnitin originality seal, and institutional Letter of Recommendation.
        </p>

        {/* Clear Fee Transparency Ledger */}
        <div className={s.ledgerBox}>
          <div className={s.ledgerItem}>
            <span className={s.ledgerLabel}>Academic Capstone Review &amp; Plagiarism Clearance:</span>
            <span className={s.ledgerValue}>INCLUDED</span>
          </div>
          <div className={s.ledgerItem}>
            <span className={s.ledgerLabel}>Institutional LOR &amp; Cryptographic On-Chain Record:</span>
            <span className={s.ledgerValue}>INCLUDED</span>
          </div>
          <div className={s.ledgerItem}>
            <span className={s.ledgerLabel}>Official Verification Fee:</span>
            <span className={`${s.ledgerValue} ${s.ledgerPayable}`}>₹299</span>
          </div>
          <p className={s.ledgerNote}>
            💡 <strong>Provisional Record Notice:</strong> Once your ₹299 statutory verification fee and 12-digit UTR are submitted, your candidate dossier is upgraded from provisional to <strong>VERIFIED</strong> on the public registry.
          </p>
        </div>
      </div>

      {/* Quick Autofill Lookup */}
      <div className={s.lookupSection}>
        <div className={s.lookupTitle}>Candidate Profile Lookup</div>
        <p className={s.lookupSubtitle}>
          Enter your Certificate ID or Registered Email to instantly autofill your project and candidate profile.
        </p>
        <div className={s.lookupRow}>
          <input
            type="text"
            className={s.lookupInput}
            placeholder="e.g. CERT-DBERT-2026-FSD-103 or candidate@email.com"
            value={lookupQuery}
            onChange={(e) => setLookupQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && executeLookup(lookupQuery)}
          />
          <button
            type="button"
            className={s.lookupBtn}
            onClick={() => executeLookup(lookupQuery)}
            disabled={isSearching}
          >
            {isSearching ? 'Searching...' : 'Find Record →'}
          </button>
        </div>
      </div>

      {/* SUCCESS RECEIPT (If Submitted) */}
      {submittedResult ? (
        <div className={s.receiptCard}>
          <div className={s.receiptHead}>
            <div className={s.receiptIcon}>✓</div>
            <div>
              <h2 className={s.receiptTitle}>
                {submittedResult.alreadySubmitted
                  ? 'Verification Submission Already on File'
                  : 'Verification Payment Received & Recorded'}
              </h2>
            </div>
          </div>
          <p className={s.receiptText}>
            Your ₹299 project verification submission has been securely recorded in the registry ledger. Our admissions team is validating your 12-digit UTR against bank records to issue your official credentials.
          </p>

          <div className={s.receiptDetails}>
            <div className={s.receiptRow}>
              <span>Submission Ref ID:</span>
              <span className={s.receiptVal}>{submittedResult.submissionId}</span>
            </div>
            <div className={s.receiptRow}>
              <span>Candidate Name:</span>
              <span className={s.receiptVal}>{submittedResult.fullName}</span>
            </div>
            {submittedResult.certId && (
              <div className={s.receiptRow}>
                <span>Certificate ID:</span>
                <span className={s.receiptVal}>{submittedResult.certId}</span>
              </div>
            )}
            <div className={s.receiptRow}>
              <span>Domain Track:</span>
              <span className={s.receiptVal}>{submittedResult.domain}</span>
            </div>
            <div className={s.receiptRow}>
              <span>12-Digit UTR:</span>
              <span className={s.receiptVal} style={{ color: '#34D399' }}>{submittedResult.utrNumber}</span>
            </div>
            <div className={s.receiptRow}>
              <span>Fee Reconciled:</span>
              <span className={s.receiptVal} style={{ color: '#34D399' }}>₹299 Paid in Full</span>
            </div>
          </div>

          <a
            href={whatsAppProofUrl}
            target="_blank"
            rel="noopener noreferrer"
            className={s.waBtn}
          >
            <span>📱 Send Transaction Proof on WhatsApp (+91 81929 11360) &rarr;</span>
          </a>
        </div>
      ) : (
        /* 2-COLUMN PAYMENT & SUBMISSION GRID */
        <div className={s.layoutGrid}>
          {/* LEFT COLUMN: Payment Methods & QR Code */}
          <div className={s.card}>
            <div className={s.cardHeader}>
              <h2 className={s.cardTitle}>1. Scan &amp; Pay ₹299</h2>
              <span className={s.stepBadge}>Step 1</span>
            </div>

            <div className={s.qrWrapper}>
              <div className={s.qrImageFrame}>
                <Image
                  src="/qrcode.jpeg"
                  alt="DBERT Official UPI QR Code for ₹299 Verification"
                  width={220}
                  height={220}
                  className={s.qrImage}
                  priority
                />
              </div>

              <div className={s.vpaBadge}>
                <span>{VPA}</span>
                <button
                  type="button"
                  className={s.copyVpaBtn}
                  onClick={handleCopyVpa}
                >
                  {copiedVpa ? 'Copied!' : 'Copy UPI'}
                </button>
              </div>

              <div style={{ fontSize: '0.82rem', color: '#8A9AB5', textAlign: 'center' }}>
                Merchant: <strong>{MERCHANT_NAME}</strong> · Amount: <strong style={{ color: '#34D399' }}>₹299</strong>
              </div>

              {/* 1-Tap Mobile UPI Launchers */}
              <div className={s.upiDeepLinks}>
                <a href={upiGenericUrl} className={s.upiAppBtn}>
                  Default UPI App
                </a>
                <a href={upiGPayUrl} className={s.upiAppBtn}>
                  Google Pay
                </a>
                <a href={upiPhonePeUrl} className={s.upiAppBtn}>
                  PhonePe
                </a>
                <a href={upiPaytmUrl} className={s.upiAppBtn}>
                  Paytm
                </a>
              </div>

              <button
                type="button"
                className={s.downloadQrBtn}
                onClick={handleDownloadQr}
              >
                📥 Download High-Res QR Code
              </button>
            </div>
          </div>

          {/* RIGHT COLUMN: Submission Form */}
          <div className={s.card}>
            <div className={s.cardHeader}>
              <h2 className={s.cardTitle}>2. Submit Transaction Proof</h2>
              <span className={s.stepBadge}>Step 2</span>
            </div>

            {errorMsg && (
              <div className={s.errorBanner}>
                {errorMsg}
              </div>
            )}

            <form onSubmit={handleSubmit}>
              <div className={s.formGroup}>
                <label className={s.formLabel}>Full Legal Name *</label>
                <input
                  type="text"
                  className={s.formInput}
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  placeholder="e.g. John Doe"
                  required
                />
              </div>

              <div className={s.formGroup}>
                <label className={s.formLabel}>Registered Email *</label>
                <input
                  type="email"
                  className={s.formInput}
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="e.g. candidate@domain.com"
                  required
                />
              </div>

              <div className={s.formGroup}>
                <label className={s.formLabel}>WhatsApp Phone Number *</label>
                <input
                  type="tel"
                  className={s.formInput}
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  placeholder="e.g. 9876543210"
                  required
                />
              </div>

              <div className={s.formGroup}>
                <label className={s.formLabel}>Certificate ID (If Assigned)</label>
                <input
                  type="text"
                  className={`${s.formInput} ${certId ? s.formInputReadOnly : ''}`}
                  value={certId}
                  onChange={(e) => setCertId(e.target.value)}
                  placeholder="e.g. CERT-DBERT-2026-FSD-103"
                />
              </div>

              <div className={s.formGroup}>
                <label className={s.formLabel}>Domain Track</label>
                <input
                  type="text"
                  className={s.formInput}
                  value={domain}
                  onChange={(e) => setDomain(e.target.value)}
                  placeholder="e.g. Full Stack Web Development"
                />
              </div>

              <div className={s.formGroup}>
                <label className={s.formLabel}>12-Digit UPI Transaction UTR *</label>
                <input
                  type="text"
                  maxLength={12}
                  className={`${s.formInput} ${s.utrInput}`}
                  value={utrNumber}
                  onChange={(e) => setUtrNumber(e.target.value.replace(/\D/g, ''))}
                  placeholder="e.g. 403819283019"
                  required
                />
                <div className={s.formHelper}>
                  Enter the 12-digit numeric reference (UTR / UPI Ref ID) from your bank or payment app receipt.
                </div>
              </div>

              <div className={s.formGroup}>
                <label className={s.formLabel}>Additional Remarks (Optional)</label>
                <input
                  type="text"
                  className={s.formInput}
                  value={remarks}
                  onChange={(e) => setRemarks(e.target.value)}
                  placeholder="Project name or college details"
                />
              </div>

              <button
                type="submit"
                className={s.submitBtn}
                disabled={submitting}
              >
                {submitting ? 'Recording Submission...' : 'Complete Verification & Unlock Credentials (₹299) →'}
              </button>
            </form>
          </div>
        </div>
      )}
      {/* ══════════════════════════════════════════════════════════════════════
          Pre-Vetted Engineers Showcase & Direct Directory Routing
          ══════════════════════════════════════════════════════════════════════ */}
      <div className={s.engineersSection}>
        <div className={s.engineersHeader}>
          <div className={s.engineersTitleGroup}>
            <div className={s.engineersBadge}>
              <span>●</span> Active Talent Roster &middot; 79+ Verified Engineers
            </div>
            <h2 className={s.engineersTitle}>
              Pre-Vetted Engineers Already Verified &amp; Listed
            </h2>
            <p className={s.engineersSubtitle}>
              Candidates who completed final deliverable verification have their Turnitin-audited dossier and institutional LOR permanently indexed for corporate recruiters on the Sovereign Directory.
            </p>
          </div>
          <Link href="/verify/directory" className={s.directoryExploreBtn}>
            Explore Pre-Vetted Directory (79+ Profiles) &rarr;
          </Link>
        </div>

        <div className={s.engineersGrid}>
          {FEATURED_ENGINEERS.map((eng) => (
            <div key={eng.certId} className={s.engineerCard}>
              <div>
                <div className={s.engineerCardTop}>
                  <span className={s.engineerDomainPill}>{eng.domain}</span>
                  <span className={s.engineerScoreBadge}>{eng.score}/100</span>
                </div>
                <h3 className={s.engineerName}>{eng.name}</h3>
                <div className={s.engineerCollege}>{eng.college}</div>
                <div className={s.engineerStack}>
                  {eng.stack.map((t) => (
                    <span key={t} className={s.engineerTechPill}>{t}</span>
                  ))}
                </div>
              </div>
              <Link href={`/verify/${eng.certId}`} className={s.engineerDossierLink} target="_blank">
                View Proof Dossier &rarr;
              </Link>
            </div>
          ))}
        </div>
      </div>

      {/* ══════════════════════════════════════════════════════════════════════
          Provisional vs. Verified Career Impact Comparison
          ══════════════════════════════════════════════════════════════════════ */}
      <div className={s.comparisonSection}>
        <h2 className={s.comparisonTitle}>Provisional Record vs. Verified Credential</h2>
        <p className={s.comparisonSubtitle}>
          Compare what is unlocked once your repository deliverables undergo official Turnitin originality audit and mentor sign-off.
        </p>
        <div className={s.comparisonTableWrap}>
          <table className={s.comparisonTable}>
            <thead>
              <tr>
                <th className={s.featureCol}>Evaluation Dimension</th>
                <th className={s.provisionalCol}>Provisional Status</th>
                <th className={s.verifiedCol}>Verified Pre-Vetted Status</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className={s.featureCol}>Credential Document</td>
                <td className={s.provisionalCol}>🔒 Watermarked &amp; Locked Preview</td>
                <td className={s.verifiedCol}>✓ Cryptographic SHA-256 PDF Packet</td>
              </tr>
              <tr>
                <td className={s.featureCol}>Academic Evaluation Rubric</td>
                <td className={s.provisionalCol}>🔒 Locked (Pending Verification)</td>
                <td className={s.verifiedCol}>✓ 9-Dimension Rubric + Turnitin &lt;3% Seal</td>
              </tr>
              <tr>
                <td className={s.featureCol}>Institutional Letter of Recommendation</td>
                <td className={s.provisionalCol}>✗ Not Generated</td>
                <td className={s.verifiedCol}>✓ Official LOR on Venture Studio Letterhead</td>
              </tr>
              <tr>
                <td className={s.featureCol}>Pre-Vetted Engineers Directory</td>
                <td className={s.provisionalCol}>✗ Excluded / Unlisted</td>
                <td className={s.verifiedCol}>✓ Searchable by 100+ Hiring Partners</td>
              </tr>
              <tr>
                <td className={s.featureCol}>Direct LMS Employer Connect</td>
                <td className={s.provisionalCol}>✗ Inactive</td>
                <td className={s.verifiedCol}>✓ 1-Click Recruiter Messaging &amp; Inbound</td>
              </tr>
              <tr>
                <td className={s.featureCol}>Capstone Performance Stipend</td>
                <td className={s.provisionalCol}>🔒 Locked Gate 1</td>
                <td className={s.verifiedCol}>✓ Eligible for ₹5,000 Milestone Payout</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* What Unlocks Upon Project Verification (Executive Value Showcase) */}
      <div className={s.valueSection}>
        <h2 className={s.valueSectionTitle}>What Unlocks Upon Final Project Verification</h2>
        <p className={s.valueSectionSubtitle}>
          Completing your statutory verification transforms your provisional submission into an accredited engineering dossier backed by Turnitin originality validation, executive mentorship endorsement, and direct hiring partner exposure.
        </p>

        <div className={s.valueGrid}>
          {/* Card 1: Certificate */}
          <div className={s.valueCard}>
            <span className={`${s.valueCardTag} ${s.tagCert}`}>Document 01</span>
            <h3 className={s.valueCardTitle}>Certificate of Completion</h3>
            <p className={s.valueCardDesc}>
              MSME-registered official certification featuring cryptographic SHA-256 validation seal, unique Certificate ID, and signed authorization by Program Head Mr. Abhinav Sharma.
            </p>
          </div>

          {/* Card 2: Academic Rubric */}
          <div className={s.valueCard}>
            <span className={`${s.valueCardTag} ${s.tagEval}`}>Document 02</span>
            <h3 className={s.valueCardTitle}>Turnitin Academic Rubric (Score/100)</h3>
            <p className={s.valueCardDesc}>
              US Letter portrait appraisal with 9 rigorous engineering dimensions, code quality audit, Git velocity assessment, and official Turnitin &lt;3.0% originality clearance seal.
            </p>
          </div>

          {/* Card 3: Letter of Recommendation */}
          <div className={s.valueCard}>
            <span className={`${s.valueCardTag} ${s.tagLor}`}>Document 03</span>
            <h3 className={s.valueCardTitle}>Institutional Letter of Recommendation</h3>
            <p className={s.valueCardDesc}>
              Official executive LOR on DBERT venture studio letterhead signed by Mr. Abhinav Sharma (<a href="https://github.com/ainabhinavsharma" target="_blank" rel="noopener noreferrer" style={{ color: '#38BDF8', textDecoration: 'underline' }}>Mentor Profile &rarr;</a>) endorsing your technical problem-solving and repository contributions for corporate recruiters, master&apos;s admissions, and visas.
            </p>
          </div>

          {/* Card 4: Directory Listing */}
          <div className={s.valueCard}>
            <span className={`${s.valueCardTag} ${s.tagDir}`}>Recruiter Portal</span>
            <h3 className={s.valueCardTitle}>Listed as Pre-Vetted Engineer</h3>
            <p className={s.valueCardDesc}>
              Instant promotion to the public Pre-Vetted Engineers Directory (dbert.in/verify/directory) accessed by 100+ hiring partners and tech founders with 0% recruiter markup.
            </p>
          </div>

          {/* Card 5: LinkedIn Verification */}
          <div className={s.valueCard}>
            <span className={`${s.valueCardTag} ${s.tagLinkedIn}`}>Career Authority</span>
            <h3 className={s.valueCardTitle}>1-Click LinkedIn Credential</h3>
            <p className={s.valueCardDesc}>
              One-click direct addition to your LinkedIn &ldquo;Licenses &amp; Certifications&rdquo; section with live cryptographic verification link that boosts recruiter inbound inquiries.
            </p>
          </div>

          {/* Card 6: Performance Stipend */}
          <div className={s.valueCard}>
            <span className={`${s.valueCardTag} ${s.tagStipend}`}>Financial Benefit</span>
            <h3 className={s.valueCardTitle}>Performance Stipend Access</h3>
            <p className={s.valueCardDesc}>
              Unlocks verified candidate status required to submit pull requests on /stipend/tasks and withdraw milestone performance rewards (₹5,000–₹18,000) directly via UPI.
            </p>
          </div>
        </div>

        {/* Directory Highlight Callout */}
        <div className={s.directoryCalloutBanner}>
          <div className={s.calloutText}>
            <h4 className={s.calloutHeading}>⭐ Recruiter Direct Exposure Guarantee</h4>
            <p className={s.calloutSub}>
              Verified engineers are actively recommended to enterprise startups and tech companies looking for immediately deployable candidates with proven repository commits.
            </p>
          </div>
          <div className={s.calloutBadge}>Top 3% Talent Roster</div>
        </div>
      </div>

    </div>
  );
}
