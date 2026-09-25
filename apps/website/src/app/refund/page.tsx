import React from 'react';
import { Metadata } from 'next';
import { pageMetadata } from '@/lib/seo';


export const metadata = pageMetadata('/refund');

export default function RefundPage() {
  return (
    <div className="container pad-block">
      <div className="measure-lg">
        <div className="mb-lg">
          <div className="doclabel">
            § 01 — STATUTORY POLICY <span className="rev">rev: 2026.2</span>
          </div>
          <h1>Refund Policy</h1>
          <p className="page-intro">
            Clear, transparent guidelines regarding program fee transactions, evaluation windows, and incubation retainers.
          </p>
        </div>
        
        <div className="stack gap-6">
          <div className="card card-lift">
            <span className="doclabel text-xs mb-1">§ 01 — TRANSACTION GUIDELINES</span>
            <h2 className="card-title my-2">1. Upskilling Track Admissions</h2>
            <p className="body-copy">
              Please review all program details carefully before enrolling. Course admissions across our upskilling tracks (Launchpad, Accelerate, and Fellowship) are processed through secure payment gateways (Razorpay) with statutory GST compliance invoicing.
            </p>
          </div>

          <div className="card card-lift">
            <span className="doclabel text-xs mb-1">§ 02 — PREREQUISITES &amp; SYLLABUS AUDIT</span>
            <h2 className="card-title my-2">2. Evaluation &amp; Curriculum Prerequisites</h2>
            <p className="body-copy">
              We encourage all applicants to thoroughly inspect curriculum topics, technology stacks, weekly sprint obligations, and certification criteria prior to payment completion.
            </p>
          </div>

          <div className="card card-lift">
            <span className="doclabel text-xs mb-1">§ 03 — STARTUP ENGAGEMENT</span>
            <h2 className="card-title my-2">3. Startup Incubation Fees</h2>
            <p className="body-copy">
              Startup incubation fees, equity agreements, and custom feature retainers are governed under signed bilateral service level agreements (SLAs) with defined delivery milestones.
            </p>
          </div>

          <div className="card card-lift">
            <span className="doclabel text-xs mb-1">§ 04 — CANDIDATE SUPPORT</span>
            <h2 className="card-title my-2">4. Questions &amp; Support</h2>
            <p className="body-copy">
              If you have any questions regarding enrollment details, transaction records, or credential issuance, our support staff is available at <a href="mailto:contactus@dbert.online" className="accent-link">contactus@dbert.online</a>.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
