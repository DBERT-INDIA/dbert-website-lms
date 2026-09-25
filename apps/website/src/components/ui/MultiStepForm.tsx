'use client';

import React, { useState, useEffect } from 'react';
import styles from './MultiStepForm.module.css';
import { CircleCheck } from 'lucide-react';
import f from './forms.module.css';
import Link from 'next/link';

export default function StartupRegisterForm() {
  const [step, setStep] = useState<number>(1);
  const [formData, setFormData] = useState({
    startupName: '',
    founderName: '',
    email: '',
    phone: '',
    city: '',
    stage: 'Idea',
    domain: 'AI Agent Development',
    teamSize: '1-5',
    currentFunding: 'Bootstrapped',
    servicesNeeded: [] as string[],
    description: '',
    challengeStmt: '',
    consent: false
  });
  
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [isHydrated, setIsHydrated] = useState(false);

  // Restoring a part-completed form from sessionStorage is exactly the
  // "subscribe to an external system on mount" case the rule's own docs allow;
  // it cannot move into a useState initialiser without breaking SSR hydration,
  // and React batches these three updates into a single render anyway.
  /* eslint-disable react-hooks/set-state-in-effect -- see note above */
  useEffect(() => {
    const savedData = sessionStorage.getItem('dbert_startup_form');
    const savedStep = sessionStorage.getItem('dbert_startup_step');
    if (savedData) {
      try {
        setFormData(JSON.parse(savedData));
      } catch (e) {}
    }
    if (savedStep) {
      setStep(parseInt(savedStep, 10));
    }
    setIsHydrated(true);
  }, []);
  /* eslint-enable react-hooks/set-state-in-effect */

  useEffect(() => {
    if (isHydrated) {
      sessionStorage.setItem('dbert_startup_form', JSON.stringify(formData));
      sessionStorage.setItem('dbert_startup_step', step.toString());
    }
  }, [formData, step, isHydrated]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleCheckboxChange = (service: string) => {
    setFormData(prev => {
      const services = prev.servicesNeeded.includes(service)
        ? prev.servicesNeeded.filter(s => s !== service)
        : [...prev.servicesNeeded, service];
      return { ...prev, servicesNeeded: services };
    });
  };

  const handleNext = (e: React.FormEvent) => {
    e.preventDefault();
    if (step < 4) setStep(prev => prev + 1);
  };

  const handleBack = () => {
    if (step > 1) setStep(prev => prev - 1);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.consent) {
      setErrorMsg('Please agree to terms and conditions.');
      return;
    }

    setLoading(true);
    setErrorMsg('');

    try {
      const res = await fetch('/api/startups/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      if (res.ok) {
        setSuccess(true);
        // Trigger GA4 event if tracking helper is available
        try {
          const w = window as any;
          if (w.gtag) {
            w.gtag('event', 'startup_register_submit', {
              startup_stage: formData.stage,
              domain: formData.domain
            });
          }
        } catch (err) {}
        sessionStorage.removeItem('dbert_startup_form');
        sessionStorage.removeItem('dbert_startup_step');
      } else {
        const data = await res.json();
        setErrorMsg(data.error || 'Something went wrong. Please try again.');
      }
    } catch (err) {
      setErrorMsg('Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className={`card ${f.statePanel}`}>
        <span className="icon-chip"><CircleCheck aria-hidden="true" /></span>
        <h2 className="card-title">Registration Submitted!</h2>
        <p className={f.hint}>
          Thank you for applying. Our incubation advisory board will review your profile and contact you within 3 business days.
        </p>
        <Link href="/" className="btn btn-primary">Return to Homepage</Link>
      </div>
    );
  }

  return (
    <div className={styles.formContainer}>
      <div className={styles.stepsIndicator}>
        {[1, 2, 3, 4].map(s => (
          <div key={s} className={`${styles.stepDot} ${step >= s ? styles.activeDot : ''}`}>
            <span>{s}</span>
          </div>
        ))}
      </div>

      <form className="card" onSubmit={step === 4 ? handleSubmit : handleNext}>
        {errorMsg && <div className={styles.errorAlert}>{errorMsg}</div>}

        {step === 1 && (
          <div className={styles.formStep}>
            <h2 className={styles.stepTitle}>Step 1: Contact Information</h2>
            <div className={styles.fieldGroup}>
              <label>Startup Name *</label>
              <input type="text" name="startupName" required value={formData.startupName} onChange={handleInputChange} placeholder="e.g. Acme AI" />
            </div>
            <div className={styles.fieldGroup}>
              <label>Founder Name *</label>
              <input type="text" name="founderName" required value={formData.founderName} onChange={handleInputChange} placeholder="Your name" />
            </div>
            <div className={styles.fieldGroup}>
              <label>Email Address *</label>
              <input type="email" name="email" required value={formData.email} onChange={handleInputChange} placeholder="you@dbert.online" />
            </div>
            <div className={styles.fieldGroup}>
              <label>Phone / WhatsApp * (10 digits)</label>
              <input type="tel" name="phone" required pattern="[0-9]{10}" title="Please enter a valid 10-digit phone number" value={formData.phone} onChange={handleInputChange} placeholder="10 digit mobile" />
            </div>
            <div className={styles.fieldGroup}>
              <label>City *</label>
              <input type="text" name="city" required value={formData.city} onChange={handleInputChange} placeholder="Ghaziabad" />
            </div>
          </div>
        )}

        {step === 2 && (
          <div className={styles.formStep}>
            <h2 className={styles.stepTitle}>Step 2: Startup Metrics</h2>
            <div className={styles.fieldGroup}>
              <label>Current Stage</label>
              <select name="stage" value={formData.stage} onChange={handleInputChange}>
                <option value="Idea">Idea / Pre-MVP</option>
                <option value="MVP">MVP Ready</option>
                <option value="Early Revenue">Early Revenue</option>
                <option value="Scaling">Scaling / Growth</option>
              </select>
            </div>
            <div className={styles.fieldGroup}>
              <label>Primary Domain</label>
              <select name="domain" value={formData.domain} onChange={handleInputChange}>
                <option value="AI Agent Development">AI Agent Development</option>
                <option value="Full Stack Development">Full Stack Development</option>
                <option value="Python Automation">Python Automation</option>
                <option value="Data Analytics">Data Analytics</option>
              </select>
            </div>
            <div className={styles.fieldGroup}>
              <label>Team Size</label>
              <select name="teamSize" value={formData.teamSize} onChange={handleInputChange}>
                <option value="1-5">1-5 Members</option>
                <option value="6-15">6-15 Members</option>
                <option value="16-30">16-30 Members</option>
                <option value="30+">30+ Members</option>
              </select>
            </div>
            <div className={styles.fieldGroup}>
              <label>Current Funding Status</label>
              <select name="currentFunding" value={formData.currentFunding} onChange={handleInputChange}>
                <option value="Bootstrapped">Bootstrapped</option>
                <option value="Pre-Seed">Pre-Seed / Angel</option>
                <option value="Seed Funded">Seed Funded</option>
                <option value="Series A+">Series A+</option>
              </select>
            </div>
          </div>
        )}

        {step === 3 && (
          <div className={styles.formStep}>
            <h2 className={styles.stepTitle}>Step 3: Incubation Services Needed</h2>
            <div className={styles.checkboxContainer}>
              {[
                { name: 'Technical Assistance', value: 'technical' },
                { name: 'Hiring Assistance', value: 'hiring' },
                { name: 'Seed Funding support', value: 'funding' },
                { name: 'Services Against Equity', value: 'equity' },
                { name: 'Legal & Compliance', value: 'legal' },
                { name: 'AI/ML Infrastructure Setup', value: 'infrastructure' }
              ].map(service => (
                <label key={service.value} className={styles.checkboxLabel}>
                  <input
                    type="checkbox"
                    checked={formData.servicesNeeded.includes(service.name)}
                    onChange={() => handleCheckboxChange(service.name)}
                  />
                  <span>{service.name}</span>
                </label>
              ))}
            </div>
            <div className={`${styles.fieldGroup} ${f.spacedTop3}`}>
              <label>Describe your project *</label>
              <textarea name="description" required value={formData.description} onChange={handleInputChange} placeholder="Tell us about your startup idea..." />
            </div>
          </div>
        )}

        {step === 4 && (
          <div className={styles.formStep}>
            <h2 className={styles.stepTitle}>Step 4: Final Validation</h2>
            <div className={styles.fieldGroup}>
              <label>What is your biggest technical challenge? *</label>
              <textarea name="challengeStmt" required value={formData.challengeStmt} onChange={handleInputChange} placeholder="Tell us what bottlenecks you want DBERT to solve..." />
            </div>
            <label className={styles.consentCheckbox}>
              <input
                type="checkbox"
                required
                checked={formData.consent}
                onChange={(e) => setFormData(prev => ({ ...prev, consent: e.target.checked }))}
              />
              <span>I confirm all startup validation metrics provided are correct and agree to standard incubation terms. *</span>
            </label>
          </div>
        )}

        <div className={styles.formNav}>
          {step > 1 && (
            <button type="button" onClick={handleBack} className="btn btn-outline btn-sm">
              Back
            </button>
          )}
          <button type="submit" className={`btn btn-primary btn-sm ${f.pushRight}`} disabled={loading}>
            {loading ? 'Submitting...' : step === 4 ? 'Apply for Incubation' : 'Next Step'}
          </button>
        </div>
      </form>
    </div>
  );
}
