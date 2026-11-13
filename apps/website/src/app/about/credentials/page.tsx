import React from 'react';
import Link from 'next/link';
import HandNote from '@/components/ui/HandNote';
import { pageMetadata } from '@/lib/seo';
import styles from '../about.module.css';

export const metadata = pageMetadata('/about/credentials');

export default function CredentialsPage() {
  return (
    <div className="container pad-block">
      <div className="mb-lg">
        <div className="doclabel">
          § 05 — INSTITUTIONAL VERIFICATION <span className="rev">rev: 2026.2</span>
        </div>
        <div className="stack-h justify-start align-baseline gap-3 flex-wrap mb-2">
          <h1>Proven Engineering Credibility, Audited Impact</h1>
          <HandNote tone="blue">
            MSME verified · UDYAM registered ✎
          </HandNote>
        </div>
        <p className="intro-copy">
          The institutional registrations, compliance standards, and open-weights engineering deployments validating DBERT.
        </p>
      </div>

      <div className={styles.cardStack}>
        {/* Card 1: Regulatory & Statutory */}
        <div className="card card-lift">
          <div className="doclabel mb-1">§ REGULATORY COMPLIANCE</div>
          <h2 className={styles.cardTitleTight}>MSME Registered Corporate Entity</h2>
          <p className="prose-sm mb-3">
            Fully registered under the Ministry of Micro, Small and Medium Enterprises, Government of India. 
            DBERT operates as the technology incubation, artificial intelligence solutions, and developer training division under 
            the parent corporate enterprise <strong>Digital Blinc Education Research And Technology</strong> (Statutory Category: Micro Enterprise &middot; NIC: Computer Programming, Consultancy &amp; Educational Research).
          </p>
          <div className="card p-3 bg-muted/20 border border-line/60 rounded text-xs text-muted mb-4">
            <strong>Statutory Distinction:</strong> MSME registration validates our legal enterprise status and commercial operations under Indian law. It establishes formal corporate compliance but does not constitute UGC or AICTE degree accreditation. Our credentials represent validated production software engineering experience, senior pull-request code reviews, and tangible codebase commits.
          </div>
          <div className="pt-3 border-t border-line stack-h gap-4 flex-wrap">
            <a 
              href="https://udyamregistration.gov.in/Udyam_Verify.aspx" 
              target="_blank" 
              rel="noopener noreferrer" 
              className="accent-link text-sm font-medium"
            >
              Verify on Official Government UDYAM Portal &rarr;
            </a>
            <Link href="/verify" className="accent-link text-sm font-medium">
              Launch Online Credential Verification Engine &rarr;
            </Link>
          </div>
        </div>

        {/* Card 2: Candidate Protection & Advisory */}
        <div className="card card-lift">
          <div className="doclabel mb-1">§ CANDIDATE PROTECTION &amp; LEGAL ADVISORY</div>
          <h2 className={styles.cardTitleTight}>Zero Application Fee Guarantee &amp; Entity Advisory</h2>
          <p className="prose-sm mb-3">
            <strong>Zero Application Fee Guarantee:</strong> DBERT never charges any application, registration, screening, or interview fee for any candidate. Initial selection for our internship tracks is 100% free based solely on merit, GitHub code reviews, and technical challenge submissions.
          </p>
          <p className="prose-sm mb-3">
            <strong>Entity &amp; Identity Protection:</strong> DBERT operates exclusively under <em>Digital Blinc Education Research And Technology</em>. We have no legal relationship or affiliation with discontinued third-party operations or unofficial entities soliciting money under similar names. All official candidate correspondence originates strictly from <code>@dbert.in</code>, and official payments are made exclusively to verified merchant VPAs.
          </p>
          <div className="pt-3 border-t border-line">
            <a href="mailto:support@dbert.in" className="accent-link text-sm font-medium">
              Report Unauthorized Solicitations: support@dbert.in &rarr;
            </a>
          </div>
        </div>

        {/* Card 3: Open Science & Repositories */}
        <div className="card card-lift">
          <div className="doclabel mb-1">§ OPEN SCIENCE COMMITMENT</div>
          <h2 className={styles.cardTitleTight}>Sovereign AI &amp; Open-Source Repository Contributions</h2>
          <p className="prose-sm mb-4">
            Acknowledged across the Indian AI developer community for engineering excellence in designing modular multi-agent communication schemas, releasing open-weights localized LLM configurations, and building transparent venture incubation codebases. Fellows work directly on active systems including Alkame, Gayatri AI, Aivara Insight Lite, and DBERT Systems.
          </p>
          <div className="pt-3 border-t border-line">
            <Link href="/labs/opensource" className="accent-link text-sm font-medium">
              Inspect Open-Source Repositories &rarr;
            </Link>
          </div>
        </div>

        {/* Card 4: Published AI Weights */}
        <div className="card card-lift">
          <div className="doclabel mb-1">§ PUBLISHED AI WEIGHTS</div>
          <h2 className={styles.cardTitleTight}>DBERT_AI Open-Weights Custom Model</h2>
          <p className={styles.modelCopy}>
            Custom fine-tuned parameter weights optimized specifically for unstructured educational document parsing, deterministic web automation scripting, and agent function-calling loops. Compiled in highly efficient GGUF quantization formats and published publicly on the Ollama verified global model registry.
          </p>
          <a 
            href="https://ollama.com/DBERT/DBERT_AI" 
            target="_blank" 
            rel="noopener noreferrer" 
            className={`${styles.inlineLink} font-mono block mt-3 p-3 raise rounded border border-line`}
          >
            Run Locally in Terminal: ollama run DBERT/DBERT_AI &rarr;
          </a>
        </div>

        {/* Card 5: Domain Authenticity */}
        <div className="card card-lift">
          <div className="doclabel mb-1">§ DOMAIN AUTHENTICITY &amp; TRANSITION</div>
          <h2 className={styles.cardTitleTight}>Official Web Domain: DBERT.online is Now DBERT.in</h2>
          <p className="prose-sm mb-4">
            Statutory notice: <strong>dbert.online is not the active platform</strong>. To maintain sovereign infrastructure standards and protect learners and partners from obsolete or unofficial third-party mirrors, all operations, digital contracts, and cryptographic credential registries are anchored exclusively to <strong>dbert.in</strong> (transitioned from dbert.online).
          </p>
          <div className="pt-3 border-t border-line">
            <Link href="/dbert-online" className="accent-link text-sm font-medium">
              Read Domain Migration Announcement &amp; Advisory &rarr;
            </Link>
          </div>
        </div>

        {/* Card 6: Learner Impact Hierarchy */}
        <div className="card card-lift">
          <div className="doclabel mb-1">§ LEARNER IMPACT AUDITOR</div>
          <h2 className={styles.cardTitleTight}>Audited Learner Impact &amp; Credential Directory</h2>
          <p className="prose-sm mb-3">
            To ensure complete transparency in our published metrics, we clearly differentiate between evaluated learners, formally certified candidates, and intensive venture fellows:
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 my-3">
            <div className="p-3 bg-muted/20 border border-line/60 rounded">
              <div className="text-xl font-bold font-mono text-gold">1,500+</div>
              <div className="text-xs text-muted font-medium mt-1">Evaluated Learners</div>
              <div className="text-xs text-muted/80 mt-1">Developers upskilled across technical masterclasses, open hackathons, and initial assessments.</div>
            </div>
            <div className="p-3 bg-muted/20 border border-line/60 rounded">
              <div className="text-xl font-bold font-mono text-ok">465+</div>
              <div className="text-xs text-muted font-medium mt-1">Certified Fellows</div>
              <div className="text-xs text-muted/80 mt-1">Candidates with verifiable UUID credentials in our sovereign candidate directory.</div>
            </div>
            <div className="p-3 bg-muted/20 border border-line/60 rounded">
              <div className="text-xl font-bold font-mono text-signal">120+</div>
              <div className="text-xs text-muted font-medium mt-1">Venture Fellows</div>
              <div className="text-xs text-muted/80 mt-1">Intensive squad fellows deployed directly on live venture repos and multi-agent production codebases.</div>
            </div>
          </div>
          <div className="pt-3 border-t border-line stack-h gap-4 flex-wrap">
            <Link href="/verify/directory" className="accent-link text-sm font-medium">
              Browse Sovereign Candidate Directory (465+ Records) &rarr;
            </Link>
            <Link href="/learners" className="accent-link text-sm font-medium">
              Inspect Career Pathways Ladder &rarr;
            </Link>
            <Link href="/about/team" className="accent-link text-sm font-medium">
              Meet Mentorship Leadership &rarr;
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
