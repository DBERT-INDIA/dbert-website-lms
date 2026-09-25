import React from 'react';
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
          <h1 className="page-title-sm">
            Building in the Open, Shipping for Everyone
          </h1>
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
            <div className="card">
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

            <div className="card">
              <h3 className="card-heading">
                Gayatri AI Repository Collaboration
              </h3>
              <p className="card-copy-12">
                An open-source educational framework providing schools and developers with offline-first, local multi-agent simulations.
              </p>
              <ul className={s.bulletList}>
                <li>Modular Python libraries configuring communication channels between localized agents</li>
                <li>Automated assessment code setups to parse student prompt inputs</li>
                <li>Open-weights configurations to execute agent demonstrations without external API costs</li>
              </ul>
              <a 
                href="https://github.com/Gayatri-Education/Gayatri-AI" 
                target="_blank" 
                rel="noopener noreferrer" 
                className="inline-link"
              >
                View Gayatri-AI on GitHub ↗
              </a>
            </div>
          </div>
        </section>

        {/* Action Call */}
        <div className="card callout-plain">
          <div className="doclabel mb-2">§ 04 — JOIN RESEARCH COLLABORATION</div>
          <h2 className="card-title">Submit a Research Proposal</h2>
          <p className="page-lede">
            Are you interested in collaborating on academic briefs, contributing to open-source agent libraries, or testing local model configurations? Apply to DBERT Labs.
          </p>
          <a href="/labs/collaborate" className="btn btn-primary btn-lg">Submit Research Proposal</a>
        </div>

      </div>
    </div>
  );
}
