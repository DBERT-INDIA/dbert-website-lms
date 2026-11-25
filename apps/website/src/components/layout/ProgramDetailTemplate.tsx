'use client';

import React, { useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import HandNote from '@/components/ui/HandNote';
import { 
  CheckCircle2, 
  CircleCheck, 
  Calendar, 
  Zap, 
  GitPullRequest, 
  Award, 
  ShieldCheck, 
  ExternalLink,
  ArrowRight,
  Smartphone,
  Lock,
  ArrowLeft
} from 'lucide-react';
import s from './ProgramDetailTemplate.module.css';

const ENROLLMENT_TRACKS = [
  'AI Agent Development', 'Data Analyst', 'Full Stack Development', 'Python Automation',
  'UI/UX Design', 'DevOps & Cloud', 'Mobile App Development', 'Cybersecurity', 'Digital Marketing',
];

export interface CurriculumBlock {
  period: string;
  title: string;
  topics: string[];
}

export interface ProductionRepo {
  name: string;
  badgeText?: string;
  description: string;
  keyModules?: string[];
  githubUrl?: string;
  url?: string;
  role?: string;
}

export interface ProgramDetailTemplateProps {
  title: string;
  subtitle?: string;
  price: string;
  duration: string;
  audience: string;
  outcome: string;
  curriculum: CurriculumBlock[];
  headerSlot?: React.ReactNode;
  repoReference?: ProductionRepo;
  repoReferences?: ProductionRepo[];
}

export default function ProgramDetailTemplate({
  title,
  subtitle,
  price,
  duration,
  audience,
  outcome,
  curriculum,
  headerSlot,
  repoReference,
  repoReferences
}: ProgramDetailTemplateProps) {
  const [step, setStep] = useState<'details' | 'payment'>('details');
  const [formData, setFormData] = useState({ name: '', email: '', phone: '', college: '', utr: '', track: '' });
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [submissionId, setSubmissionId] = useState('');
  const [claimStatus, setClaimStatus] = useState<'pending' | 'verified' | 'rejected'>('pending');
  const [errorMsg, setErrorMsg] = useState('');

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleProceedToPayment = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.name.trim() || !formData.email.trim() || !formData.phone.trim()) {
      setErrorMsg('Please enter your full name, email, and 10-digit WhatsApp number.');
      return;
    }
    if (!formData.track) {
      setErrorMsg('Select your learning track.');
      return;
    }
    setErrorMsg('');
    setStep('payment');
  };

  const handleFinalEnrollment = async (e: React.FormEvent) => {
    e.preventDefault();
    const cleanUtr = formData.utr.trim().toUpperCase();
    if (!cleanUtr || cleanUtr.length < 6) {
      setErrorMsg('Please enter a valid 12-digit UPI UTR / Transaction Reference number.');
      return;
    }

    setLoading(true);
    setErrorMsg('');

    try {
      const res = await fetch('/api/courses/enroll', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          fullName: formData.name.trim(),
          email: formData.email.trim().toLowerCase(),
          phone: formData.phone.trim(),
          college: formData.college.trim(),
          domain: formData.track,
          utrNumber: cleanUtr
        })
      });

      const data = await res.json();
      if (!res.ok || !data.success) {
        throw new Error(data.error || 'Enrollment submission failed. Please try again.');
      }

      setSubmissionId(data.submissionId || '');
      setClaimStatus(data.claimStatus);
      setSuccess(true);
    } catch (err: any) {
      setErrorMsg(err.message || 'Network error while validating payment. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const upiDeepLink = `upi://pay?pa=Q652429146@ybl&pn=DBERT%20Admissions&am=499&cu=INR&tn=DBERT%20Course%20Seat`;

  return (
    <div className="container py-xl">
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify({
        "@context": "https://schema.org",
        "@type": "Course",
        "name": title,
        "description": subtitle || `${duration} Guided Education Curriculum`,
        "provider": {
          "@type": "Organization",
          "name": "DBERT",
          "sameAs": "https://dbert.in"
        },
        "offers": {
          "@type": "Offer",
          "price": "499",
          "priceCurrency": "INR",
          "category": "Security Deposit"
        }
      }) }} />
      
      <div className="mb-lg">
        <div className="doclabel">
          § 01 — {duration.toUpperCase()} INDUSTRIAL CURRICULUM <span className="rev">rev: 2026.2</span>
        </div>
        <div className="stack-h align-baseline gap-3 flex-wrap">
          <h1>{title}</h1>
          <HandNote tone="amber">
            evaluated code reviews · live PRs ✍
          </HandNote>
        </div>
        <p className="body-copy">{subtitle || `${duration} Guided Education Curriculum`}</p>

        {/* Quick Program Meta Strip */}
        <div className={s.metaStrip}>
          <span className={s.metaPill}>
            <Calendar size={14} className="text-accent" aria-hidden="true" />
            <span><strong>{duration}</strong> (8 Sprint Cycles)</span>
          </span>
          <span className={s.metaPill}>
            <Zap size={14} className="text-signal" aria-hidden="true" />
            <span><strong>10–15 Hours/Week</strong> (Async Sprints)</span>
          </span>
          <span className={s.metaPill}>
            <GitPullRequest size={14} className="text-accent" aria-hidden="true" />
            <span><strong>Production PRs</strong> (Senior Code Reviews)</span>
          </span>
          <span className={s.metaPill}>
            <Award size={14} className="text-ok" aria-hidden="true" />
            <span><strong>Verifiable Certificate</strong> (SHA-256 Auth)</span>
          </span>
        </div>

        {headerSlot && <div className="mt-4">{headerSlot}</div>}
      </div>

      <div className={s.layout}>
        {/* Left Column: Course Content FIRST */}
        <div className="stack">
          <section className={s.curriculumSection}>
            <div className={s.curriculumHead}>
              <div className="doclabel text-xs mb-1">§ CURRICULUM ARCHITECTURE</div>
              <h2>Weekly Production Sprints &amp; Deliverables</h2>
              <p className={s.curriculumSub}>
                Hands-on engineering modules worked through on real code. You write executable scripts, build backend pipelines, and submit evaluated pull requests each sprint.
              </p>
            </div>

            <div className={s.curriculumStack}>
              {curriculum.map((item, idx) => (
                <div key={idx} className={s.curriculumBlock}>
                  <div className={s.blockHeader}>
                    <span className={s.periodBadge}>{item.period}</span>
                    <span className={s.paceBadge}>4 Weekly Sprints &middot; Evaluated PR Review</span>
                  </div>
                  <h3 className={s.moduleTitle}>{item.title}</h3>
                  <ul className={s.topicList}>
                    {item.topics.map((t, tIdx) => (
                      <li key={tIdx} className={s.topicItem}>
                        <span className={s.topicBullet} aria-hidden="true" />
                        <span>{t}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </section>

          {/* ACTIVE OPPORTUNITIES / REPOSITORIES */}
          {((repoReferences && repoReferences.length > 0) || repoReference) && (
            <section className={s.squadSection}>
              <div className={s.squadHead}>
                <div className="doclabel text-xs mb-1">§ ACTIVE PRODUCTION OPPORTUNITIES</div>
                <h2>Where Interns Are Contributing Right Now</h2>
                <p className={s.squadLead}>
                  We do not assign isolated classroom exercises. Your weekly sprint tasks and capstone map directly to these active production repositories maintained across our venture studio squads.
                </p>
              </div>

              <div className={s.squadGrid}>
                {(repoReferences || [repoReference!]).map((repo, rIdx) => (
                  <div key={rIdx} className={s.squadCard}>
                    <div className={s.squadTop}>
                      <div className={s.badgeGroup}>
                        {repo.badgeText && (
                          <span className={s.squadCohortBadge}>{repo.badgeText}</span>
                        )}
                        <span className={s.squadVerifiedBadge}>
                          <ShieldCheck size={12} className="inline mr-1 text-ok" />
                          Production
                        </span>
                      </div>
                      {(repo.githubUrl || repo.url) && (
                        <a
                          href={repo.githubUrl || repo.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className={s.repoLink}
                          aria-label={`View ${repo.name} repository on GitHub`}
                        >
                          <ExternalLink size={14} />
                        </a>
                      )}
                    </div>
                    <h3 className={s.repoName}>{repo.name}</h3>
                    <p className={s.repoDesc}>{repo.description}</p>
                    {repo.keyModules && repo.keyModules.length > 0 && (
                      <div className={s.tagRow}>
                        {repo.keyModules.map((mod, idx) => (
                          <span key={idx} className={s.techTag}>
                            {mod}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </section>
          )}
        </div>

        {/* Right Column: Sticky Sidebar with Details & Enrollment */}
        <aside className={s.stickySidebar} aria-label="Program Investment and Enrollment">
          <div className={s.sidebarCard}>
            <span className={s.feeLabel}>Total Program Fee</span>
            <div style={{ display: 'flex', alignItems: 'baseline', gap: '8px' }}>
              <strong className={s.feeValue} style={{ fontSize: '1.75rem', color: '#10B981' }}>₹1,999</strong>
              <span style={{ fontSize: '12px', color: '#94A3B8' }}>(All inclusive)</span>
            </div>
            <div style={{ background: 'rgba(245, 158, 11, 0.1)', border: '1px solid rgba(245, 158, 11, 0.3)', borderRadius: '8px', padding: '10px 12px', marginTop: '10px' }}>
              <div style={{ fontSize: '11px', fontWeight: 800, color: '#FBBF24', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                Pay in 2 Steps
              </div>
              <div style={{ fontSize: '12.5px', color: '#F1F5F9', marginTop: '2px', lineHeight: '1.4' }}>
                <strong>₹499 Security Deposit</strong> today to secure seat · <strong>₹1,500</strong> balance payable after batch kickoff within 7 days.
              </div>
            </div>
          </div>

          <div className={s.sidebarCard}>
            <h3 className={s.sidebarTitle}>Who It&apos;s For</h3>
            <p className={s.sidebarCopy}>{audience}</p>
          </div>

          <div className={s.sidebarCard}>
            <h3 className={s.sidebarTitle}>Verified Outcome</h3>
            <p className={s.sidebarCopy}>{outcome}</p>
          </div>

          {/* Unified UPI QR Enrollment Card */}
          <div className={s.sidebarCard}>
            {success ? (
              <div className={s.successBlock}>
                <span className="icon-chip"><CircleCheck aria-hidden="true" /></span>
                <h3 className={s.successTitle}>
                  {claimStatus === 'verified' ? 'Security deposit verified'
                    : claimStatus === 'rejected' ? 'Payment claim rejected' : 'Deposit submitted for verification'}
                </h3>
                <p className={s.successCopy}>
                  Receipt reference <code>{submissionId}</code>.{' '}
                  {claimStatus === 'pending'
                    ? 'Admissions will review the payment reference against the settlement ledger.'
                    : claimStatus === 'rejected'
                      ? 'Contact admissions with your receipt reference if you believe this claim should be verified.'
                      : 'The payment has been matched to your enrollment.'}
                </p>
                <div style={{ marginTop: '16px' }}>
                  <a 
                    href="https://lms.dbert.in/portal/payment-claims"
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="btn btn-primary btn-sm"
                    style={{ width: '100%', display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: '8px', textDecoration: 'none' }}
                  >
                    <span>View payment status in LMS</span>
                    <ArrowRight size={14} />
                  </a>
                </div>
              </div>
            ) : step === 'details' ? (
              <form onSubmit={handleProceedToPayment} className={s.checkoutForm}>
                <h3 className={s.checkoutTitle}>Secure Your Seat</h3>
                <p className={s.checkoutCopy}>Reserve with ₹499 security deposit (credited in full).</p>
                
                {errorMsg && <div className={s.error}>{errorMsg}</div>}
                
                <input
                  type="text"
                  name="name"
                  required
                  placeholder="Full Legal Name"
                  aria-label="Full Legal Name"
                  value={formData.name}
                  onChange={handleInputChange}
                  className={s.input}
                />
                <input
                  type="email"
                  name="email"
                  required
                  placeholder="Email Address"
                  aria-label="Email Address"
                  value={formData.email}
                  onChange={handleInputChange}
                  className={s.input}
                />
                <input
                  type="tel"
                  name="phone"
                  required
                  placeholder="10-Digit WhatsApp Phone"
                  aria-label="Phone Number"
                  value={formData.phone}
                  onChange={handleInputChange}
                  className={s.input}
                />
                <input
                  type="text"
                  name="college"
                  placeholder="College / University Name"
                  aria-label="College Name"
                  value={formData.college}
                  onChange={handleInputChange}
                  className={s.input}
                />
                <label>
                  Learning track
                  <select
                    value={formData.track}
                    onChange={(event) => setFormData({ ...formData, track: event.target.value })}
                    className={s.input}
                    required
                  >
                    <option value="">Choose a track</option>
                    {ENROLLMENT_TRACKS.map((track) => <option key={track} value={track}>{track}</option>)}
                  </select>
                </label>

                <button type="submit" className={`btn btn-primary btn-sm ${s.submit}`} style={{ background: 'linear-gradient(135deg, #F59E0B, #D97706)', color: '#0F172A', fontWeight: 800 }}>
                  <span>Proceed to UPI QR (₹499)</span>
                  <ArrowRight size={14} style={{ marginLeft: '6px' }} />
                </button>
              </form>
            ) : (
              <form onSubmit={handleFinalEnrollment} className={s.checkoutForm}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
                  <button 
                    type="button" 
                    onClick={() => setStep('details')}
                    style={{ background: 'transparent', border: 'none', color: '#94A3B8', fontSize: '12px', display: 'flex', alignItems: 'center', gap: '4px', cursor: 'pointer' }}
                  >
                    <ArrowLeft size={12} /> Back
                  </button>
                  <span style={{ fontSize: '11px', color: '#FBBF24', fontWeight: 700 }}>STEP 2: UPI PAYMENT</span>
                </div>

                <div style={{ textAlign: 'center', background: '#0F172A', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '12px', padding: '14px', marginBottom: '12px' }}>
                  <div style={{ fontSize: '11px', color: '#94A3B8', textTransform: 'uppercase', fontWeight: 700 }}>Scan with any UPI App</div>
                  <div style={{ fontSize: '20px', fontWeight: 800, color: '#34D399', margin: '4px 0 10px' }}>Pay ₹499</div>
                  
                  <div style={{ width: '160px', height: '160px', margin: '0 auto', background: '#FFFFFF', borderRadius: '8px', padding: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <Image
                      src="/images/qrcode.jpeg"
                      alt="DBERT UPI QR Code"
                      width={144}
                      height={144}
                      style={{ objectFit: 'contain' }}
                      priority
                    />
                  </div>

                  <div style={{ fontSize: '11px', color: '#CBD5E1', marginTop: '8px', fontFamily: 'monospace' }}>
                    UPI ID: <strong>Q652429146@ybl</strong>
                  </div>
                </div>

                <div style={{ display: 'flex', gap: '6px', marginBottom: '12px' }}>
                  <a
                    href={upiDeepLink}
                    className="btn btn-secondary btn-sm"
                    style={{ flex: 1, fontSize: '11px', padding: '6px 8px', textAlign: 'center', textDecoration: 'none', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '4px', borderRadius: '6px' }}
                  >
                    <Smartphone size={12} /> Open UPI App
                  </a>
                </div>

                {errorMsg && <div className={s.error} style={{ marginBottom: '10px' }}>{errorMsg}</div>}

                <label style={{ fontSize: '12px', color: '#CBD5E1', fontWeight: 600, display: 'block', marginBottom: '4px' }}>
                  12-Digit UPI Transaction ID / UTR <span style={{ color: '#EF4444' }}>*</span>
                </label>
                <input
                  type="text"
                  name="utr"
                  required
                  placeholder="e.g. 418293849102"
                  maxLength={16}
                  value={formData.utr}
                  onChange={handleInputChange}
                  className={s.input}
                  style={{ textTransform: 'uppercase', letterSpacing: '1px', fontFamily: 'monospace' }}
                />

                <button 
                  type="submit" 
                  className={`btn btn-primary btn-sm ${s.submit}`} 
                  disabled={loading}
                  style={{ background: 'linear-gradient(135deg, #10B981, #059669)', color: '#FFFFFF', fontWeight: 800, marginTop: '8px' }}
                >
                  <Lock size={13} style={{ marginRight: '6px' }} />
                  {loading ? 'Verifying...' : 'Confirm Seat & Enroll (₹499)'}
                </button>
              </form>
            )}
          </div>
        </aside>
      </div>
    </div>
  );
}
