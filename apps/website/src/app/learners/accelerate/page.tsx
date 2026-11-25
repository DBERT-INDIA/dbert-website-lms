import { pageMetadata } from '@/lib/seo';
import AccelerateDomainView from '@/components/accelerate/AccelerateDomainView';

export const metadata = pageMetadata('/learners/accelerate');

export default function AccelerateProgramPage() {
  return <AccelerateDomainView />;
}
