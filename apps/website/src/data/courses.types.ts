export type TrackStatus = 'published' | 'draft' | 'archived';

export interface CurriculumModule {
  period: string;
  title: string;
  topics: string[];
  deliverable: string;
}

export interface TechnologyItem {
  name: string;
  role: string;
}

export interface CapstoneSpec {
  title: string;
  description: string;
  status: 'active' | 'proposed';
  ventureName: string;
  repositoryUrl?: string;
  acceptanceCriteria: string[];
}

export interface TrackFaq {
  question: string;
  answer: string;
}

export interface RegionalOpportunity {
  title: string;
  roleDescription: string;
  cityTag: string;
  location: string;
  placement: string;
  href: string;
  tags: string[];
}

export interface FellowshipTrack {
  id: string;
  slug: string;
  canonicalPath: string;
  name: string;
  shortName: string;
  badge: string;
  category: 'AI & Data' | 'Software & Cloud' | 'Product & Growth';
  featured: boolean;
  displayOrder: number;
  status: TrackStatus;
  duration: string;
  weeklyCommitment: string;
  heroOutcome: string;
  shortDescription: string;
  fullDescription: string;
  whoShouldApply: string[];
  prerequisites: string[];
  outcomes: string[];
  technologies: TechnologyItem[];
  curriculum: CurriculumModule[];
  capstone: CapstoneSpec;
  evaluation: string[];
  faqs: TrackFaq[];
  relatedSlugs: string[];
  regionalOpportunities: RegionalOpportunity[];
}
