'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { 
  Database, 
  FileCode, 
  Cpu, 
  LineChart, 
  PackageCheck, 
  CheckCircle2, 
  ArrowRight, 
  ShieldAlert, 
  Sparkles,
  Terminal,
  Code2
} from 'lucide-react';
import styles from './PipelineInteractiveConsole.module.css';

interface StageDetail {
  id: string;
  num: string;
  shortName: string;
  title: string;
  tagline: string;
  icon: React.ComponentType<{ size?: number; className?: string }>;
  duration: string;
  deliverableFile: string;
  specs: { label: string; value: string }[];
  description: string;
  dataSnippetTitle: string;
  beforeSnippet: string;
  afterSnippet: string;
  keyActionNotes: string[];
}

const STAGES: StageDetail[] = [
  {
    id: 'stage-1',
    num: '01',
    shortName: 'Sanitize & Dedup',
    title: 'Data Collection & Sanitization Audit',
    tagline: 'Stripping noise, HTML boilerplate, and duplicate vectors before GPU memory ingestion',
    icon: Database,
    duration: 'Days 1–3',
    deliverableFile: 'raw_sanitized_corpus.jsonl',
    specs: [
      { label: 'Deduplication Method', value: 'MinHash LSH (0.85 threshold)' },
      { label: 'Entropy Filtering', value: 'Perplexity cutoff < 120' },
      { label: 'Encoding Normalize', value: 'UTF-8 strict with NFC form' },
      { label: 'Rejection Rate', value: 'Avg 42% raw data rejected' }
    ],
    description: 'We audit raw unstructured corporate repositories, PDFs, customer tickets, and database dumps. Instead of feeding dirty scrapings into expensive GPU runs, Stage 01 purges corrupt text, strips token-hogging boilerplate, and normalizes encodings.',
    dataSnippetTitle: 'Corpus Cleansing Comparison',
    beforeSnippet: `// RAW SCRAPED INPUT (DIRTY)
{
  "html": "<div class='nav-ad'>Promo 50%</div>\\n\\nContract #9910...\\n\\nContract #9910...",
  "status": "DUPLICATE_FOUND",
  "encoding": "windows-1252"
}`,
    afterSnippet: `// SANITIZED JSONL RECORD (CLEAN)
{
  "text": "Contract terms define sovereign deployment obligations across regional node clusters.",
  "tokens": 42,
  "normalized": true
}`,
    keyActionNotes: [
      'Removes recurring boilerplate that triggers hallucination loops',
      'MinHash similarity clustering discards duplicate documents',
      'Normalizes text schemas for deterministic tokenization'
    ]
  },
  {
    id: 'stage-2',
    num: '02',
    shortName: 'PII Scrubbing',
    title: 'Instruction Formatting & PII Masking',
    tagline: 'Converting unstructured corpora into role-based instruction pairs with zero data leaks',
    icon: FileCode,
    duration: 'Days 4–5',
    deliverableFile: 'instructions_pii_masked.jsonl',
    specs: [
      { label: 'PII Masking Engine', value: 'Regex + Spacy NER Transformers' },
      { label: 'Schema Standard', value: 'ChatML (system / user / assistant)' },
      { label: 'Token Window', value: '4,096 context chunk target' },
      { label: 'Synthetic Pairs', value: 'Self-Instruct augmented' }
    ],
    description: 'Models trained on raw data leak employee names, phone numbers, and financial details. Stage 02 uses Named Entity Recognition (NER) to scrub PII deterministically and formats data into standard ChatML conversational instruction schemas.',
    dataSnippetTitle: 'PII Redaction & Role Formatting',
    beforeSnippet: `// BEFORE: SENSITIVE PRIVATE TICKET
Customer: Rajesh Sharma (98765-43210, rajesh@corp.in)
Account: Axis Bank #981023910
Query: Reset my API billing threshold.`,
    afterSnippet: `// AFTER: MASKED CHATML INSTRUCTION PAIR
{
  "messages": [
    {"role": "system", "content": "You are DBERT Financial Agent."},
    {"role": "user", "content": "Reset API billing threshold for account [ACCT_MASKED_01]"},
    {"role": "assistant", "content": "Threshold reset initiated for verified account token."}
  ]
}`,
    keyActionNotes: [
      'Deterministic entity masking prevents private data extraction',
      'Formats into system, user, and assistant conversational turns',
      'Enforces structured JSON keys for consistent API responses'
    ]
  },
  {
    id: 'stage-3',
    num: '03',
    shortName: 'LoRA / QLoRA',
    title: 'Fine-Tuning Execution (LoRA / QLoRA)',
    tagline: 'Gradient descent on multi-node NVIDIA GPUs with frozen base weights and low-rank adapters',
    icon: Cpu,
    duration: 'Days 6–9',
    deliverableFile: 'adapter_model.safetensors (24MB)',
    specs: [
      { label: 'Adapter Rank (r)', value: 'r=16, alpha=32' },
      { label: 'Target Matrices', value: 'q_proj, k_proj, v_proj, o_proj' },
      { label: 'Base Quantization', value: '4-bit NormalFloat (NF4)' },
      { label: 'Optimizer', value: 'Paged AdamW (lr=2e-4)' }
    ],
    description: 'We freeze the base foundation weights (e.g. Llama-3 8B or Qwen-2.5 14B) and inject trainable low-rank adaptation matrices. This achieves full model accuracy while slashing GPU memory requirements by 75% and preventing catastrophic forgetting.',
    dataSnippetTitle: 'PyTorch / PEFT Hyperparameters',
    beforeSnippet: `# TRADITIONAL FULL FINE-TUNING (EXPENSIVE)
Model Size: 14 Billion Parameters
Hardware: 8x H100 80GB SXM ($30,000/mo)
VRAM Consumed: 320 GB
Risk: Destroys base reasoning`,
    afterSnippet: `# DBERT EFFICIENT QLoRA EXECUTION
peft_config = LoraConfig(
    r=16, lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05, bias="none"
)
# VRAM: 18 GB on a single RTX 4090 / A10G`,
    keyActionNotes: [
      'Freezes base weights to preserve foundational reasoning logic',
      'Injects 20% conversational replay data to prevent forgetting',
      'Generates lightweight 24MB adapter file swappable in milliseconds'
    ]
  },
  {
    id: 'stage-4',
    num: '04',
    shortName: 'Benchmark & Regress',
    title: 'Empirical Benchmark & Regression Validation',
    tagline: 'Measuring classification accuracy, JSON schema validity, and latency against withheld test splits',
    icon: LineChart,
    duration: 'Days 10–12',
    deliverableFile: 'benchmark_audit_report.pdf',
    specs: [
      { label: 'Validation Split', value: '15% held-out test split' },
      { label: 'Syntax Compliance', value: '99.8% Pydantic JSON pass' },
      { label: 'Latency Benchmark', value: '48.2 tokens/sec on local GPU' },
      { label: 'Regression Check', value: 'MMLU logic delta < 0.4%' }
    ],
    description: 'We run automated evaluation suites against withheld corporate test cases. We verify that domain-specific questions are answered with >98% precision and that general logic (math, reasoning) has not degraded.',
    dataSnippetTitle: 'Automated Evaluation Harness',
    beforeSnippet: `// BASE UNTRAINED MODEL EVALUATION
Input: "Extract tax id and taxable line items"
Output: "Sure! In many jurisdictions, taxes are calculated..."
Result: ❌ FAILED (Chatty, no JSON schema)`,
    afterSnippet: `// DBERT CHECKPOINT EVALUATION
Input: "Extract tax id and taxable line items"
Output: {"tax_id": "GSTIN-07AAB", "items": [{"subtotal": 12500}]}
Result: ✅ PASSED (100% Validated against Pydantic schema)`,
    keyActionNotes: [
      'Stress-tests JSON compliance across 1,000 synthetic test cases',
      'Measures token generation velocity and memory saturation',
      'Assures zero catastrophic regression on general reasoning'
    ]
  },
  {
    id: 'stage-5',
    num: '05',
    shortName: 'Quantize & Export',
    title: 'GGUF / AWQ Quantization & Standalone Engine Deploy',
    tagline: 'Fusing adapters and exporting compiled weights for pure standalone bare-metal execution — zero Ollama or LM Studio needed',
    icon: PackageCheck,
    duration: 'Days 13–14',
    deliverableFile: 'model-q4_k_m.gguf (4.8GB)',
    specs: [
      { label: 'Export Format', value: 'GGUF / AWQ + Standalone Binary' },
      { label: 'Memory Footprint', value: 'Reduced from 16GB to 4.8GB' },
      { label: 'Runtime Engine', value: 'Native C++ / Python (No 3rd Party)' },
      { label: 'Data Egress', value: 'Zero external internet calls' }
    ],
    description: 'We fuse trained LoRA adapters directly into base weights, quantize into high-throughput 4-bit or 8-bit GGUF files, and compile a standalone native C++ binary. Your model runs directly in offline memory without requiring Ollama, LM Studio, or external container services.',
    dataSnippetTitle: 'Instant Standalone Binary Launch',
    beforeSnippet: `# CLOUD PROPRIETARY API (RECURRING BILLING)
curl https://api.cloud-provider.com/v1/chat/completions \\
  -H "Authorization: Bearer $EXPENSIVE_KEY"
# Risk: Data logs stored by third-party vendor`,
    afterSnippet: `# STANDALONE DBERT BARE-METAL EXECUTION (ZERO DEPENDENCIES)
# No Ollama, No LM Studio, No Docker needed:
./dbert-engine --model ./model-q4_k_m.gguf --port 8080 --ctx 8192
# Direct C++ / Python bindings loaded into local VRAM:
python -c "import dbert; model = dbert.load('./model-q4_k_m.gguf'); print(model.generate('Schema test'))"`,
    keyActionNotes: [
      'Compiles 16GB model down to 4.8GB for zero-friction local storage',
      'Executes directly in native C++ memory without Ollama or LM Studio',
      'Eliminates third-party wrappers, license telemetry, and API bills completely'
    ]
  }
];

export default function PipelineInteractiveConsole() {
  const [activeStageId, setActiveStageId] = useState<string>('stage-1');

  const activeStage = STAGES.find(s => s.id === activeStageId) || STAGES[0];
  const IconComponent = activeStage.icon;

  return (
    <div className={styles.wrapper}>
      {/* Stage Selector Rail */}
      <div className={styles.railHeader}>
        <div className="flex justify-between items-center flex-wrap gap-2 mb-3">
          <span className="doclabel text-xs">INTERACTIVE MLOPS CONSOLE</span>
          <span className="font-mono text-xs text-accent">5 Deterministic Sprints · 14-Day Delivery</span>
        </div>
        
        <div className={styles.rail} role="tablist" aria-label="Fine-Tuning Stages">
          {STAGES.map((stage) => {
            const isActive = stage.id === activeStageId;
            const StageIcon = stage.icon;
            return (
              <button
                key={stage.id}
                role="tab"
                aria-selected={isActive}
                onClick={() => setActiveStageId(stage.id)}
                className={`${styles.tabBtn} ${isActive ? styles.tabBtnActive : ''}`}
              >
                <div className={styles.tabNodeWrap}>
                  <span className={styles.tabNum}>{stage.num}</span>
                  <StageIcon size={16} className={styles.tabIcon} />
                </div>
                <div className={styles.tabTextCol}>
                  <span className={styles.tabShortName}>{stage.shortName}</span>
                  <span className={styles.tabDuration}>{stage.duration}</span>
                </div>
                {isActive && <span className={styles.activePill} />}
              </button>
            );
          })}
        </div>
      </div>

      {/* Main Stage Detail Display Panel */}
      <div className={styles.stagePanel}>
        <div className={styles.panelTop}>
          <div className="flex items-start gap-4">
            <div className={styles.iconBox}>
              <IconComponent size={28} className="text-accent" />
            </div>
            <div>
              <div className="flex items-center gap-3 flex-wrap">
                <span className="doclabel" style={{ color: 'var(--signal)', borderColor: 'var(--signal)' }}>
                  STAGE {activeStage.num} OF 05
                </span>
                <span className="tag-chip text-xs font-mono">{activeStage.duration}</span>
                <span className="proof-mark text-xs font-mono">
                  Output: {activeStage.deliverableFile}
                </span>
              </div>
              <h3 className={styles.stageHeading}>{activeStage.title}</h3>
              <p className={styles.stageTagline}>{activeStage.tagline}</p>
            </div>
          </div>
        </div>

        {/* 2-Column Content Grid: Specs & Description Left, Code Snippet Right */}
        <div className={styles.contentGrid}>
          {/* Left Column: Description & Engineering Specifications */}
          <div className={styles.leftCol}>
            <p className={styles.stageDescription}>
              {activeStage.description}
            </p>

            <div className={styles.specsCard}>
              <div className="font-mono text-xs text-accent uppercase font-bold mb-3 flex items-center gap-2">
                <Terminal size={14} /> Stage Engineering Metrics
              </div>
              <div className={styles.specsGrid}>
                {activeStage.specs.map((spec, i) => (
                  <div key={i} className={styles.specItem}>
                    <span className={styles.specLabel}>{spec.label}</span>
                    <span className={styles.specValue}>{spec.value}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className={styles.actionNotesBlock}>
              <h4 className="font-mono text-xs font-bold text-white mb-2 uppercase">Execution Deliverables:</h4>
              <ul className={styles.actionList}>
                {activeStage.keyActionNotes.map((note, idx) => (
                  <li key={idx} className="flex items-start gap-2 text-xs text-muted">
                    <CheckCircle2 size={14} className="text-emerald-400 shrink-0 mt-0.5" />
                    <span>{note}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Right Column: Interactive Code & Data Transformation Viewer */}
          <div className={styles.rightCol}>
            <div className={styles.codeHeader}>
              <div className="flex items-center gap-2">
                <Code2 size={16} className="text-signal" />
                <span className="font-mono text-xs font-bold text-white">{activeStage.dataSnippetTitle}</span>
              </div>
              <span className="text-[10px] font-mono text-muted">Real Pipeline Transformation</span>
            </div>

            <div className={styles.comparisonBox}>
              <div className={styles.snippetBlock}>
                <div className={styles.snippetLabelRedline}>BEFORE: UNOPTIMIZED / INSECURE</div>
                <pre className={styles.codeSnippet}>{activeStage.beforeSnippet}</pre>
              </div>

              <div className={styles.snippetBlockAfter}>
                <div className={styles.snippetLabelPassed}>AFTER: DBERT SANITIZED PIPELINE</div>
                <pre className={styles.codeSnippetClean}>{activeStage.afterSnippet}</pre>
              </div>
            </div>

            <div className={styles.stageBottomNav}>
              <div className="text-xs text-muted font-mono">
                Artifact: <strong className="text-white">{activeStage.deliverableFile}</strong>
              </div>
              <Link href="/about/contact" className="btn btn-primary btn-sm inline-flex items-center gap-2">
                Commission Stage {activeStage.num} &rarr;
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
