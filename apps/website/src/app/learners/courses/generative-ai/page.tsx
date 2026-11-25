import { notFound } from 'next/navigation';
import { pageMetadata } from '@/lib/seo';
import { getTrackBySlug } from '@/data/courses.config';
import FellowshipTrackTemplate from '@/components/courses/FellowshipTrackTemplate';

export const metadata = pageMetadata('/learners/courses/generative-ai');

export default function GenerativeAICoursePage() {
  const track = getTrackBySlug('generative-ai');
  if (!track) notFound();
  return <FellowshipTrackTemplate track={track} />;
}
