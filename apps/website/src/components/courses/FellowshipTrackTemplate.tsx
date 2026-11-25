import React from 'react';
import Link from 'next/link';
import {
  CheckCircle2,
  Clock,
  GitPullRequest,
  ShieldCheck,
  Award,
  ExternalLink,
  MessageSquare,
} from 'lucide-react';
import FAQAccordion from '@/components/ui/FAQAccordion';
import RegionalOpportunityBento from '@/components/ui/RegionalOpportunityBento';
import TrackLeadCaptureForm from '@/components/forms/TrackLeadCaptureForm';
import CurriculumAccordion from '@/components/courses/CurriculumAccordion';
import {
  type FellowshipTrack,
  FELLOWSHIP_FEE,
  getRelatedTracks,
} from '@/data/courses.config';
import { GEO_CITIES } from '@/data/geo_domains.config';
import { PRICING_CONFIG } from '@/config/pricing.config';
import directoryData from '@/data/directory_candidates.json';
import s from '@/app/learners/learners.module.css';

interface DirectoryEntry {
  certId: string;
  holderName: string;
  domain?: string;
  score?: number;
  grade?: string;
  verified?: boolean;
  verifyUrl?: string;
}

const DOMAIN_KEYWORDS: Record<string, string[]> = {
  'ai-agent-development': ['agent', 'intelligence', 'learning'],
  'generative-ai': ['intelligence', 'learning', 'generative'],
  'machine-learning': ['learning', 'intelligence'],
  'full-stack-development': ['full stack', 'web'],
  'python-automation': ['python'],
  'data-analytics': ['data'],
  'ui-ux-design': ['ui', 'ux', 'design'],
  'devops-cloud': ['cloud', 'devops'],
  'mobile-app-development': ['mobile', 'flutter'],
  'cybersecurity': ['security', 'cyber'],
  'digital-marketing': ['marketing', 'growth'],
};

function getTrackAlumni(slug: string): DirectoryEntry[] {
  const kw = DOMAIN_KEYWORDS[slug] || [slug.split('-')[0]];
  return (directoryData as DirectoryEntry[])
    .filter((c) => c.verified !== false && kw.some((k) => (c.domain || '').toLowerCase().includes(k)))
    .sort((a, b) => (b.score || 0) - (a.score || 0))
    .slice(0, 3);
}

interface FellowshipTrackTemplateProps {
  track: FellowshipTrack;
}

export default function FellowshipTrackTemplate({ track }: FellowshipTrackTemplateProps) {
  const relatedTracks = getRelatedTracks(track);
  const verifiedAlumni = getTrackAlumni(track.slug);
  const applyUrl = `https://lms.dbert.in/#signup?domain=${track.slug}&next=/internships/${track.slug}`;
  const whatsappUrl = `https://wa.me/${PRICING_CONFIG.admissionsWhatsApp}?text=${encodeURIComponent(
    `Hi DBERT Admissions, I have a question about the ${track.name} Fellowship (${track.canonicalPath}).`
  )}`;

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Course',
        '@id': `https://dbert.in${track.canonicalPath}#course`,
        name: `${track.name} — DBERT Applied Fellowship`,
        description: track.heroOutcome,
        provider: {
          '@type': 'Organization',
          name: 'Digital Blinc Education Research And Technology (DBERT)',
          url: 'https://dbert.in',
        },
        courseCode: `DBERT-${track.id.toUpperCase().slice(0, 6)}-2026`,
        courseMode: 'Online (Remote Squad Sprints & Senior Code Review)',
        timeRequired: 'P2M',
        educationalCredentialAwarded: 'DBERT 3-Document Verifiable Credential Packet',
        offers: {
          '@type': 'Offer',
          category: 'Total Program Fee',
          price: String(FELLOWSHIP_FEE.amount),
          priceCurrency: FELLOWSHIP_FEE.currency,
          availability: 'https://schema.org/InStock',
          url: `https://dbert.in${track.canonicalPath}`,
        },
      },
      {
        '@type': 'BreadcrumbList',
        itemListElement: [
          { '@type': 'ListItem', position: 1, name: 'Home', item: 'https://dbert.in' },
          { '@type': 'ListItem', position: 2, name: 'Courses', item: 'https://dbert.in/learners/courses' },
          { '@type': 'ListItem', position: 3, name: track.name, item: `https://dbert.in${track.canonicalPath}` },
        ],
      },
      {
        '@type': 'FAQPage',
        mainEntity: track.faqs.map((f) => ({
          '@type': 'Question',
          name: f.question,
          acceptedAnswer: { '@type': 'Answer', text: f.answer },
        })),
      },
    ],
  };

  return (
    <div className="glow-wrapper">
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      <div className="glow-spot" />

      {/* 1. Breadcrumb + 2. Hero */}
      <div className="container page-head">
        <nav aria-label="Breadcrumb" className="text-xs font-mono text-muted mb-4 flex items-center justify-center gap-2 flex-wrap">
          <Link href="/" className="hover:text-accent">Home</Link>
          <span aria-hidden="true">/</span>
          <Link href="/learners/courses" className="hover:text-accent">Fellowship Tracks</Link>
          <span aria-hidden="true">/</span>
          <span className="text-[var(--text-primary)]">{track.name}</span>
        </nav>

        <div className="doclabel">
          § 01 — FELLOWSHIP TRACK <span className="rev">{track.badge}</span>
        </div>

        <h1 className="page-title">{track.name}</h1>

        <p className={s.courseLede}>{track.heroOutcome}</p>

        {/* 3. Verified Fee, Duration, Commitment Strip */}
        <div className="flex justify-center gap-3 flex-wrap mt-6 text-xs font-mono">
          <span className="proof-mark">
            <span>Total Fee: {FELLOWSHIP_FEE.formattedTotal}</span>
          </span>
          <span className="proof-mark">
            <span>Duration: {track.duration}</span>
          </span>
          <span className="proof-mark">
            <span>Commitment: {track.weeklyCommitment}</span>
          </span>
          <Link href="/learners/fellowship#placement-policy" className="proof-mark proof-mark-signal">
            <span>100% Guaranteed Production Internship (Terms)</span>
          </Link>
        </div>

        {/* 4. Primary & Secondary CTAs */}
        <div className="stack-h gap-4 justify-center flex-wrap mt-8">
          <Link
            href={`/enroll/1999?domain=${encodeURIComponent(track.name)}`}
            className="btn btn-primary btn-lg"
          >
            Enroll Now — {FELLOWSHIP_FEE.formattedTotal} (₹1,500 Balance if ₹499 Paid) &rarr;
          </Link>
          <a href="#curriculum" className="btn btn-outline btn-lg">
            Explore 8-Week Syllabus
          </a>
          <Link href={`/learners/courses/${track.slug}/remote`} className="btn btn-outline btn-lg">
            Remote &amp; City Hubs &rarr;
          </Link>
        </div>
      </div>

      {/* 5. Trust / Evidence Strip */}
      <div className="section-band">
        <div className="container">
          <h2 className="sr-only">Fellowship verification and standards</h2>
          <div className="bento-grid-3">
            <div className="bento-card center">
              <span className="icon-chip"><GitPullRequest aria-hidden="true" /></span>
              <h3 className="accent-note">Senior PR Code Reviews</h3>
              <p className="text-sm">Every pull request is reviewed against linting, security, and testing criteria before merge.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><ShieldCheck aria-hidden="true" /></span>
              <h3 className="accent-note">Verifiable UUID Credentials</h3>
              <p className="text-sm">Graduates receive a 3-document packet verifiable by employers on <Link href="/verify" className="underline">dbert.in/verify</Link>.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><Clock aria-hidden="true" /></span>
              <h3 className="accent-note">2-Month Sprint Structure</h3>
              <p className="text-sm">Remote milestone-based sprints designed to fit alongside college or existing engineering work.</p>
            </div>
          </div>
        </div>
      </div>

      {/* 6. Overview, Who Should Apply, Prerequisites & Outcomes */}
      <div className="container pad-block">
        <div className="article">
          <h2>Program Overview</h2>
          <p>{track.fullDescription}</p>

          <div className="grid gap-6 md:grid-cols-2 my-8">
            <div className="card p-6 bg-card border border-line">
              <h3 className="font-mono text-base font-bold text-white mb-3">Who Should Apply</h3>
              <ul className="list-disc pl-5 text-sm text-[var(--text-secondary)] space-y-2">
                {track.whoShouldApply.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </div>

            <div className="card p-6 bg-card border border-line">
              <h3 className="font-mono text-base font-bold text-white mb-3">Prerequisites</h3>
              <ul className="list-disc pl-5 text-sm text-[var(--text-secondary)] space-y-2">
                {track.prerequisites.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </div>
          </div>

          <h2>What You Will Learn &amp; Ship</h2>
          <ul className="space-y-2 my-4">
            {track.outcomes.map((outcome) => (
              <li key={outcome} className="flex items-start gap-2.5 text-sm text-[var(--text-secondary)]">
                <CheckCircle2 size={16} className="text-ok shrink-0 mt-0.5" aria-hidden="true" />
                <span>{outcome}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* 7. Technologies & Why Each Is Used */}
      <div className="section-band border-t border-b border-line">
        <div className="container pad-block">
          <div className="doclabel mb-2">§ 02 — PRODUCTION STACK</div>
          <h2 className="section-title mb-6">Technologies &amp; Engineering Role</h2>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {track.technologies.map((tech) => (
              <div key={tech.name} className="card p-5 bg-card border border-line">
                <div className="font-mono text-sm font-bold text-accent mb-1">{tech.name}</div>
                <p className="text-xs text-[var(--text-secondary)] leading-relaxed">{tech.role}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* 8. Week-by-Week Curriculum Accordion */}
      <div id="curriculum" className="container pad-block">
        <div className="doclabel mb-2">§ 03 — 8-WEEK CURRICULUM</div>
        <h2 className="section-title mb-2">Week-by-Week Sprints &amp; Deliverables</h2>
        <p className="text-sm text-muted mb-6 max-w-2xl">
          Each two-week sprint builds toward a reviewed pull request and verifiable deliverable.
        </p>
        <div className="max-w-3xl">
          <CurriculumAccordion trackId={track.id} modules={track.curriculum} />
        </div>
      </div>

      {/* 9. Capstone & Repository Status */}
      <div className="section-band border-t border-b border-line">
        <div className="container pad-block">
          <div className="doclabel mb-2">§ 04 — CAPSTONE &amp; CODE REVIEW</div>
          <h2 className="section-title mb-6">Capstone Specification</h2>
          <div className="grid gap-6 md:grid-cols-2">
            <div className="card p-6 bg-card border border-line">
              <div className="flex items-center justify-between gap-2 mb-3 flex-wrap">
                <span className="tag-chip text-xs font-mono">
                  {track.capstone.status === 'active' ? 'Active Venture Repository' : 'Proposed Capstone Concept'}
                </span>
                <span className="text-xs font-mono text-muted">Squad: {track.capstone.ventureName}</span>
              </div>
              <h3 className="font-mono text-lg font-bold text-white mb-2">{track.capstone.title}</h3>
              <p className="text-sm text-[var(--text-secondary)] mb-4">{track.capstone.description}</p>
              {track.capstone.repositoryUrl && (
                <a
                  href={track.capstone.repositoryUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1.5 text-xs font-mono text-accent hover:underline"
                >
                  <span>Inspect Venture Repository</span>
                  <ExternalLink size={13} aria-hidden="true" />
                </a>
              )}
              <h4 className="font-mono text-xs uppercase tracking-wider text-muted mt-5 mb-2">
                Acceptance Criteria
              </h4>
              <ul className="list-disc pl-5 text-xs text-[var(--text-secondary)] space-y-1.5">
                {track.capstone.acceptanceCriteria.map((c) => (
                  <li key={c}>{c}</li>
                ))}
              </ul>
            </div>

            <div className="card p-6 bg-card border border-line">
              <div className="doclabel mb-2">EVALUATION RUBRIC</div>
              <h3 className="font-mono text-lg font-bold text-white mb-3">How Your Work Is Graded</h3>
              <ul className="space-y-3 text-sm text-[var(--text-secondary)]">
                {track.evaluation.map((ev) => (
                  <li key={ev} className="flex items-start gap-2">
                    <Award size={16} className="text-accent shrink-0 mt-0.5" aria-hidden="true" />
                    <span>{ev}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* 10. Fee, Placement & Policy Transparency */}
      <div className="container pad-block">
        <div className="doclabel mb-2">§ 05 — FEE &amp; PLACEMENT POLICY</div>
        <h2 className="section-title mb-6">Transparent Fee &amp; Guarantee Terms</h2>
        <div className="grid gap-6 md:grid-cols-2">
          <div className="card p-6 bg-card border border-accent/40" style={{ background: 'linear-gradient(135deg, rgba(245,158,11,0.08), rgba(15,23,42,0.9))' }}>
            <span className="font-mono text-xs text-accent uppercase tracking-wider">₹1,999 Incubation · Tiered Value Ladder</span>
            <div className="text-3xl font-mono font-bold text-white mt-2 mb-2">
              {FELLOWSHIP_FEE.formattedTotal}{' '}
              <span className="text-sm text-muted font-normal">INR (2 Months · All Inclusive)</span>
            </div>
            <p className="text-xs text-[var(--text-secondary)] mb-3">
              {FELLOWSHIP_FEE.label} Candidates who have already paid the {FELLOWSHIP_FEE.formattedDeposit} caution deposit only complete the remaining {FELLOWSHIP_FEE.formattedBalance} balance via{' '}
              <Link href="/enroll/1999" className="text-accent underline">/enroll/1999</Link>.
            </p>
            <ul className="text-xs text-[var(--text-primary)] space-y-1.5 mb-4">
              <li>✅ <strong>1. Verified Certificate:</strong> Turnitin-scored 3-doc packet on <Link href="/verify" className="underline">/verify</Link></li>
              <li>💰 <strong>2. ₹5,000+ Stipend Unlock:</strong> Released at Gate 1 (3 approved PRs + &ge;75% attendance)</li>
              <li>🎯 <strong>3. 100% Placement Assistance:</strong> Round-1 screening waiver + Pre-Vetted Directory listing</li>
            </ul>
            <div className="flex flex-wrap gap-2 items-center mb-3">
              <Link
                href={`/enroll/1999?domain=${encodeURIComponent(track.name)}`}
                className="btn btn-primary btn-sm"
              >
                Enroll Now — {FELLOWSHIP_FEE.formattedTotal} &rarr;
              </Link>
              <Link
                href="/enroll/1999"
                className="btn btn-outline btn-sm"
              >
                Pay {FELLOWSHIP_FEE.formattedBalance} Balance
              </Link>
            </div>
            <div className="p-3 rounded-lg border border-line/70 bg-black/30 text-xs text-[var(--text-secondary)] mb-3">
              <strong className="text-white">3 Two-Month DBERT Tracks Compared:</strong>{' '}
              Beginner 0-to-1{' '}
              <Link href={`/learners/launchpad?domain=${encodeURIComponent(track.slug)}`} className="text-accent underline">
                Launchpad (₹7,999)
              </Link>{' '}
              &middot; Applied Intermediate{' '}
              <Link href={`/learners/accelerate?domain=${encodeURIComponent(track.slug)}`} className="text-accent underline">
                Accelerate (₹4,999)
              </Link>{' '}
              &middot; Production Client Repo{' '}
              <a href="https://lms.dbert.in/program" target="_blank" rel="noopener noreferrer" className="text-emerald-400 underline">
                Fellowship / LMS Program (₹1,999)
              </a>.
            </div>
            <p className="text-xs text-muted">
              Zero application fee for screening. Covered by our{' '}
              <Link href="/refund" className="underline">refund &amp; cancellation policy</Link> and{' '}
              <Link href="/terms" className="underline">terms of service</Link>.
            </p>
          </div>

          <div className="card p-6 bg-card border border-line">
            <span className="font-mono text-xs text-accent uppercase tracking-wider">Placement Guarantee Definition</span>
            <h3 className="font-mono text-base font-bold text-white mt-2 mb-2">
              What &ldquo;100% Guaranteed Production Internship&rdquo; Means
            </h3>
            <p className="text-xs text-[var(--text-secondary)] leading-relaxed mb-3">
              Upon completing your 8-week sprint milestones and passing senior code review, you are guaranteed assignment to an active internal DBERT portfolio venture (such as Gayatri AI, Alkame, or Aivara) or a verified partner squad. This is a real production internship assignment — not an unconditional full-time job offer.
            </p>
            <Link href="/learners/fellowship#placement-policy" className="text-xs font-mono text-accent hover:underline">
              Read full placement &amp; eligibility policy &rarr;
            </Link>
          </div>
        </div>
      </div>

      {/* 11. Verified Alumni Evidence (Real Registry Records Only) */}
      <div className="section-band border-t border-b border-line">
        <div className="container pad-block">
          <div className="doclabel mb-2">§ 06 — VERIFIED CREDENTIAL REGISTRY</div>
          <h2 className="section-title mb-2">Verified Fellows in This Domain</h2>
          <p className="text-sm text-muted mb-6">
            Real credential records from <Link href="/verify/directory" className="underline">dbert.in/verify/directory</Link>. Every ID is independently verifiable.
          </p>
          {verifiedAlumni.length > 0 ? (
            <div className="grid gap-4 md:grid-cols-3">
              {verifiedAlumni.map((alum) => (
                <Link
                  key={alum.certId}
                  href={alum.verifyUrl || `/verify/${alum.certId}`}
                  className="card p-5 bg-card border border-line hover:border-accent transition-colors"
                >
                  <div className="text-xs font-mono text-accent mb-1">{alum.certId}</div>
                  <div className="font-mono text-base font-bold text-white">{alum.holderName}</div>
                  <div className="text-xs text-muted mt-1">{alum.domain}</div>
                  {typeof alum.score === 'number' && (
                    <div className="text-xs font-mono text-ok mt-2">
                      Evaluated Score: {alum.score}/100 {alum.grade ? `(${alum.grade})` : ''}
                    </div>
                  )}
                </Link>
              ))}
            </div>
          ) : (
            <div className="card p-6 bg-card border border-line text-sm text-muted">
              No track-specific alumni cards are pinned here yet. Browse all verified fellows directly in the{' '}
              <Link href="/verify/directory" className="text-accent underline">public credential directory</Link>.
            </div>
          )}
        </div>
      </div>

      {/* 12. Regional Opportunities & Multi-City Target Hubs */}
      {track.regionalOpportunities.length > 0 && (
        <RegionalOpportunityBento
          sectionNumber="§ 07"
          title={`${track.name} Internships`}
          description={`Active squad openings for ${track.name} fellows across remote and hybrid hubs.`}
          domainName={track.name}
          hubHref={`https://lms.dbert.in/internships/${track.slug}`}
          jobsHref={`https://lms.dbert.in/jobs/${track.slug}`}
          opportunities={track.regionalOpportunities}
        />
      )}

      <div className="container pb-block">
        <div className="card p-6 bg-card border border-line">
          <div className="doclabel mb-2">§ 07B — MULTI-CITY COURSE &amp; INTERNSHIP HUBS (2027 COHORT)</div>
          <h3 className="font-mono text-lg font-bold text-white mb-2">
            {track.name} Course &amp; Internships Across All 18 Indian Tech Cities
          </h3>
          <p className="text-xs text-muted mb-4">
            Target your preferred metro corridor or join 100% remotely. Every city track connects directly to localized sprint details and the ₹1,999 fast-track seat:
          </p>
          <div className="flex flex-wrap gap-2">
            {Object.values(GEO_CITIES).map((city) => (
              <Link
                key={city.slug}
                href={`/learners/courses/${track.slug}/${city.slug}`}
                className="tag-chip text-xs font-mono hover:border-accent hover:text-accent transition-colors"
              >
                📍 {city.shortName} Course
              </Link>
            ))}
          </div>
          <div className="mt-4 pt-3 border-t border-line/50 text-xs text-muted">
            Looking for open internship roles? Browse{' '}
            <Link href={`/internships/${track.slug}`} className="text-accent underline">
              {track.name} Internships across 18 cities &rarr;
            </Link>
          </div>
        </div>
      </div>

      {/* 13. FAQs */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 08 — FREQUENTLY ASKED QUESTIONS</div>
        <h2 className="section-title mb-4">Common Questions</h2>
        <div className="measure">
          <FAQAccordion items={track.faqs} />
        </div>
      </div>

      {/* 14. Related Tracks */}
      {relatedTracks.length > 0 && (
        <div className="section-band border-t border-line">
          <div className="container pad-block">
            <div className="doclabel mb-2">§ 09 — RELATED TRACKS</div>
            <h2 className="section-title mb-6">Explore Adjacent Fellowship Tracks</h2>
            <div className="grid gap-4 md:grid-cols-3">
              {relatedTracks.map((rel) => (
                <Link
                  key={rel.slug}
                  href={rel.canonicalPath}
                  className="card p-5 bg-card border border-line hover:border-accent transition-colors"
                >
                  <span className="tag-chip text-xs font-mono">{rel.badge}</span>
                  <h3 className="font-mono text-base font-bold text-white mt-3 mb-1">{rel.name}</h3>
                  <p className="text-xs text-[var(--text-secondary)] mb-3">{rel.shortDescription}</p>
                  <span className="text-xs font-mono text-accent">Explore Curriculum &rarr;</span>
                </Link>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* 15. Application & Admissions Handoff */}
      <div className="container pad-block">
        <div className="grid gap-8 lg:grid-cols-2 items-start">
          <div className="card p-8 bg-card border border-line">
            <div className="doclabel mb-2">§ 10 — APPLY OR TALK TO ADMISSIONS</div>
            <h2 className="text-2xl font-bold text-white mb-3">
              Ready to apply for {track.name}?
            </h2>
            <p className="text-sm text-[var(--text-secondary)] mb-6">
              Screening is 100% free with zero application fee. Submit your GitHub/application on the LMS portal, or message admissions on WhatsApp if you need guidance before applying.
            </p>
            <div className="stack-h gap-3 flex-wrap">
              <Link
                href={`/enroll/1999?domain=${encodeURIComponent(track.name)}`}
                className="btn btn-primary btn-lg"
              >
                Enroll Now — {FELLOWSHIP_FEE.formattedTotal} &rarr;
              </Link>
              <a
                href={whatsappUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-outline btn-lg inline-flex items-center gap-2"
              >
                <MessageSquare size={16} aria-hidden="true" />
                <span>WhatsApp Admissions</span>
              </a>
              <a
                href={applyUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="text-xs font-mono text-muted hover:text-accent underline ml-1"
              >
                External screening option (LMS) ↗
              </a>
            </div>
          </div>

          <TrackLeadCaptureForm
            initialDomain={track.slug}
            initialProgram="fellowship"
            title={`Request ${track.name} Syllabus`}
            subtitle="Receive track details and speak with an engineering mentor."
          />
        </div>
      </div>
    </div>
  );
}
