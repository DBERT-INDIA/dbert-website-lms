import React, { Suspense } from 'react';
import type { Metadata } from 'next';
import EnrollmentClient from './EnrollmentClient';

export const metadata: Metadata = {
  title: 'Technical Incubation Enrollment (₹1,999 Program) | DBERT',
  description:
    'Complete your technical incubation enrollment for the ₹1,999 program. Official DBERT admissions and technical incubation enrollment portal. Access production GitHub repositories, 1:1 mentor code reviews, and verified credentials.',
  alternates: {
    canonical: 'https://dbert.in/enroll/1999'
  },
  openGraph: {
    title: 'Technical Incubation Enrollment (₹1,999 Program) — DBERT',
    description:
      'Official DBERT admissions and technical incubation enrollment portal. Complete program fee payment and UTR submission to confirm your seat.',
    url: 'https://dbert.in/enroll/1999',
    siteName: 'DBERT — Digital Blinc Education Research and Technology',
    images: [
      {
        url: 'https://dbert.in/images/og-verify.png',
        width: 1200,
        height: 630,
        alt: 'DBERT Technical Incubation Enrollment'
      }
    ],
    locale: 'en_IN',
    type: 'website'
  }
};

export default function Enrollment1999Page() {
  return (
    <Suspense
      fallback={
        <div style={{ maxWidth: '1040px', margin: '40px auto', padding: '24px', color: '#8A9AB5', textAlign: 'center' }}>
          Loading DBERT Enrollment Portal...
        </div>
      }
    >
      <EnrollmentClient />
    </Suspense>
  );
}
