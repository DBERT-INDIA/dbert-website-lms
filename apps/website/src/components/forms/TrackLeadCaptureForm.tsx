'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { CheckCircle2, ArrowRight, ShieldCheck, Zap, MessageSquare } from 'lucide-react';
import { getPublishedTracks } from '@/data/courses.config';
import s from './TrackLeadCaptureForm.module.css';

export interface TrackLeadCaptureFormProps {
  initialDomain?: string;
  initialCity?: string;
  initialProgram?: 'fellowship' | 'course' | 'both';
  title?: string;
  subtitle?: string;
}

export const DOMAIN_OPTIONS = getPublishedTracks().map((track) => ({
  slug: track.slug,
  label: track.name,
}));

export default function TrackLeadCaptureForm({
  initialDomain = 'ai-agent-development',
  initialCity = '',
  initialProgram = 'fellowship',
  title = 'Fast-Track Admissions & Syllabus Access',
  subtitle = 'Get immediate syllabus access, cohort fee details, and speak with an engineering mentor.'
}: TrackLeadCaptureFormProps) {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    college: '',
    graduationYear: '2026',
    domain: initialDomain,
    programInterest: initialProgram,
    city: initialCity
  });

  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [leadId, setLeadId] = useState('');
  const [submitted, setSubmitted] = useState(false);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const urlParams = new URLSearchParams(window.location.search);
      const utmSource = urlParams.get('utm_source') || '';
      const utmMedium = urlParams.get('utm_medium') || '';
      const utmCampaign = urlParams.get('utm_campaign') || '';
      const cityParam = urlParams.get('city') || initialCity;
      const domainParam = urlParams.get('domain') || initialDomain;

      queueMicrotask(() => {
        setFormData((prev) => ({
          ...prev,
          city: cityParam || prev.city,
          domain: domainParam || prev.domain,
          ...(utmSource ? { utmSource } : {}),
          ...(utmMedium ? { utmMedium } : {}),
          ...(utmCampaign ? { utmCampaign } : {})
        }));
      });
    }
  }, [initialCity, initialDomain]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleProgramChange = (prog: 'fellowship' | 'course') => {
    setFormData((prev) => ({ ...prev, programInterest: prog }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.name.trim() || formData.name.trim().length < 2) {
      setErrorMsg('Please enter your full legal name.');
      return;
    }
    if (!formData.email.trim() || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email.trim())) {
      setErrorMsg('Please enter a valid email address.');
      return;
    }
    if (!formData.phone.trim() || formData.phone.trim().replace(/\D/g, '').length < 10) {
      setErrorMsg('Please enter a valid 10-digit WhatsApp number.');
      return;
    }

    setLoading(true);
    setErrorMsg('');

    try {
      const res = await fetch('/api/leads/capture', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      const data = await res.json();
      if (!res.ok || !data.success) {
        throw new Error(data.error || 'Submission failed. Please try again.');
      }
      setLeadId(data.leadId);
      setSubmitted(true);
    } catch (err: any) {
      setErrorMsg(err.message || 'Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (submitted) {
    const whatsappMsg = encodeURIComponent(
      `Hi DBERT Admissions! I just registered my interest for the ${formData.domain} track (Ref: ${leadId}). Name: ${formData.name}, College: ${formData.college || 'N/A'}. Please share the syllabus brochure and enrollment details.`
    );

    return (
      <div className={s.leadCard}>
        <div className={s.successCard}>
          <CheckCircle2 className={s.successIcon} />
          <h3 className={s.successTitle}>Admissions Request Received</h3>
          <p className={s.successDesc}>
            Thank you, <strong>{formData.name}</strong>! Your application token is{' '}
            <code style={{ color: '#10b981', background: 'rgba(16,185,129,0.1)', padding: '2px 6px', borderRadius: 4 }}>
              {leadId}
            </code>
            . Our senior engineering admissions squad is preparing your custom syllabus dossier.
          </p>

          <a
            href={`https://wa.me/918192911360?text=${whatsappMsg}`}
            target="_blank"
            rel="noopener noreferrer"
            className={s.whatsappCta}
          >
            <MessageSquare size={18} />
            Connect on WhatsApp Admissions
          </a>

          <div style={{ marginTop: 16 }}>
            <Link
              href={`/enroll/1999?email=${encodeURIComponent(formData.email)}&domain=${encodeURIComponent(formData.domain)}`}
              className={s.fastTrackLink}
            >
              Direct Program Seat Confirmation (₹1,999) →
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={s.leadCard} id="apply-lead-form">
      <div className={s.leadHeader}>
        <div style={{ marginBottom: 10 }}>
          <span className={s.leadBadge}>
            <ShieldCheck size={13} /> Admissions &amp; Syllabus
          </span>
        </div>
        <h3 className={s.leadTitle}>{title}</h3>
        <p className={s.leadSubtitle}>{subtitle}</p>
      </div>

      <form onSubmit={handleSubmit} className={s.formGrid}>
        {errorMsg && <div className={s.errorBanner}>{errorMsg}</div>}

        <div className={s.inputGroup}>
          <label className={s.label}>Program Track Interest</label>
          <div className={s.radioGroup}>
            <div
              className={`${s.radioLabel} ${formData.programInterest === 'fellowship' ? s.radioLabelActive : ''}`}
              onClick={() => handleProgramChange('fellowship')}
            >
              <span>2-Mo Fellowship</span>
              <span>₹1,999 · 100% Guaranteed Production Internship</span>
            </div>
            <div
              className={`${s.radioLabel} ${formData.programInterest === 'course' ? s.radioLabelActive : ''}`}
              onClick={() => handleProgramChange('course')}
            >
              <span>3-Mo Professional Course</span>
              <span>Full Stack Mastery · EMI</span>
            </div>
          </div>
        </div>

        <div className={s.inputGroup}>
          <label htmlFor="domain-select" className={s.label}>Specialization Domain</label>
          <select
            id="domain-select"
            name="domain"
            value={formData.domain}
            onChange={handleChange}
            className={s.select}
          >
            {DOMAIN_OPTIONS.map((opt) => (
              <option key={opt.slug} value={opt.slug}>
                {opt.label}
              </option>
            ))}
          </select>
        </div>

        <div className={s.inputGroup}>
          <label htmlFor="name-input" className={s.label}>Full Name</label>
          <input
            id="name-input"
            type="text"
            name="name"
            placeholder="e.g. Rahul Sharma"
            value={formData.name}
            onChange={handleChange}
            required
            className={s.input}
          />
        </div>

        <div className={s.inputGroup}>
          <label htmlFor="email-input" className={s.label}>Email Address</label>
          <input
            id="email-input"
            type="email"
            name="email"
            placeholder="rahul.sharma@college.edu"
            value={formData.email}
            onChange={handleChange}
            required
            className={s.input}
          />
        </div>

        <div className={s.inputGroup}>
          <label htmlFor="phone-input" className={s.label}>WhatsApp Phone (+91)</label>
          <input
            id="phone-input"
            type="tel"
            name="phone"
            placeholder="98765 43210"
            value={formData.phone}
            onChange={handleChange}
            required
            className={s.input}
          />
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: 10 }}>
          <div className={s.inputGroup}>
            <label htmlFor="college-input" className={s.label}>College / University</label>
            <input
              id="college-input"
              type="text"
              name="college"
              placeholder="e.g. IIT, NIT, PES, Anna Univ"
              value={formData.college}
              onChange={handleChange}
              className={s.input}
            />
          </div>

          <div className={s.inputGroup}>
            <label htmlFor="city-input" className={s.label}>City</label>
            <input
              id="city-input"
              type="text"
              name="city"
              placeholder="e.g. Bengaluru"
              value={formData.city}
              onChange={handleChange}
              className={s.input}
            />
          </div>
        </div>

        <button type="submit" disabled={loading} className={s.submitBtn}>
          {loading ? (
            'Submitting...'
          ) : (
            <>
              Get Syllabus &amp; Apply <ArrowRight size={16} />
            </>
          )}
        </button>

        <Link
          href={`/enroll/1999?domain=${encodeURIComponent(formData.domain)}`}
          className={s.fastTrackLink}
        >
          <Zap size={13} style={{ color: '#f59e0b' }} /> Confirm Your Seat Now (₹1,999) →
        </Link>

        <div style={{ marginTop: 14, textAlign: 'center', fontSize: '0.8rem', color: '#94a3b8' }}>
          Applying directly for an internship?{' '}
          <a
            href="https://lms.dbert.in/apply"
            target="_blank"
            rel="noopener noreferrer"
            style={{ color: '#38bdf8', textDecoration: 'underline', fontWeight: 600 }}
          >
            Apply on the LMS Portal →
          </a>
        </div>
      </form>
    </div>
  );
}
