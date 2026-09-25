import React from 'react';
import Link from 'next/link';
import StepTimeline from '@/components/ui/StepTimeline';
import FAQAccordion from '@/components/ui/FAQAccordion';
import { pageMetadata } from '@/lib/seo';
import { Monitor, Package, Shield, Server, Database, Lock, Cpu } from 'lucide-react';

export const metadata = pageMetadata('/startups/services/infrastructure');

export default function InfrastructureServicePage() {
  const steps = [
    { number: '01', title: 'Compute Audit & Sizing', description: 'We evaluate your context window targets, concurrent query volumes, and parameter sizes to architect optimal bare-metal GPU instance specifications.' },
    { number: '02', title: 'Private VPC & Reverse Proxy Setup', description: 'We configure isolated Virtual Private Clouds, Nginx reverse proxies, SSL TLS encryption rules, and strict SSH zero-trust access boundaries.' },
    { number: '03', title: 'Containerized Runtime Deployment', description: 'We spin up Dockerized localized model runtimes (Ollama, vLLM), optimize PostgreSQL pgvector indexes, and execute simulated high-load burst tests.' }
  ];

  const faqs = [
    {
      question: 'Why do you recommend local open-weights serving over cloud APIs like OpenAI or Anthropic?',
      answer: 'Public commercial APIs present three substantial enterprise threats: escalating per-token inference costs at scale, arbitrary latency throttling during peak hours, and unencrypted exposure of sensitive customer database query payloads. Serving open-weights models (such as Llama-3 and Qwen) locally via vLLM or Ollama inside an isolated VPC guarantees total mathematical privacy and fixed, predictable infrastructure costs.'
    },
    {
      question: 'Which cloud GPU platforms and instance configurations do you deploy for incubated startups?',
      answer: 'We deploy multi-cloud compute architecture across AWS EC2 (G4dn, G5, and P4 instances), GCP, RunPod bare-metal GPU nodes, and Lambda Labs. By automating dynamic node scaling and spot-instance redundancy, we reduce computational operational costs by up to 60% compared to default cloud provider setups.'
    },
    {
      question: 'How do you structure high-performance vector databases for enterprise RAG retrieval?',
      answer: 'We build hardened PostgreSQL database clusters equipped with the pgvector extension. We configure specialized indexing algorithms—including Hierarchical Navigable Small World (HNSW) and Inverted File Flat (IVFFlat)—to guarantee sub-100ms semantic search queries even across multi-million document embedding vector stores.'
    },
    {
      question: 'How do you protect private model runtimes from distributed denial-of-service (DDoS) attacks?',
      answer: 'All backend model serving endpoints reside behind strict Nginx reverse proxies configured with rate-limiting token buckets, IP filtering, and SSL TLS termination. External requests never communicate directly with bare-metal GPU inference ports.'
    },
    {
      question: 'Is continuous infrastructure health monitoring and database backup management included?',
      answer: 'Yes. Every enterprise infrastructure build incorporates automated daily automated encrypted snapshot backups for PostgreSQL vector volumes, alongside real-time Prometheus and Grafana alerting dashboards tracking VRAM consumption, token generation throughput, and error rates.'
    }
  ];

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Service',
        name: 'DBERT Cloud & AI Infrastructure Engineering & GPU Provisioning',
        serviceType: 'VPC Design, Localized LLM Hosting, Bare-Metal GPU Provisioning, Vector Database Clustering',
        description: 'Hardened enterprise Cloud and AI server infrastructure engineering: provision bare-metal GPU clusters, deploy secure Ollama and vLLM local serving runtimes, and scale PostgreSQL pgvector databases.',
        provider: {
          '@type': 'Organization',
          name: 'DBERT Labs Industrial Training & Venture Studio',
          url: 'https://dbert.online'
        },
        offers: {
          '@type': 'Offer',
          category: 'Venture Infrastructure Engineering',
          price: '55000',
          priceCurrency: 'INR',
          description: 'Flat-fee VPC setup and GPU clustering suite or fully bundled within equity studio incubation',
          url: 'https://dbert.online/startups/services/infrastructure'
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

      {/* Hero Header Section & What It Is */}
      <div className="container page-head">
        <div className="doclabel">
          § 01 — VENTURE INFRASTRUCTURE SERVICE <span className="rev">rev: 2026.2</span>
        </div>
        <h1 className="page-title">
          Deploy Production AI at Scale &mdash; Reliably &amp; Securely
        </h1>
        <p className="lede-wide">
          De-risk enterprise server scaling operations and eliminate external token dependency. We engineer isolated Virtual Private Cloud (VPC) architectures, provision cost-optimized bare-metal GPU clusters, configure containerized Ollama/vLLM open-weights runtimes, and harden high-throughput pgvector relational databases.
        </p>
      </div>

      {/* Born-From Origin Section (Operational Provenance) */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 02 — OPERATIONAL PROVENANCE &amp; ORIGIN</div>
        <h2 className="section-title mb-2">Born From Operating Real AI Server Laboratories</h2>
        <p className="prose-sm text-muted mb-6 max-w-3xl">
          At DBERT Labs, we abide by a definitive industrial ethos: <strong>we construct and manage our server clusters in our own physical and cloud laboratories before designing startup topologies</strong>. Our Cloud &amp; AI Infrastructure service originated directly from administering our Private LLM Hosting hardware arrays and industrial training server networks, where we process massive concurrent student compiling workloads and enterprise document inference tasks daily.
        </p>
        <div className="card p-6 bg-card border border-line flex flex-col md:flex-row gap-6 align-center">
          <div className="flex-1">
            <span className="font-mono text-xs text-accent uppercase font-bold tracking-wider">The Engineering Motivation</span>
            <p className="text-xs text-muted leading-relaxed mt-2">
              We observed that pre-seed AI startups were frequently crippled by exorbitant cloud hosting bills—spending thousands of dollars monthly on underutilized GPU instances and inefficient API wrappers. By deploying containerized local model inference engines inside custom VPC architectures, we empower our incubated portfolio ventures to run enterprise-grade artificial intelligence models at a fraction of the operating cost of commercial API providers.
            </p>
            <div className="stack-h gap-4 mt-4">
              <Link href="/ai-solutions/llm-training/private-hosting" className="accent-link text-xs font-mono font-medium">Inspect Our Private Bare-Metal LLM Hardware &rarr;</Link>
              <Link href="/ai-solutions/products/document-ai" className="accent-link text-xs font-mono font-medium">Explore Document AI Production Infrastructure &rarr;</Link>
            </div>
          </div>
        </div>
      </div>

      {/* Key Metrics Grid (Secondary BG) - Why It Matters */}
      <div className="section-band border-t border-b border-line">
        <div className="container">
          <div className="doclabel mb-2">§ 03 — INFRASTRUCTURE BENCHMARKS &amp; SECURITY</div>
          <div className="bento-grid-3">
            <div className="bento-card center">
              <span className="icon-chip"><Monitor aria-hidden="true" /></span>
              <h3 className="accent-note">60% GPU Cost Saving</h3>
              <p className="text-sm">Optimal sizing and multi-cloud provisioning of bare-metal GPU instances (AWS, RunPod, GCP) tailored precisely to model weight parameters.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><Shield aria-hidden="true" /></span>
              <h3 className="accent-note">Complete VPC Isolation</h3>
              <p className="text-sm">Establish airtight virtual private network perimeter boundaries, ensuring unencrypted customer query logs never escape your private network.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><Package aria-hidden="true" /></span>
              <h3 className="accent-note">vLLM &amp; Ollama Serving</h3>
              <p className="text-sm">Deploy containerized localized model runtimes behind Nginx reverse proxies to maintain fast, predictable concurrent token generation velocities.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Core Deliverables (Primary BG) */}
      <div className="container pad-block">
        <div className="doclabel mb-2">§ 04 — SERVER ARCHITECTURE DELIVERABLES</div>
        <h2 className="section-title mb-4">
          Production Infrastructure That Handles Carrier-Grade Traffic
        </h2>
        <div className="bento-grid-3">
          <div className="bento-card">
            <h4 className="block-title font-mono text-sm uppercase text-white mb-2">
              1. GPU Compute Provisioning
            </h4>
            <p className="prose-sm text-muted">
              We precisely size your compute workloads—establishing AWS EC2 instances (G4dn, G5, P4 VRAM capacities) or high-efficiency bare-metal RunPod clusters to fit your exact context horizons.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Strict VRAM memory requirement calculations</li>
              <li>&bull; AWS, GCP, RunPod &amp; Lambda Labs cluster setups</li>
              <li>&bull; Automated spot-instance scaling &amp; failover rules</li>
            </ul>
          </div>

          <div className="bento-card">
            <h4 className="block-title font-mono text-sm uppercase text-white mb-2">
              2. Private Serving Environments
            </h4>
            <p className="prose-sm text-muted">
              Host open-weights neural networks safely. We spin up localized model serving container registries using Ollama or vLLM, locking down data privacy and eliminating external token fees.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Localized serving of Llama-3, Mistral, Qwen models</li>
              <li>&bull; Nginx reverse proxies with SSL TLS terminating gates</li>
              <li>&bull; Model weight quantization (4-bit/8-bit GGUF/AWQ)</li>
            </ul>
          </div>

          <div className="bento-card">
            <h4 className="block-title font-mono text-sm uppercase text-white mb-2">
              3. Vector Database Clustering
            </h4>
            <p className="prose-sm text-muted">
              Scale enterprise RAG queries without bottlenecks. We deploy high-throughput PostgreSQL relational database clusters natively equipped with optimized pgvector semantic indexing.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; HNSW &amp; IVFFlat vector search indexing structures</li>
              <li>&bull; Containerized connection pooling (PgBouncer)</li>
              <li>&bull; Automated encrypted daily snapshot volume backups</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Enterprise Security & Risk Mitigation */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 05 — SECURITY RIGOR &amp; INFRASTRUCTURE DEFENSE</div>
        <h2 className="section-title mb-2">Eliminating Single Point of Failures &amp; Leaks</h2>
        <p className="prose-sm text-muted mb-6 max-w-2xl">
          An insecure AI server setup can lead to unauthorized data exfiltration, model extraction, and devastating DDoS API token consumption bills. We erect carrier-grade defensive boundaries.
        </p>

        <div className="grid gap-6 md:grid-cols-2 my-4">
          <div className="card p-6 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-2">Zero-Trust Network Zoning</h4>
            <p className="text-xs text-muted">
              We implement rigid zero-trust security perimeter policies. Database read/write replicas and localized GPU inference ports remain isolated inside private subnet firewalls, accessible exclusively via authenticated SSH Bastion gates and mutual TLS connections.
            </p>
          </div>
          <div className="card p-6 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-2">Rate-Limit Burst Throttling</h4>
            <p className="text-xs text-muted">
              By standing up specialized algorithmic rate-limiting reverse proxies at the ingress gate, our architecture absorbs unexpected spikes in incoming client traffic—protecting backend inference containers from out-of-memory kernel panics and computational freeze-ups.
            </p>
          </div>
        </div>
      </div>

      {/* Pricing & Incubation Engagement Structures */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 06 — COMMERCIAL INFRASTRUCTURE TIERING</div>
        <h2 className="section-title mb-2">Transparent Server Engineering Packages</h2>
        <p className="prose-sm text-muted mb-6 max-w-2xl">
          Select between specialized standalone infrastructure sprints or obtain comprehensive server provisioning natively bundled into DBERT equity studio incubation.
        </p>

        <div className="grid gap-6 md:grid-cols-3 my-6">
          <div className="card p-6 bg-card border border-line flex flex-col justify-between">
            <div>
              <span className="font-mono text-xs text-muted uppercase">VPC Setup Sprint</span>
              <div className="text-2xl font-mono font-bold text-white mt-2 mb-1">₹55,00,0 <span className="text-xs text-muted font-normal">flat fee</span></div>
              <p className="text-xs text-muted mt-2">Concentrated 7-day engineering sprint to stand up isolated Virtual Private Cloud boundaries and Nginx gateways.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>AWS/GCP Virtual Private Cloud network setup</li>
                <li>SSL TLS encryption &amp; SSH Bastion zoning</li>
                <li>PostgreSQL pgvector relational container setup</li>
              </ul>
            </div>
            <Link href="/about/contact" className="btn btn-outline w-full mt-4">Book VPC Sprint &rarr;</Link>
          </div>

          <div className="card p-6 bg-card border-2 border-accent relative flex flex-col justify-between">
            <div className="absolute -top-3 right-4 bg-accent text-zinc-950 font-mono text-[10px] uppercase font-bold px-2 py-0.5 rounded">High Throughput</div>
            <div>
              <span className="font-mono text-xs text-accent uppercase">Full Local LLM Suite</span>
              <div className="text-2xl font-mono font-bold text-emerald-400 mt-2 mb-1">₹1,25,000 <span className="text-xs text-muted font-normal">package</span></div>
              <p className="text-xs text-muted mt-2">Comprehensive bare-metal GPU clustering and open-weights localized serving deployment for scaling SaaS systems.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>RunPod/AWS multi-node GPU cluster setup</li>
                <li>Ollama &amp; vLLM high-speed localized endpoints</li>
                <li>HNSW pgvector indexing &amp; automated backups</li>
              </ul>
            </div>
            <Link href="/about/contact" className="btn btn-primary w-full mt-4">Inquire LLM Suite &rarr;</Link>
          </div>

          <div className="card p-6 bg-card border border-line flex flex-col justify-between">
            <div>
              <span className="font-mono text-xs text-muted uppercase">Incubated Venture</span>
              <div className="text-2xl font-mono font-bold text-white mt-2 mb-1">Included</div>
              <p className="text-xs text-muted mt-2">Full end-to-end cloud GPU infrastructure design and persistent MLOps monitoring bundled directly into DBERT equity incubation.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>0% out-of-pocket setup engineering fees</li>
                <li>Access to DBERT micro-grants for compute costs</li>
                <li>90-day post-launch container health monitoring</li>
              </ul>
            </div>
            <Link href="/startups/register" className="btn btn-outline w-full mt-4">Apply For Incubation &rarr;</Link>
          </div>
        </div>
      </div>

      {/* Timeline Section (Secondary BG) */}
      <div className="band-top border-t border-line">
        <div className="container-sm">
          <div className="doclabel mb-2">§ 07 — DEPLOYMENT ROADMAP</div>
          <h2 className="subsection-title mb-4">
            Our Infrastructure Deployment Pipeline
          </h2>
          <StepTimeline steps={steps} />
        </div>
      </div>

      {/* Frequently Asked Questions Section */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 08 — INFRASTRUCTURE KNOWLEDGE BASE</div>
        <h2 className="section-title mb-4">Frequently Asked Questions</h2>
        <div className="measure">
          <FAQAccordion items={faqs} />
        </div>
      </div>

      {/* Related Solutions Mesh */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 09 — RELATED INCUBATION SERVICES &amp; PRODUCTS</div>
        <h2 className="section-title mb-4">Explore Complementary Venture Services</h2>
        <div className="grid gap-4 md:grid-cols-3">
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">Private LLM Hosting</h4>
            <p className="text-xs text-muted mb-3">Learn about our physical bare-metal enterprise hosting arrays designed for sovereign AI operational secrecy.</p>
            <Link href="/ai-solutions/llm-training/private-hosting" className="accent-link text-xs">View Hardware Hosting &rarr;</Link>
          </div>
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">Technical Architecture Build</h4>
            <p className="text-xs text-muted mb-3">Pair infrastructure setups directly with senior software engineering squads writing features for your main codebase.</p>
            <Link href="/startups/services/technical" className="accent-link text-xs">View Technical Service &rarr;</Link>
          </div>
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">Funding &amp; Micro-Grants</h4>
            <p className="text-xs text-muted mb-3">Access dilution-free micro-grants ranging up to ₹5,00,000 directly allocated to offset your GPU server bills.</p>
            <Link href="/startups/services/funding" className="accent-link text-xs">View Funding Support &rarr;</Link>
          </div>
        </div>
      </div>

      {/* CTA Block (Primary BG) */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 10 — INITIATE INFRASTRUCTURE BUILD</div>
        <div className="bento-card callout">
          <h2 className="card-title">Go Live with Complete Operational Assurance</h2>
          <p className="page-lede">
            Ready to secure data compliance, provision cost-optimized bare-metal GPU clusters, configure vector database registers, and serve models locally? Apply for DBERT Incubation today.
          </p>
          <Link href="/startups/register" className="btn btn-primary btn-lg mt-4">Register Your Startup &rarr;</Link>
        </div>
      </div>
    </div>
  );
}

