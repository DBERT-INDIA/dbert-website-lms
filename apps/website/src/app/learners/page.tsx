import React from 'react';
import Link from 'next/link';
import CareerLadder from '@/components/ui/CareerLadder';
import HandNote from '@/components/ui/HandNote';
import HandDrawnArrow from '@/components/ui/HandDrawnArrow';
import Faq from '@/components/seo/Faq';
import s from './learners.module.css';
import { pageMetadata } from '@/lib/seo';

export const metadata = pageMetadata('/learners');

const learnerFaqs = [
  {
    question: 'Is the DBERT Fellowship really a paid AI internship?',
    answer:
      'Yes. Unlike attendance-based online certification programs, our Applied AI Fellowship places candidates into development squads building live software systems for incubated enterprise clients. The stipend ranges from ₹5,000 to ₹18,000 and is paid directly against delivery milestones and code pull requests reviewed by senior engineers.'
  },
  {
    question: 'Can I skip Launchpad and apply straight to Accelerate or Fellowship?',
    answer:
      'Yes. If you already possess intermediate Python competence, Git command line fluency, and basic familiarity with data parsing, you can bypass Launchpad and enter Accelerate directly. Similarly, self-taught engineers can skip courses entirely by passing our rigorous external code screening challenge at internship.dbert.online.'
  },
  {
    question: 'Do you guarantee an artificial intelligence job placement upon completion?',
    answer:
      'No, and we urge transparency regarding Indian educational guarantees. What we provide is an indisputable, independently verifiable professional record: merged commits on live repositories, technical letters of recommendation signed by lead architects, and direct talent referrals to our vetted partner startup network.'
  },
  {
    question: 'How do employers verify DBERT certificates and experience letters?',
    answer:
      'Every completion certificate and professional fellowship recommendation letter carries a secure cryptographic credential ID. Hiring managers and HR departments enter this ID directly at dbert.online/verify to inspect verified project deliverables without waiting for manual email confirmation.'
  },
  {
    question: 'Are installment plans (EMI) available for Launchpad and Accelerate fee structures?',
    answer:
      'Yes. Both DBERT Launchpad (₹7,999) and DBERT Accelerate (₹4,999) support flexible monthly payment installments at checkout, allowing learners to spread program costs across their training iterations.'
  },
];

const jsonLd = {
  '@context': 'https://schema.org',
  '@graph': [
    {
      '@type': 'ItemList',
      name: 'DBERT AI Career Progression Pathways',
      itemListElement: [
        {
          '@type': 'ListItem',
          position: 1,
          name: 'DBERT Launchpad (Foundations)',
          url: 'https://dbert.online/learners/launchpad',
        },
        {
          '@type': 'ListItem',
          position: 2,
          name: 'DBERT Accelerate (Applied Industrial Engineering)',
          url: 'https://dbert.online/learners/accelerate',
        },
        {
          '@type': 'ListItem',
          position: 3,
          name: 'DBERT Fellowship (Paid AI Internship)',
          url: 'https://dbert.online/learners/fellowship',
        },
        {
          '@type': 'ListItem',
          position: 4,
          name: 'DBERT Verified Talent Career Placement',
          url: 'https://dbert.online/learners/jobs',
        },
      ],
    },
    {
      '@type': 'FAQPage',
      mainEntity: learnerFaqs.map((f) => ({
        '@type': 'Question',
        name: f.question,
        acceptedAnswer: {
          '@type': 'Answer',
          text: f.answer,
        },
      })),
    },
  ],
};

export default function LearnersLandingPage() {
  const ladderSteps = [
    {
      num: '01',
      tag: 'Beginner Friendly',
      title: 'DBERT Launchpad',
      price: '₹7,999 / 2 months',
      forText: 'Designed for complete beginners, non-technical professionals, and students wishing to transition into coding.',
      outcome: 'Master foundational Python syntax, Git version control, command line commands, and basic data formats (JSON/CSV).',
      ctaText: 'Start Launchpad',
      ctaHref: '/learners/launchpad'
    },
    {
      num: '02',
      tag: 'Industrial Training',
      title: 'DBERT Accelerate',
      price: '₹4,999 / 3 months',
      forText: 'For intermediate programmers, computer science graduates, and Launchpad track graduates.',
      outcome: 'Build production-ready AI applications, implement RAG systems, connect APIs, and receive a verified completion certificate.',
      ctaText: 'Explore Accelerate',
      ctaHref: '/learners/accelerate',
      isFeatured: true
    },
    {
      num: '03',
      tag: 'Experience Track',
      title: 'DBERT Fellowship (Paid)',
      price: '₹1,599 / 3 months',
      forText: 'Top-tier graduates from our Accelerate courses are selected through code challenges to work on real client systems.',
      outcome: 'Earn remote experience letters, contribute directly to live startup products, and receive performance-based stipends.',
      ctaText: 'Apply for Fellowship',
      ctaHref: 'https://internship.dbert.online/',
      isFeatured: true
    },
    {
      num: '04',
      tag: 'AI Job Market',
      title: 'AI Jobs',
      price: 'Career Placement',
      forText: 'Exclusively for fellowship graduates with verified client contributions on their GitHub profiles.',
      outcome: 'Get direct referrals to our network of 4+ partner startups, receive resume scoring reviews, and prepare for code screenings.',
      ctaText: 'View Jobs',
      ctaHref: '/learners/jobs'
    }
  ];

  return (
    <div className="container pad-block">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <div className="mb-lg">
        <div className="doclabel">
          § 01 — LEARNER PATHWAYS <span className="rev">rev: 2026.2</span>
        </div>
        <h1 className="relative inline-block">
          AI career programs built as a progressive engineering ladder
          <HandNote className="absolute -right-8 -top-6 text-lg hidden md:block" tone="blue">
            Structured Path
          </HandNote>
        </h1>
        <p className="intro-copy">
          Four structured rungs, executed sequentially: your very first validated Python script, a production applied RAG training pipeline, an embedded paid engineering fellowship on live venture repositories, and a curated jobs board restricted strictly to verified contributors.
        </p>
      </div>

      <div className="mb-lg relative">
        <CareerLadder steps={ladderSteps} />
        <div className="absolute -bottom-16 right-20 z-20 hidden md:block">
           <HandDrawnArrow color="var(--signal)" width={60} height={60} className="transform -scale-y-100 rotate-45" />
           <HandNote tone="amber" className="absolute top-10 left-10 whitespace-nowrap text-sm">
             Progress step-by-step
           </HandNote>
        </div>
      </div>

      {/* Comprehensive Rungs & Technical Pathways Breakdown */}
      <div className="article mb-lg">
        <h2>Why an AI career ladder outperforms detached course catalogues</h2>
        <p>
          Legacy edtech platforms across India treat technology education as an disconnected supermarket of video courses. You buy a course on data analytics, another on basic neural networks, and a bootcamp on React web development—each operating in total isolation. When you present this collection of completion certificates to engineering recruiters in 2026, the market response is consistent indifference.
        </p>
        <p>
          Why? Because real-world engineering software development is cumulative, not transactional. You cannot calibrate an autonomous agent without understanding API data serialization; you cannot design production Retrieval-Augmented Generation (RAG) loops without mastering vector indexing and terminal environment configurations. Our learning ecosystem structures the acquisition of applied artificial intelligence competence as an interdependent ladder where every milestone directly serves as an operational prerequisite for the next.
        </p>

        <h3>Rung 1: DBERT Launchpad — Structural Foundation</h3>
        <p>
          The first barrier for most non-technical professionals and non-computer science students is syntax hesitation and tooling anxiety. In the <Link href="/learners/launchpad">DBERT Launchpad program</Link>, we replace generalized algorithmic puzzles with operational system instruction. Over two months (8 weekly sprints), learners transition from writing their initial command-line statements to manipulating structured JSON data schemas, controlling Git branch merges, and deploying lightweight automation scripts. To review our transition framework for candidates entering without academic engineering backgrounds, examine our complete <Link href="/blog/non-tech-to-ai-career">Python &amp; AI Engineering Roadmap for Non-CS Students</Link>.
        </p>

        <h3>Rung 2: DBERT Accelerate — Applied Industrial Engineering</h3>
        <p>
          Once syntax fluency is established, developers graduate into the <Link href="/learners/accelerate">DBERT Accelerate engineering track</Link>. Here, tutorials terminate and structural building begins. Students implement live Retrieval-Augmented Generation architectures over unformatted PDFs, deploy vector database clusters using pgvector and Milvus, and configure function-calling loops against models locally and via high-throughput endpoints. For a technical deep dive into the exact vector retrieval mechanisms you will master, study our implementation guide on <Link href="/blog/rag-pipeline-tutorial-from-scratch">Building a Production RAG Architecture from Scratch</Link>.
        </p>

        <h3>Rung 3: DBERT Applied Fellowship — Production Code &amp; Stipends</h3>
        <p>
          The transition from student to professional software engineer requires surviving genuine code review on live systems. In our selective <Link href="/learners/fellowship">Paid AI Fellowship</Link>, admitted developers join embedded sprint squads under lead architects to build custom models and data ingestion layers for incubated startups within our <Link href="/startups/portfolio">Venture Portfolio</Link>. Fellows leave with verifiable Git contribution histories, professional experience letters, and earned stipends ranging from ₹5,000 to ₹18,000. Learn how this technical engagement operates in our comprehensive <Link href="/blog/paid-ai-internship-india-guide-2026">2026 Guide to Landing Paid AI Internships in India</Link>.
        </p>

        <h3>Rung 4: Verified Talent Referral &amp; Career Placement</h3>
        <p>
          The culminating rung of the ladder is restricted exclusively to engineers who have successfully shipped validated code to real repositories. Instead of broadcasting generic resumes into automated tracking software, fellowship alumni access our dedicated <Link href="/learners/jobs">AI Jobs Board</Link>. Partner startups and enterprise engineering managers review verified contribution logs directly, cutting through screening noise to extend interviews for high-compensation technical roles. For detailed industry compensation analysis across entry to senior roles, refer to our benchmark report on <Link href="/blog/ai-agent-developer-salary-2026">AI Agent Developer Salary Scales in India 2026</Link>.
        </p>

        <h2>The Evidence Wall: Verifiable Letters vs. Attendance Participation</h2>
        <div className="disclosure">
          <p>
            <strong>The Evaluation Standard:</strong> In current AI recruitment markets, unverified certificates of online attendance have zero predictive value for technical performance. An engineer is evaluated exclusively by their code output, error resolution habits, and architectural reasoning during live technical screenings.
          </p>
          <p>
            <strong>Independently Verifiable Credentials:</strong> To eliminate credential fraud and guarantee recruiter trust, every accomplishment within the DBERT ecosystem is cryptographically recorded. Hiring managers can enter any certificate ID directly into our global <Link href="/verify">Certificate Verification Engine</Link> to audit explicit learning tracks, mentor signatures, and Git repository contributions without requiring third-party outreach.
          </p>
          <p>
            <strong>Transparent Fee Structures &amp; EMI:</strong> We maintain complete fiscal clarity across our learning tracks. Launchpad tuition is fixed at ₹7,999; Accelerate at ₹4,999; and Fellowship onboarding at ₹1,599 (covering dedicated mentor review hours and certificate issuance). Flexible EMI installment structures remain accessible across all learning tiers.
          </p>
        </div>
      </div>

      <div className={s.domainGrid}>
        {[
          { title: 'AI Agent Development', desc: 'Construct autonomous AI workflow agents using LangChain, CrewAI orchestration frameworks, and structured tool calling loops.', salary: 'LangGraph, CrewAI & Ollama', slug: 'ai-agent-development', badge: 'Trending #1' },
          { title: 'Generative AI Systems', desc: 'Build multi-provider LLM pipelines, prompt evaluation harnesses, dynamic vector indexing, and streaming front-ends.', salary: 'Llama-3, vLLM & RAG', slug: 'generative-ai', badge: 'High Impact' },
          { title: 'Machine Learning & Fine-Tuning', desc: 'Perform data preprocessing, feature engineering, and parameter-efficient fine-tuning (LoRA/QLoRA) on open-weights foundation models.', salary: 'PyTorch, LoRA & HuggingFace', slug: 'machine-learning', badge: 'Deep Tech' },
          { title: 'Full Stack AI Engineering', desc: 'Build responsive web applications with React, Next.js, Node.js, vector database indexing, and streaming LLM completion responses.', salary: 'Next.js, pgvector & TypeScript', slug: 'full-stack-development', badge: 'Most Popular' },
          { title: 'Python System Automation', desc: 'Deploy concurrent web scraping engines, configure Selenium/Playwright testing harnesses, parse complex JSON schemas, and trigger automated alerts.', salary: 'Python, Playwright & Celery', slug: 'python-automation', badge: 'High Demand' },
          { title: 'Applied Data Analytics', desc: 'Perform data cleaning pipelines with Python Pandas, formulate analytical SQL schemas, and assemble automated dashboard visualization frameworks.', salary: 'Pandas, SQL & Metabase', slug: 'data-analytics', badge: 'Evergreen' }
        ].map((domain, idx) => (
          <div key={idx} className="card stack-between">
            <div>
              <div className={s.badgeRow}>
                <span className={s.badge}>{domain.badge}</span>
              </div>
              <h3 className={s.domainTitle}>{domain.title}</h3>
              <p className={s.domainDesc}>{domain.desc}</p>
            </div>
            <div>
              <p className={s.salary}>{domain.salary}</p>
              <Link href={`/learners/courses/${domain.slug}`} className={s.pathLink}>Inspect Career Track &rarr;</Link>
            </div>
          </div>
        ))}
      </div>

      {/* Frequently Asked Questions Section */}
      <div className="article my-8">
        <Faq items={learnerFaqs} heading="AI Engineering Career Ladder — Frequently Asked Questions" />
      </div>

      <div className={s.nextGrid}>
        <div className={`card ${s.nextCard}`}>
          <h3 className="card-title-tight">Ace Your Technical Interviews</h3>
          <p className={s.nextDesc}>Practice rigorous system design mock screenings, refine recruiter-facing portfolios, and optimize your engineering presentation.</p>
          <Link href="/learners/interview-prep" className="btn btn-outline btn-sm">Start Interview Prep</Link>
        </div>
        <div className={`card ${s.nextCard}`}>
          <h3 className="card-title-tight">Explore AI Courses Index</h3>
          <p className={s.nextDesc}>Browse individual upskilling modules and domain technical certifications designed to complement your current specialization.</p>
          <Link href="/learners/courses" className="btn btn-outline btn-sm">View Courses Directory</Link>
        </div>
      </div>
    </div>
  );
}

