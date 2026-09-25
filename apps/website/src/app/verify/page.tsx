'use client';

import s from './verify.module.css';

import React, { useState } from 'react';
import styles from './verify.module.css';

interface VerificationResult {
  holderName: string;
  programName: string;
  domain?: string;
  issueDate: string;
  verified: boolean;
}

export default function CertificateVerifyPage() {
  const [certId, setCertId] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<VerificationResult | null>(null);
  const [errorMsg, setErrorMsg] = useState('');

  const handleVerify = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!certId) return;

    setLoading(true);
    setErrorMsg('');
    setResult(null);

    try {
      const res = await fetch(`/api/verify?certId=${encodeURIComponent(certId)}`);
      if (res.ok) {
        const data = await res.json();
        if (data.verified) {
          setResult(data);
        } else {
          setErrorMsg('Certificate ID not found or invalid.');
        }
      } else {
        setErrorMsg('Verification failed. Please check ID format.');
      }
    } catch (err) {
      setErrorMsg('Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container pad-block">
      <div className="mb-lg center">
        <div className="doclabel justify-center">
          § 01 — CRYPTOGRAPHIC VERIFICATION <span className="rev">rev: 2026.2</span>
        </div>
        <h1>Verify Certificate</h1>
        <p className="measure-sm">
          Enter a certificate identification key to verify student credentials, completion statuses, and MSME registrations.
        </p>
      </div>

      <div className={s.shell}>
        <form className={`card ${s.form}`} onSubmit={handleVerify}>
          <div className={styles.fieldGroup}>
            <label>Certificate ID *</label>
            <input 
              type="text" 
              required 
              value={certId} 
              onChange={(e) => setCertId(e.target.value)} 
              placeholder="e.g. DBERT-2026-001" 
            />
          </div>
          <button type="submit" className={`btn btn-primary btn-sm ${s.submit}`} disabled={loading}>
            {loading ? 'Verifying...' : 'Verify Certificate'}
          </button>
        </form>

        {errorMsg && <div className={styles.errorAlert}>{errorMsg}</div>}

        {result && (
          <div className={`card ${s.validCard}`}>
            <h3 className={s.validTitle}>Valid Certificate</h3>
            <div className={s.details}>
              <div><strong>Holder:</strong> {result.holderName}</div>
              <div><strong>Program:</strong> {result.programName}</div>
              {result.domain && <div><strong>Domain:</strong> {result.domain}</div>}
              <div><strong>Issue Date:</strong> {new Date(result.issueDate).toLocaleDateString()}</div>
              <div className={s.issuer}>
                Issued by Digital Blinc Education Research And Technology (MSME Registered)
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
