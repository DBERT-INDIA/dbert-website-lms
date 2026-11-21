import React from 'react';
import Link from 'next/link';
import HandNote from '@/components/ui/HandNote';
import { pageMetadata } from '@/lib/seo';
import s from '../labs.module.css';

export const metadata = pageMetadata('/labs/opensource');

export default function LabsOpensourcePage() {
  return (
    <div className="container pad-block">
      <div className="measure-lg">
        
        {/* Page Header */}
        <div className="detail-header">
          <div className="doclabel">
            § 01 — OPEN SOURCE REPOSITORIES <span className="rev">rev: 2026.2</span>
          </div>
          <div className="stack-h justify-start align-baseline gap-3 flex-wrap mb-2">
            <h1 className="page-title-sm mb-0">
              Building in the Open, Shipping for Everyone
            </h1>
            <HandNote tone="blue">
              public code · open weights ✎
            </HandNote>
          </div>
          <p className="page-intro">
            We support open-source software development. Explore our public code repositories, fine-tuned model weights, and multi-agent systems.
          </p>
        </div>

        {/* Deep Overview Section */}
        <section className="mb-lg">
          <div className="doclabel mb-2">§ 02 — ARCHITECTURAL TRANSPARENCY</div>
          <h2 className="section-heading">
            Our Commitment to Open Weights &amp; Frameworks
          </h2>
          <p className="prose-lg">
            We believe that the technical developer community grows fastest when core engineering architectures, model weights, and system dependencies are shared transparently. Open-source codebases allow developers to inspect routing logic, verify security boundaries, and run custom model evaluations locally.
          </p>
          <p className="prose-lg-flush">
            DBERT Labs actively maintains and contributes to public code repositories. We release specialized model weights optimized for edge devices, design modular orchestration packages, and collaborate on education-focused software packages.
          </p>
        </section>

        {/* Public Projects Breakdown */}
        <section className="mb-lg">
          <div className="doclabel mb-2">§ 03 — ACTIVE PUBLIC MODELS &amp; CODE</div>
          <h2 className="section-heading-4">
            Public Code &amp; Models
          </h2>
          
          <div className="stack">
            <div className="card card-lift">
              <h3 className="card-heading">
                DBERT_AI Custom Model
              </h3>
              <p className="card-copy-12">
                Our custom-tuned weights model trained on specialized data schemas and local execution scripts, designed to run smoothly on edge server configurations.
              </p>
              <ul className={s.bulletList}>
                <li>Quantized checkpoints optimized for low VRAM targets (4-bit, 5-bit GGUF parameters)</li>
                <li>Excellent compliance for parsing workflows and returning structured JSON outputs</li>
                <li>Hosted and versioned directly on the official Ollama model registry page</li>
              </ul>
              <a 
                href="https://ollama.com/DBERT/DBERT_AI" 
                target="_blank" 
                rel="noopener noreferrer" 
                className="inline-link"
              >
                Run on Ollama: ollama run DBERT/DBERT_AI ↗
              </a>
            </div>

            <div className="card card-lift">
              <h3 className="card-heading">
                Gayatri AI Repository Collaboration
              </h3>
              <p className="card-copy-12">
                An open-source educational framework providing schools and developers with offline-first, local multi-agent simulations and retrieval-augmented pedagogical guidance.
              </p>
              <ul className={s.bulletList}>
                <li>Modular Python libraries configuring communication channels between localized agents</li>
                <li>Automated assessment code setups to parse student prompt inputs and cognitive concept graphs</li>
                <li>Open-weights configurations to execute agent demonstrations without external API costs</li>
              </ul>
              <div className="stack-h gap-3 flex-wrap mt-2">
                <a 
                  href="https://github.com/Gayatri-Education/Gayatri-Demo" 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  className="inline-link font-medium"
                >
                  View Gayatri-Demo on GitHub ↗
                </a>
                <a 
                  href="https://github.com/ainabhinavsharma/Gayatri-AI" 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  className="inline-link font-medium text-muted"
                >
                  Architect Fork (ainabhinavsharma) ↗
                </a>
              </div>
            </div>

            <div className="card card-lift">
              <h3 className="card-heading">
                Alkame Markets (Nifty 50 Educational Predictor)
              </h3>
              <p className="card-copy-12">
                Open-source quantitative finance and machine learning benchmark predicting index volatility and directional movement with inductive conformal prediction guarantees.
              </p>
              <ul className={s.bulletList}>
                <li>Walk-forward backtesting pipelines evaluating XGBoost, LightGBM, and LSTM architectures</li>
                <li>Calibrated conformal prediction intervals ensuring mathematical coverage under market regime shifts</li>
                <li>FastAPI microservices streaming historical price features and technical indicators</li>
              </ul>
              <div className="stack-h gap-3 flex-wrap mt-2">
                <a 
                  href="https://github.com/Alkameinc/alkame-nifty-50-educational" 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  className="inline-link font-medium"
                >
                  View Alkame-Nifty-50 on GitHub ↗
                </a>
                <a 
                  href="https://github.com/ainabhinavsharma/alkame-nifty-50-educational" 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  className="inline-link font-medium text-muted"
                >
                  Architect Fork (ainabhinavsharma) ↗
                </a>
              </div>
            </div>

            <div className="card card-lift">
              <h3 className="card-heading">
                Aivara Autonomous Suite / DBERT Agent
              </h3>
              <p className="card-copy-12">
                Modular agentic runtime and workflow orchestration engine designed for sovereign enterprise automation and edge tool calling.
              </p>
              <ul className={s.bulletList}>
                <li>Dynamic multi-tool execution pipelines with strict output validation and error self-correction</li>
                <li>Vector memory virtualization supporting fast contextual recall and long-term agent sessions</li>
                <li>Pre-configured local model adapters for Ollama, LM Studio, and vLLM inference backends</li>
              </ul>
              <div className="stack-h gap-3 flex-wrap mt-2">
                <a 
                  href="https://github.com/DBERT-INDIA/dbert-agent" 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  className="inline-link font-medium"
                >
                  View DBERT-Agent on GitHub ↗
                </a>
              </div>
            </div>

            <div className="card card-lift">
              <h3 className="card-heading">
                DBERT Platform &amp; LMS Monorepo
              </h3>
              <p className="card-copy-12">
                The core production architecture powering dbert.in and lms.dbert.in, combining Next.js 16 Turbopack standalone SSR with Python Flask backend microservices.
              </p>
              <ul className={s.bulletList}>
                <li>Dual-stack monorepo featuring high-concurrency certificate verification and Turnitin originality tracking</li>
                <li>Automated SEO mesh matrix, programmatic sitemaps, and Schema.org semantic knowledge graphs</li>
                <li>Seamless AWS EC2 deployment automation with systemd daemon supervision</li>
              </ul>
              <div className="stack-h gap-3 flex-wrap mt-2">
                <a 
                  href="https://github.com/DBERT-INDIA/dbert-website-lms" 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  className="inline-link font-medium"
                >
                  View Monorepo on GitHub ↗
                </a>
                <a 
                  href="https://github.com/ainabhinavsharma/DBERT-LMS" 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  className="inline-link font-medium text-muted"
                >
                  Architect Fork (ainabhinavsharma) ↗
                </a>
              </div>
            </div>
          </div>
        </section>

        {/* Lead Architect & Maintainer Spotlight */}
        <section className="mb-lg">
          <div className="card card-lift" style={{ borderLeft: '4px solid #7C3AED' }}>
            <div className="doclabel mb-2">§ 04 — LEAD ARCHITECT &amp; OPEN SOURCE STEWARDSHIP</div>
            <h2 className="card-heading">Maintained by Abhinav Sharma &amp; DBERT Engineering Fellows</h2>
            <p className="prose-lg mb-3">
              All open-source repositories, model checkpoints, and evaluation rubrics are maintained under the technical stewardship of <strong>Abhinav Sharma</strong> (Founder, CTO &amp; Principal AI Architect at DBERT). We welcome pull requests, reproducible benchmark evaluations, and multi-agent experiments from our incubated fellows and the global developer community.
            </p>
            <div className="stack-h gap-3 flex-wrap">
              <a
                href="https://github.com/ainabhinavsharma"
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-primary"
              >
                Inspect github.com/ainabhinavsharma ↗
              </a>
              <Link href="/about/team" className="btn btn-secondary">
                View Engineering Leadership Registry &rarr;
              </Link>
              <Link href="/verify/directory" className="btn btn-secondary">
                Explore Verified Contributors (465+) &rarr;
              </Link>
            </div>
          </div>
        </section>

        {/* Action Call */}
        <div className="card card-lift callout-plain">
          <div className="doclabel mb-2">§ 04 — JOIN RESEARCH COLLABORATION</div>
          <h2 className="card-title">Submit a Research Proposal</h2>
          <p className="page-lede">
            Are you interested in collaborating on academic briefs, contributing to open-source agent libraries, or testing local model configurations? Apply to DBERT Labs.
          </p>
          <Link href="/labs/collaborate" className="btn btn-primary btn-lg">Submit Research Proposal</Link>
        </div>

      </div>
    </div>
  );
}
