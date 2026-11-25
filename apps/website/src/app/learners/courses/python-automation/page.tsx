import { notFound } from 'next/navigation';
import { pageMetadata } from '@/lib/seo';
import { getTrackBySlug } from '@/data/courses.config';
import FellowshipTrackTemplate from '@/components/courses/FellowshipTrackTemplate';

export const metadata = pageMetadata('/learners/courses/python-automation');

export default function PythonAutomationCoursePage() {
  const track = getTrackBySlug('python-automation');
  if (!track) notFound();
  return <FellowshipTrackTemplate track={track} />;
}
