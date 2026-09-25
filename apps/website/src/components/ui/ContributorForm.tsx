'use client';

import React, { useState } from 'react';
import { CircleCheck } from 'lucide-react';
import f from './forms.module.css';
import styles from './MultiStepForm.module.css'; // Reuse existing form styles

const DOMAIN_OPTIONS = [
  'AI Agent Development',
  'Full Stack Development',
  'Python Automation',
  'Data Analytics',
  'Data Engineering / Quant Research',
];

const MAX_COMMENT_LENGTH = 500;

export default function ContributorForm() {
  const [expanded, setExpanded] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    profilePicUrl: '',
    comment: '',
    linkedinUrl: '',
    githubUrl: '',
    domain: DOMAIN_OPTIONS[0],
  });

  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setErrorMsg('');

    try {
      const res = await fetch('/api/alkame/contributors', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
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

  if (!expanded) {
    return (
      <div className={f.centerBlock}>
        <button onClick={() => setExpanded(true)} className="btn btn-outline btn-lg">
          Currently working on this project? Add yourself →
        </button>
      </div>
    );
  }

  if (success) {
    return (
      <div className={`card ${f.panel}`}>
        <span className="icon-chip"><CircleCheck aria-hidden="true" /></span>
        <h2 className="card-title">Submitted for Review</h2>
        <p className={f.mutedCopy}>
          Thanks — your contribution will appear on this page once a DBERT admin reviews and approves it.
        </p>
      </div>
    );
  }

  return (
    <div className={`${styles.formContainer} ${f.formShell}`}>
      <form className="card" onSubmit={handleSubmit}>
        <h2 className={`${styles.stepTitle} ${f.field}`}>Join as a Contributor</h2>
        <p className={f.introCopySm}>
          Currently interning on Alkame-Nifty50? Submit your details below — your card goes live after
          a quick admin review. Your email is only used internally and is never shown publicly.
        </p>

        {errorMsg && <div className={styles.errorAlert}>{errorMsg}</div>}

        <div className={styles.fieldGroup}>
          <label>Full Name *</label>
          <input type="text" name="name" required value={formData.name} onChange={handleInputChange} placeholder="Your name" />
        </div>
        <div className={styles.fieldGroup}>
          <label>Email Address * (not shown publicly)</label>
          <input type="email" name="email" required value={formData.email} onChange={handleInputChange} placeholder="you@example.com" />
        </div>
        <div className={styles.fieldGroup}>
          <label>Profile Picture URL *</label>
          <input type="url" name="profilePicUrl" required value={formData.profilePicUrl} onChange={handleInputChange} placeholder="https://..." />
        </div>
        <div className={styles.fieldGroup}>
          <label>LinkedIn URL *</label>
          <input type="url" name="linkedinUrl" required value={formData.linkedinUrl} onChange={handleInputChange} placeholder="https://linkedin.com/in/..." />
        </div>
        <div className={styles.fieldGroup}>
          <label>GitHub URL *</label>
          <input type="url" name="githubUrl" required value={formData.githubUrl} onChange={handleInputChange} placeholder="https://github.com/..." />
        </div>
        <div className={styles.fieldGroup}>
          <label>Domain of Internship *</label>
          <select name="domain" required value={formData.domain} onChange={handleInputChange}>
            {DOMAIN_OPTIONS.map((option) => (
              <option key={option} value={option}>{option}</option>
            ))}
          </select>
        </div>
        <div className={styles.fieldGroup}>
          <label>Comment * ({formData.comment.length}/{MAX_COMMENT_LENGTH})</label>
          <textarea
            name="comment"
            required
            maxLength={MAX_COMMENT_LENGTH}
            value={formData.comment}
            onChange={handleInputChange}
            placeholder="What are you working on for Alkame?"
            rows={4}
          />
        </div>

        <div className={`${styles.formNav} ${f.navRow}`}>
          <button type="button" onClick={() => setExpanded(false)} className={`btn btn-outline ${f.flex1}`}>
            Cancel
          </button>
          <button type="submit" className={`btn btn-primary ${f.flex2}`} disabled={loading}>
            {loading ? 'Submitting...' : 'Submit for Review'}
          </button>
        </div>
      </form>
    </div>
  );
}
