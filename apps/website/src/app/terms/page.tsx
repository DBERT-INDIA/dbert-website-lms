import React from 'react';
import Link from 'next/link';
import { pageMetadata } from '@/lib/seo';

export const metadata = pageMetadata('/terms');

export default function TermsPage() {
  return (
    <div className="container pad-block">
      <div className="measure-lg">
        <div className="mb-lg">
          <div className="doclabel">
            § 01 — STATUTORY TERMS <span className="rev">rev: 2026.3</span>
          </div>
          <div className="stack-h justify-start align-baseline gap-3 flex-wrap mb-2">
            <h1 className="mb-0">Terms &amp; Conditions</h1>
          </div>
          <p className="page-intro">
            Comprehensive operating agreements, platform rules, fee structures, and governance policies for DBERT venture studio, incubation tracks, and verification ecosystems.
          </p>
        </div>
        
        <div className="stack gap-6">
          <div className="card card-lift">
            <span className="doclabel text-xs mb-1">§ 01 — CORPORATE IDENTITY</span>
            <h2 className="card-title my-2">1. Operating Entity &amp; Sovereign Domains</h2>
            <p className="body-copy">
              All incubation support, training courses, experience letters, letters of recommendation (LOR), and startup co-development agreements are coordinated and issued under the registered corporate entity <strong>Digital Blinc Education Research And Technology</strong> (MSME registered).
            </p>
            <p className="body-copy mt-2">
              The sovereign active domains for the platform are <strong>https://dbert.in</strong> (public venture studio) and <strong>https://lms.dbert.in</strong> (learning management &amp; sprint portal). Legacy domain <code>dbert.online</code> is retired and permanently redirects to <code>dbert.in</code>.
            </p>
          </div>

          <div className="card card-lift">
            <span className="doclabel text-xs mb-1">§ 02 — TRACK DEFINITIONS &amp; FEES</span>
            <h2 className="card-title my-2">2. Program Tracks &amp; Fee Ledger</h2>
            <ul className="list-disc list-inside space-y-2 text-sm text-neutral-300 mt-2">
              <li>
                <strong>Free Internship Track:</strong> Merit-based application track. <strong>Zero application or screening fees.</strong> No caution deposit or upfront payment is required to participate in evaluations or milestones.
              </li>
              <li>
                <strong>Project Verification &amp; Credential Authentication:</strong> Statutory evaluation fee of <strong>₹299</strong> to verify engineering deliverables, Turnitin originality scores, and generate official 3-document credential packets (Certificate of Completion, Academic Evaluation, LOR).
              </li>
              <li>
                <strong>Incubation Program:</strong> 2-month intensive engineering track with live client code repository assignments, 1:1 mentor code reviews, Turnitin originality evaluation, and guaranteed partner project placement. Total program fee is <strong>₹1,999</strong> (inclusive of taxes).
              </li>
              <li>
                <strong>Performance Stipend:</strong> Performance stipends (₹5,000–₹18,000) are milestone-based and earned through verified pull requests and technical reports submitted via <a href="https://lms.dbert.in/stipend/tasks" className="text-amber-400 hover:underline">/stipend/tasks</a>, subject to AI screening and senior staff review.
              </li>
            </ul>
          </div>

          <div className="card card-lift">
            <span className="doclabel text-xs mb-1">§ 03 — CREDENTIAL &amp; VERIFICATION STANDARDS</span>
            <h2 className="card-title my-2">3. Credential Authenticity &amp; Integrity</h2>
            <p className="body-copy">
              Credentials issued by DBERT are cryptographically verifiable by exact certificate ID at <Link href="/verify" className="text-amber-400 hover:underline">dbert.in/verify</Link>. Public records adhere strictly to Privacy-by-Default: candidate contact details, phone numbers, and financial records remain strictly encrypted and confidential.
            </p>
            <p className="body-copy mt-2">
              DBERT credentials represent validated engineering capability evaluated against industry rubrics and do not represent UGC/AICTE degree accreditations.
            </p>
          </div>

          <div className="card card-lift">
            <span className="doclabel text-xs mb-1">§ 04 — RECRUITER &amp; TALENT ENGAGEMENT</span>
            <h2 className="card-title my-2">4. Pre-Vetted Talent Directory &amp; Employer Terms</h2>
            <p className="body-copy">
              Recruiters accessing candidate dossiers via the Pre-Vetted Engineers Directory (<Link href="/verify/directory" className="text-amber-400 hover:underline">/verify/directory</Link>) or hiring via <Link href="/hire/pre-vetted-engineers" className="text-amber-400 hover:underline">/hire/pre-vetted-engineers</Link> agree to direct candidate communication rules, verified evaluation rubrics, and zero recruiter markup agreements.
            </p>
          </div>

          <div className="card card-lift">
            <span className="doclabel text-xs mb-1">§ 05 — STATUTORY CONTACT &amp; GRIEVANCE</span>
            <h2 className="card-title my-2">5. Grievance Redressal &amp; Support</h2>
            <p className="body-copy">
              For any questions, terms clarifications, or grievance escalations, contact:
            </p>
            <p className="mt-2 text-sm text-neutral-300">
              Compliance Officer: Abhinav Sharma (<a href="mailto:abhinav.sharma@dbert.in" className="text-amber-400 hover:underline">abhinav.sharma@dbert.in</a> / <a href="mailto:support@dbert.in" className="text-amber-400 hover:underline">support@dbert.in</a>)
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
