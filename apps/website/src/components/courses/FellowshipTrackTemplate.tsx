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
      <div className="hero-glow" aria-hidden="true" />

      {/* 1. Breadcrumb */}
      <div className="container" style={{ paddingTop: '2rem', position: 'relative', zIndex: 1 }}>
        <nav aria-label="Breadcrumb" className="text-xs font-mono text-muted mb-6 flex items-center gap-2 flex-wrap">
          <Link href="/" className="hover:text-accent">Home</Link>
          <span aria-hidden="true">/</span>
          <Link href="/learners/courses" className="hover:text-accent">Fellowship Tracks</Link>
          <span aria-hidden="true">/</span>
          <span className="text-[var(--text-primary)]">{track.name}</span>
        </nav>
      </div>

      {/* 2. Hero — Left-aligned, high-impact */}
      <div className="container" style={{ paddingBottom: '3.5rem', position: 'relative', zIndex: 1 }}>
        <div style={{ maxWidth: '820px' }}>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-accent/30 bg-accent/10 text-xs font-mono text-accent mb-5">
            <span>{track.badge}</span>
          </div>

          <h1 style={{ fontSize: 'clamp(2.1rem, 4.5vw, 3.5rem)', fontWeight: 800, lineHeight: 1.08, color: '#fff', marginBottom: '1.1rem', letterSpacing: '-0.025em' }}>
            {track.name}
            <br />
            <span style={{ background: 'linear-gradient(90deg, #38bdf8, #818cf8)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', display: 'inline-block' }}>
              Applied Fellowship
            </span>
          </h1>

          <p style={{ fontSize: '1.12rem', color: 'var(--text-secondary)', lineHeight: 1.65, maxWidth: '58ch', marginBottom: '1.75rem' }}>
            {track.heroOutcome}
          </p>

          {/* Trust proof-marks */}
          <div className="flex gap-2.5 flex-wrap mb-7 text-xs font-mono">
            <span className="proof-mark">
              <span>Fee: {FELLOWSHIP_FEE.formattedTotal} All Inclusive</span>
            </span>
            <span className="proof-mark">
              <span>Duration: {track.duration}</span>
            </span>
            <span className="proof-mark">
              <span>{track.weeklyCommitment} Weekly</span>
            </span>
            <Link href="/learners/fellowship#placement-policy" className="proof-mark proof-mark-signal">
              <span>100% Guaranteed Internship</span>
            </Link>
          </div>

          {/* Primary CTAs */}
          <div className="stack-h gap-3 flex-wrap">
            <a href="#apply-lead-form" className="btn btn-primary btn-lg">
              Request Syllabus &amp; Apply &rarr;
            </a>
            <Link
              href={`/enroll/1999?domain=${encodeURIComponent(track.name)}`}
              className="btn btn-outline btn-lg"
            >
              Confirm Seat — {FELLOWSHIP_FEE.formattedTotal}
            </Link>
            <a href="#curriculum" className="btn btn-outline btn-lg">
              View 8-Week Syllabus
            </a>
          </div>

          {/* Responsive Hero Metrics */}
          <div className="hero-metrics">
            <div className="hero-metric">
              <div className="hero-metric-value">65+</div>
              <div className="hero-metric-label">Verified Fellows</div>
            </div>
            <div className="hero-metric">
              <div className="hero-metric-value">4</div>
              <div className="hero-metric-label">Live Venture Repos</div>
            </div>
            <div className="hero-metric">
              <div className="hero-metric-value">₹5,000</div>
              <div className="hero-metric-label">5,000 Coins Stipend</div>
            </div>
            <div className="hero-metric">
              <div className="hero-metric-value">2 Mo</div>
              <div className="hero-metric-label">Sprint Structure</div>
            </div>
          </div>
        </div>
      </div>

      {/* 3. Trust / Evidence Strip */}
      <section className="section-alt">
        <div className="container">
          <h2 className="section-heading">Built on Production Standards</h2>
          <p className="section-subheading">
            Every fellow ships real code to active venture repositories under senior architectural review.
          </p>
          <div className="bento-grid-3">
            <div className="bento-card center">
              <span className="icon-chip"><GitPullRequest aria-hidden="true" /></span>
              <h3 className="accent-note">Senior Mentor Code Reviews</h3>
              <p className="text-sm">Every project submission is reviewed by a senior engineer for code quality, security, and testing before approval.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><ShieldCheck aria-hidden="true" /></span>
              <h3 className="accent-note">Verified Certificates</h3>
              <p className="text-sm">Graduates receive an official certificate, scorecard, and recommendation letter verifiable by employers on <Link href="/verify" className="underline">dbert.in/verify</Link>.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><Clock aria-hidden="true" /></span>
              <h3 className="accent-note">2-Month Guided Schedule</h3>
              <p className="text-sm">Remote milestone-based weeks designed to fit alongside college classes or existing engineering work.</p>
            </div>
          </div>
        </div>
      </section>

      {/* 4. Lead Capture Form — Placed directly below Trust Strip */}
      <section className="section-band-clear">
        <div className="container">
          <h2 className="section-heading">Get the Syllabus &amp; Fast-Track Screening</h2>
          <p className="section-subheading">
            Submit your details to receive the {track.name} curriculum dossier and connect with our admissions team.
          </p>
          <div className="max-w-xl mx-auto">
            <TrackLeadCaptureForm
              initialDomain={track.slug}
              initialProgram="fellowship"
              title={`Apply — ${track.name}`}
              subtitle="Get your syllabus dossier and talk with an engineering mentor."
            />
          </div>
        </div>
      </section>

      {/* 5. Overview, Who Should Apply, Prerequisites & Outcomes */}
      <section className="section-band-clear">
        <div className="container">
          <h2 className="section-heading">What You Will Build &amp; Ship</h2>
          <p className="section-subheading">{track.fullDescription}</p>

          <div className="grid gap-6 md:grid-cols-2 mb-10">
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

          <div className="card p-6 bg-card border border-line max-w-4xl mx-auto">
            <h3 className="font-mono text-base font-bold text-white mb-4">Key Engineering Outcomes</h3>
            <ul className="grid gap-3 md:grid-cols-2">
              {track.outcomes.map((outcome) => (
                <li key={outcome} className="flex items-start gap-2.5 text-sm text-[var(--text-secondary)]">
                  <CheckCircle2 size={16} className="text-ok shrink-0 mt-0.5" aria-hidden="true" />
                  <span>{outcome}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </section>

      {/* 6. Technologies & Why Each Is Used */}
      <section className="section-alt">
        <div className="container">
          <h2 className="section-heading">Tools &amp; Skills You Will Master</h2>
          <p className="section-subheading">
            Industry-standard frameworks and tools you will configure, test, and build with in real projects.
          </p>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {track.technologies.map((tech) => (
              <div key={tech.name} className="card p-5 bg-card border border-line">
                <div className="font-mono text-sm font-bold text-accent mb-2">{tech.name}</div>
                <p className="text-xs text-[var(--text-secondary)] leading-relaxed">{tech.role}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 7. Week-by-Week Curriculum Accordion */}
      <section id="curriculum" className="section-band-clear">
        <div className="container">
          <h2 className="section-heading">8-Week Learning Roadmap</h2>
          <p className="section-subheading">
            Step-by-step weekly modules with mentor-reviewed real-world projects.
          </p>
          <div className="max-w-3xl mx-auto">
            <CurriculumAccordion trackId={track.id} modules={track.curriculum} />
          </div>
        </div>
      </section>

      {/* 8. Capstone & Repository Status */}
      <section className="section-alt">
        <div className="container">
          <h2 className="section-heading">Final Project &amp; Grading</h2>
          <p className="section-subheading">
            Graduate by shipping a real project with a live team and passing senior mentor review.
          </p>
          <div className="grid gap-6 md:grid-cols-2">
            <div className="card p-6 bg-card border border-line">
              <div className="flex items-center justify-between gap-2 mb-3 flex-wrap">
                <span className="tag-chip text-xs font-mono">
                  {track.capstone.status === 'active' ? 'Live Team Project' : 'Guided Final Project'}
                </span>
                <span className="text-xs font-mono text-muted">Team: {track.capstone.ventureName}</span>
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
                  <span>View Live Project</span>
                  <ExternalLink size={13} aria-hidden="true" />
                </a>
              )}
              <h4 className="font-mono text-xs uppercase tracking-wider text-muted mt-5 mb-2">
                Completion Checklist
              </h4>
              <ul className="list-disc pl-5 text-xs text-[var(--text-secondary)] space-y-1.5">
                {track.capstone.acceptanceCriteria.map((c) => (
                  <li key={c}>{c}</li>
                ))}
              </ul>
            </div>

            <div className="card p-6 bg-card border border-line">
              <div className="text-xs font-mono uppercase tracking-wider text-accent mb-2">Grading Criteria</div>
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
      </section>

      {/* 9. Fee, Placement & Policy Transparency */}
      <section className="section-band-clear">
        <div className="container">
          <h2 className="section-heading">Transparent Fee &amp; Guarantee Terms</h2>
          <p className="section-subheading">
            All-inclusive tuition with zero hidden charges, backed by verified certificates and internship placement.
          </p>
          <div className="grid gap-6 md:grid-cols-2">
            <div className="card p-6 bg-card border border-accent/40" style={{ background: 'linear-gradient(135deg, rgba(245,158,11,0.08), rgba(15,23,42,0.9))' }}>
              <div className="font-mono text-xs text-accent uppercase tracking-wider mb-2">₹1,999 Total · All Inclusive · 2 Months</div>
              <div className="text-3xl font-mono font-bold text-white mb-3">
                {FELLOWSHIP_FEE.formattedTotal}{' '}
                <span className="text-sm text-muted font-normal">INR (2 Months · All Inclusive)</span>
              </div>
              <p className="text-xs text-[var(--text-secondary)] mb-4">
                Total 2-month fellowship fee (includes mentorship, project reviews, live team placement &amp; verified certificate). Complete your enrollment at{' '}
                <Link href="/enroll/1999" className="text-accent underline">/enroll/1999</Link>.
              </p>
              <ul className="text-xs text-[var(--text-primary)] space-y-2 mb-5">
                <li>✅ <strong>1. Verified Certificate:</strong> Plagiarism-checked certificate &amp; recommendation letter on <Link href="/verify" className="underline">/verify</Link></li>
                <li>💰 <strong>2. ₹5,000 Stipend (5,000 Coins via UPI):</strong> Unlocked after 2-month completion (10 hrs/wk, 2 certifications, 75 tasks &amp; approved capstone) + up to ₹18,000 Ambassador bonus</li>
                <li>🎯 <strong>3. 100% Placement Assistance:</strong> Fast-track interviews + verified graduate profile</li>
              </ul>
              <div className="flex flex-wrap gap-2 items-center mb-4">
                <Link
                  href={`/enroll/1999?domain=${encodeURIComponent(track.name)}`}
                  className="btn btn-primary btn-sm"
                >
                  Enroll Now — {FELLOWSHIP_FEE.formattedTotal} &rarr;
                </Link>
              </div>
              <div className="p-3 rounded-lg border border-line/70 bg-black/30 text-xs text-[var(--text-secondary)] mb-3">
                <strong className="text-white">Compare 2-Month DBERT Tracks:</strong>{' '}
                Beginner{' '}
                <Link href={`/learners/launchpad?domain=${encodeURIComponent(track.slug)}`} className="text-accent underline">
                  Launchpad (₹7,999)
                </Link>{' '}
                &middot; Intermediate{' '}
                <Link href={`/learners/accelerate?domain=${encodeURIComponent(track.slug)}`} className="text-accent underline">
                  Accelerate (₹4,999)
                </Link>{' '}
                &middot; Live Team{' '}
                <a href="https://lms.dbert.in/program" target="_blank" rel="noopener noreferrer" className="text-emerald-400 underline">
                  Fellowship (₹1,999)
                </a>.
              </div>
              <p className="text-xs text-muted">
                Two internship tracks: ₹499 Security Deposit Track on LMS or ₹1,999 Fellowship. Covered by our{' '}
                <Link href="/refund" className="underline">refund policy</Link> and{' '}
                <Link href="/terms" className="underline">terms of service</Link>.
              </p>
            </div>

            <div className="card p-6 bg-card border border-line">
              <div className="font-mono text-xs text-accent uppercase tracking-wider mb-2">Placement Guarantee</div>
              <h3 className="font-mono text-base font-bold text-white mb-3">
                What &ldquo;100% Guaranteed Internship&rdquo; Means
              </h3>
              <p className="text-xs text-[var(--text-secondary)] leading-relaxed mb-4">
                Upon completing your 8-week milestones and passing mentor review, you are guaranteed placement onto an active DBERT partner project (such as Gayatri AI, Alkame, or Aivara) or a verified hiring partner team. This is a real hands-on internship placement — not an unconditional full-time job offer.
              </p>
              <Link href="/learners/fellowship#placement-policy" className="text-xs font-mono text-accent hover:underline">
                Read full placement &amp; eligibility policy &rarr;
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* 10. Verified Alumni Evidence */}
      <section className="section-alt">
        <div className="container">
          <h2 className="section-heading">Verified Graduates</h2>
          <p className="section-subheading">
            Real graduate records from <Link href="/verify/directory" className="underline">dbert.in/verify/directory</Link>. Every certificate ID is independently verifiable.
          </p>
          {verifiedAlumni.length > 0 ? (
            <div className="grid gap-4 md:grid-cols-3">
              {verifiedAlumni.map((alum) => (
                <Link
                  key={alum.certId}
                  href={alum.verifyUrl || `/verify/${alum.certId}`}
                  className="card p-5 bg-card border border-line hover:border-accent transition-colors block"
                >
                  <div className="text-xs font-mono text-accent mb-2">{alum.certId}</div>
                  <div className="font-mono text-base font-bold text-white mb-1">{alum.holderName}</div>
                  <div className="text-xs text-muted mb-2">{alum.domain}</div>
                  {typeof alum.score === 'number' && (
                    <div className="text-xs font-mono text-ok pt-2 border-t border-line/50">
                      Evaluated Score: {alum.score}/100 {alum.grade ? `(${alum.grade})` : ''}
                    </div>
                  )}
                </Link>
              ))}
            </div>
          ) : (
            <div className="card p-6 bg-card border border-line text-sm text-muted">
              No track-specific graduate cards are pinned here yet. Browse all verified graduates in the{' '}
              <Link href="/verify/directory" className="text-accent underline">public graduate directory</Link>.
            </div>
          )}
        </div>
      </section>

      {/* 11. Mid-Page CTA Conversion Banner */}
      <section className="section-band-clear">
        <div className="container">
          <div className="cta-banner">
            <div className="cta-inline-band">
              <div>
                <h2 className="text-2xl font-bold text-white mb-2">
                  Ready to join the {track.name} Fellowship?
                </h2>
                <p className="text-sm text-[var(--text-secondary)]">
                  No free track: Lock your ₹1,999 Fellowship seat or choose the ₹499 Security Deposit Track via admissions.
                </p>
              </div>
              <div className="stack-h gap-3 flex-wrap" style={{ minWidth: 'max-content' }}>
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
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 12. Regional Opportunities & Multi-City Target Hubs */}
      {track.regionalOpportunities.length > 0 && (
        <RegionalOpportunityBento
          sectionNumber=""
          title={`${track.name} Internships`}
          description={`Active squad openings for ${track.name} fellows across remote and hybrid hubs.`}
          domainName={track.name}
          hubHref={`https://lms.dbert.in/internships/${track.slug}`}
          jobsHref={`https://lms.dbert.in/jobs/${track.slug}`}
          opportunities={track.regionalOpportunities}
        />
      )}

      <section className="section-band-clear">
        <div className="container">
          <h2 className="section-heading">Regional Hubs &amp; City Tracks</h2>
          <p className="section-subheading">
            Target your preferred metro corridor or join 100% remotely across all 18 Indian tech cities.
          </p>
          <div className="card p-6 bg-card border border-line">
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
      </section>

      {/* 13. FAQs */}
      <section className="section-alt">
        <div className="container">
          <h2 className="section-heading">Frequently Asked Questions</h2>
          <p className="section-subheading">
            Everything you need to know about cohort schedules, code reviews, and credential verification.
          </p>
          <div className="measure mx-auto">
            <FAQAccordion items={track.faqs} />
          </div>
        </div>
      </section>

      {/* 14. Related Tracks */}
      {relatedTracks.length > 0 && (
        <section className="section-band-clear">
          <div className="container">
            <h2 className="section-heading">Explore Adjacent Fellowship Tracks</h2>
            <p className="section-subheading">
              Compare closely related engineering tracks in the DBERT curriculum.
            </p>
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
        </section>
      )}

      {/* 15. Final CTA Band */}
      <section className="section-alt">
        <div className="container">
          <div className="cta-banner">
            <div className="cta-inline-band">
              <div>
                <h2 className="text-2xl font-bold text-white mb-2">
                  Confirm Your {track.name} Seat
                </h2>
                <p className="text-sm text-[var(--text-secondary)]">
                  Two official tracks: ₹1,999 Fellowship direct or ₹499 Security Deposit Track via LMS ({applyUrl.replace('https://', '')}).
                </p>
              </div>
              <div className="stack-h gap-3 flex-wrap" style={{ minWidth: 'max-content' }}>
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
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
