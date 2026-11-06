'use client';

import React from 'react';
import Link from 'next/link';
import styles from './Footer.module.css';
import { trackEvent } from '@/lib/analytics';

interface FooterLink {
  label: string;
  href: string;
  external?: boolean;
}

interface FooterColumn {
  label: string;
  links: FooterLink[];
}

const columns: FooterColumn[] = [
  {
    label: 'Startups & Equity',
    links: [
      { label: 'AI Venture Incubation', href: '/startups' },
      { label: 'Services Directory', href: '/startups/services' },
      { label: 'Services Against Equity', href: '/startups/services/equity' },
      { label: 'FAST Agreement & Term Sheets', href: '/startups/services/equity/term-sheets' },
      { label: 'Technical Co-Founder', href: '/startups/services/technical' },
      { label: 'Pre-Seed Grants & Compute', href: '/startups/services/funding' },
      { label: 'Portfolio Startups', href: '/startups/portfolio' },
    ],
  },
  {
    label: 'Enterprise AI',
    links: [
      { label: 'Enterprise Solutions Overview', href: '/ai-solutions' },
      { label: 'Products Directory', href: '/ai-solutions/products' },
      { label: 'DBERT Chat (VPC LLM)', href: '/ai-solutions/products/dbert-chat' },
      { label: 'Document AI OCR Pipeline', href: '/ai-solutions/products/document-ai' },
      { label: 'Certificate Verification API', href: '/ai-solutions/products/certificate-verification-api' },
      { label: 'AI Hiring Suite & ATS', href: '/ai-solutions/products/hiring-automation-suite' },
      { label: 'Intern Management Software', href: '/ai-solutions/products/intern-management-system' },
    ],
  },
  {
    label: 'AI Academy',
    links: [
      { label: 'AI Career Roadmap', href: '/learners' },
      { label: 'Full Stack AI Development', href: '/learners/courses/full-stack-development' },
      { label: 'Data Analytics & Power BI', href: '/learners/courses/data-analytics' },
      { label: 'Python Automation & Scraping', href: '/learners/courses/python-automation' },
      { label: 'AI Agent Development', href: '/learners/courses/ai-agent-development' },
      { label: 'Paid AI Fellowship Track', href: '/learners/fellowship' },
      { label: 'All Engineering Tracks', href: '/learners/courses' },
    ],
  },
  {
    label: 'Labs & Trust',
    links: [
      { label: 'DBERT Applied Labs', href: '/labs' },
      { label: 'Technical Preprints', href: '/labs/publications' },
      { label: 'Open Source Repositories', href: '/labs/opensource' },
      { label: 'Verify Credential ID', href: '/verify' },
      { label: 'MSME Statutory Audit', href: '/about/credentials' },
      { label: 'Engineering Team', href: '/about/team' },
      { label: 'Commercial Retainers', href: '/pricing' },
    ],
  },
  {
    label: 'Live Opportunities',
    links: [
      { label: 'Full Stack Internships Mumbai', href: 'https://lms.dbert.in/internships/booking-system-development-intern-mumbai-remote-50', external: true },
      { label: 'Data Analyst Bangalore', href: 'https://lms.dbert.in/internships/operations-data-analyst-intern-bangalore-remote-28', external: true },
      { label: 'AI Agent Roles Delhi NCR', href: 'https://lms.dbert.in/internships/agentic-search-systems-intern-delhi-ncr-remote-11', external: true },
      { label: 'Python Automation Pune', href: 'https://lms.dbert.in/internships/social-media-automation-intern-pune-remote-67', external: true },
      { label: 'Virtual Remote Sprints', href: 'https://lms.dbert.in/internships/virtual-remote-internships', external: true },
      { label: 'Paid Internships With Stipend', href: 'https://lms.dbert.in/internships/paid-internships', external: true },
      { label: 'Job Board & Placement Hub', href: 'https://lms.dbert.in/jobs', external: true },
    ],
  },
];

export default function Footer() {
  return (
    <footer className={styles.footer} role="contentinfo">
      <div className="wrap">
        <div className={styles.grid}>
          <div className={styles.brandCol}>
            <Link href="/" className={styles.logo}>
              <span className={styles.logoMark} aria-hidden="true">
                D
              </span>
              <span className={styles.brandName}>DBERT</span>
            </Link>
            <p className={styles.blurb}>
              Digital Blinc Education Research And Technology. India&apos;s AI venture studio —
              equity-based startup incubation, enterprise sovereign products, and production engineering fellowship under one roof.
            </p>

            <div style={{ marginTop: '14px', marginBottom: '8px' }}>
              <span className="stamp-seal">MSME REGISTERED · NCR-HQ</span>
            </div>

            <address className={styles.contact}>
              <a
                href="mailto:contactus@dbert.in"
                onClick={() => trackEvent('contact_email_click')}
              >
                contactus@dbert.in
              </a>
              <a
                href="tel:+918958006294"
                onClick={() => trackEvent('contact_phone_click')}
              >
                +91 89580 06294
              </a>
              <span className={styles.addressLine}>Delhi NCR, India · Sovereign AI Studio</span>
            </address>

            <div className={styles.social}>
              <a
                href="https://www.linkedin.com/company/dbert"
                target="_blank"
                rel="noopener noreferrer"
                onClick={() => trackEvent('social_click', { platform: 'linkedin' })}
              >
                LinkedIn
              </a>
              <a
                href="https://www.youtube.com/@dbert-india"
                target="_blank"
                rel="noopener noreferrer"
                onClick={() => trackEvent('social_click', { platform: 'youtube' })}
              >
                YouTube
              </a>
              <a
                href="https://github.com/DBERT-INDIA"
                target="_blank"
                rel="noopener noreferrer"
                onClick={() => trackEvent('social_click', { platform: 'github' })}
              >
                GitHub
              </a>
            </div>
          </div>

          {columns.map((column) => (
            <div key={column.label} className={styles.col}>
              <div className={styles.colLabel}>{column.label}</div>
              <ul className={styles.linkList}>
                {column.links.map((link) => (
                  <li key={link.href}>
                    {link.external ? (
                      <a
                        href={link.href}
                        target="_blank"
                        rel="noopener noreferrer"
                        className={styles.footerLink}
                        onClick={() => trackEvent('footer_link_click', { label: link.label, href: link.href, external: true })}
                      >
                        <span>{link.label}</span>
                        <span className={styles.externalMark} aria-hidden="true">↗</span>
                      </a>
                    ) : (
                      <Link
                        href={link.href}
                        className={styles.footerLink}
                        onClick={() => trackEvent('footer_link_click', { label: link.label, href: link.href, external: false })}
                      >
                        {link.label}
                      </Link>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* ═══ REGIONAL SEO KEYWORD MESH BAR ═══ */}
        <div className={styles.seoMeshBar}>
          <div className={styles.seoMeshTitle}>POPULAR SEARCH TOPICS &amp; REGIONAL DIRECTORY</div>
          <div className={styles.seoMeshLinks}>
            <a href="https://lms.dbert.in/internships/full-stack-development" target="_blank" rel="noopener noreferrer">Full Stack Internships Mumbai &amp; Bangalore</a>
            <span className={styles.dot}>·</span>
            <a href="https://lms.dbert.in/internships/data-analyst-internship-work-from-home" target="_blank" rel="noopener noreferrer">Data Analyst Work From Home</a>
            <span className={styles.dot}>·</span>
            <a href="https://lms.dbert.in/internships/ai-automation-internship" target="_blank" rel="noopener noreferrer">AI Automation Internships Bangalore</a>
            <span className={styles.dot}>·</span>
            <a href="https://lms.dbert.in/jobs/full-stack-development" target="_blank" rel="noopener noreferrer">Full Stack AI Developer Jobs</a>
            <span className={styles.dot}>·</span>
            <Link href="/startups">AI Startup Incubator Delhi NCR</Link>
            <span className={styles.dot}>·</span>
            <Link href="/hire/pre-vetted-engineers">Hire Vetted AI Engineers India</Link>
            <span className={styles.dot}>·</span>
            <Link href="/ai-solutions/llm-training/private-hosting">Private Enterprise GPU LLM Hosting</Link>
            <span className={styles.dot}>·</span>
            <Link href="/learners/courses/python-automation">Python Automation Training India</Link>
            <span className={styles.dot}>·</span>
            <Link href="/about">MSME Registered DeepTech Foundry</Link>
            <span className={styles.dot}>·</span>
            <Link href="/dbert-online">DBERT.online is Now DBERT.in Notice</Link>
          </div>
        </div>

        <div className={styles.base}>
          <span>© {new Date().getFullYear()} DBERT · dbert.in · All rights reserved</span>
          <span className={styles.made}>
            handmade in Delhi <b>·</b> fueled by chai ☕
          </span>
          <span className={styles.legal}>
            <Link href="/privacy">Privacy</Link> · <Link href="/terms">Terms</Link> ·{' '}
            <Link href="/refund">Refund Policy</Link>
          </span>
        </div>

        <div className={styles.domainNoticeBar}>
          <Link href="/dbert-online" className={styles.domainNoticeLink}>
            Domain Notice: DBERT.online is now DBERT.in.
          </Link>
        </div>
      </div>
    </footer>
  );
}
