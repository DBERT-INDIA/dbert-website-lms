import React from 'react';
import { pageMetadata } from '@/lib/seo';


export const metadata = pageMetadata('/terms');

export default function TermsPage() {
  return (
    <div className="container pad-block">
      <div className="measure-lg">
        <div className="mb-lg">
          <div className="doclabel">
            § 01 — STATUTORY TERMS <span className="rev">rev: 2026.2</span>
          </div>
          <h1>Terms &amp; Conditions</h1>
          <p className="page-intro">
            Operating agreements, platform rules, and intellectual property governance for DBERT incubation, education, and API systems.
          </p>
        </div>
        
        <div className="stack gap-6">
          <div className="card card-lift">
            <span className="doclabel text-xs mb-1">§ 01 — CORPORATE IDENTITY</span>
            <h2 className="card-title my-2">1. Entity Details</h2>
            <p className="body-copy">
              All incubation support, training courses, experience letters, letters of recommendation (LOR), and startup co-development agreements are coordinated and issued under the registered corporate entity <strong>Digital Blinc Education Research And Technology</strong> (MSME registered).
            </p>
          </div>

          <div className="card card-lift">
            <span className="doclabel text-xs mb-1">§ 02 — PLATFORM USAGE</span>
            <h2 className="card-title my-2">2. Use of Services</h2>
            <p className="body-copy">
              By accessing our programs or utilizing our verification APIs, you agree to comply with our academic guidelines, code submission standards, and developer checklists. Any attempts to manipulate verification keys, bypass database access controls, or distribute unauthorized model weights will result in immediate suspension.
            </p>
          </div>

          <div className="card card-lift">
            <span className="doclabel text-xs mb-1">§ 03 — INCUBATION FRAMEWORKS</span>
            <h2 className="card-title my-2">3. Startup Incubation Frameworks</h2>
            <p className="body-copy">
              For startups, specific deliverables, equity configurations (between 2% to 8%), milestone timelines, and GPU allocations are managed under separate, legally binding agreements. These terms serve as base guidelines for platform access.
            </p>
          </div>

          <div className="card card-lift">
            <span className="doclabel text-xs mb-1">§ 04 — GOVERNANCE AMENDMENTS</span>
            <h2 className="card-title my-2">4. Amendments</h2>
            <p className="body-copy">
              We reserve the right to modify these Terms at any time. Your continued use of the website or related pathways following updates constitutes acceptance of the modified guidelines.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
