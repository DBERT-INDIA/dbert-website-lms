import { notFound, permanentRedirect } from 'next/navigation';

interface PageProps {
  params: Promise<{ domain: string }>;
}

const CANONICAL_SLUGS = new Set([
  'ai-agent-development',
  'generative-ai',
  'machine-learning',
  'python-automation',
  'full-stack-development',
  'data-analytics',
  'ui-ux-design',
  'devops-cloud',
  'mobile-app-development',
  'cybersecurity',
  'digital-marketing',
]);

const EQUIVALENT_SLUG_REDIRECTS: Record<string, string> = {
  'data-science': 'data-analytics',
};

export default async function LegacyDomainCourseRedirectPage({ params }: PageProps) {
  const { domain } = await params;

  if (CANONICAL_SLUGS.has(domain)) {
    permanentRedirect(`/learners/courses/${domain}`);
  }

  const mapped = EQUIVALENT_SLUG_REDIRECTS[domain];
  if (mapped) {
    permanentRedirect(`/learners/courses/${mapped}`);
  }

  notFound();
}
