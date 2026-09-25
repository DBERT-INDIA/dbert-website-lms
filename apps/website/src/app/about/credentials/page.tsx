import React from 'react';
import Link from 'next/link';
import { pageMetadata } from '@/lib/seo';
import styles from '../about.module.css';

export const metadata = pageMetadata('/about/credentials');

export default function CredentialsPage() {
  return (
    <div className="container pad-block">
      <div className="mb-lg">
        <div className="doclabel">
          § 05 — INSTITUTIONAL VERIFICATION <span className="rev">rev: 2026.2</span>
        </div>
        <h1>Proven Engineering Credibility, Audited Impact</h1>
        <p className="intro-copy">The institutional registrations, compliance standards, and open-weights engineering deployments validating DBERT.</p>
      </div>

      <div className={styles.cardStack}>
        <div className="card">
          <div className="doclabel mb-1">§ REGULATORY COMPLIANCE</div>
          <h2 className={styles.cardTitleTight}>MSME Registered Corporate Entity</h2>
          <p className="prose-sm mb-4">
            Fully registered under the Ministry of Micro, Small and Medium Enterprises, Government of India (UDYAM compliant). DBERT operates as the dedicated technology incubation, artificial intelligence solutions, and advanced developer training division under the parent corporate entity <strong>Digital Blinc Education Research And Technology</strong>, ensuring formal statutory recognition for all enterprise contracts and learner fellowship certifications.
          </p>
          <div className="pt-3 border-t border-line">
            <Link href="/verify" className="accent-link text-sm font-medium">Launch Online Certificate &amp; LOR Verification Engine &rarr;</Link>
          </div>
        </div>

        <div className="card">
          <div className="doclabel mb-1">§ OPEN SCIENCE COMMITMENT</div>
          <h2 className={styles.cardTitleTight}>Sovereign AI &amp; Open-Source Repository Contributions</h2>
          <p className="prose-sm mb-4">
            Acknowledged across the Indian AI developer community for engineering excellence in designing modular multi-agent communication schemas, releasing open-weights localized LLM configurations, and building transparent, scalable venture incubation structures. All core frameworks undergo public peer review.
          </p>
          <div className="pt-3 border-t border-line">
            <Link href="/labs/opensource" className="accent-link text-sm font-medium">Inspect Open-Source Repositories &rarr;</Link>
          </div>
        </div>

        <div className="card">
          <div className="doclabel mb-1">§ PUBLISHED AI WEIGHTS</div>
          <h2 className={styles.cardTitleTight}>DBERT_AI Open-Weights Custom Model</h2>
          <p className={styles.modelCopy}>
            Custom fine-tuned parameter weights optimized specifically for unstructured educational Document parsing, deterministic web automation scripting, and agent function-calling loops. Compiled in highly efficient GGUF quantization formats and published publicly on the Ollama verified global model registry.
          </p>
          <a 
            href="https://ollama.com/DBERT/DBERT_AI" 
            target="_blank" 
            rel="noopener noreferrer" 
            className={`${styles.inlineLink} font-mono block mt-3 p-3 raise rounded border border-line`}
          >
            Run Locally in Terminal: ollama run DBERT/DBERT_AI &rarr;
          </a>
        </div>

        <div className="card">
          <div className="doclabel mb-1">§ LEARNER IMPACT AUDITOR</div>
          <h2 className={styles.cardTitleTight}>1,500+ Upskilled Developers &amp; Fellows</h2>
          <p className="prose-sm mb-4">
            Successfully mentored over 1,500 candidates across our sequential AI developer ladder, systematically transitioning early-career university students and experienced non-technical professionals into fluent, validated code contributors actively deploying live software for venture clients.
          </p>
          <div className="pt-3 border-t border-line stack-h gap-4">
            <Link href="/learners" className="accent-link text-sm font-medium">Inspect Career Pathways Ladder &rarr;</Link>
            <Link href="/about/team" className="accent-link text-sm font-medium">Meet Mentorship Leadership &rarr;</Link>
          </div>
        </div>
      </div>
    </div>
  );
}

