import { notFound } from 'next/navigation';
import { pageMetadata } from '@/lib/seo';
import { getTrackBySlug } from '@/data/courses.config';
import FellowshipTrackTemplate from '@/components/courses/FellowshipTrackTemplate';

export const metadata = pageMetadata('/learners/courses/ai-agent-development');

export default function AIAgentCoursePage() {
  const track = getTrackBySlug('ai-agent-development');
  if (!track) notFound();
  return <FellowshipTrackTemplate track={track} />;
}
