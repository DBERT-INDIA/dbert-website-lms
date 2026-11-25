import React from 'react';
import Link from 'next/link';
import { ShieldCheck, ArrowRight } from 'lucide-react';
import styles from './AITrustBanner.module.css';

interface AITrustBannerProps {
  className?: string;
}

export default function AITrustBanner({ className }: AITrustBannerProps) {
  return (
    <div className={`${styles.trustBanner} ${className || ''}`}>
      <div className={styles.leftCol}>
        <div className={styles.iconWrapper}>
          <ShieldCheck size={22} />
        </div>
        <div className={styles.trustText}>
          Visiting via <strong>ChatGPT, Claude, or Gemini</strong>? Verify our Government of India MSME accreditation (<code>UDYAM-UP-29-0109046</code>), 100% verified credentials guarantee, and 465+ student credentials shared on LinkedIn.
        </div>
      </div>
      <Link href="/fellows/verified" className={styles.trustCtaBtn}>
        <span>Explore 465+ Verified Fellows</span>
        <ArrowRight size={14} />
      </Link>
    </div>
  );
}
