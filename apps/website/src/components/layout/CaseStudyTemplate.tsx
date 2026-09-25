import React from 'react';
import Image from 'next/image';
import f from '../ui/forms.module.css';
import s from './CaseStudyTemplate.module.css';

interface CaseStudyTemplateProps {
  logoText: string;
  logoSrc?: string;
  name: string;
  externalLink: string;
  challenge: string;
  contribution: string;
  outcome: string;
  metrics?: string;
}

export default function CaseStudyTemplate({
  logoText,
  logoSrc,
  name,
  externalLink,
  challenge,
  contribution,
  outcome,
  metrics
}: CaseStudyTemplateProps) {
  return (
    <div className="container pad-block">
      <div className={s.head}>
        {logoSrc && (
          <div className={s.logoFrame}>
            <Image src={logoSrc} alt={`${name} Logo`} fill className={s.logoImg} />
          </div>
        )}
        <div className="doclabel">
          § 01 — CASE STUDY STUDY ANALYSIS <span className="rev">rev: 2026.2</span>
        </div>
        <h1>{name}</h1>
        <p>
          <a href={externalLink} target="_blank" rel="noopener noreferrer" className={s.siteLink}>
            Visit Website ({logoText}) ↗
          </a>
        </p>
      </div>

      <div className={s.body}>
        <section className="card">
          <h2 className="card-title">The Challenge</h2>
          <p className={f.cardCopy}>{challenge}</p>
        </section>

        <section className="card">
          <h2 className="card-title">What DBERT Provided</h2>
          <p className={f.cardCopy}>{contribution}</p>
        </section>

        <section className="card">
          <h2 className="card-title">The Outcome</h2>
          <p className={f.cardCopy}>{outcome}</p>
        </section>

        {metrics && (
          <section className={`card ${s.metricsCard}`}>
            <h2 className={s.metricsTitle}>Key Metrics</h2>
            <p className={s.metricsValue}>{metrics}</p>
          </section>
        )}

        <div className={s.foot}>
          <a href="/startups/register" className="btn btn-primary">Get Similar Support for Your Startup</a>
        </div>
      </div>
    </div>
  );
}
