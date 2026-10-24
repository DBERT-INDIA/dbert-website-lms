import React from 'react';
import StartupRegisterForm from '@/components/ui/MultiStepForm';
import CohortBanner from '@/components/ui/CohortBanner';
import { pageMetadata } from '@/lib/seo';


export const metadata = pageMetadata('/startups/register');

export default function StartupRegisterPage() {
  return (
    <>
      <CohortBanner deadlineDate="August 1st, 2026" />
      <div className="container pad-block">
        <div className="mb-lg center">
          <div className="doclabel justify-center">
            § 01 — INCUBATION APPLICATION <span className="rev">rev: 2026.2</span>
          </div>
          <h1>Apply for Incubation</h1>
          <p className="measure-sm">
            Accelerate your development cycle. Join DBERT&apos;s AI incubator program and leverage customized engineering pipelines, mentors, and placement networks.
          </p>
        </div>

      <StartupRegisterForm />
    </div>
    </>
  );
}
