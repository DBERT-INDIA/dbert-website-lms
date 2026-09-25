import React from 'react';
import { pageMetadata } from '@/lib/seo';


export const metadata = pageMetadata('/privacy');

export default function PrivacyPage() {
  return (
    <div className="container pad-block">
      <div className="measure-lg">
        <div className="mb-lg">
          <div className="doclabel">
            § 01 — STATUTORY COMPLIANCE <span className="rev">rev: 2026.2</span>
          </div>
          <h1>Privacy Policy</h1>
          <p className="page-intro">
            How Digital Blinc Education Research And Technology (DBERT) protects, isolates, and secures developer, student, and startup partner data.
          </p>
        </div>
        
        <div className="stack gap-6">
          <div className="card card-lift">
            <span className="doclabel text-xs mb-1">§ 01 — SCOPE &amp; IDENTITY</span>
            <h2 className="card-title my-2">Registered Entity Overview</h2>
            <p className="body-copy">
              At DBERT (Digital Blinc Education Research And Technology, registered MSME entity), we prioritize data privacy and operational security across our website (<code>dbert.online</code>), learning platforms, and verification registries.
            </p>
          </div>

          <div className="card card-lift">
            <span className="doclabel text-xs mb-1">§ 02 — DATA INGESTION</span>
            <h2 className="card-title my-2">1. Information We Collect</h2>
            <p className="body-copy">
              We gather information strictly necessary to coordinate startup incubation tracks and engineering programs. This includes startup registration details (names, descriptions, stack outlines), learner applications (emails, names, GitHub repositories, and contact parameters), and details submitted via research collaboration forms.
            </p>
          </div>

          <div className="card card-lift">
            <span className="doclabel text-xs mb-1">§ 03 — USE OF INFORMATION</span>
            <h2 className="card-title my-2">2. How We Use Information</h2>
            <p className="body-copy">
              Your data is utilized solely to deliver services, evaluate startup registrations, coordinate mentor feedback, verify credentials, and process transaction milestones. We do not exchange, rent, or distribute candidate files or startup codebases to external commercial networks without explicit consent.
            </p>
          </div>

          <div className="card card-lift">
            <span className="doclabel text-xs mb-1">§ 04 — SECURITY &amp; ISOLATION</span>
            <h2 className="card-title my-2">3. Data Sovereignty and Security</h2>
            <p className="body-copy">
              We implement industry-standard encryption controls. Custom model weights, embeddings, or database queries run in private cloud virtual networks (VPCs) with zero-trust network boundaries, maintaining strict data isolation.
            </p>
          </div>

          <div className="card card-lift">
            <span className="doclabel text-xs mb-1">§ 05 — UPDATES &amp; AUDITS</span>
            <h2 className="card-title my-2">4. Changes to This Policy</h2>
            <p className="body-copy">
              We periodically update our policies to align with evolving statutory guidelines. Any modifications are posted directly to this page with the active revision date.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
