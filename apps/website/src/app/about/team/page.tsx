import React from 'react';
import Image from 'next/image';
import Link from 'next/link';
import HandNote from '@/components/ui/HandNote';
import { pageMetadata } from '@/lib/seo';
import { TEAM_PROJECT_REFERENCES } from '@/data/team_project_references';
import styles from '../about.module.css';

export const metadata = pageMetadata('/about/team');

export default function TeamPage() {
  const jsonLdPerson = {
    '@context': 'https://schema.org',
    '@type': 'Person',
    name: 'Abhinav Sharma',
    jobTitle: 'Founder, CTO & Principal AI Architect',
    worksFor: {
      '@type': 'Organization',
      name: 'DBERT — Digital Blinc Education Research and Technology',
      url: 'https://dbert.in',
    },
    url: 'https://dbert.in/about/team',
    image: 'https://dbert.in/images/abhinav-sharma-github.jpg',
    sameAs: [
      'https://github.com/ainabhinavsharma',
      'https://dbert.in',
    ],
    description:
      'Principal AI Architect, Founder and CTO at DBERT directing production RAG systems, conformal prediction, and engineering sprints across incubated startups.',
  };

  const jsonLdProjects = {
    '@context': 'https://schema.org',
    '@type': 'ItemList',
    name: 'DBERT Flagship Production Projects & Verified Contributors',
    itemListElement: TEAM_PROJECT_REFERENCES.map((p, idx) => ({
      '@type': 'ListItem',
      position: idx + 1,
      name: p.title,
      description: p.description,
    })),
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLdPerson) }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLdProjects) }}
      />

      <div className="container pad-block">
        <div className="measure-lg">
          <div className="detail-header">
            <div className="doclabel">
              § 05 — ENGINEERING LEADERSHIP &amp; CONTRIBUTOR REGISTRY <span className="rev">rev: 2026.3</span>
            </div>
            <div className="stack-h justify-start align-baseline gap-3 flex-wrap mb-2">
              <h1 className="page-title-sm mb-0">The Practitioners &amp; Architects Behind the Mission</h1>
              <HandNote tone="blue">
                mentors · architects · verified talent ✍
              </HandNote>
            </div>
            <p className="page-intro">
              Active software developers, research engineers, and legal compliance advisors guiding DBERT&apos;s venture incubation, sovereign AI architecture, and engineering fellowship ladders.
            </p>
          </div>

          <div className={styles.stack6}>
            {/* Principal Architect Card */}
            <div className={`card card-lift ${styles.profile}`}>
              <div className={styles.portrait}>
                <Image
                  src="/images/abhinav-sharma-github.jpg"
                  alt="Abhinav Sharma - Founder, CTO & Principal AI Architect at DBERT"
                  fill
                  sizes="120px"
                  priority
                  className={styles.founderPhoto}
                />
              </div>
              <div style={{ flex: 1 }}>
                <div className="stack-h justify-between align-center flex-wrap gap-2 mb-1">
                  <span className="doclabel text-xs">§ PRINCIPAL ARCHITECT &amp; FOUNDER</span>
                  <a
                    href="https://github.com/ainabhinavsharma"
                    target="_blank"
                    rel="noopener noreferrer"
                    className={styles.githubLink}
                    title="View Abhinav Sharma on GitHub"
                  >
                    <svg className={styles.githubIcon} viewBox="0 0 24 24" width="16" height="16">
                      <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z" />
                    </svg>
                    <span>github.com/ainabhinavsharma</span>
                    <span className={styles.externalArrow}>↗</span>
                  </a>
                </div>
                <h2 className={styles.name}>Abhinav Sharma</h2>
                <p className={styles.role}>Founder, CTO &amp; Principal AI Architect</p>
                <p className={styles.bio}>
                  Abhinav directs engineering sprints at <Link href="/labs" className="ink-link">DBERT Labs</Link> and oversees system architecture across our incubated ventures. He focuses on production RAG systems, multi-agent orchestration, conformal prediction under covariate shift, and reproducible MLOps pipelines. Under his technical direction, DBERT has built and deployed mission-critical software, open-source AI benchmarks, and trained high-performing pre-vetted engineers.
                </p>
                <div className="stack-h gap-4 mt-4 pt-4 border-t border-line flex-wrap">
                  <a
                    href="https://github.com/ainabhinavsharma"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="accent-link text-sm font-medium"
                  >
                    GitHub Repositories &rarr;
                  </a>
                  <Link href="/labs/publications" className="accent-link text-sm font-medium">Read Technical Reports &rarr;</Link>
                  <Link href="/blog" className="accent-link text-sm font-medium">Explore Engineering Articles &rarr;</Link>
                  <Link href="/about/credentials" className="accent-link text-sm font-medium">View Lab Credentials &rarr;</Link>
                </div>
              </div>
            </div>

            {/* Domain Practice Leads */}
            <div className="section-breath">
              <div className="doclabel mb-2">§ 06 — CORE PRACTICE LEADS</div>
              <h2>Specialized Domain Mentors</h2>
              <p className="body-copy mb-4">
                Fellows and incubated startups work directly under senior domain leads who supervise code quality, pull request audits, and architectural milestones.
              </p>
              <div className="bento-grid-3">
                <div className="card card-lift">
                  <span className="tag-chip mb-2">AI Systems</span>
                  <h3 className="card-title text-base mb-1">Agent Architecture &amp; RAG</h3>
                  <p className="text-xs text-muted">Directs multi-agent workflows, tool routing, fast vector embeddings, and LangChain/LlamaIndex production implementations.</p>
                </div>
                <div className="card card-lift">
                  <span className="tag-chip mb-2">Full Stack</span>
                  <h3 className="card-title text-base mb-1">Modern Web &amp; Distributed Systems</h3>
                  <p className="text-xs text-muted">Guides Next.js 16 App Router systems, reactive UIs, PostgreSQL schemas, state machines, and high-concurrency API gates.</p>
                </div>
                <div className="card card-lift">
                  <span className="tag-chip mb-2">Data &amp; Quant</span>
                  <h3 className="card-title text-base mb-1">Data Pipelines &amp; Conformal ML</h3>
                  <p className="text-xs text-muted">Supervises calibration layers, feature engineering, walk-forward validation gates, and compliance monitoring across financial models.</p>
                </div>
              </div>
            </div>

            {/* Flagship Production Projects & Verified Pre-Vetted Contributors */}
            <div className="section-breath">
              <div className="doclabel mb-2">§ 07 — PRODUCTION PROJECTS &amp; PRE-VETTED REFERENCES</div>
              <h2>Flagship Production Projects &amp; Verified Contributors</h2>
              <p className="body-copy mb-4">
                DBERT engineers don&apos;t build toy projects. Fellowship candidates and pre-vetted engineers ship production pull requests across our flagship AI platforms, fintech algorithms, and distributed infrastructure. Below are the actual production systems with their cryptographically verified contributors.
              </p>

              <div className="stack-v gap-4">
                {TEAM_PROJECT_REFERENCES.map((project) => (
                  <div key={project.id} className={styles.projectCard}>
                    <div className={styles.projectTop}>
                      <div>
                        <span className={styles.projectBadge}>{project.badge}</span>
                        <h3 className={styles.projectTitle}>{project.title}</h3>
                        <p className={styles.projectTagline}>{project.tagline}</p>
                      </div>
                      {project.portfolioUrl && (
                        <Link href={project.portfolioUrl} className="accent-link text-xs font-mono font-medium">
                          Inspect Venture Dossier &rarr;
                        </Link>
                      )}
                    </div>

                    <p className={styles.projectDesc}>{project.description}</p>

                    <div className={styles.stackChips}>
                      {project.stack.map((tech) => (
                        <span key={tech} className={styles.stackChip}>{tech}</span>
                      ))}
                    </div>

                    <div className={styles.contributorsHeader}>
                      <span className={styles.contributorsHeading}>
                        Verified Engineering Contributors ({project.totalContributors})
                      </span>
                      <span className={styles.contributorsCountBadge}>
                        § Top-Ranked Project Fellows
                      </span>
                    </div>

                    <div className={styles.contributorsGrid}>
                      {project.contributors.slice(0, 8).map((cand) => (
                        <Link
                          key={cand.certId}
                          href={cand.verifyUrl}
                          className={styles.contributorCard}
                          title={`Inspect cryptographic evaluation dossier for ${cand.name}`}
                        >
                          <div className={styles.contributorInfo}>
                            <span className={styles.contributorName}>{cand.name}</span>
                            <div className={styles.contributorMeta}>
                              <span>{cand.domain}</span>
                              <span>·</span>
                              <span className={styles.viewDossierLink}>Rubric &rarr;</span>
                            </div>
                          </div>
                          <span className={styles.scoreBadge} title={cand.grade}>
                            {cand.score}/100
                          </span>
                        </Link>
                      ))}
                    </div>

                    {project.totalContributors > 8 && (
                      <div className="mt-2 text-right">
                        <Link
                          href={`/verify/directory?project=${encodeURIComponent(project.title)}`}
                          className="accent-link text-xs font-mono"
                        >
                          + View all {project.totalContributors} verified contributors in directory &rarr;
                        </Link>
                      </div>
                    )}
                  </div>
                ))}
              </div>

              {/* Recruiter Hiring Banner */}
              <div className={styles.recruiterBanner}>
                <span className="doclabel text-xs mb-1">§ RECRUITMENT DIRECTORY ACCESS</span>
                <h3 className={styles.recruiterTitle}>Hire Pre-Vetted Project Contributors in 48 Hours</h3>
                <p className={styles.recruiterSubtitle}>
                  Every engineer listed above has been independently evaluated on production code quality, system design, originality, and real-world milestones. Cryptographic rubrics, Turnitin originality scores, and letters of recommendation are available for instant recruiter inspection.
                </p>
                <div className="stack-h gap-3 flex-wrap">
                  <Link href="/verify/directory" className="btn btn-primary btn-sm">
                    Browse All 81+ Pre-Vetted Engineers &rarr;
                  </Link>
                  <Link href="/hire/pre-vetted-engineers" className="btn btn-outline btn-sm">
                    Recruiter Value Proposition
                  </Link>
                  <a
                    href="https://lms.dbert.in/company/signup?ref=about_team"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn btn-outline btn-sm"
                  >
                    Connect on LMS for Direct Hiring ↗
                  </a>
                </div>
              </div>
            </div>

            {/* Practitioner Mentor Network */}
            <div className={`card card-lift ${styles.panel}`}>
              <div className="doclabel mb-1">§ PRACTITIONER NETWORK</div>
              <h2 className={styles.panelTitle}>Active Practitioner Mentor Network</h2>
              <p className={styles.bio}>
                DBERT maintains a selective network of practicing engineers, cloud architects, and legal compliance advisors who lead code reviews for our <Link href="/learners/fellowship" className="ink-link">Applied AI Fellows</Link> and incubated founders. Rather than theoretical lectures, candidates learn by shipping pull requests on real repositories.
              </p>
              <p className={styles.bio}>
                Mentors conduct weekly live PR reviews, system design mock sessions, and latency audits. You can also inspect the active roster of research contributors working on projects like Alkame.
              </p>
              <div className="mt-4 pt-3 border-t border-line stack-h justify-between align-center flex-wrap gap-2">
                <Link href="/startups/portfolio/alkame#team" className="accent-link text-sm font-medium">Inspect Alkame Research Contributors &rarr;</Link>
                <Link href="/labs/collaborate" className="btn btn-outline btn-sm">Join Advisor Network</Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
