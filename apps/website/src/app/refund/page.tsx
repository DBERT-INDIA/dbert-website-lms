import React from 'react';
import Link from 'next/link';
import { pageMetadata } from '@/lib/seo';
import { ShieldCheck, CheckCircle2 } from 'lucide-react';

export const metadata = pageMetadata('/refund');

export default function RefundPage() {
  return (
    <div className="container pad-block">
      <div className="measure-lg">
        <div className="mb-lg">
          <div className="doclabel">
            § 01 — STATUTORY POLICY <span className="rev">rev: 2026.3</span>
          </div>
          <div className="stack-h justify-start align-baseline gap-3 flex-wrap mb-2">
            <h1 className="mb-0">Refund &amp; Deposit Policy</h1>
          </div>
          <p className="page-intro">
            Clear, transparent statutory guidelines regarding program fees, credential verification, and financial reconciliation.
          </p>
        </div>

        <div className="stack gap-6">
          {/* Free Track & Assessment */}
          <div className="card card-lift">
            <div className="stack-h justify-between align-center mb-2">
              <span className="doclabel text-xs">§ 01 — MERIT-BASED APPLICATION &amp; SCREENING</span>
              <span className="badge badge-accent">100% Free Screening</span>
            </div>
            <h2 className="card-title my-2">1. Zero Application &amp; Screening Fees</h2>
            <p className="body-copy">
              DBERT strictly guarantees that all candidate applications, technical evaluations, algorithmic screening stages, and initial sprint tracks carry <strong>zero application, assessment, or screening fees</strong>. No deposit or caution fee is required to apply or undertake evaluations.
            </p>
          </div>

          {/* ₹299 Project Verification */}
          <div className="card card-lift">
            <div className="stack-h justify-between align-center mb-2">
              <span className="doclabel text-xs">§ 02 — CREDENTIAL AUTHENTICATION</span>
              <span className="badge badge-accent">₹299 Verification Fee</span>
            </div>
            <h2 className="card-title my-2">2. Project Verification &amp; Official Credential Issuance (₹299)</h2>
            <p className="body-copy">
              Upon completing engineering project deliverables, provisional candidates requesting Turnitin originality clearance, 9-dimension rubric evaluation, and generation of their official 3-document credential packet (Certificate of Completion, Academic Evaluation, institutional LOR) remit a statutory ₹299 verification fee.
            </p>
            <div className="p-3 bg-neutral-900 border border-neutral-800 rounded-lg my-3 text-sm text-neutral-300">
              <div className="font-semibold text-white mb-1 flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-400 inline" /> Verification Lifecycle:
              </div>
              Because project evaluations trigger automated Turnitin repository scans and dedicated faculty review, the ₹299 fee is non-refundable once evaluation processing has commenced.
            </div>
          </div>

          {/* Paid Incubation Program */}
          <div className="card card-lift">
            <div className="stack-h justify-between align-center mb-2">
              <span className="doclabel text-xs">§ 03 — PAID INCUBATION PROGRAM</span>
              <span className="badge badge-neutral">Committed Seat Allocation</span>
            </div>
            <h2 className="card-title my-2">3. ₹1,999 Incubation Program Fee</h2>
            <p className="body-copy">
              The comprehensive 2-month Incubation Program includes structured technical modules, live client repository assignments, 1:1 mentor code reviews, Turnitin-verified project evaluations, and official credential issuance.
            </p>
            <div className="p-3 bg-neutral-900 border border-neutral-800 rounded-lg my-3 text-sm text-neutral-300">
              <div className="font-semibold text-white mb-1 flex items-center gap-2">
                <ShieldCheck className="w-4 h-4 text-amber-400 inline" /> Fee Reconciliation:
              </div>
              <ul className="list-disc list-inside space-y-1 mt-1">
                <li><strong>Total Program Fee:</strong> ₹1,999 (inclusive of statutory taxes).</li>
                <li><strong>Non-Refundable Committed Seat:</strong> Because enrollment locks dedicated mentor bandwidth, client repository access, and live cloud infrastructure, the committed program fee is non-refundable once sprint access is unlocked.</li>
              </ul>
            </div>
          </div>

          {/* Startup Retainers */}
          <div className="card card-lift">
            <span className="doclabel text-xs mb-1">§ 04 — STARTUP INCUBATION RETAINERS</span>
            <h2 className="card-title my-2">3. Venture Co-Development &amp; Retainers</h2>
            <p className="body-copy">
              Startup co-development retainers, equity sweat agreements (2%–8%), and dedicated GPU allocations are managed under signed bilateral Service Level Agreements (SLAs). Milestone refunds are governed strictly by the delivery criteria set forth in the individual partnership contract.
            </p>
          </div>

          {/* Admissions Support */}
          <div className="card card-lift">
            <span className="doclabel text-xs mb-1">§ 05 — STATUTORY CONTACT</span>
            <h2 className="card-title my-2">4. Support &amp; Dispute Reconciliation</h2>
            <p className="body-copy">
              For payment queries, UTR transaction reconciliations, or deposit status tracking, candidates and partners may contact Admissions directly:
            </p>
            <div className="mt-3 text-sm text-neutral-300">
              <p>Email: <a href="mailto:support@dbert.in" className="text-amber-400 hover:underline">support@dbert.in</a> / <a href="mailto:abhinav.sharma@dbert.in" className="text-amber-400 hover:underline">abhinav.sharma@dbert.in</a></p>
              <p>WhatsApp Admissions Concierge: <a href="https://wa.me/918192911360" target="_blank" rel="noopener noreferrer" className="text-amber-400 hover:underline">+91 81929 11360</a></p>
              <p>Online Balance Portal: <Link href="/enroll/1999" className="text-amber-400 hover:underline">dbert.in/enroll/1999</Link></p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
