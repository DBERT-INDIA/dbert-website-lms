import { notFound } from 'next/navigation';
import { pageMetadata } from '@/lib/seo';
import { getTrackBySlug } from '@/data/courses.config';
import FellowshipTrackTemplate from '@/components/courses/FellowshipTrackTemplate';

export const metadata = pageMetadata('/learners/courses/data-analytics');

export default function DataAnalyticsCoursePage() {
  const track = getTrackBySlug('data-analytics');
  if (!track) notFound();
  return <FellowshipTrackTemplate track={track} />;
}
