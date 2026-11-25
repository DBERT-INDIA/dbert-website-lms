import { notFound } from 'next/navigation';
import { pageMetadata } from '@/lib/seo';
import { getTrackBySlug } from '@/data/courses.config';
import FellowshipTrackTemplate from '@/components/courses/FellowshipTrackTemplate';

export const metadata = pageMetadata('/learners/courses/full-stack-development');

export default function FullStackCoursePage() {
  const track = getTrackBySlug('full-stack-development');
  if (!track) notFound();
  return <FellowshipTrackTemplate track={track} />;
}
