import React from 'react';
import Link from 'next/link';
import { Rocket } from 'lucide-react';
import s from './PricingNotice.module.css';

export default function PricingNotice() {
  return (
    <div className={`card ${s.panel}`}>
      <h2 className={s.title}>
        Custom Enterprise Pricing
      </h2>
      <p className={s.copy}>
        Deployed privately to your AWS/GCP VPC. Pricing scales with token volume and active users. Fill out the form below to request a tailored quote and live demo.
      </p>
      
      <div className={s.founderNote}>
        <span className="icon-chip"><Rocket aria-hidden="true" /></span>
        <span className={s.founderCopy}>
          Are you an early-stage founder? Incubated startups receive free tier access to this product.{' '}
          <Link href="/startups/register" className={s.founderLink}>Apply for Incubation →</Link>
        </span>
      </div>
    </div>
  );
}
