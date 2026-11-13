import React, { Suspense } from 'react';
import type { Metadata } from 'next';
import UnlockClient from './UnlockClient';

export const metadata: Metadata = {
  title: 'Complete Project Verification & Unlock Official Credentials (₹299) | DBERT',
  description:
    'Official DBERT candidate credential verification portal. Complete final project evaluation and ₹299 statutory fee to unlock your 3-document credential dossier, Turnitin rubric, and verified registry status.',
  alternates: {
    canonical: 'https://dbert.in/verify/unlock'
  },
  openGraph: {
    title: 'Complete Project Verification & Unlock Official Credentials | DBERT',
    description:
      'Official DBERT candidate credential verification portal. Complete final project evaluation and ₹299 statutory fee to unlock your 3-document credential dossier.',
    url: 'https://dbert.in/verify/unlock',
    siteName: 'DBERT Verification Engine'
  }
};

export default function UnlockPage() {
  return (
    <Suspense
      fallback={
        <div style={{ minHeight: '60vh', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#8A9AB5' }}>
          Loading DBERT Verification Gateway...
        </div>
      }
    >
      <UnlockClient />
    </Suspense>
  );
}
