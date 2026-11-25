import type { Metadata } from 'next';
import {
  GEO_CITIES,
  GEO_SHORT_DOMAIN_LABELS,
  buildProgramCityDescription,
  buildProgramCityTitle,
} from '@/data/geo_domains.config';
import type { ProgramTierKey } from '@/components/programs/ProgramCityLanding';

const TIER_ROUTE_PREFIX: Record<ProgramTierKey, string> = {
  fellowship: '/learners/courses',
  launchpad: '/learners/launchpad',
  accelerate: '/learners/accelerate',
};

export function generateProgramCityParams() {
  const slugs = Object.keys(GEO_SHORT_DOMAIN_LABELS);
  const cities = Object.keys(GEO_CITIES);
  const params: { slug: string; city: string }[] = [];
  for (const slug of slugs) {
    for (const city of cities) {
      params.push({ slug, city });
    }
  }
  return params;
}

export function buildProgramCityMetadata(
  tier: ProgramTierKey,
  slug: string,
  city: string
): Metadata {
  if (!GEO_SHORT_DOMAIN_LABELS[slug] || !GEO_CITIES[city]) {
    return {
      title: 'Program Track Not Found',
      description: 'The requested 2-month DBERT program city track could not be found.',
    };
  }

  const title = buildProgramCityTitle(tier, slug, city);
  const description = buildProgramCityDescription(tier, slug, city);
  const canonicalUrl = `https://dbert.in${TIER_ROUTE_PREFIX[tier]}/${slug}/${city}`;

  return {
    title,
    description,
    alternates: { canonical: canonicalUrl },
    openGraph: {
      title: `${title} | DBERT`,
      description,
      url: canonicalUrl,
      type: 'website',
    },
    twitter: {
      card: 'summary',
      title: `${title} | DBERT`,
      description,
    },
  };
}
