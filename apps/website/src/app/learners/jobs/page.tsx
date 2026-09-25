import React from 'react';
import { pageMetadata } from '@/lib/seo';
import s from '../learners.module.css';


export const metadata = pageMetadata('/learners/jobs');

export default function JobBoardPage() {
  const jobs = [
    { 
      title: 'AI Agent Developer Intern', 
      company: 'Digital Blaize', 
      type: 'Remote / Internship', 
      salary: '₹12,000 – ₹18,000 / month stipend',
      requirements: 'Familiarity with Python, LangChain/CrewAI, and Git. Candidates must have built at least one multi-agent automation project.',
      desc: 'Assist in building autonomous workflow agents, configuring browser scraping nodes, and writing API database integrations.' 
    },
    { 
      title: 'Full Stack AI Developer', 
      company: 'Alkame Inc.', 
      type: 'Remote / Full-time', 
      salary: '₹4,80,000 – ₹7,20,000 LPA starting package',
      requirements: 'Next.js App Router, Node.js backend APIs, pgvector schema designs, and AWS EC2 server hosting setups.',
      desc: 'Co-develop semantic database indexes, build interactive token-streaming chat consoles, and maintain secure user authentication dashboards.' 
    },
    { 
      title: 'Data & BI Systems Engineer', 
      company: 'Aivara Technologies', 
      type: 'Remote / Full-time', 
      salary: '₹5,00,000 – ₹8,00,000 LPA starting package',
      requirements: 'Python Pandas, python-pptx automated reporting, OpenRouter LLM context budget control, and PostgreSQL schemas.',
      desc: 'Work on Aivara Insight Lite: automated CSV ingestion, variance decomposition, and automated slide deck generation.' 
    },
    { 
      title: 'Local AI Systems Developer (Open Source)', 
      company: 'Gayatri AI', 
      type: 'Remote / Fellowship', 
      salary: '₹10,000 – ₹15,000 / month stipend',
      requirements: 'Ollama GGUF quantization, local model caching, Python CLI automation, and offline education simulations.',
      desc: 'Develop lightweight multi-agent educational simulations deployed across internet-constrained rural schools.' 
    },
    { 
      title: 'Data Analytics Associate', 
      company: 'Cognitive Solutions', 
      type: 'Remote / Full-time', 
      salary: '₹4,00,000 – ₹6,50,000 LPA starting package',
      requirements: 'Python Pandas database cleaning, complex SQL queries, and designing interactive visual dashboards using Metabase/Plotly.',
      desc: 'Clean corporate transaction logs, run data queries to identify latency bottlenecks, and build visual metrics dashboards.' 
    }
  ];

  return (
    <div className="glow-wrapper">
      <div className="glow-spot"></div>

      {/* Hero Header Section */}
      <div className="container page-head">
        <div className="doclabel">
          § 01 — CAREER HIRING PORTAL <span className="rev">rev: 2026.2</span>
        </div>
        <h1 className="page-title">
          Your Next Career Move Starts Here
        </h1>
        <p className="lede-wide">
          Access entry-level engineering roles and internship pathways posted directly by our network of partner startups and corporate clients.
        </p>
      </div>

      {/* Key Info Row (Secondary BG) */}
      <div className="section-band">
        <div className="container center">
          <div className="doclabel mb-2">§ 02 — EXCLUSIVE NETWORK PLACEMENTS</div>
          <p className="band-lede">
            This job board is reserved for candidates who have completed our structured upskilling courses or participated in the DBERT Paid Internship. Below are active roles posted directly by our partners seeking developers with verified project portfolios.
          </p>
        </div>
      </div>

      {/* Active Openings (Primary BG) */}
      <div className="container pad-block">
        <div className="doclabel mb-2">§ 03 — ACTIVE OPEN OPPORTUNITIES</div>
        <h2 className="section-title">
          Active Opportunities
        </h2>
        <div className={s.jobList}>
          {jobs.map((job, idx) => (
            <div key={idx} className={`bento-card ${s.jobCard}`}>
              <div className={s.jobTop}>
                <span className={s.companyTag}>{job.company}</span>
                <span className={s.jobSalary}>{job.salary}</span>
              </div>
              <h3 className={s.jobTitle}>{job.title}</h3>
              <p className={s.jobDesc}>{job.desc}</p>
              <div className={s.reqBlock}>
                <strong className={s.reqLabel}>Role Requirements:</strong>
                <p className={s.reqBody}>{job.requirements}</p>
              </div>
              <div className={s.jobFoot}>
                <span className={s.jobType}>{job.type}</span>
                <a href="https://internship.dbert.online/" target="_blank" rel="noopener noreferrer" className="btn btn-primary btn-sm">Apply via Portal</a>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Action Call (Secondary BG) */}
      <div className="band-top">
        <div className="container">
          <div className="doclabel mb-2">§ 04 — PLACEMENT ACCELERATION</div>
          <div className="bento-card cta-panel">
            <h2 className="card-title">Fast-Track Your Placement</h2>
            <p className="page-lede">
              Applications are reviewed and prioritized for DBERT Internship graduates. Pass technical evaluations to secure direct matching referrals.
            </p>
            <a href="https://internship.dbert.online/" target="_blank" rel="noopener noreferrer" className="btn btn-outline btn-lg">Apply for Internship Track</a>
          </div>
        </div>
      </div>
    </div>
  );
}
