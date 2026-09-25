import React from 'react';
import Link from 'next/link';
import { pageMetadata } from '@/lib/seo';

export const metadata = pageMetadata('/labs/research');

export default function LabsResearchPage() {
  return (
    <div className="container pad-block">
      <div className="measure-lg">
        
        {/* Page Header */}
        <div className="detail-header">
          <div className="doclabel">
            § 04 — RESEARCH SEGMENTS <span className="rev">rev: 2026.3</span>
          </div>
          <h1 className="page-title-sm">
            Pioneering the Next Wave of Intelligent Systems
          </h1>
          <p className="page-intro">
            Advancing the architectural boundaries of artificial intelligence. We research and deploy multi-agent communication topologies, local model parameter compression, and deterministic educational systems.
          </p>
        </div>

        {/* Deep Overview Section */}
        <section className="mb-lg">
          <h2 className="section-heading">
            Empowering Open Science &amp; Local Sovereign Intelligence
          </h2>
          <p className="prose-lg">
            At DBERT Labs, we hold that the future of enterprise artificial intelligence depends upon localized, inspectable, and highly specialized architectures. Relying exclusively on closed third-party multi-tenant APIs restricts engineering control, incurs unpredictable inference costs, and exposes proprietary user data to third-party retention models. Our operational research division focuses on quantizing open-weights models and designing deterministic agent coordination frameworks that run reliably across sovereign cloud instances and consumer edge hardware.
          </p>
          <p className="prose-lg-flush">
            We document our structural methodologies in public <Link href="/labs/publications">Technical Briefs</Link>, maintain open-weights checkpoints, and integrate validated findings directly into DBERT&apos;s <Link href="/startups">Venture Incubation Frameworks</Link> and <Link href="/learners">Learner Upskilling Ladders</Link>. Every research initiative is subject to strict engineering oversight by our verified <Link href="/about/team">Research Leadership Team</Link>.
          </p>
        </section>

        {/* Deliverables Breakdown */}
        <section className="mb-lg">
          <h2 className="section-heading-4">
            Our Primary Technical Research Segments
          </h2>
          
          <div className="stack">
            <div className="card">
              <div className="doclabel mb-1">§ RESEARCH TRACK 01</div>
              <h3 className="card-heading">
                Multi-Agent System Topologies &amp; Governance
              </h3>
              <p className="card-copy">
                We analyze message routing efficiency, deterministic tool execution, state graph consistency, and context-caching protocols inside collaborative agent clusters.
              </p>
              <ul className="indent-list">
                <li>Investigating stateful routing patterns and cyclic fallback architectures using advanced agent orchestration abstractions</li>
                <li>Developing deterministic JSON schema enforcement loops and tool validation guardrails</li>
                <li>Optimizing token context consumption and reducing latency budgets during iterative reasoning cycles</li>
              </ul>
              <div className="mt-4 pt-3 border-t border-line stack-h justify-between align-center">
                <span className="text-sm text-muted">Related Benchmark: <Link href="/blog/ai-agent-developer-salary-2026" className="ink-link">2026 Agent Systems Market Analysis</Link></span>
                <Link href="/labs/publications" className="accent-link text-sm font-medium">Read Technical Reports &rarr;</Link>
              </div>
            </div>

            <div className="card">
              <div className="doclabel mb-1">§ RESEARCH TRACK 02</div>
              <h3 className="card-heading">
                LLM Compression, Quantization &amp; Edge Execution
              </h3>
              <p className="card-copy">
                We formulate model weight pruning algorithms and quantization calibrations to deploy custom-tuned architectures natively on localized enterprise hardware.
              </p>
              <ul className="indent-list">
                <li>Tuning weight parameter alignments via parameter-efficient LoRA, QLoRA, and DoRA adapter frameworks</li>
                <li>Compiling and evaluating 4-bit, 5-bit, and 8-bit GGUF/AWQ quantized checkpoints for memory-constrained VRAM targets</li>
                <li>Benchmarking tokens-per-second generation velocity across Apple Silicon and Nvidia enterprise hardware setups</li>
              </ul>
              <div className="mt-4 pt-3 border-t border-line stack-h justify-between align-center">
                <span className="text-sm text-muted">Active Artifact: <Link href="https://ollama.com/DBERT/DBERT_AI" target="_blank" rel="noopener noreferrer" className="ink-link">DBERT_AI Open-Weights Registry</Link></span>
                <Link href="/ai-solutions/llm-training/private-hosting" className="accent-link text-sm font-medium">View Sovereign Infrastructure &rarr;</Link>
              </div>
            </div>

            <div className="card">
              <div className="doclabel mb-1">§ RESEARCH TRACK 03</div>
              <h3 className="card-heading">
                Deterministic RAG &amp; Educational Evaluation Topologies
              </h3>
              <p className="card-copy">
                We construct hallucination-resistant retrieval loops, code synthesis evaluation pipelines, and containerized technical screening runtimes.
              </p>
              <ul className="indent-list">
                <li>Designing structural semantic document chunking heuristics and hybrid dense-sparse (BM25 + pgvector) indexing architectures</li>
                <li>Building automated, deterministic code evaluation suites inside isolated Linux container sandboxes</li>
                <li>Implementing continuous cross-encoder reranking algorithms for high-precision institutional document citations</li>
              </ul>
              <div className="mt-4 pt-3 border-t border-line stack-h justify-between align-center">
                <span className="text-sm text-muted">Tutorial Blueprint: <Link href="/blog/rag-pipeline-tutorial-from-scratch" className="ink-link">Production RAG Architecture from Scratch</Link></span>
                <Link href="/learners/accelerate" className="accent-link text-sm font-medium">Inspect Accelerate Track &rarr;</Link>
              </div>
            </div>
          </div>
        </section>

        {/* Action Call */}
        <div className="card callout-plain">
          <h2 className="card-title">Collaborate with DBERT Laboratories</h2>
          <p className="page-lede">
            Are you an academic researcher, open-source repository maintainer, or enterprise engineering team seeking to partner on sovereign LLM infrastructures or multi-agent evaluations? Engage our technical leadership.
          </p>
          <div className="stack-h gap-4 mt-4">
            <Link href="/labs/collaborate" className="btn btn-primary btn-lg">Submit Collaboration Proposal</Link>
            <Link href="/about/team" className="btn btn-outline btn-lg">Inspect Engineering Leadership</Link>
          </div>
        </div>

      </div>
    </div>
  );
}

