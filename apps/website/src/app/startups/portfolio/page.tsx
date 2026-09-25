import React from 'react';
import Link from 'next/link';
import { pageMetadata } from '@/lib/seo';
import s from '../startups.module.css';


export const metadata = pageMetadata('/startups/portfolio');

export default function StartupsPortfolioPage() {
  const startups = [
    {
      name: 'Alkame Inc.',
      linkText: 'alkameinc.info',
      url: 'https://alkameinc.info/',
      slug: 'alkame',
      sector: 'Fintech &amp; Market Intelligence',
      challenge: 'Required a resilient pipeline to ingest, parse, and analyze real-time market signals across 6,300+ listed stocks simultaneously.',
      contribution: 'DBERT architected a high-throughput streaming message-bus using Redis streams, Kafka, and pgvector database indices to store semantic signal vectors.',
      outcome: 'Achieved sub-100ms signal latency across thousands of concurrent tickers, enabling dynamic vector search over historical transaction patterns.',
      metrics: '₹1.2Cr Seed Raised | Sub-100ms Latency | 6,300+ Stocks'
    },
    {
      name: 'Cognitive Solutions',
      linkText: 'cognitivesolutions.co.in',
      url: 'https://cognitivesolutions.co.in/',
      slug: 'cognitive-solutions',
      sector: 'Robotics &amp; Computer Vision',
      challenge: 'Struggled to train and evaluate computer vision models for automated robotic joint alignment under varying factory floor conditions.',
      contribution: 'DBERT configured localized GPU nodes on-premises, optimized training datasets pipelines, and trained custom PyTorch weights models.',
      outcome: 'Robotic vision models achieved 98.4% alignment precision across simulated factory runs, cutting hardware downtime by 40%.',
      metrics: '98.4% Precision | 40% Downtime Reduction | Bootstrapped'
    },
    {
      name: 'Digital Blaize',
      linkText: 'digitalblaize.in',
      url: 'https://digitalblaize.in/',
      slug: 'digital-blaize',
      sector: 'Enterprise AI &amp; Upskilling',
      challenge: 'Needed a scalable, secure, and offline-first internal onboarding platform to train and review junior developer squads on production code.',
      contribution: 'DBERT configured containerized development sandboxes and deployed DBERT_AI local weights to automate code audits and progress checks.',
      outcome: 'Halved engineer onboarding timelines, allowing junior squads to push verified, compliant features to production repos within 15 days.',
      metrics: '15-Day Onboarding | 50% Time Saved | Enterprise Contract'
    },
    {
      name: 'Gayatri AI',
      linkText: 'github.com/Gayatri-Education',
      url: 'https://github.com/Gayatri-Education/Gayatri-AI',
      slug: 'gayatri-ai',
      sector: 'EdTech &amp; Open Source',
      challenge: 'Aims to distribute lightweight multi-agent educational simulations to local schools operating with limited internet bandwidth.',
      contribution: 'DBERT co-developed open-source local orchestration modules, allowing schools to run multi-agent scripts on offline PC systems.',
      outcome: 'Launched offline agent simulators deployed across local schools, enabling students to learn prompt setups without API costs.',
      metrics: '10+ Schools Deployed | ₹0 API Costs | Open Source'
    }
  ];

  return (
    <div className="glow-wrapper">
      <div className="glow-spot"></div>

      {/* Hero Header Section */}
      <div className="container page-head">
        <div className="doclabel">
          § 01 — INCUBATED VENTURE PORTFOLIO <span className="rev">rev: 2026.2</span>
        </div>
        <h1 className="page-title">
          Startups We Helped Build and Launch
        </h1>
        <p className="lede-wide">
          Real teams. Real products. Real impact. See how DBERT-incubated startups transformed ideas into production-grade AI systems shipping to customers.
        </p>
      </div>

      {/* Startup Portfolio Grid (Secondary BG) */}
      <div className="section-band-lg">
        <div className="container">
          <div className="doclabel mb-4">§ 02 — CO-DEVELOPED CASE STUDIES</div>
          <div className="bento-grid-2">
            {startups.map((startup, idx) => (
              <div key={idx} className={`bento-card on-ink ${s.portfolioCard}`}>
                <div>
                  <div className={s.portfolioTop}>
                    <span className="pill">{startup.sector}</span>
                    <a href={startup.url} target="_blank" rel="noopener noreferrer" className={s.portfolioLink}>{startup.linkText} ↗</a>
                  </div>
                  <h3 className={s.portfolioName}>{startup.name}</h3>

                  <div className={s.portfolioFacts}>
                    <div>
                      <strong className={s.factLabel}>Challenge:</strong>
                      <p className={s.factBody}>{startup.challenge}</p>
                    </div>
                    <div>
                      <strong className={s.factLabel}>DBERT Contribution:</strong>
                      <p className={s.factBody}>{startup.contribution}</p>
                    </div>
                  </div>
                </div>

                <div className={s.portfolioFoot}>
                  <div className={s.metricBar}>
                    <span className={s.metricText}>{startup.metrics}</span>
                  </div>
                  <Link href={`/startups/portfolio/${startup.slug}`} className={`btn btn-outline btn-sm ${s.btnBlock}`}>View Case Study →</Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA Section (Primary BG) */}
      <div className="container pad-block">
        <div className="doclabel mb-2">§ 03 — JOIN INCUBATION</div>
        <div className="bento-card callout">
          <h2 className="card-title">Your Startup Could Be Next</h2>
          <p className="page-lede">
            Get direct technical guidance, micro-grants for server hosting, candidate alignment sprints, and services-against-equity MVP co-development.
          </p>
          <Link href="/startups/register" className="btn btn-primary btn-lg">Register Your Startup</Link>
        </div>
      </div>
    </div>
  );
}
