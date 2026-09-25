import React from 'react';
import Link from 'next/link';
import { pageMetadata } from '@/lib/seo';
import s from './labs.module.css';
import { BookOpen, Laptop, Microscope } from 'lucide-react';

export const metadata = pageMetadata('/labs');

export default function DBERTLabsLandingPage() {
  return (
    <div className="container pad-block">
      <div className="mb-lg">
        <div className="doclabel">
          § 04 — LABS ARCHIVES <span className="rev">rev: 2026.3</span>
        </div>
        <h1>Where Breakthrough Systems Begin</h1>
        <p className={s.hubLede}>
          DBERT Labs is an applied artificial intelligence engineering facility and technical research division. 
          We investigate multi-agent orchestration architectures, local LLM edge quantization, custom rag evaluation harnesses, and algorithmic financial intelligence—open-sourcing our findings and feeding validated systems directly into our incubation and learning ecosystems.
        </p>
      </div>

      <div className={s.hubGrid}>
        <div className="card stack-between">
          <div>
            <span className="icon-chip"><Microscope aria-hidden="true" /></span>
            <h3 className="card-heading-lg">Research Segments</h3>
            <p className="body-copy">
              Inspect our active structural investigations: multi-agent system governance, sovereign LLM compression, hybrid vector RAG architectures, and automated evaluation toolboxes.
            </p>
          </div>
          <Link href="/labs/research" className="accent-label">Explore Technical Research &rarr;</Link>
        </div>

        <div className="card stack-between">
          <div>
            <span className="icon-chip"><BookOpen aria-hidden="true" /></span>
            <h3 className="card-heading-lg">Technical Publications</h3>
            <p className="body-copy">
              Examine our peer-reviewed style engineering briefs, complete with academic citations (DOI/Scholar), reproducible hyperparameters, and empirical hardware latency benchmarks.
            </p>
          </div>
          <Link href="/labs/publications" className="accent-label">Explore Published Reports &rarr;</Link>
        </div>

        <div className="card stack-between">
          <div>
            <span className="icon-chip"><Laptop aria-hidden="true" /></span>
            <h3 className="card-heading-lg">Open Source Repositories</h3>
            <p className="body-copy">
              Deploy DBERT&apos;s contributions to public open-weights registries (DBERT_AI custom LLM on Ollama) and educational systems (Gayatri AI syntax parsers).
            </p>
          </div>
          <Link href="/labs/opensource" className="accent-label">Explore Open-Source Code &rarr;</Link>
        </div>
      </div>

      <div className={`card ${s.ctaCard}`}>
        <h2 className="card-title">Academic &amp; Institutional Collaboration</h2>
        <p className={s.ctaCopy}>
          Partner with DBERT Labs on custom engineering research sprints, sovereign AI cluster benchmarks, or specialized dataset alignment projects under verified legal frameworks.
        </p>
        <div className="stack-h gap-4 mt-4">
          <Link href="/labs/collaborate" className="btn btn-primary">Submit Collaboration Proposal</Link>
          <Link href="/about/credentials" className="btn btn-outline">Inspect Institutional Verification</Link>
        </div>
      </div>
    </div>
  );
}

