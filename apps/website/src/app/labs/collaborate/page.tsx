'use client';

import React, { useState } from 'react';
import styles from './collaborate.module.css';
import s from '../labs.module.css';
import f from '@/components/ui/forms.module.css';
import { CircleCheck } from 'lucide-react';

export default function LabsCollaboratePage() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    organization: '',
    organizationType: 'Academic',
    researchArea: 'Multi-Agent AI Systems',
    proposal: ''
  });

  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setErrorMsg('');

    try {
      const res = await fetch('/api/labs/collaborate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      if (res.ok) {
        setSuccess(true);
      } else {
        const data = await res.json();
        setErrorMsg(data.error || 'Failed to submit proposal. Please try again.');
      }
    } catch (err) {
      setErrorMsg('Network error. Please check your connection.');
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="container pad-block">
        <div className={`card ${s.successPanel}`}>
          <span className="icon-chip"><CircleCheck aria-hidden="true" /></span>
          <h2 className="card-title">Proposal Submitted!</h2>
          <p className={f.mutedCopy}>
            Thank you for reaching out to DBERT Labs. Our research alignment board will review your proposal and respond within 5 business days.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="container pad-block">
      <div className="mb-lg center">
        <div className="doclabel justify-center">
          § 01 — LABS PARTNERSHIP PROPOSAL <span className="rev">rev: 2026.2</span>
        </div>
        <h1>Labs Collaboration Proposal</h1>
        <p className="measure-sm">
          Submit your research proposal, open source partnership idea, or model validation plan.
        </p>
      </div>

      <div className="measure-sm">
        <form className="card" onSubmit={handleSubmit}>
          {errorMsg && <div className={styles.errorAlert}>{errorMsg}</div>}
          
          <div className={styles.fieldGroup}>
            <label>Full Name *</label>
            <input type="text" name="name" required value={formData.name} onChange={handleInputChange} placeholder="Your name" />
          </div>

          <div className={styles.fieldGroup}>
            <label>Email Address *</label>
            <input type="email" name="email" required value={formData.email} onChange={handleInputChange} placeholder="you@organization.edu" />
          </div>

          <div className={styles.fieldGroup}>
            <label>Organization / University *</label>
            <input type="text" name="organization" required value={formData.organization} onChange={handleInputChange} placeholder="Name of your institution" />
          </div>

          <div className={styles.fieldGroup}>
            <label>Organization Type</label>
            <select name="organizationType" value={formData.organizationType} onChange={handleInputChange}>
              <option value="Academic">Academic Institution</option>
              <option value="Industry">Industry partner</option>
              <option value="Independent Researcher">Independent Researcher</option>
              <option value="Other">Other</option>
            </select>
          </div>

          <div className={styles.fieldGroup}>
            <label>Primary Research Area</label>
            <select name="researchArea" value={formData.researchArea} onChange={handleInputChange}>
              <option value="Multi-Agent AI Systems">Multi-Agent AI Systems</option>
              <option value="LLM Optimization & Compressions">LLM Optimization &amp; Compressions</option>
              <option value="Educational AI Technologies">Educational AI Technologies</option>
              <option value="Trading Algorithm Research">Trading Algorithm Research</option>
            </select>
          </div>

          <div className={styles.fieldGroup}>
            <label>Proposal / Project Description *</label>
            <textarea name="proposal" required value={formData.proposal} onChange={handleInputChange} placeholder="Outline research scope, goals, and how DBERT Labs can collaborate..." />
          </div>

          <button type="submit" className={`btn btn-primary btn-sm ${s.submitBtn}`} disabled={loading}>
            {loading ? 'Submitting Proposal...' : 'Submit Proposal'}
          </button>
        </form>
      </div>
    </div>
  );
}
