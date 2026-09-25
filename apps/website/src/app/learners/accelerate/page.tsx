import React from 'react';
import ProgramDetailTemplate from '@/components/layout/ProgramDetailTemplate';
import { pageMetadata } from '@/lib/seo';

export const metadata = pageMetadata('/learners/accelerate');

export default function AccelerateProgramPage() {
  return (
    <ProgramDetailTemplate
      title="DBERT Accelerate"
      subtitle="Applied Industrial AI Engineering — 3 Months of Production Sprints"
      price="₹4,999"
      duration="3 months"
      audience="Computer science graduates, self-taught programmers, and Launchpad alumni ready to build and deploy production AI pipelines."
      outcome="Build and deploy 3 production-grade project modules, establish active GitHub contributions repositories, receive a verified course completion certificate, and secure direct eligibility for the paid DBERT Fellowship."
      repoReferences={[
        {
          name: 'dbert-labs / dbert-agent',
          url: 'https://github.com/dbert-labs',
          role: 'Core AI Systems & Autonomous Workflow Engineer',
          badgeText: 'DBERT Production Stack',
          description: 'Production multi-agent execution pipeline orchestrating local Ollama LLMs with live web search, function execution sandboxes, and JSON signal schemas.',
          keyModules: ['StateGraph Workflow Loop', 'Ollama Local Weight Inference', 'Streaming Token Generator', 'Sandboxed Python REPL']
        },
        {
          name: 'Aivara-Technologies / aivara-insight-lite',
          url: 'https://github.com/Aivara-Technologies/aivara-insight-lite',
          role: 'Full Stack RAG & Systems Developer',
          badgeText: 'Aivara Enterprise Track',
          description: 'Locally hosted analytical system inferring data schemas, computing driver variance, and querying vector databases with LangChain and pgvector.',
          keyModules: ['pgvector Embedding Index', 'Hybrid Semantic Search', 'Document Parser & Chunker', 'Automated Slide Export']
        }
      ]}
      curriculum={[
        {
          period: "Weeks 1–4",
          title: "Specialized Stack Setup, Containerization & Schema Design",
          topics: [
            "Advanced architecture deep dive: AI Agent state machines (LangGraph/CrewAI), Production RAG pipelines (Next.js/PostgreSQL/pgvector), or System Automation (Playwright/Celery).",
            "Configuring local server dependencies, installing environment packages, and building multi-stage container sets with Docker and docker-compose.",
            "Designing robust database schemas, vector indexing parameters (HNSW/IVFFlat), security controls, and authenticated API endpoints."
          ]
        },
        {
          period: "Weeks 5–8",
          title: "Production Sprints, Vector RAG & Live Repositories",
          topics: [
            "Sprint 1: Building a functional multi-agent coordination loop with tool calling, context compression, and error recovery.",
            "Sprint 2: Implementing pgvector database connections, hybrid search (dense + BM25 sparse), and automated background task queues.",
            "Conducting code review check-ins on live pull requests, profiling token generation latency, and resolving concurrency bottlenecks."
          ]
        },
        {
          period: "Weeks 9–12",
          title: "Cloud VPC Staging, Telemetry & Fellowship Handoff",
          topics: [
            "Packaging and deploying containerized applications to private cloud VPCs (AWS EC2 / Supabase) with automated CI/CD and SSL termination.",
            "Implementing Prometheus metrics and OpenTelemetry tracing for LLM latency, memory consumption, and error rates.",
            "Writing technical README documentation, passing automated unit and integration test suites, and receiving direct eligibility for the paid DBERT Fellowship."
          ]
        }
      ]}
    />
  );
}

