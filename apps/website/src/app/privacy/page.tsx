import React from 'react';
import HandNote from '@/components/ui/HandNote';
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
          <div className="stack-h justify-start align-baseline gap-3 flex-wrap mb-2">
            <h1 className="mb-0">Privacy Policy</h1>
            <HandNote tone="blue">
              statutory MSME framework ✍
            </HandNote>
          </div>
          <p className="page-intro">
            How Digital Blinc Education Research And Technology (DBERT) protects, isolates, and secures developer, student, and startup partner data.
          </p>
        </div>
        
        <div className="stack gap-6">
          <div className="card card-lift">
            <span className="doclabel text-xs mb-1">§ 01 — SCOPE &amp; IDENTITY</span>
            <h2 className="card-title my-2">Registered Entity Overview</h2>
            <p className="body-copy">
              At DBERT (Digital Blinc Education Research And Technology, registered MSME entity UDYAM-UP-28-0105315), we prioritize data privacy and operational security across our website (<code>dbert.online</code>), learning platforms, and verification registries.
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
            <span className="doclabel text-xs mb-1">§ 03 — COOKIES &amp; THIRD-PARTY ADVERTISING</span>
            <h2 className="card-title my-2">2. Cookies, Google AdSense &amp; Analytics Disclosure</h2>
            <p className="body-copy mb-3">
              We and our trusted third-party partners (such as Google AdSense, Google Analytics 4) use cookies, web beacons, and similar tracking technologies to analyze site traffic, personalize content, and serve relevant advertisements based on prior visits to this website or other sites on the Internet.
            </p>
            <ul className="list-disc pl-5 space-y-2 text-sm text-zinc-300">
              <li>
                <strong>Google AdSense &amp; DoubleClick Cookie:</strong> Google, as a third-party vendor, uses cookies to serve ads on <code>dbert.online</code>. Google&apos;s use of advertising cookies enables it and its partners to serve ads to users based on their visits to our site and/or other sites on the Internet.
              </li>
              <li>
                <strong>User Opt-Out:</strong> Users may opt out of personalized advertising by visiting <a href="https://www.google.com/settings/ads" target="_blank" rel="noopener noreferrer" className="text-accent underline">Google Ads Settings</a>. Alternatively, you may opt out of third-party vendor cookies for personalized advertising by visiting <a href="https://www.aboutads.info" target="_blank" rel="noopener noreferrer" className="text-accent underline">aboutads.info</a>.
              </li>
              <li>
                <strong>Log Files &amp; Telemetry:</strong> Like most standard website servers, we utilize log files and anonymized telemetry (browser type, referring/exit pages, platform type, date/time stamp, and analytical click counts) to administer the portal and monitor platform health.
              </li>
            </ul>
          </div>

          <div className="card card-lift">
            <span className="doclabel text-xs mb-1">§ 04 — USE OF INFORMATION</span>
            <h2 className="card-title my-2">3. How We Use Information</h2>
            <p className="body-copy">
              Your data is utilized solely to deliver services, evaluate startup registrations, coordinate mentor feedback, verify credentials, and process transaction milestones. We do not exchange, rent, or distribute candidate files or startup codebases to external commercial networks without explicit consent.
            </p>
          </div>

          <div className="card card-lift">
            <span className="doclabel text-xs mb-1">§ 05 — SECURITY &amp; ISOLATION</span>
            <h2 className="card-title my-2">4. Data Sovereignty and Security</h2>
            <p className="body-copy">
              We implement industry-standard encryption controls. Custom model weights, embeddings, or database queries run in private cloud virtual networks (VPCs) with zero-trust network boundaries, maintaining strict data isolation.
            </p>
          </div>

          <div className="card card-lift">
            <span className="doclabel text-xs mb-1">§ 06 — UPDATES &amp; AUDITS</span>
            <h2 className="card-title my-2">5. Changes to This Policy</h2>
            <p className="body-copy">
              We periodically update our policies to align with evolving statutory guidelines. Any modifications are posted directly to this page with the active revision date.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
