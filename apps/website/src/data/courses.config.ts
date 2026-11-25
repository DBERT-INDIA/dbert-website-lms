import { PRICING_CONFIG, formatINR } from '@/config/pricing.config';
import type { FellowshipTrack } from './courses.types';
import { CORE_FELLOWSHIP_TRACKS } from './courses.core';
import { SPECIALIZED_FELLOWSHIP_TRACKS } from './courses.specialized';

export type { FellowshipTrack, CurriculumModule, TechnologyItem, CapstoneSpec, TrackFaq, RegionalOpportunity } from './courses.types';

export const FELLOWSHIP_FEE = {
  amount: PRICING_CONFIG.totalProgramFee,
  cautionDeposit: PRICING_CONFIG.cautionDeposit,
  balancePayable: PRICING_CONFIG.balancePayable,
  currency: 'INR' as const,
  formattedTotal: formatINR(PRICING_CONFIG.totalProgramFee),
  formattedDeposit: formatINR(PRICING_CONFIG.cautionDeposit),
  formattedBalance: formatINR(PRICING_CONFIG.balancePayable),
  label: 'Total 2-month fellowship program fee (includes mentorship, PR reviews, active repo assignment & 3-document credential packet).',
};

export const ALL_FELLOWSHIP_TRACKS: FellowshipTrack[] = [
  ...CORE_FELLOWSHIP_TRACKS,
  ...SPECIALIZED_FELLOWSHIP_TRACKS,
].sort((a, b) => a.displayOrder - b.displayOrder);

export function getPublishedTracks(): FellowshipTrack[] {
  return ALL_FELLOWSHIP_TRACKS.filter((t) => t.status === 'published');
}

export function getFeaturedTracks(): FellowshipTrack[] {
  return getPublishedTracks().filter((t) => t.featured);
}

export function getTrackBySlug(slug: string): FellowshipTrack | undefined {
  return ALL_FELLOWSHIP_TRACKS.find((t) => t.slug === slug && t.status === 'published');
}

export function getRelatedTracks(track: FellowshipTrack): FellowshipTrack[] {
  return track.relatedSlugs
    .map((slug) => getTrackBySlug(slug))
    .filter((t): t is FellowshipTrack => Boolean(t));
}

/**
 * Runtime/test integrity validator to prevent duplicate IDs, duplicate slugs,
 * invalid canonical paths, or missing required fields.
 */
export function validateCatalogueIntegrity(tracks: FellowshipTrack[] = ALL_FELLOWSHIP_TRACKS): string[] {
  const errors: string[] = [];
  const seenIds = new Set<string>();
  const seenSlugs = new Set<string>();

  for (const track of tracks) {
    if (!track.id || !track.slug || !track.name) {
      errors.push(`Track missing required id/slug/name: ${JSON.stringify(track.id || track.slug)}`);
    }
    if (seenIds.has(track.id)) {
      errors.push(`Duplicate track id: ${track.id}`);
    }
    seenIds.add(track.id);

    if (seenSlugs.has(track.slug)) {
      errors.push(`Duplicate track slug: ${track.slug}`);
    }
    seenSlugs.add(track.slug);

    if (track.canonicalPath !== `/learners/courses/${track.slug}`) {
      errors.push(`Invalid canonicalPath for ${track.slug}: ${track.canonicalPath}`);
    }
    if (!track.curriculum.length) {
      errors.push(`Track ${track.slug} has empty curriculum`);
    }
    if (!track.faqs.length) {
      errors.push(`Track ${track.slug} has empty FAQs`);
    }
  }

  return errors;
}
