import React from 'react';
import type { Metadata } from 'next';
import DirectoryClient, { type CandidateDirectoryItem } from './DirectoryClient';
import directoryData from '@/data/directory_candidates.json';

export const metadata: Metadata = {
  title: 'Alphabetical Intern Credential Directory | DBERT',
  description:
    'Complete sovereign registry and alphabetical directory of DBERT technical incubation fellows, verified internship certificates, and evaluation rubrics.',
  openGraph: {
    title: 'DBERT Credential Directory — Technical Incubation Fellows',
    description:
      'Search and verify DBERT internship candidates alphabetically. Official credential repository for Artificial Intelligence, Data Analytics, and Software Engineering.',
    url: 'https://dbert.in/verify/directory',
    siteName: 'DBERT',
    type: 'website',
  },
};

export default function DirectoryPage() {
  const candidates = directoryData as CandidateDirectoryItem[];

  return <DirectoryClient candidates={candidates} />;
}
