import { notFound } from 'next/navigation';
import { pageMetadata } from '@/lib/seo';
import { getTrackBySlug } from '@/data/courses.config';
import FellowshipTrackTemplate from '@/components/courses/FellowshipTrackTemplate';

export const metadata = pageMetadata('/learners/courses/devops-cloud');

export default function DevOpsCloudCoursePage() {
  const track = getTrackBySlug('devops-cloud');
  if (!track) notFound();
  return <FellowshipTrackTemplate track={track} />;
}
