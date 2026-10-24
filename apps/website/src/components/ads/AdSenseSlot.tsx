'use client';

import React from 'react';
import styles from './AdSenseSlot.module.css';

export interface AdSenseSlotProps {
  slotId?: string;
  format?: 'auto' | 'rectangle' | 'horizontal';
  responsive?: boolean;
  className?: string;
}

export default function AdSenseSlot({
  slotId = '0000000000',
  format = 'auto',
  responsive = true,
  className = '',
}: AdSenseSlotProps) {
  return (
    <aside className={`${styles.adContainer} ${className}`} aria-label="Sponsored Industry Partner">
      <div className={styles.adHeader}>
        <span className={styles.adTag}>SPONSORED · VERIFIED DEEPTECH PARTNER</span>
        <span className={styles.adPolicy}>Google AdSense</span>
      </div>
      <div className={styles.adBody}>
        {/* Responsive ad container styled to Option A dark foundry surface */}
        <ins
          className="adsbygoogle"
          style={{ display: 'block', minHeight: '90px', width: '100%' }}
          data-ad-client="ca-pub-0000000000000000"
          data-ad-slot={slotId}
          data-ad-format={format}
          data-full-width-responsive={responsive ? 'true' : 'false'}
        />
        <div className={styles.adNotice}>
          <span>Enterprise AI Systems &bull; Developer Infrastructure &bull; Career Resources</span>
        </div>
      </div>
    </aside>
  );
}
