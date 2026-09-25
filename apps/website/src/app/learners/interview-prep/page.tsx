import React from 'react';
import StepTimeline from '@/components/ui/StepTimeline';
import { pageMetadata } from '@/lib/seo';
import s from '../learners.module.css';
import { BookOpen, FileText, Mic, Code, Award } from 'lucide-react';


export const metadata = pageMetadata('/learners/interview-prep');

export default function InterviewPrepPage() {
  const steps = [
    { number: '01', title: '1-on-1 Mock Technical Audits', description: 'Schedule mock technical panels with industry practitioners. Get real time feedback on coding efficiency, system design concepts, and database query optimizations.' },
    { number: '02', title: 'GitHub & Resume Scoring', description: 'Ensure your repositories, README documentation, LinkedIn profiles, and resumes highlight the correct keywords and project outcomes that AI recruiters query.' },
    { number: '03', title: 'System Design Question Banks', description: 'Access curated question registers covering AI agent coordination patterns, vector indexing rules, and API token-streaming caching schemas.' }
  ];

  return (
    <div className="glow-wrapper">
      <div className="glow-spot"></div>

      {/* Hero Header Section */}
      <div className="container page-head">
        <div className="doclabel">
          § 01 — TECHNICAL INTERVIEW AUDIT <span className="rev">rev: 2026.2</span>
        </div>
        <h1 className="page-title">
          Land Your First AI Engineering Role
        </h1>
        <p className="lede-wide">
          Build the technical skills, communication structures, and resume layouts needed to clear rigorous coding interviews and system audits.
        </p>
      </div>

      {/* Key Metrics Grid (Secondary BG) */}
      <div className="section-band">
        <div className="container">
          <div className="bento-grid-3">
            <div className="bento-card center">
              <span className="icon-chip"><Mic aria-hidden="true" /></span>
              <h3 className="accent-note">Mock Interviews</h3>
              <p className="text-sm">1-on-1 mock panel sessions with senior developers focusing on live coding and database design.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><Code aria-hidden="true" /></span>
              <h3 className="accent-note">Live Coding Drills</h3>
              <p className="text-sm">Real time algorithm evaluations addressing REST APIs, Python memory limits, and logic parsing.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><Award aria-hidden="true" /></span>
              <h3 className="accent-note">Portfolio Reviews</h3>
              <p className="text-sm">Exhaustive code audits of your active GitHub projects, README documentation, and system architecture.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content (Primary BG) */}
      <div className="container pad-block">
        <div className="doclabel mb-2">§ 02 — HIRING PIPELINE STRATEGY</div>
        <div className="bento-grid-2">
          <div className="stack">
            <h2 className="section-title">
              Crack the AI Engineering Hiring Pipeline
            </h2>
            <p className="prose-lg">
              Getting hired as an AI developer or data analyst requires more than just listing projects on a resume. Tech recruiters look for candidates who can explain vector space dimensionality, write optimized database queries, solve complex coding tasks, and design scalable system architectures under pressure. A generic software resume will often be rejected by automated scanner algorithms before a human ever reviews it.
            </p>
          </div>
          <div className={`bento-card ${s.accentPanel}`}>
            <h3 className={s.accentPanelTitle}>Resume &amp; GitHub Optimization</h3>
            <ul className={s.accentList}>
              <li><strong>Keyword alignment</strong>: Target exact terms (e.g. pgvector, CrewAI, token caching) to pass automated ATS filters.</li>
              <li><strong>Commit history curation</strong>: Structure repo README files, flow charts, and clean configurations.</li>
              <li><strong>Outcome framing</strong>: Quantify project descriptions focusing on execution speeds and compute optimizations.</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Timeline Section (Secondary BG) */}
      <div className="band-top">
        <div className="container-sm">
          <div className="doclabel mb-2">§ 03 — CAREER ACCELERATION ROADMAP</div>
          <h2 className="subsection-title">
            Your Career Acceleration Roadmap
          </h2>
          <StepTimeline steps={steps} />
        </div>
      </div>

      {/* Action Call (Primary BG) */}
      <div className="container pad-block">
        <div className="doclabel mb-2">§ 04 — INITIALIZE CAREER SUPPORT</div>
        <div className="bento-card callout-plain">
          <h2 className="card-title">Get Interview-Ready and Get Hired</h2>
          <p className="page-lede">
            Get direct feedback from industry mentors and optimize your public code profiles. Access DBERT Career Services.
          </p>
          <a href="/learners" className="btn btn-primary btn-lg">Explore Career Tracks</a>
        </div>
      </div>
    </div>
  );
}
