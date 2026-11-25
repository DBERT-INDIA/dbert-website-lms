import { notFound } from 'next/navigation';
import { pageMetadata } from '@/lib/seo';
import { getTrackBySlug } from '@/data/courses.config';
import FellowshipTrackTemplate from '@/components/courses/FellowshipTrackTemplate';

export const metadata = pageMetadata('/learners/courses/digital-marketing');

export default function DigitalMarketingCoursePage() {
  const track = getTrackBySlug('digital-marketing');
  if (!track) notFound();
  return <FellowshipTrackTemplate track={track} />;
}
