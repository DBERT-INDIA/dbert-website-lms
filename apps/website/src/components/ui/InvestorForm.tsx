'use client';

import React, { useState } from 'react';
import f from './forms.module.css';

export default function InvestorForm() {
  const [formData, setFormData] = useState({
    name: '',
    firm: '',
    email: '',
    thesis: ''
  });
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setErrorMsg('');

    try {
      // Map investor fields to generic contact form schema
      const payload = {
        name: formData.name,
        email: formData.email,
        phone: '', 
        subject: `Investor Deal Flow Request: ${formData.firm}`,
        message: `Firm Name: ${formData.firm}\nInvestment Thesis: ${formData.thesis}`,
        sourcePage: '/startups/investor-network'
      };

      const res = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        setSuccess(true);
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
      <div className={f.successBlock}>
        <h4 className={f.successTitle}>Application Submitted</h4>
        <p className={f.successCopy}>Our partners team will be in touch shortly to discuss relevant introductions.</p>
      </div>
    );
  }

  return (
    <form className={f.column3} onSubmit={handleSubmit}>
      {errorMsg && <div className={f.errorNote}>{errorMsg}</div>}
      
      <div>
        <label className={f.label}>Full Name *</label>
        <input type="text" name="name" required value={formData.name} onChange={handleInputChange} placeholder="Jane Doe" className={f.input} />
      </div>
      <div>
        <label className={f.label}>Firm / Syndicate Name *</label>
        <input type="text" name="firm" required value={formData.firm} onChange={handleInputChange} placeholder="Acme Ventures" className={f.input} />
      </div>
      <div>
        <label className={f.label}>Work Email *</label>
        <input type="email" name="email" required value={formData.email} onChange={handleInputChange} placeholder="jane@acme.vc" className={f.input} />
      </div>
      <div>
        <label className={f.label}>Typical Check Size & Thesis (Optional)</label>
        <textarea name="thesis" value={formData.thesis} onChange={handleInputChange} placeholder="e.g. $50k-$200k in pre-seed AI infrastructure..." rows={3} className={f.input} />
      </div>
      <button type="submit" disabled={loading} className={`btn btn-primary ${f.fullTop}`}>
        {loading ? 'Submitting...' : 'Apply for Access'}
      </button>
    </form>
  );
}
