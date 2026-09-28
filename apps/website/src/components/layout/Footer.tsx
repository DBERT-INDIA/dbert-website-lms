import React from 'react';
import Link from 'next/link';
import styles from './Footer.module.css';

const columns = [
  {
    label: 'Startups',
    links: [
      { label: 'Incubation Program', href: '/startups' },
      { label: 'Services Directory', href: '/startups/services' },
      { label: 'Equity Model & Terms', href: '/startups/services/equity' },
      { label: 'Standard Term Sheets', href: '/startups/services/equity/term-sheets' },
      { label: 'Startup Portfolio', href: '/startups/portfolio' },
      { label: 'Register Startup', href: '/startups/register' },
    ],
  },
  {
    label: 'Enterprise AI',
    links: [
      { label: 'Solutions Overview', href: '/ai-solutions' },
      { label: 'Products Catalog', href: '/ai-solutions/products' },
      { label: 'DBERT Chat (VPC LLM)', href: '/ai-solutions/products/dbert-chat' },
      { label: 'Document AI Engine', href: '/ai-solutions/products/document-ai' },
      { label: 'Certificate Verification API', href: '/ai-solutions/products/certificate-verification-api' },
      { label: 'Custom Training Pipeline', href: '/ai-solutions/llm-training/pipeline' },
    ],
  },
  {
    label: 'Learners',
    links: [
      { label: 'DBERT Launchpad', href: 'https://internship.dbert.online/launchpad', external: true },
      { label: 'DBERT Accelerate', href: 'https://internship.dbert.online/accelerate', external: true },
      { label: 'The AI Fellowship', href: '/learners/fellowship' },
      { label: 'Engineering Courses', href: '/learners/courses' },
      { label: 'Job Board & Placement', href: 'https://internship.dbert.online/jobs', external: true },
      { label: 'Verify Certificate', href: '/verify' },
    ],
  },
  {
    label: 'Labs & Trust',
    links: [
      { label: 'DBERT Research Labs', href: '/labs' },
      { label: 'Technical Preprints', href: '/labs/publications' },
      { label: 'Audited Credentials', href: '/about/credentials' },
      { label: 'Open Source Repos', href: '/labs/opensource' },
      { label: 'Practitioners & Team', href: '/about/team' },
      { label: 'Commercial Pricing', href: '/pricing' },
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

            <address className={styles.contact}>
              <a href="mailto:contactus@dbert.online">contactus@dbert.online</a>
              <a href="tel:+918958006294">+91 89580 06294</a>
              <span className={styles.addressLine}>Delhi, India · Sovereign AI Studio</span>
            </address>

            <div className={styles.social}>
              <a
                href="https://www.linkedin.com/company/dbert"
                target="_blank"
                rel="noopener noreferrer"
              >
                LinkedIn
              </a>
              <a
                href="https://www.youtube.com/@dbert-india"
                target="_blank"
                rel="noopener noreferrer"
              >
                YouTube
              </a>
              <a href="https://github.com/DBERT-INDIA" target="_blank" rel="noopener noreferrer">
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
                      >
                        <span>{link.label}</span>
                        <span className={styles.externalMark} aria-hidden="true">↗</span>
                      </a>
                    ) : (
                      <Link href={link.href} className={styles.footerLink}>
                        {link.label}
                      </Link>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className={styles.base}>
          <span>© {new Date().getFullYear()} DBERT · dbert.online · All rights reserved</span>
          <span className={styles.made}>
            handmade in Delhi <b>·</b> fueled by chai ☕
          </span>
          <span className={styles.legal}>
            <Link href="/privacy">Privacy</Link> · <Link href="/terms">Terms</Link> ·{' '}
            <Link href="/refund">Refund Policy</Link>
          </span>
        </div>
      </div>
    </footer>
  );
}
