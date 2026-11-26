import React from 'react';
import CaseStudyTemplate from '@/components/layout/CaseStudyTemplate';
import { pageMetadata } from '@/lib/seo';

export const metadata = pageMetadata('/startups/portfolio/dhanvee');

export default function DhanveeCaseStudyPage() {
  return (
    <CaseStudyTemplate
      logoText="dhanvee.info · dhanvee.online"
      name="Dhanvee"
      externalLink="https://dhanvee.info/"
      challenge="Dhanvee set out to build a transparent, people-first P2P lending beta for Indian borrowers and retail lenders — eliminating hidden fine print while providing instant monthly payment estimates, risk disclosures upfront, and a structured 4-track hiring pipeline across Bangalore, Chennai, Delhi NCR, Hyderabad, Mumbai, Pune, and Remote."
      contribution="DBERT co-architected Dhanvee's full-stack Next.js 15 + Drizzle ORM + PostgreSQL platform, implemented the interactive AI credit simulator and plain-English borrower/lender onboarding workflows, and connected Dhanvee's 4 core internship tracks (Business Development Partner, Machine Learning Analyst, AI Agent Developer, and Python Developer) directly to DBERT LMS (lms.dbert.in)."
      outcome="Dhanvee launched its production beta across dhanvee.info and dhanvee.online with 28 geo-targeted role pages, an automated assessment & proctoring pipeline, and live internship postings syndicated on DBERT LMS so fellows can apply and contribute directly to production sprints."
      metrics="4 Live Role Tracks on LMS | 7 Hub Cities | AI Credit Simulator | Beta Live"
      slug="dhanvee"
    />
  );
}
