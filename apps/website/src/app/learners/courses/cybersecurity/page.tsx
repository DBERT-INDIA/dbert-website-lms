import React from 'react';
import Link from 'next/link';
import FAQAccordion from '@/components/ui/FAQAccordion';
import { pageMetadata } from '@/lib/seo';
import RegionalOpportunityBento from '@/components/ui/RegionalOpportunityBento';
import s from '../../learners.module.css';
import { Layers, Award, Sparkles } from 'lucide-react';

export const metadata = pageMetadata('/learners/courses/cybersecurity');

export default function CybersecurityCoursePage() {
  const faqs = [
    {
        "question": "Is cybersecurity purely offensive hacking or defensive monitoring?",
        "answer": "The highest fresher demand in India is in defensive SOC (Security Operations Center) analysis, SIEM log monitoring, and vulnerability assessment. We teach both red-team and blue-team paradigms."
    },
    {
        "question": "Do I need deep programming knowledge to start cybersecurity?",
        "answer": "You need foundational networking concepts (IP, TCP/UDP, DNS, HTTP) and basic Python scripting for automation. We teach security-focused scripting as part of the curriculum."
    },
    {
        "question": "What tools are utilized in the hands-on security labs?",
        "answer": "You perform practical drills with Burp Suite Community, Nmap, Wireshark, Kali Linux tools, and enterprise SIEM monitoring on isolated sandboxed vulnerable targets."
    },
    {
        "question": "Can recruiters verify my cybersecurity credentials?",
        "answer": "Yes. Each completed certificate is registered in the public institutional directory at dbert.in/verify, complete with project evaluations and security domain endorsements."
    },
    {
        "question": "What roles and packages do cybersecurity freshers achieve?",
        "answer": "Graduates step into roles such as SOC Analyst (L1), Junior Penetration Tester, Cybersecurity Associate, and Information Security Engineer, earning \u20b94.5\u2013\u20b910.5 LPA."
    }
];

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Course',
        name: 'Become a Cybersecurity & Threat Defense Specialist',
        description: 'Master ethical hacking, OWASP Top 10 web vulnerabilities, network packet analysis with Wireshark, SOC incident response, and SIEM security telemetry monitoring.',
        provider: {
          '@type': 'Organization',
          name: 'DBERT Labs Industrial Training & Venture Studio',
          url: 'https://dbert.in'
        },
        courseCode: 'DBERT-ENG-CYBER-2026',
        courseMode: 'Blended (Synchronous Cohort & Remote Production Lab Sprints)',
        educationalCredentialAwarded: 'Verified Cybersecurity & Threat Defense Systems Diploma',
        offers: {
          '@type': 'Offer',
          category: 'Tuition Fee',
          price: '28000',
          priceCurrency: 'INR',
          availability: 'https://schema.org/InStock',
          validFrom: '2026-01-01',
          url: 'https://dbert.in/learners/courses/cybersecurity'
        }
      },
      {
        '@type': 'FAQPage',
        mainEntity: faqs.map((f: { question: string; answer: string }) => ({
          '@type': 'Question',
          name: f.question,
          acceptedAnswer: {
            '@type': 'Answer',
            text: f.answer
          }
        }))
      }
    ]
  };

  const tools = ["Wireshark", "Nmap", "Burp Suite", "Metasploit", "OWASP Top 10", "SIEM (Wazuh/Splunk)", "Linux Hardening", "Network Security", "Cryptography", "SOC Analysis", "Incident Response", "Python for Sec"];

  return (
    <div className="glow-wrapper">
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      <div className="glow-spot"></div>

      {/* Hero Header Section */}
      <div className="container page-head">
        <div className="doclabel">
          § 01 — CAREER TRACK <span className="rev">rev: 2026.2</span>
        </div>
        <h1 className="page-title">
          Become a Cybersecurity & Threat Defense Specialist
        </h1>
        <p className={s.courseTagline}>
          ₹4,50,000 – ₹10,50,000 LPA Verified Average Starting Remuneration
        </p>
        <p className={s.courseLede}>
          Master ethical hacking, OWASP Top 10 web vulnerabilities, network packet analysis with Wireshark, SOC incident response, and SIEM security telemetry monitoring.
        </p>
      </div>

      {/* Key Metrics Grid */}
      <div className="section-band">
        <div className="container">
          <h2 className="sr-only">Key Course Highlights</h2>
          <div className="bento-grid-3">
            <div className="bento-card center">
              <div className="bento-icon"><Layers className="w-5 h-5 text-accent" /></div>
              <h3 className="bento-title">Practical Project Sprints</h3>
              <p className="bento-text">
                8 intensive weekly sprints shipping real deliverables under senior engineering and design review.
              </p>
            </div>
            <div className="bento-card center">
              <div className="bento-icon"><Award className="w-5 h-5 text-accent" /></div>
              <h3 className="bento-title">Verifiable Credentials</h3>
              <p className="bento-text">
                Every completed certification is cryptographically registered and verifiable at dbert.in/verify.
              </p>
            </div>
            <div className="bento-card center">
              <div className="bento-icon"><Sparkles className="w-5 h-5 text-accent" /></div>
              <h3 className="bento-title">Direct Portal Referrals</h3>
              <p className="bento-text">
                Direct referral consideration to active corporate internships and startup venture pipelines.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Capstone Projects Section */}
      <div className="container pad-block">
        <div className="doclabel mb-2">§ 02 — PRODUCTION CAPSTONES</div>
        <h2 className="section-title mb-6">Real Systems Built and Shipped</h2>
        <div className="grid gap-6 md:grid-cols-2">
          <div className="card p-6 bg-card border border-line">
            <h3 className="text-xl font-bold mb-3 text-white">OWASP Top 10 Web Application Penetration Audit</h3>
            <p className="text-sm text-muted leading-relaxed">
              Conduct an in-depth vulnerability audit against a vulnerable web application, identifying SQL injections, CSRF flaws, and IDOR vulnerabilities, compiling an executive remediation report.
            </p>
          </div>
          <div className="card p-6 bg-card border border-line">
            <h3 className="text-xl font-bold mb-3 text-white">SIEM Deployment & Incident Response Telemetry</h3>
            <p className="text-sm text-muted leading-relaxed">
              Configure an open-source SIEM agent on Linux servers, generate simulated brute-force and privilege escalation attacks, and write automated incident alerting rules.
            </p>
          </div>
        </div>
      </div>

      {/* Transparent Tuition & Zero-Cost EMI Table */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 03 — TUITION INVESTMENT &amp; EMI SCHEDULES</div>
        <h2 className="section-title mb-2">Transparent Indian Tuition &amp; Zero-Cost Financing</h2>
        <p className="prose-sm text-muted mb-6 max-w-2xl">
          We practice absolute financial transparency. Enroll directly with our straightforward upfront tuition or utilize flexible Zero-Cost EMI schedules through verified Indian educational lending partners.
        </p>

        <div className="grid gap-6 md:grid-cols-2 my-6">
          <div className="card p-6 bg-card border border-line">
            <span className="font-mono text-xs text-muted uppercase tracking-wider">One-Time Upfront Tuition</span>
            <div className="text-3xl font-mono font-bold text-white mt-2 mb-1">₹28,000 <span className="text-sm text-muted font-normal">INR (All Inclusive)</span></div>
            <p className="text-xs text-muted mb-4">Covers synchronous practical instruction, cloud lab access, comprehensive code and design reviews, and global certification database entry.</p>
            <ul className="list-disc pl-4 text-xs text-muted space-y-2 mb-6">
              <li>Permanent access to recorded architecture and design sessions</li>
              <li>Weekly 1-on-1 mentor optimization reviews</li>
              <li>Direct hiring referral recommendations for audited graduates</li>
            </ul>
            <Link href="/learners/launchpad?domain=cybersecurity" className="btn btn-primary w-full">Explore Launchpad Track &rarr;</Link>
          </div>

          <div className="card p-6 bg-card border-2 border-accent relative">
            <div className="absolute -top-3 right-4 bg-accent text-zinc-950 font-mono text-[10px] uppercase font-bold px-2 py-0.5 rounded">Zero-Cost EMI</div>
            <span className="font-mono text-xs text-accent uppercase tracking-wider">9-Month Installment Schedule</span>
            <div className="text-3xl font-mono font-bold text-emerald-400 mt-2 mb-1">₹3,111 <span className="text-sm text-muted font-normal">/ month (₹0 Interest)</span></div>
            <p className="text-xs text-muted mb-4">Available via authorized banking partnerships with zero processing surcharges or security deposit requirements for qualified candidates.</p>
            <ul className="list-disc pl-4 text-xs text-muted space-y-2 mb-6">
              <li>Expedited digital financial verification protocol</li>
              <li>Immediate course and lab access upon installment authorization</li>
              <li>Complete structural parity with lump-sum fee applicants</li>
            </ul>
            <Link href="/about/contact" className="btn btn-outline w-full">Inquire About EMI Financing</Link>
          </div>
        </div>
      </div>

      {/* Production Technologies Mastered */}
      <div className={`container ${s.techBlock} border-t border-line`}>
        <div className="doclabel mb-2">§ 04 — CORE TOOLING</div>
        <h2 className={s.techHeading}>Production Technologies Mastered</h2>
        <div className={s.techRow}>
          {tools.map((tool: string, idx: number) => (
            <span key={idx} className={s.techChip}>
              {tool}
            </span>
          ))}
        </div>
      </div>

      {/* Frequently Asked Questions */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 05 — KNOWLEDGE BASE</div>
        <h2 className="section-title mb-4">Frequently Asked Questions</h2>
        <div className="measure">
          <FAQAccordion items={faqs} />
        </div>
      </div>

      {/* Live Regional Opportunities */}
      <RegionalOpportunityBento
        sectionNumber="§ 06"
        title="Cybersecurity & SOC Defense Internships"
        description="Connect directly to real security assessments, log auditing sprints, and threat defense monitoring across Bangalore, Delhi NCR, Hyderabad, and Remote."
        domainName="Become a Cybersecurity & Threat Defense Specialist"
        hubHref="https://lms.dbert.in/internships/cybersecurity"
        jobsHref="https://lms.dbert.in/jobs/cybersecurity"
        opportunities={[
          {
            title: 'Become a Cybersecurity & Threat Defense Specialist Intern',
            roleDescription: 'Master ethical hacking, OWASP Top 10 web vulnerabilities, network packet analysis with Wireshark, SOC incident response, and SIEM security telemetry monitoring.',
            cityTag: 'Remote',
            location: 'India · Remote / Hybrid',
            stipend: '₹5,000 – ₹18,000 / mo',
            tags: ['Remote', 'Verified', 'Active Sprint'],
            href: 'https://lms.dbert.in/internships/cybersecurity',
          }
        ]}
      />
    </div>
  );
}
