'use client';

import React, { useState } from 'react';
import Script from 'next/script';
import { CircleCheck, GitBranch, ExternalLink, Calendar, Zap, GitPullRequest, Award } from 'lucide-react';
import f from '../ui/forms.module.css';
import s from './ProgramDetailTemplate.module.css';

export interface RepoReference {
  name: string;
  url: string;
  role?: string;
  badgeText?: string;
  description?: string;
  keyModules?: string[];
}

interface ProgramDetailTemplateProps {
  title: string;
  subtitle?: string;
  price: string;
  duration: string;
  audience: string;
  outcome: string;
  curriculum: { period: string; title: string; topics: string[] }[];
  headerSlot?: React.ReactNode;
  repoReference?: RepoReference;
  repoReferences?: RepoReference[];
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
  const [formData, setFormData] = useState({ name: '', email: '', phone: '' });
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleCheckout = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setErrorMsg('');

    try {
      const amountInPaise = parseInt(price.replace(/[^0-9]/g, ''), 10) * 100;
      
      const orderRes = await fetch('/api/payments/create-order', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          programName: title,
          amount: amountInPaise,
          name: formData.name,
          email: formData.email,
          phone: formData.phone
        })
      });

      const orderData = await orderRes.json();
      
      if (!orderRes.ok) {
        throw new Error(orderData.error || 'Failed to create order');
      }

      const options = {
        key: orderData.keyId,
        amount: amountInPaise,
        currency: 'INR',
        name: 'DBERT',
        description: `Enrollment: ${title}`,
        order_id: orderData.orderId,
        handler: async function (response: any) {
          try {
            const verifyRes = await fetch('/api/payments/verify', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                razorpay_order_id: response.razorpay_order_id,
                razorpay_payment_id: response.razorpay_payment_id,
                razorpay_signature: response.razorpay_signature,
                enrollmentId: orderData.enrollmentId
              })
            });
            const verifyData = await verifyRes.json();
            if (verifyRes.ok) {
              setSuccess(true);
            } else {
              setErrorMsg(verifyData.error || 'Payment verification failed');
            }
          } catch (err) {
            setErrorMsg('Payment verification error');
          }
        },
        prefill: {
          name: formData.name,
          email: formData.email,
          contact: formData.phone
        },
        theme: {
          color: '#5B8CFF'
        },
        modal: {
          ondismiss: function () {
            setErrorMsg('Payment cancelled. You can try again when ready.');
          }
        }
      };

      const razorpay = new (window as any).Razorpay(options);
      razorpay.on('payment.failed', function (response: any) {
        const reason = response?.error?.reason || 'Payment failed';
        setErrorMsg(`${reason}. Please try again.`);
      });
      razorpay.open();

    } catch (err: any) {
      setErrorMsg(err.message || 'Error initiating checkout');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container pad-block">
      <Script src="https://checkout.razorpay.com/v1/checkout.js" strategy="lazyOnload" />
      <Script id={`course-schema-${title.replace(/\s+/g, '-').toLowerCase()}`} type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify({
        "@context": "https://schema.org",
        "@type": "Course",
        "name": title,
        "description": outcome,
        "provider": {
          "@type": "Organization",
          "name": "DBERT",
          "sameAs": "https://dbert.online"
        },
        "offers": {
          "@type": "Offer",
          "price": price.replace(/[^0-9]/g, ''),
          "priceCurrency": "INR",
          "category": "Paid"
        }
      }) }} />
      
      <div className="mb-lg">
        <div className="doclabel">
          § 01 — 2-MONTH INDUSTRIAL CURRICULUM <span className="rev">rev: 2026.2</span>
        </div>
        <h1>{title}</h1>
        <p>{subtitle || `${duration} Guided Education Curriculum`}</p>

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
        {/* Left Column: Course Content FIRST, followed by Active Production Repos */}
        <div className="stack">
          {/* 1. CURRICULUM CONTENT FIRST */}
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

          {/* 2. ACTIVE OPPORTUNITIES / REPOSITORIES (AFTER CURRICULUM) */}
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
                        {repo.role && (
                          <span className={s.squadRoleBadge}>Role: {repo.role}</span>
                        )}
                      </div>
                      <a
                        href={repo.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="btn btn-outline btn-sm font-mono text-xs inline-flex items-center gap-1.5"
                      >
                        <GitBranch className="w-3.5 h-3.5" />
                        <span>Inspect Codebase</span>
                        <ExternalLink className="w-3 h-3 text-muted" />
                      </a>
                    </div>
                    <h3 className={s.repoName}>{repo.name}</h3>
                    {repo.description && (
                      <p className={s.repoDesc}>{repo.description}</p>
                    )}
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
        <div className="stack">
          <div className={s.sidebarCard}>
            <span className={s.feeLabel}>Program Investment</span>
            <strong className={s.feeValue}>{price}</strong>
            <div className={s.feeMeta}>
              <span>Duration: <strong>{duration}</strong></span>
              <span>&bull;</span>
              <span>8 Sprints</span>
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

          {/* Checkout Form */}
          <div className={s.sidebarCard}>
            {success ? (
              <div className={s.successBlock}>
                <span className="icon-chip"><CircleCheck aria-hidden="true" /></span>
                <h3 className={s.successTitle}>Enrollment Successful</h3>
                <p className={s.successCopy}>We have received your payment. Check your email for cohort onboarding instructions.</p>
              </div>
            ) : (
              <form onSubmit={handleCheckout} className={s.checkoutForm}>
                <h3 className={s.checkoutTitle}>Secure Enrollment</h3>
                <p className={s.checkoutCopy}>Confirm your details to initiate payment validation.</p>
                
                {errorMsg && <div className={s.error}>{errorMsg}</div>}
                
                <input type="text" name="name" required placeholder="Full Name" value={formData.name} onChange={handleInputChange} className={s.input} />
                <input type="email" name="email" required placeholder="Email Address" value={formData.email} onChange={handleInputChange} className={s.input} />
                <input type="tel" name="phone" required placeholder="Phone Number" value={formData.phone} onChange={handleInputChange} className={s.input} />
                
                <button type="submit" className={`btn btn-primary btn-sm ${s.submit}`} disabled={loading}>
                  {loading ? 'Processing...' : `Enrol for ${price}`}
                </button>
              </form>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
