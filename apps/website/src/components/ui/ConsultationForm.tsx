'use client';

import React, { useState } from 'react';
import styles from './MultiStepForm.module.css';
import { Calendar } from 'lucide-react';
import f from './forms.module.css';

export default function ConsultationForm() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    companyName: '',
    companySize: '',
    serviceType: 'Discovery',
    description: '',
    preferredDate: ''
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
      const res = await fetch('/api/consultation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      if (res.ok) {
        setSuccess(true);
        try {
          const w = window as any;
          if (w.gtag) {
            w.gtag('event', 'consultation_form_submit', {
              service_type: formData.serviceType
            });
          }
        } catch (err) {}
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
        <span className="icon-chip"><Calendar aria-hidden="true" /></span>
        <h2 className="card-title">Consultation Requested!</h2>
        <p className={f.hint}>
          Thank you for reaching out. Our enterprise team will review your request and contact you to confirm the date and time.
        </p>
        <button onClick={() => setSuccess(false)} className="btn btn-outline btn-sm">Book Another</button>
      </div>
    );
  }

  return (
    <div className={`${styles.formContainer} ${f.narrowForm}`}>
      <form className="card" onSubmit={handleSubmit}>
        <h2 className={`${styles.stepTitle} ${f.field}`}>Request AI Consultation</h2>
        
        {errorMsg && <div className={styles.errorAlert}>{errorMsg}</div>}

        <div className={styles.fieldGroup}>
          <label>Full Name *</label>
          <input type="text" name="name" required value={formData.name} onChange={handleInputChange} placeholder="Your name" />
        </div>
        <div className={styles.fieldGroup}>
          <label>Email Address *</label>
          <input type="email" name="email" required value={formData.email} onChange={handleInputChange} placeholder="you@company.com" />
        </div>
        <div className={styles.fieldGroup}>
          <label>Phone Number *</label>
          <input type="tel" name="phone" required value={formData.phone} onChange={handleInputChange} placeholder="Contact number" />
        </div>
        
        <div className={styles.fieldGroup}>
          <label>Company Name</label>
          <input type="text" name="companyName" value={formData.companyName} onChange={handleInputChange} placeholder="e.g. Acme Corp" />
        </div>
        
        <div className={styles.fieldGroup}>
          <label>Company Size</label>
          <select name="companySize" value={formData.companySize} onChange={handleInputChange}>
            <option value="">Select size...</option>
            <option value="1-10">1-10 Employees</option>
            <option value="11-50">11-50 Employees</option>
            <option value="51-200">51-200 Employees</option>
            <option value="201-500">201-500 Employees</option>
            <option value="500+">500+ Employees</option>
          </select>
        </div>

        <div className={styles.fieldGroup}>
          <label>Service Type *</label>
          <select name="serviceType" value={formData.serviceType} onChange={handleInputChange} required>
            <option value="Discovery">Discovery & Strategy</option>
            <option value="Architecture">System Architecture</option>
            <option value="Implementation">Custom Implementation</option>
            <option value="Optimization">Model Optimization</option>
          </select>
        </div>

        <div className={styles.fieldGroup}>
          <label>Preferred Date</label>
          <input type="date" name="preferredDate" value={formData.preferredDate} onChange={handleInputChange} />
        </div>

        <div className={styles.fieldGroup}>
          <label>Project Description</label>
          <textarea name="description" value={formData.description} onChange={handleInputChange} placeholder="Briefly describe what you're looking to build or solve..." rows={4} />
        </div>

        <div className={`${styles.formNav} ${f.spacedTop}`}>
          <button type="submit" className={`btn btn-primary ${f.full}`} disabled={loading}>
            {loading ? 'Submitting...' : 'Request Consultation'}
          </button>
        </div>
      </form>
    </div>
  );
}
