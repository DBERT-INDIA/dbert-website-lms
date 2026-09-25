import React from 'react';
import CaseStudyTemplate from '@/components/layout/CaseStudyTemplate';
import Image from 'next/image';
import { pageMetadata } from '@/lib/seo';


export const metadata = pageMetadata('/startups/portfolio/cognitive-solutions');

export default function CognitiveSolutionsCaseStudyPage() {
  return (
    <CaseStudyTemplate
      logoText="cognitivesolutions.site"
      logoSrc="/cognitive.png"
      name="Cognitive Solutions"
      externalLink="https://www.cognitivesolutions.site/"
      challenge="Cognitive Solutions aimed to establish a scalable talent acquisition model to support their growing client integrations across Robotics, IoT, and AI agent frameworks. Their internal training infrastructure was unable to keep pace with client project onboarding, leading to resource delays and bottlenecks in their hardware-software integration pipeline."
      contribution="DBERT engineered a shared training framework and custom recruitment pathway. We synchronized Cognitive Solutions' stack parameters (ROS, Python automation, and device communication protocols) with our advanced learner curricula. We then established a targeted placement channel that pre-vetted interns through live simulation reviews before deployment."
      outcome="The collaborative pipeline successfully trained and placed qualified junior developers directly into live AI, IoT, and robotics integration projects. Technical onboarding time was reduced by 60%, allowing Cognitive Solutions to meet all client deployment schedules."
      metrics="60% Reduction in Onboarding | 100% Client Deployment Compliance"
    />
  );
}
