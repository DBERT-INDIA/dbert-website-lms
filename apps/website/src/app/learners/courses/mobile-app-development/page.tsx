import { notFound } from 'next/navigation';
import { pageMetadata } from '@/lib/seo';
import { getTrackBySlug } from '@/data/courses.config';
import FellowshipTrackTemplate from '@/components/courses/FellowshipTrackTemplate';

export const metadata = pageMetadata('/learners/courses/mobile-app-development');

export default function MobileAppCoursePage() {
  const track = getTrackBySlug('mobile-app-development');
  if (!track) notFound();
  return <FellowshipTrackTemplate track={track} />;
}
