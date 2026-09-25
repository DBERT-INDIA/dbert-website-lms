import React from 'react';
import CaseStudyTemplate from '@/components/layout/CaseStudyTemplate';
import { pageMetadata } from '@/lib/seo';


export const metadata = pageMetadata('/startups/portfolio/gayatri-ai');

export default function GayatriAICaseStudyPage() {
  return (
    <CaseStudyTemplate
      logoText="gayatridevi.ai"
      logoSrc="/gayatri-ai.png"
      name="Gayatri AI"
      externalLink="https://gayatridevi.ai/"
      challenge="Gayatri AI sought to establish open-source educational frameworks capable of deploying localized, low-resource AI agent nodes in classroom environments. They faced significant hurdles in optimizing model weight parameters for standard school CPUs and structuring clear API wrappers for students learning AI concepts in public registries."
      contribution="DBERT Labs spearheaded the open-source collaboration, delegating technical researchers and developers to commit directly to their repository. We designed modular multi-agent orchestration libraries, configured automated validation setups to review student-submitted prompts, and optimized local model pipelines utilizing Ollama integrations."
      outcome="The collaborative open-source partnership successfully published the Gayatri-AI framework. The libraries now support lightweight, offline-first multi-agent systems, enabling school environments to run interactive AI agent demonstrations on existing lab computers with sub-2s generation latency."
      metrics="10+ Schools Deployed | ₹0 API Costs | Open Source"
    />
  );
}
