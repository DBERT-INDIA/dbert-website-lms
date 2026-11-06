import React from 'react';
import Link from 'next/link';
import Script from 'next/script';
import { pageMetadata } from '@/lib/seo';
import FAQAccordion from '@/components/ui/FAQAccordion';
import s from './dbert-online.module.css';

export const metadata = pageMetadata('/dbert-online');

const faqList = [
  {
    question: 'Why did DBERT replace dbert.online with dbert.in?',
    answer:
      'DBERT unified its global and national infrastructure under the sovereign Indian top-level domain (.in). As an MSME-registered venture studio and deeptech foundry operating from Delhi NCR, dbert.in represents our primary authoritative brand for startup incubation, software products, and developer fellowships.',
  },
  {
    question: 'Is dbert.online still active or operated by DBERT?',
    answer:
      'No. dbert.online is not the active platform anymore. All official operations, code repositories, student dashboards, and partner services have permanently transitioned to dbert.in and its subdomains (lms.dbert.in, api.dbert.in). Any traffic reaching dbert.online is automatically 301-redirected to dbert.in.',
  },
  {
    question: 'Are internship certificates issued under dbert.online still valid?',
    answer:
      'Yes, absolutely. All certificates, academic rubrics, and letters of recommendation issued during the dbert.online tenure remain 100% cryptographically authentic. You can verify any credential ID at dbert.in/verify regardless of which domain URL is printed on legacy documents.',
  },
  {
    question: 'Where do registered students and fellows log into their LMS dashboard?',
    answer:
      'Interns and fellowship candidates should navigate to https://lms.dbert.in to access course materials, weekly sprint submissions, code reviews, and stipend tracking.',
  },
  {
    question: 'How can I ensure I am communicating with the authentic DBERT team?',
    answer:
      'All legitimate communications originate exclusively from @dbert.in or @dbert.info email addresses and our verified contact number (+91 89580 06294). DBERT never conducts official operations or collects fees through unverified third-party domains.',
  },
];

const structuredFaqData = {
  '@context': 'https://schema.org',
  '@type': 'FAQPage',
  mainEntity: faqList.map((item) => ({
    '@type': 'Question',
    name: item.question,
    acceptedAnswer: {
      '@type': 'Answer',
      text: item.answer,
    },
  })),
};

const breadcrumbData = {
  '@context': 'https://schema.org',
  '@type': 'BreadcrumbList',
  itemListElement: [
    {
      '@type': 'ListItem',
      position: 1,
      name: 'Home',
      item: 'https://dbert.in',
    },
    {
      '@type': 'ListItem',
      position: 2,
      name: 'DBERT.online Domain Notice',
      item: 'https://dbert.in/dbert-online',
    },
  ],
};

export default function DbertOnlineMigrationPage() {
  return (
    <div className={`wrap ${s.pageWrap}`}>
      <Script
        id="domain-migration-faq-schema"
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredFaqData) }}
      />
      <Script
        id="domain-migration-breadcrumb-schema"
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbData) }}
      />

      {/* ── HERO SECTION ── */}
      <section className={s.hero}>
        <div className={s.eyebrow}>
          <span className={s.pulseDot} aria-hidden="true" />
          <span>Official Domain Migration Advisory · Rev 2026.2</span>
        </div>
        <h1 className={s.heroTitle}>
          DBERT.online is Now DBERT.in
        </h1>
        <p className={s.heroSub}>
          Official notice on the domain migration of Digital Blinc Education Research And Technology.
          Please note that <strong>dbert.online is not the active platform</strong>; our authoritative
          incubation programs, enterprise AI software, learning portal, and credential registries
          are hosted exclusively at <strong>dbert.in</strong>.
        </p>

        {/* ── SECURITY / CLARIFICATION BANNER ── */}
        <div className={s.securityBanner}>
          <div className={s.securityHeader}>
            <span className={s.securityBadge}>Security &amp; Authenticity Notice</span>
            <h2 className={s.securityTitle}>dbert.online is Not the Operating Web Domain</h2>
          </div>
          <p className={s.securityText}>
            To protect learners, founders, and enterprise partners against outdated bookmarks or unauthorized
            clones, DBERT has consolidated all digital assets under <strong>dbert.in</strong>. All legacy links targeting
            dbert.online are permanently redirected via HTTP 301 to ensure uninterrupted continuity.
          </p>

          <div className={s.domainCompareGrid}>
            <div className={s.domainBoxOld}>
              <span className={`${s.domainStatusLabel} ${s.domainStatusOld}`}>Legacy Domain (Deprecated)</span>
              <span className={s.domainValue}>dbert.online</span>
            </div>
            <div className={s.domainBoxNew}>
              <span className={`${s.domainStatusLabel} ${s.domainStatusNew}`}>Authoritative Domain (Active)</span>
              <span className={s.domainValue}>dbert.in</span>
            </div>
          </div>
        </div>
      </section>

      {/* ── DESTINATIONS BENTO GRID ── */}
      <section>
        <h2 className={s.sectionTitle}>Official DBERT Services &amp; Destinations</h2>
        <p className={s.sectionLead}>
          Access verified portals directly on dbert.in for your venture incubation, career progression, and credentials.
        </p>

        <div className={s.bentoGrid}>
          <div className={s.bentoCard}>
            <div className={s.bentoCardTop}>
              <span className={s.bentoCardTag}>LMS &amp; Fellowships</span>
              <h3 className={s.bentoCardTitle}>Learning Management System</h3>
              <p className={s.bentoCardDesc}>
                Access active internship cohorts, sprint tasks, pull request reviews, and remote AI developer fellowships.
              </p>
            </div>
            <a
              href="https://lms.dbert.in"
              target="_blank"
              rel="noopener noreferrer"
              className={s.bentoCardLink}
            >
              Launch LMS Portal (lms.dbert.in) →
            </a>
          </div>

          <div className={s.bentoCard}>
            <div className={s.bentoCardTop}>
              <span className={s.bentoCardTag}>Verification Registry</span>
              <h3 className={s.bentoCardTitle}>Verify Certificate ID</h3>
              <p className={s.bentoCardDesc}>
                Validate cryptographic 256-bit credentials, academic rubrics, and project attributions issued to alumni.
              </p>
            </div>
            <Link href="/verify" className={s.bentoCardLink}>
              Verify Credentials (dbert.in/verify) →
            </Link>
          </div>

          <div className={s.bentoCard}>
            <div className={s.bentoCardTop}>
              <span className={s.bentoCardTag}>Venture Studio</span>
              <h3 className={s.bentoCardTitle}>Startup Incubation</h3>
              <p className={s.bentoCardDesc}>
                Services-against-equity co-development for technical founders building AI MVPs with 100% code ownership.
              </p>
            </div>
            <Link href="/startups" className={s.bentoCardLink}>
              Explore Incubation (dbert.in/startups) →
            </Link>
          </div>

          <div className={s.bentoCard}>
            <div className={s.bentoCardTop}>
              <span className={s.bentoCardTag}>Enterprise Software</span>
              <h3 className={s.bentoCardTitle}>Enterprise AI Solutions</h3>
              <p className={s.bentoCardDesc}>
                Production-grade VPC LLM chat, document AI OCR pipelines, and hiring automation systems ready to deploy.
              </p>
            </div>
            <Link href="/ai-solutions" className={s.bentoCardLink}>
              Browse AI Products (dbert.in/ai-solutions) →
            </Link>
          </div>
        </div>
      </section>

      {/* ── SECURITY BEST PRACTICES ── */}
      <section>
        <h2 className={s.sectionTitle}>Authenticity &amp; Security Verification Guidelines</h2>
        <p className={s.sectionLead}>
          Ensure you are interacting with genuine DBERT digital infrastructure across all channels.
        </p>

        <div className={s.trustGrid}>
          <div className={s.trustCard}>
            <h3 className={s.trustCardTitle}>1. Check Browser Address</h3>
            <p className={s.trustCardDesc}>
              Confirm the address bar displays <code>https://dbert.in</code> or official subdomains such as <code>lms.dbert.in</code>.
            </p>
          </div>

          <div className={s.trustCard}>
            <h3 className={s.trustCardTitle}>2. Look for Valid SSL</h3>
            <p className={s.trustCardDesc}>
              All legitimate DBERT web endpoints feature modern HTTPS TLS encryption issued to our official entity.
            </p>
          </div>

          <div className={s.trustCard}>
            <h3 className={s.trustCardTitle}>3. Verify Email Senders</h3>
            <p className={s.trustCardDesc}>
              Official correspondence is dispatched exclusively from <code>@dbert.in</code> or <code>@dbert.info</code> domains.
            </p>
          </div>

          <div className={s.trustCard}>
            <h3 className={s.trustCardTitle}>4. MSME Statutory Proof</h3>
            <p className={s.trustCardDesc}>
              DBERT is registered under the Ministry of MSME, Government of India. Review our statutory credentials on our about page.
            </p>
          </div>
        </div>
      </section>

      {/* ── FREQUENTLY ASKED QUESTIONS ── */}
      <section className={s.faqSection}>
        <h2 className={s.sectionTitle}>Frequently Asked Questions About the Migration</h2>
        <p className={s.sectionLead}>
          Answers regarding our transition from dbert.online to dbert.in, certificate validity, and portal links.
        </p>
        <FAQAccordion items={faqList} />
      </section>
    </div>
  );
}
