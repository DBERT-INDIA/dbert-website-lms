import React from 'react';
import CaseStudyTemplate from '@/components/layout/CaseStudyTemplate';
import { pageMetadata } from '@/lib/seo';


export const metadata = pageMetadata('/startups/portfolio/digital-blaize');

export default function DigitalBlaizeCaseStudyPage() {
  return (
    <CaseStudyTemplate
      logoText="digitalblaize.com"
      logoSrc="/digital-blaize.png"
      name="Digital Blaize"
      externalLink="https://digitalblaize.com/"
      challenge="Digital Blaize aimed to scale its multi-disciplinary educational programs across diverse technological sectors (including Robotics, AI/ML engineering, IoT setups, and Python Automation). To sustain this expansion, they required a steady pipeline of skilled developers capable of maintaining student platforms and co-developing curriculum sandbox environments."
      contribution="DBERT incubated their growth model, establishing direct pipelines to our upskilled student network. We deployed interns specializing in full-stack Next.js interfaces, automated grading systems, and database configurations. Additionally, DBERT's technical mentors reviewed and optimized their core learning management portal."
      outcome="Digital Blaize successfully scaled its curriculum delivery across 6 technical domains. More than 500 learners received hands-on training using sandbox portals developed by DBERT-deployed engineers, and platform load capacity was improved by 40%."
      metrics="6 Technical Domains | 500+ Learners | 40% Load Improvement"
    />
  );
}
