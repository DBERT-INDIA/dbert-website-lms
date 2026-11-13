import React from 'react';
import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import HandNote from '@/components/ui/HandNote';

const CITY_NAMES: Record<string, string> = {
  'remote': 'Remote / Work From Home',
  'bengaluru': 'Bengaluru',
  'delhi-ncr': 'Delhi NCR',
  'mumbai': 'Mumbai',
  'pune': 'Pune',
  'hyderabad': 'Hyderabad',
  'chennai': 'Chennai',
  'kolkata': 'Kolkata',
  'ahmedabad': 'Ahmedabad',
  'jaipur': 'Jaipur',
  'lucknow': 'Lucknow',
  'chandigarh': 'Chandigarh',
  'noida': 'Noida',
  'gurgaon': 'Gurgaon',
};

const ROLE_INFO: Record<string, { title: string; skills: string[]; stipend: string; desc: string }> = {
  'full-stack-development': {
    title: 'Full Stack Web Development',
    skills: ['Next.js App Router', 'React 19', 'TypeScript', 'Node.js', 'PostgreSQL', 'Tailwind CSS'],
    stipend: '₹8,000 – ₹18,000 / month',
    desc: 'Build full-stack web architectures, implement pgvector similarity search, and deploy production microservices with active users.'
  },
  'ai-agent-development': {
    title: 'AI Agent & LLM Systems',
    skills: ['LangGraph', 'CrewAI', 'Ollama', 'vLLM', 'Python', 'FastAPI', 'RAG'],
    stipend: '₹10,000 – ₹18,000 / month',
    desc: 'Construct autonomous agent state machines, tool-calling execution loops, and local open-weights foundation model deployments.'
  },
  'data-analytics': {
    title: 'Data Analytics & Corporate BI',
    skills: ['SQL', 'Python Pandas', 'Power BI', 'Metabase', 'Data Modeling', 'ETL'],
    stipend: '₹6,000 – ₹15,000 / month',
    desc: 'Transform raw corporate transaction records into structured analytical databases, variance decompositions, and executive BI dashboards.'
  },
  'python-automation': {
    title: 'Python Automation & Scraping',
    skills: ['Playwright', 'Scrapy', 'Celery', 'Redis', 'Python Async', 'PostgreSQL'],
    stipend: '₹7,000 – ₹15,000 / month',
    desc: 'Deploy resilient web extraction pipelines, headless browser testing harnesses, and automated data synchronization workflows.'
  },
  'devops-cloud': {
    title: 'DevOps & Cloud Engineering',
    skills: ['Docker', 'Kubernetes', 'AWS EC2', 'GitHub Actions', 'Terraform', 'CI/CD'],
    stipend: '₹8,000 – ₹16,000 / month',
    desc: 'Architect containerized clusters, automated CI/CD deployment pipelines, and secure cloud networking environments.'
  },
  'ui-ux-design': {
    title: 'UI/UX Design & Prototyping',
    skills: ['Figma', 'Auto-Layout', 'Design Systems', 'User Research', 'Wireframing'],
    stipend: '₹6,000 – ₹14,000 / month',
    desc: 'Design component tokens, user journey flows, and high-fidelity interactive product prototypes for venture applications.'
  },
  'cybersecurity': {
    title: 'Cybersecurity & Threat Defense',
    skills: ['OWASP Top 10', 'Wireshark', 'Burp Suite', 'SIEM Logs', 'SOC Analysis', 'Linux'],
    stipend: '₹8,000 – ₹16,000 / month',
    desc: 'Audit web applications for injection vulnerabilities, analyze network packet captures, and harden infrastructure against intrusion.'
  },
  'mobile-app-development': {
    title: 'Mobile App Development',
    skills: ['Flutter', 'Dart', 'React Native', 'Mobile APIs', 'Offline SQLite', 'State Management'],
    stipend: '₹7,000 – ₹15,000 / month',
    desc: 'Build cross-platform iOS and Android applications connected to cloud backends with offline local caching.'
  },
  'digital-marketing': {
    title: 'Digital Marketing & Growth',
    skills: ['Technical SEO', 'Google Analytics 4', 'Meta Ads', 'CRO', 'Content Marketing'],
    stipend: '₹5,000 – ₹12,000 / month',
    desc: 'Optimize organic search acquisition, analyze conversion funnels, and manage targeted growth campaigns across digital channels.'
  }
};

interface PageProps {
  params: Promise<{
    role: string;
    city: string;
  }>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { role, city } = await params;
  const roleData = ROLE_INFO[role];
  const cityName = CITY_NAMES[city];

  if (!roleData || !cityName) {
    return {
      title: 'Internship Not Found | DBERT',
      description: 'The requested internship category was not found.'
    };
  }

  const title = `${roleData.title} Internships in ${cityName} (2026 Batch)`;
  const description = `Apply for ${roleData.title} internships in ${cityName}. Build live client codebases under senior review, earn ${roleData.stipend} performance stipends, and earn verifiable MSME credentials.`;

  return {
    title: `${title} | DBERT`,
    description,
    alternates: {
      canonical: `https://dbert.in/internships/${role}/${city}`
    },
    openGraph: {
      title: `${title} | DBERT`,
      description,
      url: `https://dbert.in/internships/${role}/${city}`,
      type: 'website'
    }
  };
}

export default async function ProgrammaticInternshipPage({ params }: PageProps) {
  const { role, city } = await params;
  const roleData = ROLE_INFO[role];
  const cityName = CITY_NAMES[city];

  if (!roleData || !cityName) {
    notFound();
  }

  const isRemote = city.toLowerCase() === 'remote';

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'JobPosting',
        title: `${roleData.title} Intern (${cityName})`,
        description: `<p>${roleData.desc}</p><p><strong>Required Skills:</strong> ${roleData.skills.join(', ')}</p><p><strong>Stipend:</strong> ${roleData.stipend}</p><p><strong>Location:</strong> ${cityName}</p>`,
        datePosted: '2026-11-01T00:00:00+05:30',
        validThrough: '2027-06-30T23:59:59+05:30',
        employmentType: 'INTERN',
        hiringOrganization: {
          '@type': 'Organization',
          name: 'DBERT Venture Network',
          sameAs: 'https://dbert.in',
          logo: 'https://dbert.in/logo.svg'
        },
        jobLocationType: isRemote ? 'TELECOMMUTE' : undefined,
        applicantLocationRequirements: {
          '@type': 'Country',
          name: 'IN'
        },
        baseSalary: {
          '@type': 'MonetaryAmount',
          currency: 'INR',
          value: {
            '@type': 'QuantitativeValue',
            minValue: 5000,
            maxValue: 18000,
            unitText: 'MONTH'
          }
        },
        directApply: true
      },
      {
        '@type': 'BreadcrumbList',
        itemListElement: [
          {
            '@type': 'ListItem',
            position: 1,
            name: 'Home',
            item: 'https://dbert.in'
          },
          {
            '@type': 'ListItem',
            position: 2,
            name: 'Internships',
            item: 'https://dbert.in/internships'
          },
          {
            '@type': 'ListItem',
            position: 3,
            name: `${roleData.title} in ${cityName}`,
            item: `https://dbert.in/internships/${role}/${city}`
          }
        ]
      },
      {
        '@type': 'FAQPage',
        mainEntity: [
          {
            '@type': 'Question',
            name: `What are the eligibility requirements for ${roleData.title} internships in ${cityName}?`,
            acceptedAnswer: {
              '@type': 'Answer',
              text: `Applicants should have basic competence in ${roleData.skills.slice(0, 3).join(', ')}. Students across all engineering colleges in India (B.Tech, BCA, MCA, B.Sc) are eligible. Selection is based purely on code screening with zero application fees.`
            }
          },
          {
            '@type': 'Question',
            name: `Is this ${roleData.title} internship in ${cityName} paid?`,
            acceptedAnswer: {
              '@type': 'Answer',
              text: `Yes. Interns receive performance stipends ranging from ${roleData.stipend} paid against milestone deliverables and senior pull request reviews.`
            }
          },
          {
            '@type': 'Question',
            name: `How do I apply for the next ${cityName} cohort?`,
            acceptedAnswer: {
              '@type': 'Answer',
              text: `Applications are processed directly on our LMS portal at lms.dbert.in. Choose your track during signup to auto-fill your application.`
            }
          }
        ]
      }
    ]
  };

  return (
    <div className="glow-wrapper">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <div className="glow-spot"></div>

      {/* Hero Header */}
      <div className="container page-head">
        <div className="doclabel">
          § 01 — {cityName.toUpperCase()} REGIONAL SPRINT <span className="rev">cohort: 2026</span>
        </div>
        <div className="stack-h justify-center align-baseline gap-3 flex-wrap">
          <h1 className="page-title">
            {roleData.title} Internships in {cityName}
          </h1>
          <HandNote tone="amber">
            stipends ₹5K–₹18K ✎
          </HandNote>
        </div>
        <p className="lede-wide">
          {roleData.desc} Join our embedded venture squads, receive senior pull-request reviews, and graduate with cryptographic MSME credentials.
        </p>

        <div className="flex justify-center gap-3 flex-wrap mt-4">
          <span className="proof-mark proof-mark-signal">
            <span>⚡ {roleData.stipend} Stipend</span>
          </span>
          <span className="proof-mark">
            <span>✓ Verified Turnitin Rubrics</span>
          </span>
          <span className="proof-mark">
            <span>✓ {isRemote ? '100% Virtual Sprints' : `${cityName} Hub & Remote`}</span>
          </span>
          <span className="proof-mark">
            <span>✓ MSME Registered Credentials</span>
          </span>
        </div>
      </div>

      {/* Primary Conversion Section */}
      <div className="section-band">
        <div className="container center">
          <div className="doclabel mb-2">§ 02 — FAST-TRACK APPLICATION</div>
          <h2 className="section-title mb-2">Apply for {roleData.title} on LMS</h2>
          <p className="band-lede mb-6">
            Your application will be routed with the <strong>{roleData.title}</strong> track automatically pre-selected in our evaluation system.
          </p>

          <div className="flex justify-center gap-4 flex-wrap">
            <a
              href={`https://lms.dbert.in/#signup?domain=${role}&next=/internships/${role}/${city}`}
              target="_blank"
              rel="noopener noreferrer"
              className="btn btn-primary btn-lg"
            >
              Apply on LMS (Track Auto-Selected) ↗
            </a>
            <a
              href={`https://lms.dbert.in/internships/${role}`}
              target="_blank"
              rel="noopener noreferrer"
              className="btn btn-outline btn-lg"
            >
              View All Live Openings on Portal ↗
            </a>
            <Link href="/enroll/1999" className="btn btn-outline btn-lg">
              Confirm Fellowship Seat (₹1,500 Balance) →
            </Link>
          </div>
        </div>
      </div>

      {/* Tech Stack & Core Competencies */}
      <div className="container pad-block">
        <div className="doclabel mb-2">§ 03 — TECHNICAL SPECIFICATIONS</div>
        <h2 className="section-title">
          Core Technologies &amp; Deliverables
        </h2>

        <div className="grid gap-6 md:grid-cols-2 my-6">
          <div className="card p-6 bg-card border border-line">
            <h3 className="font-mono text-lg font-bold text-white mb-3">Target Stack &amp; Tools</h3>
            <p className="text-xs text-muted mb-4">
              Fellows use these production tools daily to write clean, modular, and maintainable software:
            </p>
            <div className="flex flex-wrap gap-2">
              {roleData.skills.map((skill, idx) => (
                <span key={idx} className="tag-chip text-xs font-mono">
                  {skill}
                </span>
              ))}
            </div>
          </div>

          <div className="card p-6 bg-card border border-line">
            <h3 className="font-mono text-lg font-bold text-white mb-3">What You Ship</h3>
            <ul className="text-xs text-[var(--text-secondary)] space-y-2 list-disc list-inside">
              <li>Pull requests reviewed and graded by senior staff architects.</li>
              <li>Turnitin originality report proving zero plagiarism on capstones.</li>
              <li>Official 3-document credential packet (Certificate, Evaluation Rubric, LOR).</li>
              <li>Referral visibility to partner startups across India.</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Breadcrumb Navigation & City Interlinking */}
      <div className="band-top">
        <div className="container">
          <div className="doclabel mb-2">§ 04 — REGIONAL INTERNSHIP HUBS</div>
          <p className="text-xs text-muted mb-4">
            Explore {roleData.title} opportunities across other major Indian tech corridors:
          </p>
          <div className="flex flex-wrap gap-2 mb-6">
            {Object.entries(CITY_NAMES).map(([cSlug, cName]) => (
              <Link
                key={cSlug}
                href={`/internships/${role}/${cSlug}`}
                className={`tag-chip text-xs font-mono ${cSlug === city ? 'border-accent text-accent' : ''}`}
              >
                {cName}
              </Link>
            ))}
          </div>

          <div className="text-center pt-4 border-t border-line">
            <Link href="/internships" className="btn btn-outline btn-sm">
              &larr; Return to All Internship Domains
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
