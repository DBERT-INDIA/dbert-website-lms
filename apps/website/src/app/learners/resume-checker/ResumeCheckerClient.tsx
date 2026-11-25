'use client';

import { useEffect, useId, useRef, useState, type FormEvent } from 'react';
import Link from 'next/link';
import s from './resume-checker.module.css';

const DOMAINS = [
  { id: 'full-stack-development', label: 'Full Stack Dev', canonical: 'Full Stack Development' },
  { id: 'ai-agent-development', label: 'AI Agent Dev', canonical: 'AI Agent Development' },
  { id: 'data-analytics', label: 'Data Analyst', canonical: 'Data Analyst' },
  { id: 'python-automation', label: 'Python Automation', canonical: 'Python Automation' },
  { id: 'devops-cloud', label: 'DevOps & Cloud', canonical: 'DevOps & Cloud' },
  { id: 'cybersecurity', label: 'Cybersecurity', canonical: 'Cybersecurity' },
  { id: 'ui-ux-design', label: 'UI/UX Design', canonical: 'UI/UX Design' },
];

type JobFit = {
  matched: string[];
  missing: string[];
  next_steps: Array<{ label: string; href: string }>;
};

type AuditResult = {
  status: 'success';
  score: number;
  color: string;
  tier: string;
  locked: boolean;
  breakdown: Record<'keywords' | 'impact_verbs' | 'structure' | 'length_hygiene', { percentage: number }>;
  strengths?: string[];
  job_fit?: JobFit;
  critical_missing_keywords?: string[];
  recommendations?: { bullet_rewrites?: Array<{ original: string; improved: string; why: string }> };
  matched_jobs?: Array<{
    id: number | string;
    title: string;
    company_name: string;
    location?: string;
    stipend_min?: number;
    stipend_max?: number;
  }>;
  lms_signup_url?: string;
};

type AuditInput = {
  resume: { file: File } | { text: string };
  domain: string;
  jobDescription: string;
};

type Contact = { name: string; email: string; phone: string };

const MAX_PDF_BYTES = 5 * 1024 * 1024;
const MAX_JOB_DESCRIPTION_LENGTH = 6000;

async function requestAudit(input: AuditInput, contact?: Contact) {
  const body = new FormData();
  if ('file' in input.resume) {
    body.set('file', input.resume.file);
  } else {
    body.set('text', input.resume.text);
  }
  body.set('domain', input.domain);
  if (input.jobDescription) body.set('job_description', input.jobDescription);
  if (contact) {
    body.set('name', contact.name);
    body.set('email', contact.email);
    body.set('phone', contact.phone);
  }

  const response = await fetch('/api/tools/ats-checker', { method: 'POST', body });
  const data: AuditResult | { status: 'error'; message?: string } | null = await response.json().catch(() => null);
  if (!response.ok || data?.status !== 'success') {
    const message = data?.status === 'error' ? data.message : undefined;
    throw new Error(message || 'The audit could not be completed. Please try again.');
  }
  return data;
}

function getDbertHref(href: string) {
  try {
    const link = new URL(href, 'https://dbert.in');
    if (link.origin === 'https://dbert.in') return link.pathname + link.search + link.hash;
    if (link.origin === 'https://lms.dbert.in') return link.href;
  } catch {
    return null;
  }
  return null;
}

function JobFitResults({ fit, headingId }: { fit: JobFit; headingId: string }) {
  return (
    <section className={s.sectionBox} aria-labelledby={headingId}>
      <h3 id={headingId} className={s.fitTitle}>Job description match</h3>
      <p className={s.fitNote}>Use these keyword matches to check what your résumé shows for this role.</p>
      <div className={s.fitColumns}>
        <div>
          <h4>Matched skills</h4>
          {fit.matched.length > 0
            ? <ul className={s.fitList}>{fit.matched.map((skill) => <li key={skill}>{skill}</li>)}</ul>
            : <p className={s.fitNote}>No matching keywords found.</p>}
        </div>
        <div>
          <h4>Missing or unclear skills</h4>
          {fit.missing.length > 0
            ? <ul className={s.fitList}>{fit.missing.map((skill) => <li key={skill}>{skill}</li>)}</ul>
            : <p className={s.fitNote}>No missing keywords found.</p>}
        </div>
      </div>
      {fit.next_steps.length > 0 && (
        <div>
          <h4>Suggested next steps</h4>
          <ul className={s.fitLinks}>
            {fit.next_steps.map((step) => {
              const href = getDbertHref(step.href);
              return <li key={step.href + step.label}>{href ? <a href={href}>{step.label}</a> : step.label}</li>;
            })}
          </ul>
        </div>
      )}
    </section>
  );
}

export default function ResumeCheckerClient() {
  const id = useId();
  const [selectedDomain, setSelectedDomain] = useState(DOMAINS[0].canonical);
  const [activeTab, setActiveTab] = useState<'upload' | 'paste'>('upload');
  const [resumeText, setResumeText] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [pending, setPending] = useState<'scan' | 'unlock' | null>(null);
  const requestPending = useRef(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [unlockError, setUnlockError] = useState('');
  const [audit, setAudit] = useState<{ input: AuditInput; result: AuditResult } | null>(null);
  const scanResult = audit?.result;

  const fileInputRef = useRef<HTMLInputElement>(null);
  const resultsRef = useRef<HTMLHeadingElement>(null);

  useEffect(() => {
    if (audit) resultsRef.current?.focus();
  }, [audit]);

  function selectFile(file?: File) {
    if (!file) return;
    setSelectedFile(null);
    if (file.type !== 'application/pdf' && (file.type || !/\.pdf$/i.test(file.name))) {
      setErrorMsg('Choose a PDF résumé.');
    } else if (file.size === 0 || file.size > MAX_PDF_BYTES) {
      setErrorMsg('Choose a text-based PDF résumé up to 5 MB.');
    } else {
      setSelectedFile(file);
      setErrorMsg('');
    }
  }

  async function handleScan() {
    if (requestPending.current) return;
    const text = resumeText.trim();
    const resume = activeTab === 'upload' ? (selectedFile ? { file: selectedFile } : null) : { text };
    if (!resume) {
      setErrorMsg('Choose a PDF résumé or switch to pasted text.');
      return;
    }
    if ('text' in resume && text.length < 30) {
      setErrorMsg('Paste at least 30 characters of résumé text.');
      return;
    }

    const input = { resume, domain: selectedDomain, jobDescription: jobDescription.trim() };
    setErrorMsg('');
    setUnlockError('');
    setPending('scan');
    requestPending.current = true;
    try {
      const result = await requestAudit(input);
      setAudit({ input, result });
    } catch (error) {
      setErrorMsg(error instanceof Error ? error.message : 'The scanner could not be reached. Try again.');
    } finally {
      requestPending.current = false;
      setPending(null);
    }
  }

  async function handleUnlock(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!audit || requestPending.current) return;
    const fields = new FormData(event.currentTarget);
    const contact = {
      name: String(fields.get('name') ?? '').trim(),
      email: String(fields.get('email') ?? '').trim(),
      phone: String(fields.get('phone') ?? '').trim(),
    };
    if (!contact.name) {
      setUnlockError('Enter your full name.');
      return;
    }

    setUnlockError('');
    setPending('unlock');
    requestPending.current = true;
    try {
      const result = await requestAudit(audit.input, contact);
      if (result.locked) throw new Error('The report is still locked. Verify your email and try again.');
      setAudit({ input: audit.input, result });
    } catch (error) {
      setUnlockError(error instanceof Error ? error.message : 'The report could not be unlocked.');
    } finally {
      requestPending.current = false;
      setPending(null);
    }
  }



  return (
    <div className={s.toolCard}>
      <div className={s.stepTitle} id={id + '-domain'}>Target technical domain</div>
      <div className={s.domainPills} role="group" aria-labelledby={id + '-domain'}>
        {DOMAINS.map((d) => (
          <button
            key={d.id}
            type="button"
            aria-pressed={selectedDomain === d.canonical}
            className={`${s.domainPill} ${selectedDomain === d.canonical ? s.domainPillActive : ''}`}
            onClick={() => setSelectedDomain(d.canonical)}
          >
            {d.label}
          </button>
        ))}
      </div>

      <div className={s.tabNav} role="group" aria-label="Résumé input method">
        <button
          type="button"
          aria-pressed={activeTab === 'upload'}
          className={`${s.tabBtn} ${activeTab === 'upload' ? s.tabBtnActive : ''}`}
          onClick={() => setActiveTab('upload')}
        >
          📄 Upload PDF Resume
        </button>
        <button
          type="button"
          aria-pressed={activeTab === 'paste'}
          className={`${s.tabBtn} ${activeTab === 'paste' ? s.tabBtnActive : ''}`}
          onClick={() => setActiveTab('paste')}
        >
          📝 Paste Resume Text
        </button>
      </div>

      {activeTab === 'upload' ? (
        <div
          className={s.dropZone}
          onDragOver={(e) => e.preventDefault()}
          onDrop={(e) => {
            e.preventDefault();
            selectFile(e.dataTransfer.files[0]);
          }}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept="application/pdf,.pdf"
            hidden
            onChange={(e) => {
              selectFile(e.currentTarget.files?.[0]);
              e.currentTarget.value = '';
            }}
          />
          <button
            className={s.filePicker}
            type="button"
            onClick={() => fileInputRef.current?.click()}
            aria-describedby={id + '-pdf-hint'}
          >
            <span className={s.pickerTitle}>
              {selectedFile ? 'Selected PDF: ' + selectedFile.name : 'Choose or drop a PDF résumé'}
            </span>
            <span className={s.fitNote} id={id + '-pdf-hint'}>Text-based PDF, up to 5 MB</span>
          </button>
        </div>
      ) : (
        <div className={s.inputField}>
          <label htmlFor={id + '-resume'}>Résumé text</label>
          <textarea
            id={id + '-resume'}
            className={s.textPaste}
            placeholder="Include your skills, experience, projects, and education."
            value={resumeText}
            onChange={(e) => setResumeText(e.target.value)}
          />
        </div>
      )}

      <div className={s.inputField}>
        <label htmlFor={id + '-job-description'}>Job description (optional)</label>
        <textarea
          id={id + '-job-description'}
          className={s.jobDescription}
          aria-describedby={id + '-fit-note'}
          placeholder="Paste the role requirements and preferred skills."
          maxLength={MAX_JOB_DESCRIPTION_LENGTH}
          value={jobDescription}
          onChange={(event) => setJobDescription(event.target.value)}
        />
        <p id={id + '-fit-note'} className={s.fitNote}>Compare your résumé with the skills listed for this role.</p>
      </div>

      <p className={s.formError} role="alert">{errorMsg}</p>

      <div className={s.actionRow}>
        <div className={s.securityNote}>
          DBERT processes your résumé and any job description you provide.
        </div>
        <button
          type="button"
          className="btn btn-primary"
          style={{ padding: '12px 28px', fontSize: '0.95rem' }}
          disabled={pending !== null}
          onClick={handleScan}
        >
          {pending === 'scan' ? 'Auditing résumé…' : 'Run résumé audit'}
        </button>
      </div>
      <span className="sr-only" role="status">
        {pending === 'scan' ? 'Auditing résumé…' : ''}
      </span>

      {/* Live Scan Results */}
      {scanResult && (
        <section className={s.resultsWrap} aria-labelledby={id + '-audit-results'}>
          <h2 id={id + '-audit-results'} ref={resultsRef} tabIndex={-1} className={s.fitTitle}>Audit results</h2>
          <div className={s.scoreGrid}>
            <div>
              <div className={s.scoreGauge} style={{ borderColor: scanResult.color }}>
                <div className={s.scoreNum}>{scanResult.score}</div>
                <div className={s.scoreLabel}>ATS Score</div>
              </div>
              <div className={s.tierBadge} style={{ backgroundColor: scanResult.color }}>
                {scanResult.tier}
              </div>
            </div>

            <div>
              <div className={s.barRow}>
                <span>Keyword &amp; Tech Stack Alignment</span>
                <b>{scanResult.breakdown.keywords.percentage}%</b>
              </div>
              <div className={s.barTrack}>
                <div className={s.barFill} style={{ width: `${scanResult.breakdown.keywords.percentage}%` }} />
              </div>

              <div className={s.barRow}>
                <span>Action Verbs &amp; Metric Density</span>
                <b>{scanResult.breakdown.impact_verbs.percentage}%</b>
              </div>
              <div className={s.barTrack}>
                <div className={s.barFill} style={{ width: `${scanResult.breakdown.impact_verbs.percentage}%` }} />
              </div>

              <div className={s.barRow}>
                <span>Section &amp; Contact ATS Hygiene</span>
                <b>{scanResult.breakdown.structure.percentage}%</b>
              </div>
              <div className={s.barTrack}>
                <div className={s.barFill} style={{ width: `${scanResult.breakdown.structure.percentage}%` }} />
              </div>

              <div className={s.barRow}>
                <span>Length &amp; Formatting Balance</span>
                <b>{scanResult.breakdown.length_hygiene.percentage}%</b>
              </div>
              <div className={s.barTrack}>
                <div className={s.barFill} style={{ width: `${scanResult.breakdown.length_hygiene.percentage}%` }} />
              </div>
            </div>
          </div>

          {scanResult.job_fit && <JobFitResults fit={scanResult.job_fit} headingId={id + '-job-fit'} />}

          <div className={s.strengthsCard}>
            <div className={s.strengthsTitle}>✅ Key Strengths Identified</div>
            <ul className={s.strengthsList}>
              {(scanResult.strengths || []).map((st: string, idx: number) => (
                <li key={idx}>{st}</li>
              ))}
            </ul>
          </div>

          {scanResult.locked ? (
            <form className={s.gateCtaBox} method="post" onSubmit={handleUnlock} aria-labelledby={id + '-unlock'}>
              <h3 className={s.gateTitle} id={id + '-unlock'}>Unlock the full report</h3>
              <p className={s.gateDesc}>
                Get suggested résumé edits and related openings for this audit. When Gemini is available, it analyzes a résumé excerpt for the full report.
              </p>
              <div className={s.gateInputs}>
                <label className={s.inputField}>
                  <span>Full name</span>
                  <input name="name" autoComplete="name" className={s.gateInput} required />
                </label>
                <label className={s.inputField}>
                  <span>Email address</span>
                  <input type="email" name="email" autoComplete="email" className={s.gateInput} required />
                </label>
                <label className={s.inputField}>
                  <span>WhatsApp number (optional)</span>
                  <input type="tel" name="phone" autoComplete="tel" className={s.gateInput} />
                </label>
                <p className={s.formError} role="alert">{unlockError}</p>
                <button type="submit" className="btn btn-primary" disabled={pending !== null}>
                  {pending === 'unlock' ? 'Unlocking…' : 'Unlock report and activate LMS account'}
                </button>
              </div>
            </form>
          ) : (
            <div className={s.unlockedSection}>
              <div className={s.sectionBox}>
                <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#ef4444', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '8px' }}>
                  ⚠️ Critical Missing Keywords ({scanResult.critical_missing_keywords?.length || 0})
                </div>
                <div className={s.missingPills}>
                  {(scanResult.critical_missing_keywords || []).map((kw: string, idx: number) => (
                    <span key={idx} className={s.missingPill}>
                      {kw}
                    </span>
                  ))}
                </div>
              </div>

              <div className={s.sectionBox}>
                <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#d97706', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '12px' }}>
                  ✨ AI Bullet-Point Impact Rewrites
                </div>
                {(scanResult.recommendations?.bullet_rewrites || []).map((rw, idx) => (
                  <div key={idx} className={s.rewriteItem}>
                    <div className={s.rewriteOriginal}>Original: {rw.original}</div>
                    <div className={s.rewriteImproved}>Improved: {rw.improved}</div>
                    <div className={s.rewriteWhy}>Why: {rw.why}</div>
                  </div>
                ))}
              </div>

              <div className={s.sectionBox}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                  <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#10b981', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                    💼 Verified Partner Roles Matching Your Profile
                  </div>
                  <Link href="https://lms.dbert.in/jobs" className="t-gold t-sm" style={{ fontWeight: 700 }}>
                    View All Openings →
                  </Link>
                </div>
                {(scanResult.matched_jobs || []).length > 0 ? (
                  (scanResult.matched_jobs || []).map((job) => (
                    <div key={job.id} className={s.jobItem}>
                      <div>
                        <div className={s.jobTitle}>{job.title}</div>
                        <div className={s.jobMeta}>{job.company_name} · {job.location || 'Remote'}{job.stipend_min && job.stipend_max ? ` · ₹${job.stipend_min.toLocaleString()}–₹${job.stipend_max.toLocaleString()}/mo` : ''}</div>
                      </div>
                      <a href={`https://lms.dbert.in/apply/${encodeURIComponent(job.id)}`} className="btn btn-secondary" style={{ padding: '6px 14px', fontSize: '0.8rem' }}>
                        Apply Now
                      </a>
                    </div>
                  ))
                ) : (
                  <p style={{ color: '#94a3b8', fontSize: '0.85rem' }}>
                    No exact title matches right now — check our live internship discovery board on LMS.
                  </p>
                )}
              </div>

              <div style={{ textAlign: 'center', marginTop: '24px' }}>
                <a
                  href={(scanResult.lms_signup_url && getDbertHref(scanResult.lms_signup_url)) || 'https://lms.dbert.in/portal/cv'}
                  className="btn btn-primary"
                  style={{ padding: '14px 32px', fontSize: '1rem', fontWeight: 700 }}
                >
                  🚀 Open in DBERT CV Builder &amp; Optimize on LMS
                </a>
              </div>
            </div>
          )}
        </section>
      )}
    </div>
  );
}
