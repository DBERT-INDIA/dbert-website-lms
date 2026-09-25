import React from 'react';
import Link from 'next/link';
import FAQAccordion from '@/components/ui/FAQAccordion';
import { pageMetadata } from '@/lib/seo';
import s from '../../learners.module.css';
import { Cpu, Zap, Activity, Briefcase, GitBranch } from 'lucide-react';

export const metadata = pageMetadata('/learners/courses/machine-learning');

export default function MachineLearningCoursePage() {
  const faqs = [
    {
      question: 'What mathematical or coding knowledge do I need to begin this course?',
      answer: 'A working understanding of basic linear algebra and statistics (mean, variance, vectors), along with foundational Python programming (NumPy/Pandas). Candidates with no prior Python experience should begin with our Launchpad foundation track.'
    },
    {
      question: 'Do we train models from scratch or perform parameter-efficient fine-tuning (PEFT)?',
      answer: 'While we cover core neural network architectures and loss functions, production engineering emphasizes Parameter-Efficient Fine-Tuning (LoRA & QLoRA) on modern open-weights foundation models (Llama-3, Mistral) to deliver commercial domain adaptations.'
    },
    {
      question: 'Can I run the fine-tuning exercises on consumer laptop GPUs or cloud environments?',
      answer: 'Yes. Our labs leverage 4-bit and 8-bit quantization (QLoRA) enabling fine-tuning on cost-effective GPUs (NVIDIA RTX series or Google Colab T4/A100 instances), with local inference served through Ollama.'
    },
    {
      question: 'What production repositories will I inspect and contribute to?',
      answer: 'You will work directly with patterns from our live intern repositories: Gayatri-Tutor-V3 (synthetic data generation & local LLaMA fine-tuning) and Alkame Nifty-50 (ensemble ML predictors, backtesting & feature engineering).'
    },
    {
      question: 'How do employers verify my ML credentials?',
      answer: 'Graduates receive a cryptographically verified credential serial number that recruiters can audit instantly at dbert.online/verify, coupled with verifiable Git commits.'
    }
  ];

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Course',
        name: 'Machine Learning & LLM Fine-Tuning Systems Track',
        description: 'Industrial engineering course teaching end-to-end machine learning pipelines, synthetic instruction curation, PEFT/LoRA fine-tuning on open-weights models, and quantitative evaluation.',
        provider: {
          '@type': 'Organization',
          name: 'DBERT Labs Industrial Training & Venture Studio',
          url: 'https://dbert.online'
        },
        courseCode: 'DBERT-ENG-MLFT-2026',
        courseMode: 'Blended (Cohort Sprints & GPU Lab Work)',
        educationalCredentialAwarded: 'Verified Machine Learning Systems Professional Diploma',
        offers: {
          '@type': 'Offer',
          category: 'Tuition Fee',
          price: '34000',
          priceCurrency: 'INR',
          availability: 'https://schema.org/InStock',
          validFrom: '2026-01-01',
          url: 'https://dbert.online/learners/courses/machine-learning'
        }
      },
      {
        '@type': 'FAQPage',
        mainEntity: faqs.map((f) => ({
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
          § 01 — CAREER TRACK <span className="rev">rev: 2026.2</span>
        </div>
        <h1 className="page-title">
          Become a Machine Learning &amp; Fine-Tuning Engineer
        </h1>
        <p className={s.courseTagline}>
          ₹6,00,000 – ₹15,00,000 LPA Verified Average Starting Remuneration
        </p>
        <p className={s.courseLede}>
          Master classical machine learning architectures, statistical feature engineering, synthetic instruction dataset curation, and parameter-efficient fine-tuning (PEFT/LoRA) on open-weights models.
        </p>
      </div>

      {/* Key Metrics Grid */}
      <div className="section-band">
        <div className="container">
          <div className="bento-grid-3">
            <div className="bento-card center">
              <span className="icon-chip"><Cpu aria-hidden="true" /></span>
              <h3 className="accent-note">Open-Weights Fine-Tuning</h3>
              <p className="text-sm">Fine-tune Llama-3 and Mistral models using LoRA and QLoRA on domain-specific instruction datasets.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><Activity aria-hidden="true" /></span>
              <h3 className="accent-note">Feature &amp; Loss Engineering</h3>
              <p className="text-sm">Build reproducible data cleansing pipelines, extract statistical features, and monitor convergence loss curves.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><Briefcase aria-hidden="true" /></span>
              <h3 className="accent-note">Audited Git Portfolio</h3>
              <p className="text-sm">Ship trained model adapters, evaluation benchmarks, and inference endpoints to public GitHub repositories.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Reference Repo Spotlight */}
      <div className="container pad-block">
        <div className="card p-6 bg-card border border-line flex flex-col md:flex-row gap-6 items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <span className="badge badge-emerald text-xs font-mono">Reference Repositories</span>
              <span className="font-mono text-sm text-white font-bold">Gayatri-Tutor-V3 &amp; Alkame-Nifty-50</span>
            </div>
            <p className="text-xs text-muted leading-relaxed mb-4">
              Learn from real intern implementations: synthetic instruction dataset generation and Llama fine-tuning from Gayatri-Tutor-V3, combined with feature engineering, ensemble model training, and backtesting from Alkame-Nifty-50.
            </p>
            <div className="flex flex-wrap gap-2">
              {['Synthetic Data Curation', 'LoRA / QLoRA', 'GGUF Quantization', 'Ensemble Predictors', 'Model Evaluation'].map((tag, idx) => (
                <span key={idx} className="text-[11px] px-2 py-0.5 rounded bg-raise border border-line text-zinc-300 font-mono">
                  {tag}
                </span>
              ))}
            </div>
          </div>
          <div className="flex flex-col gap-2 self-start">
            <a
              href="https://github.com/Gayatri-Education/Gayatri-Tutor-V3"
              target="_blank"
              rel="noopener noreferrer"
              className="btn btn-outline btn-sm font-mono text-xs inline-flex items-center gap-2 whitespace-nowrap"
            >
              <GitBranch className="w-3.5 h-3.5" />
              Gayatri-Tutor-V3 Repo &rarr;
            </a>
            <a
              href="https://github.com/Alkameinc/alkame-nifty-50-educational"
              target="_blank"
              rel="noopener noreferrer"
              className="btn btn-ghost btn-sm font-mono text-xs inline-flex items-center gap-2 whitespace-nowrap"
            >
              <GitBranch className="w-3.5 h-3.5" />
              Alkame Nifty-50 Repo &rarr;
            </a>
          </div>
        </div>
      </div>

      {/* Course Curriculum & Skills */}
      <div className="container pad-block">
        <div className="doclabel mb-2">§ 02 — TECHNICAL CURRICULUM ARCHITECTURE</div>
        <h2 className="section-title mb-4">
          What You&apos;ll Master
        </h2>
        <div className="bento-grid-2">
          <div className="bento-card">
            <h3 className="block-title">
              1. Applied Machine Learning &amp; Feature Pipelines
            </h3>
            <p className="prose-sm text-muted">
              Wrangle complex real-world datasets with NumPy and Pandas. Implement feature extraction, categorical encoding, cross-validation, and train ensemble models (Random Forests, XGBoost).
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Statistical data cleansing &amp; missing value imputation</li>
              <li>&bull; Feature engineering, rolling transformations &amp; correlation analysis</li>
              <li>&bull; Precision, Recall, F1, ROC-AUC, and backtest performance auditing</li>
            </ul>
          </div>

          <div className="bento-card">
            <h3 className="block-title">
              2. Open-Weights LLM Fine-Tuning &amp; Quantization
            </h3>
            <p className="prose-sm text-muted">
              Curate domain-specific instruction datasets, format JSONL training pairs, and apply LoRA/QLoRA adapters to open-weights models. Export 4-bit GGUF models for local execution.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Synthetic instruction dataset generation &amp; quality filtering</li>
              <li>&bull; Parameter-Efficient Fine-Tuning (PEFT/LoRA/QLoRA) with PyTorch</li>
              <li>&bull; Quantization to GGUF and local inference deployment via Ollama</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Capstone Projects Section */}
      <div className="section-band-lg border-t border-b border-line">
        <div className="container">
          <div className="doclabel mb-2">§ 03 — CAPSTONE PRODUCTION PROJECTS</div>
          <h2 className="section-title mb-4">
            Production Projects You&apos;ll Ship to Your Git Repository
          </h2>
          <div className="bento-grid-2">
            <div className="bento-card on-ink">
              <span className="pill">Capstone Project 1 &middot; LLM Fine-Tuning</span>
              <h3 className={s.projectTitle}>Domain-Adapted Technical Tutor Model</h3>
              <p className="prose-sm text-muted">
                A custom fine-tuned Llama-3 model trained on synthetic programming exercises, evaluated against standard benchmarks, quantized into 4-bit GGUF, and deployed with a local REST inference endpoint.
              </p>
            </div>
            <div className="bento-card on-ink">
              <span className="pill">Capstone Project 2 &middot; Quantitative ML</span>
              <h3 className={s.projectTitle}>Multi-Factor Market Ensemble Predictor</h3>
              <p className="prose-sm text-muted">
                A complete financial machine learning pipeline featuring feature extraction, historical backtesting, and ensemble model prediction deployed with interactive performance dashboards.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Tuition Card */}
      <div className="container pad-block">
        <div className="doclabel mb-2">§ 04 — TUITION &amp; ADMISSION</div>
        <h2 className="section-title mb-2">Transparent Indian Tuition &amp; Flexible EMI</h2>
        <p className="prose-sm text-muted mb-6 max-w-2xl">
          Complete upfront transparency without hidden fees. Access live cohort sprints, GPU lab environments, and expedited startup referral opportunities.
        </p>

        <div className="grid gap-6 md:grid-cols-2 my-6">
          <div className="card p-6 bg-card border border-line">
            <span className="font-mono text-xs text-muted uppercase tracking-wider">One-Time Upfront Tuition</span>
            <div className="text-3xl font-mono font-bold text-white mt-2 mb-1">₹34,000 <span className="text-sm text-muted font-normal">INR (All Inclusive)</span></div>
            <p className="text-xs text-muted mb-4">Includes full synchronous cohort sessions, cloud GPU compute allocations, code review check-ins, and permanent credential registration.</p>
            <Link href="/learners/launchpad?domain=machine-learning" className="btn btn-primary w-full">
              Explore Launchpad Track &rarr;
            </Link>
          </div>

          <div className="card p-6 bg-card border-2 border-accent relative">
            <div className="absolute -top-3 right-4 bg-accent text-zinc-950 font-mono text-[10px] uppercase font-bold px-2 py-0.5 rounded">Zero-Cost EMI</div>
            <span className="font-mono text-xs text-accent uppercase tracking-wider">9-Month Installment Schedule</span>
            <div className="text-3xl font-mono font-bold text-emerald-400 mt-2 mb-1">₹3,777 <span className="text-sm text-muted font-normal">/ month (₹0 Interest)</span></div>
            <p className="text-xs text-muted mb-4">Structured through authorized Indian banking partners with minimal documentation and zero interest surcharge.</p>
            <Link href="/about/contact" className="btn btn-outline w-full">Inquire About EMI Financing</Link>
          </div>
        </div>
      </div>

      {/* Technologies Mastered */}
      <div className={`container ${s.techBlock} border-t border-line`}>
        <div className="doclabel mb-2">§ 05 — PRODUCTION TECHNOLOGIES</div>
        <h2 className={s.techHeading}>Production Technologies Mastered</h2>
        <div className={s.techRow}>
          {['PyTorch', 'Hugging Face', 'LoRA / QLoRA', 'Scikit-Learn', 'Pandas', 'NumPy', 'XGBoost', 'Ollama', 'GGUF', 'Weights & Biases', 'Docker'].map((tool, idx) => (
            <span key={idx} className={s.techChip}>
              {tool}
            </span>
          ))}
        </div>
      </div>

      {/* FAQ Section */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 06 — KNOWLEDGE BASE</div>
        <h2 className="section-title mb-4">Frequently Asked Questions</h2>
        <div className="measure">
          <FAQAccordion items={faqs} />
        </div>
      </div>

      {/* CTA */}
      <div className="container pb-block">
        <div className="bento-card callout-plain p-8 border border-line bg-card text-center">
          <div className="doclabel mb-1">§ 07 — ENROLL IN INDUSTRIAL TRAINING</div>
          <h2 className="card-title text-2xl font-bold text-white mb-2">Launch Your Machine Learning Career</h2>
          <p className="page-lede text-sm text-muted max-w-xl mx-auto mb-6">
            Ready to fine-tune open-weights models, architect robust ML pipelines, and build an auditable GitHub portfolio? Enroll today in DBERT Industrial Training.
          </p>
          <div className="stack-h gap-4 justify-center">
            <Link href="/learners/launchpad?domain=machine-learning" className="btn btn-primary btn-lg">
              Start 2-Month Launchpad Track &rarr;
            </Link>
            <Link href="/learners/courses" className="btn btn-outline btn-lg">
              View All 6 Courses
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
