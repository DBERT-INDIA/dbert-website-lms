import React from 'react';
import Link from 'next/link';
import StepTimeline from '@/components/ui/StepTimeline';
import FAQAccordion from '@/components/ui/FAQAccordion';
import PipelineInteractiveConsole from '@/components/pipeline/PipelineInteractiveConsole';
import { pageMetadata } from '@/lib/seo';
import { Cpu, Database, ShieldCheck, CheckCircle, Terminal, Zap, Layers, Server } from 'lucide-react';

export const metadata = pageMetadata('/ai-solutions/llm-training/pipeline');

export default function FineTuningPipelinePage() {
  const steps = [
    { number: '01', title: 'Data Collection & Sanitization Audit', description: 'We extract records from unstructured document databases, RESTful APIs, customer support logs, and historical code archives—stripping duplicates, HTML boilerplate, and formatting syntax defects.' },
    { number: '02', title: 'Instruction Formatting & PII Scrubbing', description: 'We convert sanitized raw datasets into structured instruction-following conversational schemas containing explicit system roles, user prompts, assistant target completions, and automated PII masking.' },
    { number: '03', title: 'Fine-Tuning Execution (LoRA/QLoRA)', description: 'We configure optimal hyperparameter bounds—including Rank (r=8 or 16), Alpha (16), attention dropout rates, and target linear weights—running gradient descent loops on multi-node GPU clusters.' },
    { number: '04', title: 'Empirical Benchmark Evaluation', description: 'We rigorously evaluate checkpoint inference against withheld validation datasets to measure exact classification accuracy, syntax JSON parsing success rates, and token generation latencies.' },
    { number: '05', title: 'Compilation & GGUF/AWQ Quantization', description: 'We fuse trained LoRA adapter parameters back into base foundation checkpoints, quantize weights into high-speed 4-bit/8-bit GGUF or AWQ files, and deploy to sovereign server registries.' }
  ];

  const faqs = [
    {
      question: 'Why is rigorous data sanitization more critical than GPU cluster size during fine-tuning?',
      answer: 'A widespread industrial misconception is that throwing thousands of H100 GPU compute hours at unverified datasets will yield superior artificial intelligence reasoning. In reality, neural network fine-tuning is hyper-sensitive to "garbage-in, garbage-out" dynamics. Unsanitized duplicates cause severe weight memorization (overfitting), while syntax formatting flaws generate repeating hallucination loops. Our Stage 01 and 02 sanitization and PII scrubbing protocols consume over 40% of the total engineering lifecycle to guarantee pristine instruction schema quality.'
    },
    {
      question: 'What specific hyperparameter configurations do you implement during LoRA/QLoRA loops?',
      answer: 'For general enterprise reasoning and RAG extraction tasks, we standardly inject Low-Rank Adaptation (LoRA) adapters into query and value projection matrices (q_proj, v_proj) using a rank of r=8 or r=16 accompanied by a scaling alpha of 16 and a gentle learning rate of 2e-4 with cosine scheduling. When training on complex multi-line code generation or structured schema formatting, we extend target adapter injection across all linear transformer layers while applying 4-bit NormalFloat (NF4) quantization to freeze base foundational weights.'
    },
    {
      question: 'How do you test for semantic regression and avoid catastrophic forgetting?',
      answer: 'To ensure fine-tuned checkpoints do not suffer from catastrophic forgetting—where mastering domain terminology destroys foundational logical deduction—we interleave 20% high-quality foundational conversational replay data into every domain training batch. During Stage 04 Evaluation, we run multi-domain regression suites comparing base checkpoint accuracy against fine-tuned checkpoints across math, logic, and grammar benchmarks.'
    },
    {
      question: 'What hardware infrastructure executes these pipeline stages and how long does an average run take?',
      answer: 'Training loop execution runs on dedicated bare-metal NVIDIA GPU server clusters located inside our isolated RunPod and AWS Virtual Private Cloud hosting infrastructure. A standardized 10,000-record LoRA training epoch across a 7B or 14B parameter model typically completes computational execution within 12 to 24 hours, with the end-to-end 5-stage engineering lifecycle completing within a structured 14-day commercial sprint.'
    },
    {
      question: 'Can incubated early-stage startup pioneers access this 5-stage fine-tuning pipeline?',
      answer: 'Yes. Startup pioneers accepted into the DBERT Venture Studio gain complete native access to our entire 5-stage fine-tuning pipeline without paying cash engineering invoices. We execute data curation, hyperparameter optimization, and weight quantization directly on incubated founder repositories under our standardized services-against-equity exchange.'
    }
  ];

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Service',
        name: 'DBERT 5-Stage LLM Fine-Tuning Engineering Pipeline',
        serviceType: 'Data Sanitization, Instruction Dataset Formatting, LoRA/QLoRA Hyperparameter Training, Model Benchmarking, GGUF/AWQ Quantization',
        description: 'Rigorous 5-stage industrial engineering lifecycle transforming unstructured enterprise data archives into specialized, quantized open-weights language model checkpoints.',
        provider: {
          '@type': 'Organization',
          name: 'DBERT Labs Industrial Training & Venture Studio',
          url: 'https://dbert.online'
        },
        offers: {
          '@type': 'Offer',
          category: 'Fine-Tuning Engineering Sprint',
          price: '75000',
          priceCurrency: 'INR',
          description: 'Concentrated 14-day fine-tuning pipeline sprint or bundled into startup equity studio co-development'
        }
      },
      {
        '@type': 'FAQPage',
        mainEntity: faqs.map(f => ({
          '@type': 'Question',
          name: f.question,
          acceptedAnswer: {
            '@type': 'Answer',
            text: f.answer
          }
        }))
      }
    ]
  };

  return (
    <div className="glow-wrapper">
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      <div className="glow-spot"></div>

      {/* Hero Header Section */}
      <div className="container page-head">
        <div className="doclabel">
          § 01 — FINE-TUNING METHODOLOGY <span className="rev">rev: 2026.2</span>
        </div>
        <h1 className="page-title">
          The 5-Stage Fine-Tuning Pipeline &mdash; Industrial MLOps
        </h1>
        <p className="lede-wide">
          A mathematically disciplined engineering lifecycle designed to transform raw, unstructured enterprise databases into hardened, specialized open-weights model checkpoints capable of high-speed local inference.
        </p>
      </div>

      {/* Interactive MLOps Console (Directly under Hero) */}
      <div className="container pad-block border-t border-line">
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-8 gap-4">
          <div>
            <div className="doclabel mb-2">§ 02 — INTERACTIVE STAGES &amp; LIVE ARTIFACTS</div>
            <h2 className="section-title mb-2">
              The 5-Stage Transformation Lifecycle
            </h2>
            <p className="prose-sm text-muted max-w-2xl">
              Inspect how raw enterprise document dumps are cleansed, PII-scrubbed, trained via parameter-efficient LoRA adapters, benchmarked against semantic drift, and quantized into high-speed local inference formats.
            </p>
          </div>
          <div className="md:max-w-sm w-full bg-card border border-line-strong rounded-lg p-4 shadow-lg relative">
            <div className="flex items-center justify-between gap-2 mb-2 pb-2 border-b border-line">
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
                <span className="font-mono text-xs font-bold text-white uppercase tracking-wider">Air-Gapped Sovereign Execution</span>
              </div>
              <span className="handnote blue text-xs">zero external telemetry</span>
            </div>
            <p className="text-xs text-muted leading-relaxed mb-3">
              Compiled weights execute directly on bare-metal hardware via native C++ / PyTorch runtimes &mdash; <strong>100% standalone with zero dependency on Ollama, LM Studio, Docker, or third-party wrappers</strong>.
            </p>
            <div className="grid grid-cols-2 gap-2 text-[11px] font-mono border-t border-line/60 pt-2 text-zinc-300">
              <div className="flex items-center gap-1.5">
                <span className="text-emerald-400">✓</span> No Ollama runtime required
              </div>
              <div className="flex items-center gap-1.5">
                <span className="text-emerald-400">✓</span> No LM Studio dependency
              </div>
              <div className="flex items-center gap-1.5">
                <span className="text-emerald-400">✓</span> 100% offline isolated RAM
              </div>
              <div className="flex items-center gap-1.5">
                <span className="text-emerald-400">✓</span> Direct C++ / Python bindings
              </div>
            </div>
          </div>
        </div>

        <PipelineInteractiveConsole />
      </div>

      {/* Hardware Provisioning & VRAM Topology with Handcrafted Touch */}
      <div className="container pad-block border-t border-line">
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-8 gap-4">
          <div>
            <div className="doclabel mb-2">§ 03 — PHYSICAL HARDWARE &amp; VRAM FEASIBILITY</div>
            <h2 className="section-title mb-2">Actual VRAM Demands &mdash; Not Cloud Sales Fluff</h2>
            <p className="prose-sm text-muted max-w-2xl">
              We dimension hardware down to actual parameter quantization, KV cache headroom, and batch attention size so you never overpay for GPU capacity you do not need.
            </p>
          </div>
          <div className="text-right flex flex-col items-end">
            <span className="handnote text-[1.1rem]">audited on bare-metal racks ↗</span>
            <span className="text-[11px] font-mono text-muted tracking-wide mt-1">no cloud markups</span>
          </div>
        </div>

        <div className="grid gap-6 md:grid-cols-3 mt-6">
          {/* Workstation Card */}
          <div className="card bg-card border border-line flex flex-col justify-between relative">
            <div>
              <div className="flex items-center justify-between mb-4">
                <span className="font-mono text-xs text-accent uppercase font-bold tracking-wider">Edge / Workstation</span>
                <span className="font-mono text-[11px] bg-zinc-800 text-zinc-300 px-2 py-0.5 rounded">7B – 8B Models</span>
              </div>
              <h3 className="font-mono text-xl font-bold text-white mb-2">Single RTX 4090 <span className="text-sm text-muted font-normal">(24GB)</span></h3>
              <p className="text-[13px] text-muted mb-6 leading-relaxed">
                4-bit NormalFloat QLoRA with batch size 4 and 4k context. Ideal for local RAG adapters, code syntax linters, and departmental pilots.
              </p>
              
              <div className="space-y-3 border-t border-line/60 pt-4 font-mono text-xs">
                <div className="flex justify-between items-baseline text-muted">
                  <span>Base Weight VRAM:</span>
                  <span className="text-white font-semibold">5.8 GB (NF4)</span>
                </div>
                <div className="flex justify-between items-baseline text-muted">
                  <span>Gradient &amp; Optimizer:</span>
                  <span className="text-white font-semibold">4.2 GB (Paged AdamW)</span>
                </div>
                <div className="flex justify-between items-baseline text-muted">
                  <span>KV Cache (4k tokens):</span>
                  <span className="text-white font-semibold">2.4 GB</span>
                </div>
                <div className="flex justify-between items-baseline text-emerald-400 font-semibold pt-2 border-t border-line/60">
                  <span>Peak Headroom:</span>
                  <span>11.6 GB Safe</span>
                </div>
              </div>
            </div>

            <div className="mt-8 pt-4 border-t border-line/40 flex items-center justify-between">
              <span className="font-mono text-[11px] text-muted">~48–55 tok/s (Native C++ / GGML)</span>
              <span className="handnote blue text-sm" style={{ transform: 'rotate(-4deg)' }}>runs cool on desk</span>
            </div>
          </div>

          {/* Standard Enterprise Card */}
          <div className="card bg-card border-2 border-accent/60 relative flex flex-col justify-between">
            <div className="absolute -top-3 right-4 bg-accent text-zinc-950 font-mono text-[10px] uppercase font-bold px-2 py-0.5 rounded shadow-lg">
              Studio Standard
            </div>
            <div>
              <div className="flex items-center justify-between mb-4">
                <span className="font-mono text-xs text-accent uppercase font-bold tracking-wider">Mid-Scale Cluster</span>
                <span className="font-mono text-[11px] bg-zinc-800 text-zinc-300 px-2 py-0.5 rounded">14B – 32B Models</span>
              </div>
              <h3 className="font-mono text-xl font-bold text-white mb-2">Dual RTX 4090 / A10G Array</h3>
              <p className="text-[13px] text-muted mb-6 leading-relaxed">
                Dual 24GB/48GB VRAM configuration with ZeRO-2 stage offloading. Handles multi-turn agent logic and high-throughput document OCR.
              </p>
              
              <div className="space-y-3 border-t border-line pt-4 font-mono text-xs">
                <div className="flex justify-between items-baseline text-muted">
                  <span>Base Weight VRAM:</span>
                  <span className="text-white font-semibold">18.4 GB (NF4)</span>
                </div>
                <div className="flex justify-between items-baseline text-muted">
                  <span>LoRA Gradients:</span>
                  <span className="text-white font-semibold">8.6 GB (r=16, all-linear)</span>
                </div>
                <div className="flex justify-between items-baseline text-muted">
                  <span>KV Cache (8k context):</span>
                  <span className="text-white font-semibold">6.2 GB</span>
                </div>
                <div className="flex justify-between items-baseline text-emerald-400 font-semibold pt-2 border-t border-line/60">
                  <span>Peak Headroom:</span>
                  <span>14.8 GB Safe</span>
                </div>
              </div>
            </div>

            <div className="mt-8 pt-4 border-t border-line/40 flex items-center justify-between">
              <span className="font-mono text-[11px] text-muted">~32–40 tok/s (Bare-Metal Engine)</span>
              <span className="handnote text-sm" style={{ transform: 'rotate(-4deg)' }}>powers our studio</span>
            </div>
          </div>

          {/* High-Throughput Rack Card */}
          <div className="card bg-card border border-line flex flex-col justify-between relative">
            <div>
              <div className="flex items-center justify-between mb-4">
                <span className="font-mono text-xs text-muted uppercase font-bold tracking-wider">High-Throughput Rack</span>
                <span className="font-mono text-[11px] bg-zinc-800 text-zinc-300 px-2 py-0.5 rounded">70B+ Frontier</span>
              </div>
              <h3 className="font-mono text-xl font-bold text-white mb-2">RTX 6000 Ada / H100 Node</h3>
              <p className="text-[13px] text-muted mb-6 leading-relaxed">
                High-bandwidth memory architecture for heavy parameter weights, 32k context windows, and continuous enterprise batch embeddings.
              </p>
              
              <div className="space-y-3 border-t border-line pt-4 font-mono text-xs">
                <div className="flex justify-between items-baseline text-muted">
                  <span>Base Weight VRAM:</span>
                  <span className="text-white font-semibold">39.2 GB (8-bit Quant)</span>
                </div>
                <div className="flex justify-between items-baseline text-muted">
                  <span>Full Attention KV:</span>
                  <span className="text-white font-semibold">18.0 GB (FA-2)</span>
                </div>
                <div className="flex justify-between items-baseline text-muted">
                  <span>Multi-Tenant Ingestion:</span>
                  <span className="text-white font-semibold">Parallel 16 requests</span>
                </div>
                <div className="flex justify-between items-baseline text-emerald-400 font-semibold pt-2 border-t border-line/60">
                  <span>Memory Bandwidth:</span>
                  <span>960 GB/s</span>
                </div>
              </div>
            </div>

            <div className="mt-8 pt-4 border-t border-line/40 flex items-center justify-between">
              <span className="font-mono text-[11px] text-muted leading-relaxed">Zero external telemetry<br/>air-gapped execution</span>
              <span className="handnote blue text-sm" style={{ transform: 'rotate(-4deg)' }}>bank grade isolation</span>
            </div>
          </div>
        </div>
      </div>

      {/* Engineering Sprint Deliverables & Repository Ownership */}
      <div className="container pad-block border-t border-line">
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-8 gap-4">
          <div>
            <div className="doclabel mb-2">§ 04 — SPRINT DELIVERABLES &amp; REPOSITORIES</div>
            <h2 className="section-title mb-2">What You Actually Receive &mdash; Complete Code Ownership</h2>
            <p className="prose-sm text-muted max-w-2xl">
              We do not deliver opaque API keys or temporary dashboards. At sprint conclusion, your internal engineering team receives complete repositories, compiled checkpoints, and deployment manifests.
            </p>
          </div>
          <div className="text-right">
            <span className="handnote text-base">100% intellectual property transfer</span>
          </div>
        </div>

        <div className="grid gap-6 md:grid-cols-3">
          <div className="card p-6 bg-card border border-line flex flex-col justify-between">
            <div>
              <div className="flex items-center gap-2 mb-3">
                <Database className="w-5 h-5 text-accent" />
                <span className="font-mono text-xs text-accent font-bold uppercase tracking-wider">Artifact 01</span>
              </div>
              <h3 className="font-mono text-base font-bold text-white mb-2">Sanitized JSONL &amp; Masking Scripts</h3>
              <p className="text-xs text-muted leading-relaxed">
                Deterministic regex and NER transformation pipelines used to sanitize your raw corporate documents, accompanied by the fully validated 10,000+ instruction-tuning dataset.
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-line font-mono text-[11px] text-muted">
              Format: <span className="text-zinc-300">train.jsonl + eval.jsonl</span>
            </div>
          </div>

          <div className="card p-6 bg-card border-2 border-accent/70 flex flex-col justify-between relative">
            <div className="absolute -top-3 right-4 bg-accent text-zinc-950 font-mono text-[10px] uppercase font-bold px-2 py-0.5 rounded">
              Core Checkpoint
            </div>
            <div>
              <div className="flex items-center gap-2 mb-3">
                <Cpu className="w-5 h-5 text-emerald-400" />
                <span className="font-mono text-xs text-emerald-400 font-bold uppercase tracking-wider">Artifact 02</span>
              </div>
              <h3 className="font-mono text-base font-bold text-white mb-2">Quantized GGUF &amp; LoRA Adapter</h3>
              <p className="text-xs text-muted leading-relaxed">
                Both the standalone PyTorch PEFT adapter weights (18–45 MB) and the fully fused 4-bit / 8-bit quantized GGUF file configured for immediate zero-dependency native C++ / Python runtime execution &mdash; no Ollama or LM Studio needed.
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-line font-mono text-[11px] text-muted">
              Format: <span className="text-zinc-300">model-q4_k_m.gguf + dbert-engine</span>
            </div>
          </div>

          <div className="card p-6 bg-card border border-line flex flex-col justify-between">
            <div>
              <div className="flex items-center gap-2 mb-3">
                <Terminal className="w-5 h-5 text-signal" />
                <span className="font-mono text-xs text-signal font-bold uppercase tracking-wider">Artifact 03</span>
              </div>
              <h3 className="font-mono text-base font-bold text-white mb-2">Docker MLOps Compose &amp; Benchmark Report</h3>
              <p className="text-xs text-muted leading-relaxed">
                Complete containerized runtime stack including Nginx reverse proxy, vLLM inference server, Prometheus VRAM telemetry exporters, and the empirical regression accuracy benchmark report.
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-line font-mono text-[11px] text-muted">
              Format: <span className="text-zinc-300">docker-compose.yml + eval_radar.pdf</span>
            </div>
          </div>
        </div>
      </div>

      {/* Security Rigor & Data Decontamination */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 05 — DATA HYGIENE &amp; CRYPTOGRAPHIC DEFENSE</div>
        <h2 className="section-title mb-2">Protecting Data Integrity Through the Lifecycle</h2>
        <p className="prose-sm text-muted mb-6 max-w-2xl">
          When processing highly proprietary corporate documents, technical manuals, and financial transactions for neural training, data privacy and algorithmic hygiene require defense-in-depth protocols.
        </p>
        <div className="grid gap-6 md:grid-cols-2 my-4">
          <div className="card p-6 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-2">Automated PII Scrubbing &amp; Anonymization</h4>
            <p className="text-xs text-muted">
              Before raw client databases ever touch a training GPU memory buffer, Stage 02 executes automated regular expression and NER (Named Entity Recognition) masking algorithms. Social security numbers, bank routing codes, personal employee phone numbers, and customer addresses are systematically scrubbed and replaced with deterministic schema tokens.
            </p>
          </div>
          <div className="card p-6 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-2">Air-Gapped GPU Cluster Execution</h4>
            <p className="text-xs text-muted">
              All LoRA and QLoRA gradient calculation loops execute inside completely air-gapped Virtual Private Cloud instances on our dedicated hosting architecture. Training clusters feature zero external egress internet connectivity—preventing third-party weight tracking, unauthorized checkpoint downloading, or cloud vendor telemetry pingbacks.
            </p>
          </div>
        </div>
      </div>

      {/* FAQ Accordion Section */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 06 — PIPELINE KNOWLEDGE BASE</div>
        <h2 className="section-title mb-4">Frequently Asked Questions</h2>
        <div className="measure">
          <FAQAccordion items={faqs} />
        </div>
      </div>

      {/* Related Solutions & Academy Mesh */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 07 — RELATED AI SYSTEMS &amp; ACADEMY TRACKS</div>
        <h2 className="section-title mb-4">Explore Complementary Capabilities</h2>
        <div className="grid gap-4 md:grid-cols-3">
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">DBERT_AI Public Weights</h4>
            <p className="text-xs text-muted mb-3">Inspect our flagship in-house open model compiled through this exact 5-stage industrial lifecycle.</p>
            <Link href="/ai-solutions/llm-training/dbert-ai" className="accent-link text-xs">Explore DBERT_AI &rarr;</Link>
          </div>
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">Private Bare-Metal Hosting</h4>
            <p className="text-xs text-muted mb-3">Deploy your compiled GGUF and AWQ checkpoints directly onto secure local on-premises hardware arrays.</p>
            <Link href="/ai-solutions/llm-training/private-hosting" className="accent-link text-xs">View Private Hosting &rarr;</Link>
          </div>
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">AI Agent Development Training</h4>
            <p className="text-xs text-muted mb-3">Train your internal software engineering staff to format datasets and construct local LangChain agents.</p>
            <Link href="/learners/courses/ai-agent-development" className="accent-link text-xs">Explore Agent Course &rarr;</Link>
          </div>
        </div>
      </div>

      {/* CTA Block (Secondary BG) */}
      <div className="band-top border-t border-line">
        <div className="container">
          <div className="doclabel mb-2">§ 08 — INITIATE TRAINING PIPELINE</div>
          <div className="bento-card cta-panel bg-zinc-900 border border-line p-8 text-center rounded-lg">
            <h2 className="card-title text-3xl font-mono font-bold text-white mb-2">Launch Your Custom Fine-Tuning Pipeline Today</h2>
            <p className="page-lede text-sm text-muted max-w-2xl mx-auto mb-6">
              Ready to sanitize domain archives, fine-tune open-weights neural network models, and establish high-speed private hosting setups? Apply for DBERT Incubation or commission a standalone engineering sprint.
            </p>
            <div className="flex flex-wrap justify-center gap-4">
              <Link href="/startups/register" className="btn btn-primary btn-lg">Register Your Startup &rarr;</Link>
              <Link href="/ai-solutions/consultation" className="btn btn-outline btn-lg">Book Technical Consultation &rarr;</Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

