'use client';

import React, { useState } from 'react';
import { CircleCheck } from 'lucide-react';
import f from './forms.module.css';
import styles from './MultiStepForm.module.css'; // Reuse existing form styles

export default function ContactForm({ sourcePage = '/about/contact' }: { sourcePage?: string }) {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    subject: '',
    message: '',
    sourcePage: sourcePage
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
      const res = await fetch('/api/contact', {
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
            w.gtag('event', 'contact_form_submit', {
              source_page: formData.sourcePage
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
        <span className="icon-chip"><CircleCheck aria-hidden="true" /></span>
        <h2 className="card-title">Message Sent!</h2>
        <p className={f.hint}>
          Thank you for reaching out. A member of the DBERT team will get back to you shortly.
        </p>
        <button onClick={() => setSuccess(false)} className="btn btn-outline btn-sm">Send Another Message</button>
      </div>
    );
  }

  return (
    <div className={`${styles.formContainer} ${f.narrowForm}`}>
      <form className="card" onSubmit={handleSubmit}>
        <h2 className={`${styles.stepTitle} ${f.field}`}>Send us a message</h2>
        
        {errorMsg && <div className={styles.errorAlert}>{errorMsg}</div>}

        <div className={styles.fieldGroup}>
          <label>Full Name *</label>
          <input type="text" name="name" required value={formData.name} onChange={handleInputChange} placeholder="Your name" />
        </div>
        <div className={styles.fieldGroup}>
          <label>Email Address *</label>
          <input type="email" name="email" required value={formData.email} onChange={handleInputChange} placeholder="you@example.com" />
        </div>
        <div className={styles.fieldGroup}>
          <label>Phone / WhatsApp (Optional)</label>
          <input type="tel" name="phone" value={formData.phone} onChange={handleInputChange} placeholder="Your contact number" />
        </div>
        <div className={styles.fieldGroup}>
          <label>Subject *</label>
          <input type="text" name="subject" required value={formData.subject} onChange={handleInputChange} placeholder="How can we help you?" />
        </div>
        <div className={styles.fieldGroup}>
          <label>Message *</label>
          <textarea name="message" required value={formData.message} onChange={handleInputChange} placeholder="Your message here..." rows={5} />
        </div>

        <div className={`${styles.formNav} ${f.spacedTop}`}>
          <button type="submit" className={`btn btn-primary ${f.full}`} disabled={loading}>
            {loading ? 'Sending...' : 'Send Message'}
          </button>
        </div>
      </form>
    </div>
  );
}
