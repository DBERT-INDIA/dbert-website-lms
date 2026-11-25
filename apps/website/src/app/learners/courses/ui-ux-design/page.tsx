import { notFound } from 'next/navigation';
import { pageMetadata } from '@/lib/seo';
import { getTrackBySlug } from '@/data/courses.config';
import FellowshipTrackTemplate from '@/components/courses/FellowshipTrackTemplate';

export const metadata = pageMetadata('/learners/courses/ui-ux-design');

export default function UIUXCoursePage() {
  const track = getTrackBySlug('ui-ux-design');
  if (!track) notFound();
  return <FellowshipTrackTemplate track={track} />;
}
