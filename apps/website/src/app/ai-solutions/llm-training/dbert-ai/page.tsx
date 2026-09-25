import React from 'react';
import Link from 'next/link';
import FAQAccordion from '@/components/ui/FAQAccordion';
import { pageMetadata } from '@/lib/seo';
import s from '../../ai-solutions.module.css';
import { Terminal, Cpu, Database, ShieldCheck, CheckCircle } from 'lucide-react';

export const metadata = pageMetadata('/ai-solutions/llm-training/dbert-ai');

export default function DBERTAIModelPage() {
  const faqs = [
    {
      question: 'What is DBERT_AI and how does it differ from base open-weights LLM releases?',
      answer: 'DBERT_AI is our proprietary in-house model published on the official Ollama container registry. Unlike raw foundational models that generate unpredictable conversational verbose text, DBERT_AI has undergone thousands of instruction fine-tuning loops across structured industrial engineering datasets—optimizing its weights specifically for strict JSON schema output generation, automated Python/Docker code audits, and multi-agent task execution.'
    },
    {
      question: 'What hardware VRAM and compute memory configurations are required to run DBERT_AI locally?',
      answer: 'Because DBERT_AI is compiled into high-efficiency 4-bit and 8-bit GGUF quantization weight checkpoints, it operates smoothly on standard enterprise hardware. Running the 4-bit quantized checkpoint requires approximately 8GB of GPU VRAM (compatible with NVIDIA RTX 3060/4060 or Apple M1/M2/M3 unified memory machines), achieving concurrent token generation speeds exceeding 45 tokens per second.'
    },
    {
      question: 'How does DBERT_AI prevent hallucinations when extracting structured JSON schema records?',
      answer: 'During fine-tuning within our software laboratory, DBERT_AI was heavily penalized for generating introductory markdown pleasantries or schema hallucinations. When presented with complex document strings or unstructured logs alongside targeted JSON extraction keys, the model deterministically returns validated JSON arrays and objects suitable for direct ingestion into automated enterprise webhooks and RESTful APIs.'
    },
    {
      question: 'Can our organization procure custom LoRA adapters layered on top of the DBERT_AI base checkpoint?',
      answer: 'Yes. Enterprise IT organizations and startup founders can contract DBERT Labs to execute specialized Low-Rank Adaptation (LoRA) training loops layered directly over the DBERT_AI foundational weights—embedding your company’s internal legal covenants, medical terminology, or proprietary product documentation without modifying core reasoning logic.'
    },
    {
      question: 'Is DBERT_AI licensed for unrestricted commercial production deployment without token fee obligations?',
      answer: 'Yes. DBERT_AI is published under an open, developer-friendly commercial license. When downloaded and hosted locally inside your private server architecture or Virtual Private Cloud (VPC), your organization retains 100% data sovereignty and incurs zero recurring per-token inference royalties or commercial usage fees.'
    }
  ];

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'SoftwareApplication',
        name: 'DBERT_AI Open-Weights Specialized LLM',
        applicationCategory: 'DeveloperApplication, BusinessApplication',
        operatingSystem: 'Linux, macOS, Windows, Docker, Ollama Runtime',
        description: 'In-house fine-tuned artificial intelligence open model compiled for structured JSON extraction, automated syntax debugging, and low-latency CrewAI multi-agent execution.',
        offers: {
          '@type': 'Offer',
          price: '0',
          priceCurrency: 'USD',
          description: 'Open developer download via official Ollama registry with zero recurring per-token royalties'
        },
        author: {
          '@type': 'Organization',
          name: 'DBERT Labs Industrial Training & Venture Studio',
          url: 'https://dbert.online'
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
          § 01 — OLLAMA REGISTRY MODEL <span className="rev">rev: 2026.2</span>
        </div>
        <h1 className="page-title">
          DBERT_AI &mdash; Sovereign Intelligence You Can Deploy Anywhere
        </h1>
        <p className="lede-wide">
          Explore DBERT&apos;s in-house fine-tuned model published publicly on the official Ollama repository. Execute deterministic JSON extraction, run rigorous syntax audits, and deploy stateful multi-agent workflows directly on your physical server hardware with zero external API fees.
        </p>
        <div className="mt-6 flex flex-wrap gap-4 align-center">
          <a href="https://ollama.com/DBERT/DBERT_AI" target="_blank" rel="noopener noreferrer" className="btn btn-primary btn-sm inline-flex align-center gap-2">
            View DBERT_AI on Ollama Registry ↗
          </a>
          <Link href="/ai-solutions/llm-training/private-hosting" className="btn btn-outline btn-sm">
            Explore Enterprise Bare-Metal Hosting &rarr;
          </Link>
        </div>
      </div>

      {/* Run Command Section (Secondary BG) */}
      <div className="section-band border-t border-b border-line">
        <div className={`container ${s.codeWrapNarrow}`}>
          <div className="doclabel mb-2">§ 02 — LOCAL TERMINAL EXECUTION COMMAND</div>
          <h2 className="subsection-title">Instantaneous Containerized Launch</h2>
          <p className="text-xs text-muted mb-4">Execute this single bash command in your terminal with Ollama installed to pull quantized GGUF weights directly into local RAM:</p>
          <div className={`bento-card ${s.codeCard} bg-zinc-900 border border-accent/50 p-6 shadow-xl`}>
            <pre className={`${s.codeLg} text-emerald-400 font-mono font-bold text-xl`}>
              ollama run DBERT/DBERT_AI
            </pre>
          </div>
          <div className="mt-4 flex justify-between text-xs font-mono text-muted">
            <span>Runtime Requirement: &ge; 8GB Unified VRAM</span>
            <span>Quantization Formats: 4-bit / 8-bit GGUF</span>
          </div>
        </div>
      </div>

      {/* Born-From Origin Section (Operational Provenance) */}
      <div className="container pad-block">
        <div className="doclabel mb-2">§ 03 — OPERATIONAL PROVENANCE &amp; STUDIO ORIGIN</div>
        <h2 className="section-title mb-2">Born From Powering Real Industrial Studio Software</h2>
        <p className="prose-sm text-muted mb-6 max-w-3xl">
          At DBERT Labs, we enforce a definitive operational doctrine: <strong>we construct, deploy, and execute our AI models inside our internal software operations before releasing them publicly</strong>. DBERT_AI originated directly inside our software laboratory to serve as the local inference engine driving our commercial platforms—including Document AI syntax processing and DBERT Chat agentic retrieval.
        </p>
        <div className="card p-6 bg-card border border-line flex flex-col md:flex-row gap-6 align-center">
          <div className="flex-1">
            <span className="font-mono text-xs text-accent uppercase font-bold tracking-wider">The Engineering Motivation</span>
            <p className="text-xs text-muted leading-relaxed mt-2">
              While generalist LLMs like OpenAI GPT-4 or Anthropic Claude excel at creative copywriting, they consistently introduce parsing errors and verbose markdown pleasantries when tasked with high-speed automated enterprise JSON parsing. By compiling and publishing DBERT_AI on the Ollama registry, we provide our incubated startup pioneers and industrial apprentices with a lightweight, razor-sharp model weight checkpoint engineered strictly for structured algorithmic precision and maximum token throughput.
            </p>
            <div className="stack-h gap-4 mt-4 flex flex-wrap gap-4">
              <Link href="/ai-solutions/products/document-ai" className="accent-link text-xs font-mono font-medium">See DBERT_AI Powering Document AI &rarr;</Link>
              <Link href="/learners/courses/ai-agent-development" className="accent-link text-xs font-mono font-medium">Learn to Build Agents with DBERT_AI &rarr;</Link>
            </div>
          </div>
        </div>
      </div>

      {/* Specs Breakdown (Primary BG) */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 04 — ARCHITECTURAL CAPABILITIES</div>
        <h2 className="section-title mb-4">
          Model Architectural Specializations
        </h2>
        <div className="bento-grid-3">
          <div className="bento-card">
            <h3 className="block-title font-mono text-sm uppercase text-white mb-2">
              1. Deterministic JSON Output
            </h3>
            <p className="prose-sm text-muted">
              DBERT_AI is fine-tuned to return predictable JSON structures, eliminating parsing exceptions commonly encountered when using verbose general-purpose models.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Generates pristine JSON schemas and nested arrays</li>
              <li>&bull; Zero introductory conversational pleasantries</li>
              <li>&bull; Optimal for automated database webhooks</li>
            </ul>
          </div>

          <div className="bento-card">
            <h3 className="block-title font-mono text-sm uppercase text-white mb-2">
              2. Code Vetting &amp; Audits
            </h3>
            <p className="prose-sm text-muted">
              Trained across massive repositories of verified production code, helping developers isolate logic vulnerabilities and verify container deployment scripts.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Isolates syntax defects and SQL query bottlenecks</li>
              <li>&bull; Generates and verifies Docker build architectures</li>
              <li>&bull; Delivers precise line-by-line engineering audits</li>
            </ul>
          </div>

          <div className="bento-card">
            <h3 className="block-title font-mono text-sm uppercase text-white mb-2">
              3. Multi-Agent Workflows
            </h3>
            <p className="prose-sm text-muted">
              Integrate DBERT_AI into stateful multi-agent frameworks. The model manages context token limits efficiently, keeping response latencies ultra-low.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Natively optimized for CrewAI agent state networks</li>
              <li>&bull; Sub-1.5s response latency on bare-metal hardware</li>
              <li>&bull; Strict adherence to custom system role prompts</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Security Rigor & Model Defense Section */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 05 — SECURITY RIGOR &amp; RUNTIME DEFENSE</div>
        <h2 className="section-title mb-2">Hardening Local Inference Deployments</h2>
        <p className="prose-sm text-muted mb-6 max-w-2xl">
          Deploying AI models locally eliminates third-party cloud data risks, but requires solid infrastructure zoning to protect internal server registers from malicious prompt injection and denial-of-service memory overload.
        </p>
        <div className="grid gap-6 md:grid-cols-2 my-4">
          <div className="card p-6 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-2">Memory Sandboxing &amp; Container Isolation</h4>
            <p className="text-xs text-muted">
              When executing DBERT_AI via Ollama or vLLM container runtimes, inference ports operate within restricted Linux namespace boundaries. Even during intense high-load concurrent queries, host system registers remain mathematically isolated from container memory buffers.
            </p>
          </div>
          <div className="card p-6 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-2">Zero External Telemetry Pingbacks</h4>
            <p className="text-xs text-muted">
              Unlike commercial desktop applications and API wrappers that silently transmit usage telemetry back to cloud vendors, DBERT_AI is 100% self-contained. Your confidential corporate queries and retrieved vector embeddings remain sealed inside your local hardware array.
            </p>
          </div>
        </div>
      </div>

      {/* Commercial Fine-Tuning Engagement Structures */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 06 — COMMERCIAL FINE-TUNING &amp; CUSTOMIZATION</div>
        <h2 className="section-title mb-2">Tailor DBERT_AI to Your Enterprise Domain</h2>
        <p className="prose-sm text-muted mb-6 max-w-2xl">
          While DBERT_AI base weights are free to download and run locally, enterprises can engage our AI laboratory to execute custom LoRA domain training loops or procure private server deployments.
        </p>
        <div className="grid gap-6 md:grid-cols-3 my-6">
          <div className="card p-6 bg-card border border-line flex flex-col justify-between">
            <div>
              <span className="font-mono text-xs text-muted uppercase font-bold">Base Open Model</span>
              <div className="text-2xl font-mono font-bold text-emerald-400 mt-2 mb-1">₹0 <span className="text-xs text-muted font-normal">open download</span></div>
              <p className="text-xs text-muted mt-2">Unrestricted access to download and execute DBERT_AI weight checkpoints directly via the public Ollama terminal repository.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>Zero per-token recurring commercial royalties</li>
                <li>4-bit &amp; 8-bit GGUF quantization weight files</li>
                <li>Optimized for CrewAI &amp; LangChain pipelines</li>
              </ul>
            </div>
            <a href="https://ollama.com/DBERT/DBERT_AI" target="_blank" rel="noopener noreferrer" className="btn btn-outline w-full mt-4">Pull From Ollama ↗</a>
          </div>

          <div className="card p-6 bg-card border-2 border-accent relative flex flex-col justify-between">
            <div className="absolute -top-3 right-4 bg-accent text-zinc-950 font-mono text-[10px] uppercase font-bold px-2 py-0.5 rounded">Specialized</div>
            <div>
              <span className="font-mono text-xs text-accent uppercase font-bold">Custom LoRA Adapter Sprint</span>
              <div className="text-2xl font-mono font-bold text-white mt-2 mb-1">₹75,000 <span className="text-xs text-muted font-normal">sprint fee</span></div>
              <p className="text-xs text-muted mt-2">Concentrated 14-day training sprint to layer custom domain knowledge adapters over DBERT_AI foundational reasoning logic.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>10,000 corporate domain records instruction formatted</li>
                <li>LoRA adapter training on studio GPU clusters</li>
                <li>Delivered as proprietary compiled GGUF checkpoint</li>
              </ul>
            </div>
            <Link href="/about/contact" className="btn btn-primary w-full mt-4">Book LoRA Sprint &rarr;</Link>
          </div>

          <div className="card p-6 bg-card border border-line flex flex-col justify-between">
            <div>
              <span className="font-mono text-xs text-muted uppercase font-bold">Venture Co-Development</span>
              <div className="text-2xl font-mono font-bold text-white mt-2 mb-1">Included</div>
              <p className="text-xs text-muted mt-2">Incubated startup portfolio ventures receive complete custom fine-tuning and bare-metal server deployments natively bundled into equity co-development.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>0% upfront out-of-pocket custom training fees</li>
                <li>Dedicated senior AI research engineering squad</li>
                <li>Up to ₹5,00,000 in bundled compute micro-grants</li>
              </ul>
            </div>
            <Link href="/startups/register" className="btn btn-outline w-full mt-4">Apply For Incubation &rarr;</Link>
          </div>
        </div>
      </div>

      {/* FAQ Accordion Section */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 07 — MODEL KNOWLEDGE BASE</div>
        <h2 className="section-title mb-4">Frequently Asked Questions</h2>
        <div className="measure">
          <FAQAccordion items={faqs} />
        </div>
      </div>

      {/* Related Solutions & Academy Mesh */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 08 — RELATED AI SYSTEMS &amp; ACADEMY COURSES</div>
        <h2 className="section-title mb-4">Explore Complementary Capabilities</h2>
        <div className="grid gap-4 md:grid-cols-3">
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">5-Stage Training Pipeline</h4>
            <p className="text-xs text-muted mb-3">Audit the exact data sanitization, instruction formatting, and quantization lifecycle used to engineer DBERT_AI.</p>
            <Link href="/ai-solutions/llm-training/pipeline" className="accent-link text-xs">View Training Pipeline &rarr;</Link>
          </div>
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">Private Bare-Metal Hosting</h4>
            <p className="text-xs text-muted mb-3">Learn about our high-availability hardware server racks and zero-trust VPC environments designed for local models.</p>
            <Link href="/ai-solutions/llm-training/private-hosting" className="accent-link text-xs">View Hardware Hosting &rarr;</Link>
          </div>
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">Python Automation Training</h4>
            <p className="text-xs text-muted mb-3">Master foundational Linux terminal scripts, Python syntax, and Ollama execution registries in our Launchpad program.</p>
            <Link href="/learners/courses/python-automation" className="accent-link text-xs">Explore Python Course &rarr;</Link>
          </div>
        </div>
      </div>

      {/* Action Call */}
      <div className="container pb-block pt-8 border-t border-line">
        <div className="doclabel mb-2">§ 09 — INITIATE MODEL DEPLOYMENT</div>
        <div className="bento-card callout-plain p-8 bg-zinc-900 border border-line rounded-lg text-center">
          <h2 className="card-title text-3xl font-mono font-bold text-white mb-2">Deploy DBERT_AI Inside Your Enterprise Today</h2>
          <p className="page-lede text-sm text-muted max-w-2xl mx-auto mb-6">
            Have a custom database schema, API business logic, or confidential historical log dataset? Partner with DBERT Labs to train an open-weights model tailored specifically to your corporate workflows.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <Link href="/startups/register" className="btn btn-primary btn-lg">Register Your Startup &rarr;</Link>
            <Link href="/ai-solutions/consultation" className="btn btn-outline btn-lg">Book AI Consultation &rarr;</Link>
          </div>
        </div>
      </div>
    </div>
  );
}

