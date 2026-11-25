import React from 'react';
import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import ProgramCityLanding from '@/components/programs/ProgramCityLanding';
import { GEO_CITIES, GEO_SHORT_DOMAIN_LABELS } from '@/data/geo_domains.config';
import { buildProgramCityMetadata, generateProgramCityParams } from '@/lib/programCitySeo';

export async function generateStaticParams() {
  return generateProgramCityParams();
}

interface PageProps {
  params: Promise<{ slug: string; city: string }>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug, city } = await params;
  return buildProgramCityMetadata('launchpad', slug, city);
}

export default async function LaunchpadCityPage({ params }: PageProps) {
  const { slug, city } = await params;
  if (!GEO_SHORT_DOMAIN_LABELS[slug] || !GEO_CITIES[city]) {
    notFound();
  }
  return <ProgramCityLanding tier="launchpad" slug={slug} city={city} />;
}
