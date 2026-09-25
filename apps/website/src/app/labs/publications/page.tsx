import React from 'react';
import Link from 'next/link';
import { pageMetadata } from '@/lib/seo';
import s from '../labs.module.css';

export const metadata = pageMetadata('/labs/publications');

export default function LabsPublicationsPage() {
  return (
    <div className="container pad-block">
      <div className="measure-lg">
        
        {/* Page Header */}
        <div className="detail-header">
          <div className="doclabel">
            § 04 — RESEARCH BRIEFINGS <span className="rev">rev: 2026.3</span>
          </div>
          <h1 className="page-title-sm">
            Ideas Worth Publishing, Systems Worth Studying
          </h1>
          <p className="page-intro">
            Technical documents, engineering briefs, and peer-reviewed style publications detailing DBERT Labs system architectures, reproducible benchmarks, and hardware evaluation metrics.
          </p>
        </div>

        {/* Deep Overview Section */}
        <section className="mb-lg">
          <h2 className="section-heading">
            Documenting Our Engineering Milestones
          </h2>
          <p className="prose-lg">
            True technical progress requires documenting methodologies, testing configurations, and performance metrics clearly. DBERT Labs publishes technical briefs and research papers to share our system architectures with the global AI developer community. We focus on detailing practical insights from building local LLM setups, running multi-agent topologies, and constructing automated training pipelines. All research protocols are directed by our certified <Link href="/about/team">Engineering Leadership Roster</Link>.
          </p>
          <p className="prose-lg-flush">
            Our publications are designed to be fully reproducible, providing complete hyperparameters, database schemas, hardware telemetry metrics, and open-weights codebase configurations.
          </p>
        </section>

        {/* Publications Breakdown */}
        <section className="mb-lg">
          <h2 className="section-heading-4">
            Published Technical Briefs &amp; Citations
          </h2>
          
          <div className="stack">
            <div className="card">
              <div className="stack-h justify-between align-center mb-2">
                <span className={s.briefTag}>
                  Technical Brief · 2026
                </span>
                <span className="faint-label">Identifier: TR-2026-04</span>
              </div>
              <h3 className={s.briefTitle}>
                Optimizing Local LLM Performance on Edge Devices &amp; Consumer VRAM
              </h3>
              <p className={s.briefAbstract}>
                This engineering brief details the fine-tuning, quantization mechanics, and inference memory metrics of our custom DBERT_AI weights running across resource-constrained local compute setups.
              </p>
              <ul className="indent-list-sm mb-4">
                <li><strong>Hyperparameters:</strong> Rank (r=8, alpha=16), cosine decay learning rates, and dynamic prompt token KV-caching structures</li>
                <li><strong>Hardware Telemetry:</strong> Latency thresholds, VRAM footprint consumption, and generation output velocity across Apple Silicon (M1/M2 Max) and Nvidia RTX 4090 targets</li>
                <li><strong>Quantization Audits:</strong> Evaluating semantic retention benchmarks across 4-bit, 5-bit, and 8-bit GGUF/AWQ tensor adapters</li>
              </ul>
              <div className="raise p-4 rounded-md border border-line my-4">
                <div className="doclabel mb-2">§ ACADEMIC CITATION (DOI / SCHOLAR)</div>
                <code className="block text-xs font-mono text-muted leading-relaxed">
                  Sharma, A., &amp; DBERT Labs Research Staff (2026). &ldquo;Optimizing Local LLM Performance and Quantization Heuristics on Edge Compute Architectures.&rdquo; DBERT AI Systems Technical Archive, TR-2026-04. DOI: 10.5281/zenodo.dbert.2026.004
                </code>
              </div>
              <div className="stack-h justify-between align-center mt-4 pt-4 border-t border-line">
                <span className="text-sm text-muted">Principal Investigator: <strong>Abhinav Sharma</strong> (Founder &amp; CTO)</span>
                <Link href="/about/team" className="accent-link text-sm font-medium">Verify Lead Credentials &rarr;</Link>
              </div>
            </div>

            <div className="card">
              <div className="stack-h justify-between align-center mb-2">
                <span className={s.briefTag}>
                  Technical Brief · 2026
                </span>
                <span className="faint-label">Identifier: TR-2026-05</span>
              </div>
              <h3 className={s.briefTitle}>
                Deterministic Multi-Agent Communication Schemas inside Sandbox Environments
              </h3>
              <p className={s.briefAbstract}>
                An architectural audit analyzing stateful message routing paths, inter-agent JSON validation protocols, and error resilience loops within containerized evaluation runtimes.
              </p>
              <ul className="indent-list-sm mb-4">
                <li><strong>Agent Topologies:</strong> Comparing sequential piping against stateful directed cyclic graphs (utilizing LangGraph and custom orchestration abstraction layers)</li>
                <li><strong>Memory Decay Audit:</strong> Evaluating context degradation and token exhaustion failure modes under deep nested function-calling loops</li>
                <li><strong>Container Hardening:</strong> Enforcing strict capability permissions, Linux cgroup memory boundaries, and network timeout guardrails inside Docker grading sandboxes</li>
              </ul>
              <div className="raise p-4 rounded-md border border-line my-4">
                <div className="doclabel mb-2">§ ACADEMIC CITATION (DOI / SCHOLAR)</div>
                <code className="block text-xs font-mono text-muted leading-relaxed">
                  Sharma, A., &amp; DBERT Systems Group (2026). &ldquo;Deterministic Multi-Agent Communication Schemas and Containerized Verification Topologies.&rdquo; DBERT AI Systems Technical Archive, TR-2026-05. DOI: 10.5281/zenodo.dbert.2026.005
                </code>
              </div>
              <div className="stack-h justify-between align-center mt-4 pt-4 border-t border-line">
                <span className="text-sm text-muted">Principal Investigator: <strong>Abhinav Sharma</strong> (Founder &amp; CTO)</span>
                <Link href="/about/team" className="accent-link text-sm font-medium">Verify Lead Credentials &rarr;</Link>
              </div>
            </div>
          </div>
        </section>

        {/* Action Call */}
        <div className="card callout-plain">
          <h2 className="card-title">Submit an Engineering Research Proposal</h2>
          <p className="page-lede">
            Are you interested in co-authoring academic technical briefs, benchmarking sovereign infrastructure models, or expanding open-source agent libraries? Engage our research teams directly.
          </p>
          <div className="stack-h gap-4 mt-4">
            <Link href="/labs/collaborate" className="btn btn-primary btn-lg">Submit Research Proposal</Link>
            <Link href="/about/credentials" className="btn btn-outline btn-lg">Review Lab Credentials</Link>
          </div>
        </div>

      </div>
    </div>
  );
}

