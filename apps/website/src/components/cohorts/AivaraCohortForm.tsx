'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { CheckCircle2, ArrowLeft, ArrowRight, UploadCloud, ShieldCheck, MailCheck } from 'lucide-react';
import s from './cohort.module.css';

export const DOMAINS = [
  {
    id: 'AI Agent Development',
    title: 'AI Agent Development',
    desc: 'Autonomous multi-agent workflows, LangChain/LlamaIndex, Ollama, vector search & tool calling.',
    stack: 'Python, FastEmbed, pgvector, Next.js',
  },
  {
    id: 'Full Stack Development',
    title: 'Full Stack Development',
    desc: 'Production web apps, Next.js 16 App Router, React 19, TypeScript, PostgreSQL, state machines.',
    stack: 'Next.js, React 19, TypeScript, PostgreSQL',
  },
  {
    id: 'Python Automation',
    title: 'Python Automation',
    desc: 'Data scraping, backend orchestration, headless browsers, automated report engines, CI/CD bots.',
    stack: 'Python 3.12, Playwright, Celery, Redis',
  },
  {
    id: 'Data Analytics',
    title: 'Data Analytics',
    desc: 'Business intelligence dashboards, cohort metrics, SQL modeling, executive reporting pipelines.',
    stack: 'Pandas, SQL, Metabase, PowerBI, DuckDB',
  },
  {
    id: 'Data Engineering / Machine Learning',
    title: 'Data Engineering / Machine Learning',
    desc: 'ETL pipelines, data warehousing, model fine-tuning, embeddings generation, inference serving.',
    stack: 'HuggingFace, PyTorch, Docker, Postgres, AWS',
  },
];

export default function AivaraCohortForm() {
  const [step, setStep] = useState<number>(1);
  const [loading, setLoading] = useState<boolean>(false);
  const [submittedId, setSubmittedId] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isHydrated, setIsHydrated] = useState<boolean>(false);

  const [formData, setFormData] = useState({
    // Step 1: Personal & Academics
    fullName: '',
    email: '',
    phone: '',
    city: '',
    state: '',
    college: '',
    degree: '',
    graduationYear: '2026',
    cgpaOrPercentage: '',

    // Step 2: Track & Web Presence
    domain: DOMAINS[0].id,
    cvUrl: '',
    linkedinUrl: '',
    githubUrl: '',
    portfolioUrl: '',

    // Step 3: Background & Consents
    familyBackground: '',
    motivation: '',
    availability: 'Immediate',
    termsConsent: false,
    newsletterConsent: true,
  });

  // Restore draft from sessionStorage
  /* eslint-disable react-hooks/set-state-in-effect */
  useEffect(() => {
    try {
      const saved = sessionStorage.getItem('aivara_cohort_draft');
      const savedStep = sessionStorage.getItem('aivara_cohort_step');
      if (saved) {
        setFormData(prev => ({ ...prev, ...JSON.parse(saved) }));
      }
      if (savedStep) {
        const stepNum = parseInt(savedStep, 10);
        if (stepNum >= 1 && stepNum <= 3) setStep(stepNum);
      }
    } catch {
      // Ignore storage read errors
    }
    setIsHydrated(true);
  }, []);
  /* eslint-enable react-hooks/set-state-in-effect */

  // Sync draft to sessionStorage
  useEffect(() => {
    if (isHydrated && !submittedId) {
      try {
        sessionStorage.setItem('aivara_cohort_draft', JSON.stringify(formData));
        sessionStorage.setItem('aivara_cohort_step', String(step));
      } catch {
        // Ignore storage write errors
      }
    }
  }, [formData, step, isHydrated, submittedId]);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
  ) => {
    const { name, value, type } = e.target;
    if (type === 'checkbox') {
      const checked = (e.target as HTMLInputElement).checked;
      setFormData(prev => ({ ...prev, [name]: checked }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
  };

  const validateStep1 = (): boolean => {
    if (!formData.fullName.trim()) {
      setErrorMessage('Full name is required.');
      return false;
    }
    if (!formData.email.trim() || !formData.email.includes('@')) {
      setErrorMessage('A valid email address is required.');
      return false;
    }
    const cleanPhone = formData.phone.replace(/[\s+-]/g, '');
    if (cleanPhone.length < 10) {
      setErrorMessage('Please enter a valid 10-digit phone/WhatsApp number.');
      return false;
    }
    if (!formData.city.trim()) {
      setErrorMessage('City is required.');
      return false;
    }
    if (!formData.state.trim()) {
      setErrorMessage('State is required.');
      return false;
    }
    if (!formData.college.trim()) {
      setErrorMessage('College / University name is required.');
      return false;
    }
    if (!formData.degree.trim()) {
      setErrorMessage('Degree and branch/specialization are required.');
      return false;
    }
    if (!formData.graduationYear.trim()) {
      setErrorMessage('Graduation year is required.');
      return false;
    }
    setErrorMessage(null);
    return true;
  };

  const validateStep2 = (): boolean => {
    if (!formData.domain) {
      setErrorMessage('Please select one of the 5 internship tracks.');
      return false;
    }
    if (!formData.cvUrl.trim()) {
      setErrorMessage('CV / Resume link is required.');
      return false;
    }
    if (!formData.cvUrl.startsWith('http://') && !formData.cvUrl.startsWith('https://')) {
      setErrorMessage('CV link must be a valid URL starting with http:// or https://');
      return false;
    }
    setErrorMessage(null);
    return true;
  };

  const validateStep3 = (): boolean => {
    if (!formData.familyBackground.trim() || formData.familyBackground.trim().length < 10) {
      setErrorMessage('Please tell us briefly about your family background (parents\' occupation / household background).');
      return false;
    }
    if (!formData.termsConsent) {
      setErrorMessage('You must accept the Terms and Conditions to proceed.');
      return false;
    }
    setErrorMessage(null);
    return true;
  };

  const handleNext = (e: React.FormEvent) => {
    e.preventDefault();
    if (step === 1) {
      if (validateStep1()) setStep(2);
    } else if (step === 2) {
      if (validateStep2()) setStep(3);
    }
  };

  const handleBack = () => {
    setErrorMessage(null);
    if (step > 1) setStep(prev => prev - 1);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateStep3()) return;

    setLoading(true);
    setErrorMessage(null);

    try {
      const res = await fetch('/api/cohorts/apply', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || 'Failed to submit application. Please check your fields.');
      }

      setSubmittedId(data.id);
      try {
        sessionStorage.removeItem('aivara_cohort_draft');
        sessionStorage.removeItem('aivara_cohort_step');
      } catch {
        // Ignore
      }
    } catch (err) {
      setErrorMessage(err instanceof Error ? err.message : 'An unexpected error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Success Confirmation Screen
  if (submittedId) {
    return (
      <div className={s.formContainer}>
        <div className={`${s.formCard} ${s.successPanel}`}>
          <div className={s.successIcon}>
            <CheckCircle2 size={36} />
          </div>
          <h2>Application Received!</h2>
          <p>
            Thank you, <strong>{formData.fullName}</strong>. Your application for the{' '}
            <strong>{formData.domain}</strong> track in the Aivara Technologies Hiring Cohort has been successfully registered.
          </p>
          <div className={s.refBadge}>
            Application Reference ID: {submittedId}
          </div>
          <p className={s.helperText}>
            Our admissions board and technical review mentors will review your application, academic background, and CV.
            You will receive an official decision email regarding your status.
          </p>
          <div style={{ marginTop: '20px', display: 'flex', gap: '12px' }}>
            <Link href="/" className="btn btn-outline">
              Return to DBERT Home
            </Link>
            <Link href="/about/contact" className="btn btn-primary">
              Have Questions? Contact Us
            </Link>
          </div>
        </div>
      </div>
    );
  }

  // Calculate progress line fill percentage: step 1 = 0%, step 2 = 50%, step 3 = 100%
  const progressFill = step === 1 ? '0%' : step === 2 ? '40%' : '80%';

  return (
    <div className={s.formContainer}>
      <div className={`${s.formCard} ${s.successPanel}`} style={{ textAlign: 'center', padding: '48px 32px' }}>
        <div className={s.successIcon} style={{ background: 'rgba(139, 92, 246, 0.15)', color: 'var(--brand-purple)', margin: '0 auto 20px' }}>
          <ShieldCheck size={40} />
        </div>
        <h2 style={{ fontSize: '1.75rem', fontWeight: 700, marginBottom: '12px' }}>Aivara Cohort Applications Moved</h2>
        <p style={{ maxWidth: '580px', margin: '0 auto 24px', color: 'var(--text-muted)', lineHeight: '1.6' }}>
          All Aivara Technologies hiring cohort applications, track selections, and mentor assignments are now managed through the official <strong>DBERT Internship &amp; Learning Platform</strong>.
        </p>
        <div style={{ display: 'flex', justifyContent: 'center', gap: '16px', flexWrap: 'wrap' }}>
          <a href="https://internship.dbert.online/apply?cohort=aivara" className="btn btn-primary" style={{ padding: '14px 28px', fontSize: '1rem', fontWeight: 600 }}>
            Apply for Aivara Cohort on DBERT Platform &rarr;
          </a>
        </div>
      </div>
    </div>
  );
}
