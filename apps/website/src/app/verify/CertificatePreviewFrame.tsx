'use client';

import React, { useState } from 'react';
import s from './verify.module.css';

interface Props {
  src: string;
  alt: string;
  holderName: string;
  certId?: string;
  domain?: string;
  isLocked?: boolean;
}

export default function CertificatePreviewFrame({
  src,
  alt,
  holderName,
  certId,
  domain,
  isLocked,
}: Props) {
  const [imgError, setImgError] = useState(false);

  const preventAction = (e: React.SyntheticEvent) => {
    e.preventDefault();
    e.stopPropagation();
    return false;
  };

  return (
    <div
      className={`${s.certFrame} ${isLocked ? s.certFrameLocked : ''}`}
      title={isLocked ? 'Certificate Locked — Form Submission Required' : `Official Certificate for ${holderName}`}
      onContextMenu={preventAction}
      onDragStart={preventAction}
    >
      {/* Invisible glass shield capturing pointer interactions and right-clicks */}
      <div
        className={s.certShield}
        onContextMenu={preventAction}
        onDragStart={preventAction}
        aria-hidden="true"
      />

      {!imgError ? (
        /* eslint-disable-next-line @next/next/no-img-element */
        <img
          src={src}
          alt={alt}
          className={`${s.certImg} ${isLocked ? s.certImgBlurred : ''}`}
          onError={() => setImgError(true)}
          onContextMenu={preventAction}
          onDragStart={preventAction}
          draggable={false}
        />
      ) : (
        /* Robust Fallback Credential Canvas (Never renders a broken browser icon) */
        <div className={s.certFallbackCanvas}>
          <div className={s.fallbackBorder}>
            <div className={s.fallbackHeader}>
              <span className={s.fallbackLogoMark}>D</span>
              <div className={s.fallbackOrg}>DBERT SOVEREIGN REGISTRY</div>
            </div>
            <div className={s.fallbackTitle}>CERTIFICATE OF COMPLETION</div>
            <div className={s.fallbackHolder}>{holderName}</div>
            <div className={s.fallbackTrack}>{domain || 'Technical Incubation Track'}</div>
            <div className={s.fallbackMeta}>
              <span>ID: {certId || 'CERT-DBERT-2026'}</span>
              <span>&bull;</span>
              <span>Tamper-Proof Registry</span>
            </div>
          </div>
        </div>
      )}

      {/* Elegant Translucent Frosted Glass Lock Overlay */}
      {isLocked && (
        <div className={s.lockedOverlayTranslucent}>
          <div className={s.lockedPadlockWrap}>
            <svg
              width="28"
              height="28"
              viewBox="0 0 24 24"
              fill="none"
              stroke="#fbbf24"
              strokeWidth="2.2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
              <path d="M7 11V7a5 5 0 0 1 10 0v4" />
            </svg>
          </div>
          <div className={s.lockedBadgeText}>CERTIFICATE LOCKED</div>
          <div className={s.lockedSubText}>
            Form Submission Required to Validate &amp; Release Stipend
          </div>
          <a
            href="https://docs.google.com/forms/d/e/1FAIpQLSeHCTK_HO5ZbNHNcPiyW-04Y4bBeZ0RvQP7I4koQnW91d6phA/viewform?usp=header"
            target="_blank"
            rel="noopener noreferrer"
            className={s.lockedUnlockBtn}
          >
            Complete Form to Unlock &rarr;
          </a>
        </div>
      )}
    </div>
  );
}
