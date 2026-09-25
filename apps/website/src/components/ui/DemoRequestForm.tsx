'use client';

import React, { useState } from 'react';
import { Rocket } from 'lucide-react';
import f from './forms.module.css';
import styles from './MultiStepForm.module.css'; // Reusing form styles

interface DemoRequestFormProps {
  productName: string;
}

export default function DemoRequestForm({ productName }: DemoRequestFormProps) {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    companyName: '',
    productName: productName,
    message: ''
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
      const res = await fetch('/api/demo-request', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      if (res.ok) {
        setSuccess(true);
        try {
          const w = window as any;
          if (w.gtag) {
            w.gtag('event', 'demo_request_submit', {
              product_name: productName
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
        <span className="icon-chip"><Rocket aria-hidden="true" /></span>
        <h2 className="card-title">Demo Requested!</h2>
        <p className={f.hint}>
          Thank you for your interest in {productName}. Our product team will be in touch shortly to schedule your personalized demo.
        </p>
      </div>
    );
  }

  return (
    <div className={`${styles.formContainer} ${f.narrowForm}`}>
      <form className="card" onSubmit={handleSubmit}>
        <h2 className={`${styles.stepTitle} ${f.field}`}>Request a Demo</h2>
        <p className={f.introCopy}>See how {productName} can streamline your workflows.</p>
        
        {errorMsg && <div className={styles.errorAlert}>{errorMsg}</div>}

        <div className={styles.fieldGroup}>
          <label>Full Name *</label>
          <input type="text" name="name" required value={formData.name} onChange={handleInputChange} placeholder="Your name" />
        </div>
        <div className={styles.fieldGroup}>
          <label>Work Email *</label>
          <input type="email" name="email" required value={formData.email} onChange={handleInputChange} placeholder="you@company.com" />
        </div>
        <div className={styles.fieldGroup}>
          <label>Phone Number</label>
          <input type="tel" name="phone" value={formData.phone} onChange={handleInputChange} placeholder="Contact number" />
        </div>
        <div className={styles.fieldGroup}>
          <label>Company Name</label>
          <input type="text" name="companyName" value={formData.companyName} onChange={handleInputChange} placeholder="e.g. Acme Corp" />
        </div>
        <div className={styles.fieldGroup}>
          <label>What are you looking to achieve? (Optional)</label>
          <textarea name="message" value={formData.message} onChange={handleInputChange} placeholder="Tell us about your use case..." rows={3} />
        </div>

        <div className={`${styles.formNav} ${f.spacedTop}`}>
          <button type="submit" className={`btn btn-primary ${f.full}`} disabled={loading}>
            {loading ? 'Submitting...' : 'Get a Demo'}
          </button>
        </div>
      </form>
    </div>
  );
}
