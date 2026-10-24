import React from 'react';
import LaunchpadDomainView from '@/components/launchpad/LaunchpadDomainView';
import { pageMetadata } from '@/lib/seo';

export const metadata = pageMetadata('/learners/launchpad');

export default function LaunchpadProgramPage() {
  return <LaunchpadDomainView />;
}
