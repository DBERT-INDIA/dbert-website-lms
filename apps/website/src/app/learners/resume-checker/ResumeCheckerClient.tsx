'use client';

import React, { useState, useRef } from 'react';
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

export default function ResumeCheckerClient() {
  const [selectedDomain, setSelectedDomain] = useState(DOMAINS[0].canonical);
  const [activeTab, setActiveTab] = useState<'upload' | 'paste'>('upload');
  const [resumeText, setResumeText] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  
  // Results
  const [scanResult, setScanResult] = useState<any>(null);
  
  // Unlock Form
  const [unlockName, setUnlockName] = useState('');
  const [unlockEmail, setUnlockEmail] = useState('');
  const [unlockPhone, setUnlockPhone] = useState('');
  const [unlockLoading, setUnlockLoading] = useState(false);

  const fileInputRef = useRef<HTMLInputElement>(null);
  const resultsRef = useRef<HTMLDivElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const f = e.target.files[0];
      if (f.type !== 'application/pdf') {
        alert('Please select a valid PDF file.');
        return;
      }
      setSelectedFile(f);
      setErrorMsg('');
    }
  };

  const handleScan = async () => {
    setErrorMsg('');
    if (activeTab === 'upload' && !selectedFile) {
      setErrorMsg('Please select a PDF resume or switch to the text tab.');
      return;
    }
    if (activeTab === 'paste' && resumeText.trim().length < 30) {
      setErrorMsg('Please paste at least 30 characters of resume text.');
      return;
    }

    setLoading(true);
    try {
      let res: Response;
      if (activeTab === 'upload' && selectedFile) {
        const fd = new FormData();
        fd.append('file', selectedFile);
        fd.append('domain', selectedDomain);
        res = await fetch('/api/tools/ats-checker', {
          method: 'POST',
          body: fd,
        });
      } else {
        res = await fetch('/api/tools/ats-checker', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            text: resumeText,
            domain: selectedDomain,
          }),
        });
      }

      const data = await res.json();
      if (!res.ok || data.status === 'error') {
        throw new Error(data.message || 'Failed to scan resume');
      }

      setScanResult(data);
      setTimeout(() => {
        resultsRef.current?.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    } catch (err: any) {
      setErrorMsg(err.message || 'Error communicating with ATS scanner. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleUnlock = async () => {
    if (!unlockName.trim() || !unlockEmail.trim() || !unlockEmail.includes('@')) {
      alert('Please provide your Full Name and a valid Email address.');
      return;
    }

    setUnlockLoading(true);
    try {
      let res: Response;
      if (activeTab === 'upload' && selectedFile) {
        const fd = new FormData();
        fd.append('file', selectedFile);
        fd.append('domain', selectedDomain);
        fd.append('name', unlockName.trim());
        fd.append('email', unlockEmail.trim());
        fd.append('phone', unlockPhone.trim());
        res = await fetch('/api/tools/ats-checker', {
          method: 'POST',
          body: fd,
        });
      } else {
        res = await fetch('/api/tools/ats-checker', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            text: resumeText,
            domain: selectedDomain,
            name: unlockName.trim(),
            email: unlockEmail.trim(),
            phone: unlockPhone.trim(),
          }),
        });
      }

      const data = await res.json();
      if (!res.ok || data.status === 'error') {
        throw new Error(data.message || 'Failed to unlock audit');
      }

      setScanResult(data);
    } catch (err: any) {
      alert(err.message || 'Error unlocking audit. Please try again.');
    } finally {
      setUnlockLoading(false);
    }
  };

  return (
    <div className={s.toolCard}>
      <div className={s.stepTitle}>Step 1: Select Your Target Technical Domain</div>
      <div className={s.domainPills}>
        {DOMAINS.map((d) => (
          <button
            key={d.id}
            type="button"
            className={`${s.domainPill} ${selectedDomain === d.canonical ? s.domainPillActive : ''}`}
            onClick={() => setSelectedDomain(d.canonical)}
          >
            {d.label}
          </button>
        ))}
      </div>

      <div className={s.tabNav}>
        <button
          type="button"
          className={`${s.tabBtn} ${activeTab === 'upload' ? s.tabBtnActive : ''}`}
          onClick={() => setActiveTab('upload')}
        >
          📄 Upload PDF Resume
        </button>
        <button
          type="button"
          className={`${s.tabBtn} ${activeTab === 'paste' ? s.tabBtnActive : ''}`}
          onClick={() => setActiveTab('paste')}
        >
          📝 Paste Resume Text
        </button>
      </div>

      {activeTab === 'upload' ? (
        <div
          className={s.dropZone}
          onClick={() => fileInputRef.current?.click()}
          onDragOver={(e) => e.preventDefault()}
          onDrop={(e) => {
            e.preventDefault();
            if (e.dataTransfer.files && e.dataTransfer.files[0]) {
              const f = e.dataTransfer.files[0];
              if (f.type === 'application/pdf') {
                setSelectedFile(f);
                setErrorMsg('');
              } else {
                alert('Please drop a PDF file.');
              }
            }
          }}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept="application/pdf"
            style={{ display: 'none' }}
            onChange={handleFileChange}
          />
          <div style={{ fontSize: '2.5rem', marginBottom: '8px' }}>☁️</div>
          <div style={{ fontWeight: 700, color: '#f8fafc', fontSize: '1.05rem' }}>
            {selectedFile
              ? `Selected: ${selectedFile.name} (${(selectedFile.size / 1024).toFixed(1)} KB)`
              : 'Click to browse or drop your PDF resume'}
          </div>
          <div style={{ fontSize: '0.8rem', color: '#64748b', marginTop: '6px' }}>
            Standard 1–2 page engineering resume (Max 5MB)
          </div>
        </div>
      ) : (
        <textarea
          className={s.textPaste}
          placeholder="Paste your complete resume text here (Summary, Skills, Experience, Education, Projects)..."
          value={resumeText}
          onChange={(e) => setResumeText(e.target.value)}
        />
      )}

      {errorMsg && (
        <div style={{ color: '#ef4444', fontSize: '0.85rem', marginTop: '12px', fontWeight: 600 }}>
          ⚠️ {errorMsg}
        </div>
      )}

      <div className={s.actionRow}>
        <div className={s.securityNote}>
          🔒 100% Private &amp; Secure · No data shared with external recruiters
        </div>
        <button
          type="button"
          className="btn btn-primary"
          style={{ padding: '12px 28px', fontSize: '0.95rem' }}
          disabled={loading}
          onClick={handleScan}
        >
          {loading ? 'Auditing Resume...' : '⚡ Run Free AI ATS Audit'}
        </button>
      </div>

      {/* Live Scan Results */}
      {scanResult && (
        <div ref={resultsRef} className={s.resultsWrap}>
          <div className={s.scoreGrid}>
            <div>
              <div className={s.scoreGauge} style={{ borderColor: scanResult.color }}>
                <div className={s.scoreNum}>{scanResult.score}</div>
                <div className={s.scoreLabel}>ATS Score</div>
              </div>
              <div className={s.tierBadge} style={{ backgroundColor: scanResult.color }}>
                {scanResult.tier}
              </div>
              <div className={s.passProb}>{scanResult.pass_probability}</div>
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

          <div className={s.strengthsCard}>
            <div className={s.strengthsTitle}>✅ Key Strengths Identified</div>
            <ul className={s.strengthsList}>
              {(scanResult.strengths || []).map((st: string, idx: number) => (
                <li key={idx}>{st}</li>
              ))}
            </ul>
          </div>

          {/* Lead Gate / Conversion Gate */}
          {scanResult.locked ? (
            <div className={s.gateWrap}>
              <div className={s.blurOverlay}>
                <div style={{ fontSize: '0.9rem', fontWeight: 700, color: '#f59e0b' }}>
                  CRITICAL MISSING TECH STACK KEYWORDS (5)
                </div>
                <p>Docker containerization, PostgreSQL indexing, Next.js App Router, Jest automated tests...</p>
                <div style={{ fontSize: '0.9rem', fontWeight: 700, color: '#f59e0b', marginTop: '12px' }}>
                  AI BULLET POINT REWRITES WITH METRICS
                </div>
                <p>Architected responsive Next.js frontend reducing latency by 32% for 5,000+ users...</p>
              </div>

              <div className={s.gateCtaBox}>
                <div className={s.gateTitle}>Unlock Complete ATS Breakdown &amp; Matched Jobs</div>
                <p className={s.gateDesc}>
                  Free for engineering students. Discover your exact missing keywords, customized AI bullet point rewrites, and 1-click apply to verified partner openings.
                </p>
                <div className={s.gateInputs}>
                  <input
                    type="text"
                    placeholder="Full Name"
                    className={s.gateInput}
                    value={unlockName}
                    onChange={(e) => setUnlockName(e.target.value)}
                  />
                  <input
                    type="email"
                    placeholder="Email Address"
                    className={s.gateInput}
                    value={unlockEmail}
                    onChange={(e) => setUnlockEmail(e.target.value)}
                  />
                  <input
                    type="tel"
                    placeholder="WhatsApp Number"
                    className={s.gateInput}
                    value={unlockPhone}
                    onChange={(e) => setUnlockPhone(e.target.value)}
                  />
                  <button
                    type="button"
                    className="btn btn-primary"
                    style={{ width: '100%', padding: '12px', fontWeight: 700 }}
                    disabled={unlockLoading}
                    onClick={handleUnlock}
                  >
                    {unlockLoading ? 'Unlocking...' : 'Unlock Full Report & Activate LMS Account →'}
                  </button>
                </div>
              </div>
            </div>
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
                {(scanResult.recommendations?.bullet_rewrites || []).map((rw: any, idx: number) => (
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
                  (scanResult.matched_jobs || []).map((job: any) => (
                    <div key={job.id} className={s.jobItem}>
                      <div>
                        <div className={s.jobTitle}>{job.title}</div>
                        <div className={s.jobMeta}>{job.company_name} · {job.location || 'Remote'} · {job.stipend_min ? `₹${job.stipend_min.toLocaleString()} - ₹${job.stipend_max.toLocaleString()}/mo` : 'Competitive'}</div>
                      </div>
                      <a href={`https://lms.dbert.in/apply/${job.id}`} className="btn btn-secondary" style={{ padding: '6px 14px', fontSize: '0.8rem' }}>
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
                  href={scanResult.lms_signup_url || 'https://lms.dbert.in/portal/cv'}
                  className="btn btn-primary"
                  style={{ padding: '14px 32px', fontSize: '1rem', fontWeight: 700 }}
                >
                  🚀 Open in DBERT CV Builder &amp; Optimize on LMS
                </a>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
