import React from 'react';
import AlkameCaseStudyContent from '@/components/layout/AlkameCaseStudyContent';
import { pageMetadata } from '@/lib/seo';


export const metadata = pageMetadata('/startups/portfolio/alkame');

export default function AlkameCaseStudyPage() {
  return <AlkameCaseStudyContent />;
}
