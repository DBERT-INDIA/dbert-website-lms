import React from 'react';
import Link from 'next/link';
import styles from './Footer.module.css';

const columns = [
  {
    label: 'Startups',
    links: [
      { label: 'Incubation', href: '/startups' },
      { label: 'Term sheets', href: '/startups/services/equity/term-sheets' },
      { label: 'Portfolio', href: '/startups/portfolio' },
      { label: 'Register', href: '/startups/register' },
    ],
  },
  {
    label: 'Products',
    links: [
      { label: 'DBERT Chat', href: '/ai-solutions/products/dbert-chat' },
      { label: 'Document AI', href: '/ai-solutions/products/document-ai' },
      { label: 'Certificate API', href: '/ai-solutions/products/certificate-verification-api' },
      { label: 'LLM training', href: '/ai-solutions/llm-training' },
    ],
  },
  {
    label: 'Learners',
    links: [
      { label: 'Launchpad', href: 'https://internship.dbert.online/launchpad' },
      { label: 'Accelerate', href: 'https://internship.dbert.online/accelerate' },
      { label: 'Fellowship', href: '/learners/fellowship' },
      { label: 'Job Board', href: 'https://internship.dbert.online/jobs' },
      { label: 'Internships', href: 'https://internship.dbert.online/internships' },
    ],
  },
];

export default function Footer() {
  return (
    <footer className={styles.footer} role="contentinfo">
      <div className="wrap">
        <div className={styles.grid}>
          <div>
            <Link href="/" className={styles.logo}>
              <span className={styles.logoMark} aria-hidden="true">
                D
              </span>
              DBERT
            </Link>
            <p className={styles.blurb}>
              Digital Blinc Education Research And Technology. India&apos;s AI venture studio —
              incubation, products, and engineering education under one roof.
            </p>

            <address className={styles.contact}>
              <a href="mailto:contactus@dbert.online">contactus@dbert.online</a>
              <a href="tel:+918958006294">+91 89580 06294</a>
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
              {column.links.map((link) => (
                <Link key={link.href} href={link.href}>
                  {link.label}
                </Link>
              ))}
            </div>
          ))}
        </div>

        <div className={styles.base}>
          <span>© {new Date().getFullYear()} DBERT · dbert.online</span>
          <span className={styles.made}>
            handmade in Delhi <b>·</b> fueled by chai
          </span>
          <span className={styles.legal}>
            <Link href="/privacy">Privacy</Link> ·<Link href="/terms">Terms</Link> ·
            <Link href="/refund">Refund policy</Link>
          </span>
        </div>
      </div>
    </footer>
  );
}
