'use client';

import React, { useState, useEffect, Suspense, useCallback } from 'react';
import { useSearchParams } from 'next/navigation';
import HandNote from '@/components/ui/HandNote';
import s from './verify.module.css';

interface VerificationResult {
  holderName: string;
  programName: string;
  domain?: string;
  issueDate: string;
  verified: boolean;
}

function VerifyFormContent() {
  const searchParams = useSearchParams();
  const initialCertId = searchParams.get('certId') || searchParams.get('id') || '';
  const [certId, setCertId] = useState(initialCertId);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<VerificationResult | null>(null);
  const [errorMsg, setErrorMsg] = useState('');

  const executeVerify = useCallback(async (idToVerify: string) => {
    if (!idToVerify.trim()) return;

    setLoading(true);
    setErrorMsg('');
    setResult(null);

    try {
      const res = await fetch(`/api/verify?certId=${encodeURIComponent(idToVerify.trim())}`);
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
    } catch {
      setErrorMsg('Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  }, []);

  /* eslint-disable react-hooks/set-state-in-effect -- Auto-verify certificate on mount when arriving via QR code or direct URL parameter */
  useEffect(() => {
    if (initialCertId) {
      executeVerify(initialCertId);
    }
  }, [initialCertId, executeVerify]);
  /* eslint-enable react-hooks/set-state-in-effect */

  const handleVerify = (e: React.FormEvent) => {
    e.preventDefault();
    executeVerify(certId);
  };

  return (
    <>
      <form className={`card card-lift ${s.form}`} onSubmit={handleVerify}>
        <div className={s.fieldGroup}>
          <label htmlFor="cert-id">Certificate ID *</label>
          <input 
            id="cert-id"
            name="certId"
            aria-label="Certificate ID"
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

      {errorMsg && <div className={s.errorAlert}>{errorMsg}</div>}

      {result && (
        <div className={`card card-lift ${s.validCard}`}>
          <h2 className={s.validTitle}>Valid Certificate</h2>
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
    </>
  );
}

export default function CertificateVerifyPage() {
  return (
    <div className="container pad-block">
      <div className="mb-lg center">
        <div className="doclabel justify-center">
          § 01 — CRYPTOGRAPHIC VERIFICATION <span className="rev">rev: 2026.2</span>
        </div>
        <div className="stack-h justify-center align-baseline gap-3 flex-wrap mb-2">
          <h1>Verify Certificate</h1>
          <HandNote tone="blue">
            tamper-proof · on-chain hashes ✍
          </HandNote>
        </div>
        <p className="measure-sm">
          Enter a certificate identification key to verify student credentials, completion statuses, and MSME registrations.
        </p>
      </div>

      <div className={s.shell}>
        <Suspense fallback={
          <div className="card card-lift text-center p-6 text-muted">
            Loading verification console...
          </div>
        }>
          <VerifyFormContent />
        </Suspense>
      </div>
    </div>
  );
}

