/**
 * Canonical Geo-Targeted Programmatic SEO Taxonomy for DBERT Internships.
 * Covers 9 technical tracks across 18 major Indian technology hubs and college corridors.
 */

export interface GeoCityMeta {
  slug: string;
  name: string;
  shortName: string;
  street: string;
  locality: string;
  region: string;
  postalCode: string;
  techCorridorFocus: string;
  campusEcosystem: string;
}

export const GEO_CITIES: Record<string, GeoCityMeta> = {
  'remote': {
    slug: 'remote',
    name: 'Remote / Work From Home',
    shortName: 'Remote',
    street: 'Cloud Sandbox Hub',
    locality: 'Pan-India',
    region: 'India',
    postalCode: '110001',
    techCorridorFocus: 'Async-first distributed GitHub PR workflows supporting candidates across Tier-1, Tier-2, and Tier-3 campuses nationwide.',
    campusEcosystem: 'Pan-India virtual mentorship pods with weekly live code review office hours and remote capstone defense.'
  },
  'bengaluru': {
    slug: 'bengaluru',
    name: 'Bengaluru',
    shortName: 'Bengaluru',
    street: 'Outer Ring Road, Manyata Tech Park',
    locality: 'Bengaluru',
    region: 'Karnataka',
    postalCode: '560001',
    techCorridorFocus: 'Tailored to ORR, Koramangala, Indiranagar, and HSR SaaS, AI agent, and FinTech engineering hiring bars.',
    campusEcosystem: 'Built for VTU, RVCE, BMSCE, PES, and Bengaluru engineering graduates targeting venture-backed startups.'
  },
  'delhi-ncr': {
    slug: 'delhi-ncr',
    name: 'Delhi NCR',
    shortName: 'Delhi NCR',
    street: 'Connaught Place / Barakhamba Road',
    locality: 'Delhi NCR',
    region: 'Delhi',
    postalCode: '110001',
    techCorridorFocus: 'Aligned with D2C SaaS, enterprise EdTech, and GovTech/AI deployments across New Delhi and NCR.',
    campusEcosystem: 'Serving DTU, NSUT, IIIT-D, IP University, and DU STEM cohorts seeking audited production repos.'
  },
  'mumbai': {
    slug: 'mumbai',
    name: 'Mumbai',
    shortName: 'Mumbai',
    street: 'Bandra Kurla Complex (BKC)',
    locality: 'Mumbai',
    region: 'Maharashtra',
    postalCode: '400051',
    techCorridorFocus: 'Focused on BKC, Lower Parel, and Powai FinTech, quantitative analytics, and enterprise automation stacks.',
    campusEcosystem: 'Supporting Mumbai University, VJTI, SPIT, and NMIMS students building verifiable market & BI portfolios.'
  },
  'pune': {
    slug: 'pune',
    name: 'Pune',
    shortName: 'Pune',
    street: 'Hinjawadi Rajiv Gandhi Infotech Park',
    locality: 'Pune',
    region: 'Maharashtra',
    postalCode: '411057',
    techCorridorFocus: 'Mapped to Hinjawadi, Kharadi, and Baner SaaS product teams, cloud automation, and B2B engineering pipelines.',
    campusEcosystem: 'Designed for COEP, PICT, VIT Pune, and SPPU learners transitioning from coursework to reviewed pull requests.'
  },
  'hyderabad': {
    slug: 'hyderabad',
    name: 'Hyderabad',
    shortName: 'Hyderabad',
    street: 'HITEC City, Madhapur',
    locality: 'Hyderabad',
    region: 'Telangana',
    postalCode: '500081',
    techCorridorFocus: 'Geared toward HITEC City, Gachibowli, and Financial District cloud data platforms and GCC AI teams.',
    campusEcosystem: 'Built around JNTUH, Osmania, CBIT, and IIIT-H student builders shipping SQL, LLM, and Full Stack modules.'
  },
  'chennai': {
    slug: 'chennai',
    name: 'Chennai',
    shortName: 'Chennai',
    street: 'Old Mahabalipuram Rd, Tech Corridor',
    locality: 'Chennai',
    region: 'Tamil Nadu',
    postalCode: '600001',
    techCorridorFocus: 'Tuned for OMR & Taramani B2B SaaS unicorns, enterprise analytics, and secure API backend reliability.',
    campusEcosystem: 'Supporting Anna University, CEG, SRM, VIT Chennai, and SSN engineers preparing for technical code audits.'
  },
  'kolkata': {
    slug: 'kolkata',
    name: 'Kolkata',
    shortName: 'Kolkata',
    street: 'Sector V, Salt Lake City',
    locality: 'Kolkata',
    region: 'West Bengal',
    postalCode: '700091',
    techCorridorFocus: 'Connected to Salt Lake Sector V and New Town software delivery centers and remote AI consulting squads.',
    campusEcosystem: 'Helping Jadavpur University, IEM, Heritage, and MAKAUT students gain national startup production experience.'
  },
  'ahmedabad': {
    slug: 'ahmedabad',
    name: 'Ahmedabad',
    shortName: 'Ahmedabad',
    street: 'SG Highway, Prahlad Nagar',
    locality: 'Ahmedabad',
    region: 'Gujarat',
    postalCode: '380015',
    techCorridorFocus: 'Aligned with SG Highway and GIFT City fintech analytics, e-commerce automation, and cloud engineering.',
    campusEcosystem: 'Built for Nirma, DAIICT, LDCE, and Gujarat Technological University learners building verified portfolios.'
  },
  'jaipur': {
    slug: 'jaipur',
    name: 'Jaipur',
    shortName: 'Jaipur',
    street: 'Malviya Nagar Industrial Area',
    locality: 'Jaipur',
    region: 'Rajasthan',
    postalCode: '302017',
    techCorridorFocus: 'Tailored to Sitapura/Malviya Nagar D2C software agencies, Shopify/SaaS APIs, and remote analyst roles.',
    campusEcosystem: 'Serving MNIT, JECRC, SKIT, and Rajasthan university students seeking national client repository proof.'
  },
  'lucknow': {
    slug: 'lucknow',
    name: 'Lucknow',
    shortName: 'Lucknow',
    street: 'Vibhuti Khand, Gomti Nagar',
    locality: 'Lucknow',
    region: 'Uttar Pradesh',
    postalCode: '226010',
    techCorridorFocus: 'Focused on Gomti Nagar IT City startups, Python workflow automation, and MSME digital product stacks.',
    campusEcosystem: 'Empowering AKTU, IET Lucknow, and Babu Banarasi Das students with verified 2-month engineering credentials.'
  },
  'chandigarh': {
    slug: 'chandigarh',
    name: 'Chandigarh',
    shortName: 'Chandigarh',
    street: 'Rajiv Gandhi Chandigarh Technology Park',
    locality: 'Chandigarh',
    region: 'Chandigarh',
    postalCode: '160019',
    techCorridorFocus: 'Mapped to Chandigarh IT Park & Mohali product engineering teams in React/Next.js, Python, and DevOps.',
    campusEcosystem: 'Designed for PEC, UIET Panjab University, Chandigarh University, and Chitkara builders shipping live PRs.'
  },
  'indore': {
    slug: 'indore',
    name: 'Indore',
    shortName: 'Indore',
    street: 'Crystal IT Park, Ring Road',
    locality: 'Indore',
    region: 'Madhya Pradesh',
    postalCode: '452001',
    techCorridorFocus: 'Connected with Crystal IT Park & Super Corridor product startups building SaaS dashboards and mobile apps.',
    campusEcosystem: 'Serving SGSITS, IET DAVV, Medicaps, and Indore developers competing for remote high-growth roles.'
  },
  'coimbatore': {
    slug: 'coimbatore',
    name: 'Coimbatore',
    shortName: 'Coimbatore',
    street: 'TIDEL Park, Civil Aerodrome Post',
    locality: 'Coimbatore',
    region: 'Tamil Nadu',
    postalCode: '641014',
    techCorridorFocus: 'Aligned with TIDEL Park Coimbatore SaaS & industrial automation engineering teams.',
    campusEcosystem: 'Supporting PSG Tech, CIT, Amrita, and Kumaraguru cohorts entering applied AI, SQL, and cloud engineering.'
  },
  'kochi': {
    slug: 'kochi',
    name: 'Kochi',
    shortName: 'Kochi',
    street: 'Infopark, Kakkanad',
    locality: 'Kochi',
    region: 'Kerala',
    postalCode: '682030',
    techCorridorFocus: 'Built for Infopark Kakkanad cloud-native web apps, Flutter mobile squads, and cybersecurity audits.',
    campusEcosystem: 'Serving CUSAT, Model Engineering College, and KTU builders shipping reviewed repositories.'
  },
  'bhubaneswar': {
    slug: 'bhubaneswar',
    name: 'Bhubaneswar',
    shortName: 'Bhubaneswar',
    street: 'Infocity, Chandaka Industrial Estate',
    locality: 'Bhubaneswar',
    region: 'Odisha',
    postalCode: '751024',
    techCorridorFocus: 'Tuned for Infocity Bhubaneswar enterprise IT modernization, Data Analytics, and backend microservices.',
    campusEcosystem: 'Supporting NIT Rourkela corridor, CET/OUTR, KIIT, and SOA students with Turnitin-audited credentials.'
  },
  'noida': {
    slug: 'noida',
    name: 'Noida',
    shortName: 'Noida',
    street: 'Sector 62, Electronic City',
    locality: 'Noida',
    region: 'Uttar Pradesh',
    postalCode: '201301',
    techCorridorFocus: 'Focused on Sector 62/125 & Expressway SaaS, GenAI chatbots, high-concurrency Node/FastAPI backends.',
    campusEcosystem: 'Built for JIIT, Amity, Galgotias, GL Bajaj, and AKTU NCR learners aiming at top product teams.'
  },
  'gurgaon': {
    slug: 'gurgaon',
    name: 'Gurgaon',
    shortName: 'Gurgaon',
    street: 'DLF Cyber City, Sector 24',
    locality: 'Gurugram',
    region: 'Haryana',
    postalCode: '122002',
    techCorridorFocus: 'Calibrated to Cyber City & Udyog Vihar FinTech, logistics BI, AI agent tooling, and enterprise cloud teams.',
    campusEcosystem: 'Supporting Ashoka, NorthCap, BML Munjal, and Delhi NCR grads with measurable PR & rubric dossiers.'
  },
};

export interface GeoRoleMeta {
  slug: string;
  title: string;
  skills: string[];
  placement: string;
  desc: string;
}

export const GEO_ROLES: Record<string, GeoRoleMeta> = {
  'full-stack-development': {
    slug: 'full-stack-development',
    title: 'Full Stack Web Development',
    skills: ['Next.js App Router', 'React 19', 'TypeScript', 'Node.js', 'PostgreSQL', 'Tailwind CSS'],
    placement: '100% Guaranteed Production Internship with Dedicated Placement Assistance',
    desc: 'Build full-stack web architectures, implement pgvector similarity search, and deploy production microservices with active users.'
  },
  'ai-agent-development': {
    slug: 'ai-agent-development',
    title: 'AI Agent & LLM Systems',
    skills: ['LangGraph', 'CrewAI', 'Ollama', 'vLLM', 'Python', 'FastAPI', 'RAG'],
    placement: '100% Guaranteed Production Internship with Dedicated Placement Assistance',
    desc: 'Construct autonomous agent state machines, tool-calling execution loops, and local open-weights foundation model deployments.'
  },
  'data-analytics': {
    slug: 'data-analytics',
    title: 'Data Analytics & Corporate BI',
    skills: ['SQL', 'Python Pandas', 'Power BI', 'Metabase', 'Data Modeling', 'ETL'],
    placement: '100% Guaranteed Production Internship with Dedicated Placement Assistance',
    desc: 'Transform raw corporate transaction records into structured analytical databases, variance decompositions, and executive BI dashboards.'
  },
  'python-automation': {
    slug: 'python-automation',
    title: 'Python Automation & Scraping',
    skills: ['Playwright', 'Scrapy', 'Celery', 'Redis', 'Python Async', 'PostgreSQL'],
    placement: '100% Guaranteed Production Internship with Dedicated Placement Assistance',
    desc: 'Deploy resilient web extraction pipelines, headless browser testing harnesses, and automated data synchronization workflows.'
  },
  'devops-cloud': {
    slug: 'devops-cloud',
    title: 'DevOps & Cloud Engineering',
    skills: ['Docker', 'Kubernetes', 'AWS EC2', 'GitHub Actions', 'Terraform', 'CI/CD'],
    placement: '100% Guaranteed Production Internship with Dedicated Placement Assistance',
    desc: 'Architect containerized clusters, automated CI/CD deployment pipelines, and secure cloud networking environments.'
  },
  'ui-ux-design': {
    slug: 'ui-ux-design',
    title: 'UI/UX Design & Prototyping',
    skills: ['Figma', 'Auto-Layout', 'Design Systems', 'User Research', 'Wireframing'],
    placement: '100% Guaranteed Production Internship with Dedicated Placement Assistance',
    desc: 'Design component tokens, user journey flows, and high-fidelity interactive product prototypes for venture applications.'
  },
  'cybersecurity': {
    slug: 'cybersecurity',
    title: 'Cybersecurity & Threat Defense',
    skills: ['OWASP Top 10', 'Wireshark', 'Burp Suite', 'SIEM Logs', 'SOC Analysis', 'Linux'],
    placement: '100% Guaranteed Production Internship with Dedicated Placement Assistance',
    desc: 'Audit web applications for injection vulnerabilities, analyze network packet captures, and harden infrastructure against intrusion.'
  },
  'mobile-app-development': {
    slug: 'mobile-app-development',
    title: 'Mobile App Development',
    skills: ['Flutter', 'Dart', 'React Native', 'Mobile APIs', 'Offline SQLite', 'State Management'],
    placement: '100% Guaranteed Production Internship with Dedicated Placement Assistance',
    desc: 'Build cross-platform iOS and Android applications connected to cloud backends with offline local caching.'
  },
  'machine-learning': {
    slug: 'machine-learning',
    title: 'Machine Learning & Generative AI',
    skills: ['PyTorch', 'Transformers', 'LoRA / QLoRA', 'LangChain', 'FastAPI', 'RAG'],
    placement: '100% Guaranteed Production Internship with Dedicated Placement Assistance',
    desc: 'Fine-tune open-weights LLMs, construct production RAG vector pipelines, and deploy low-latency inference endpoints.'
  },
  'digital-marketing': {
    slug: 'digital-marketing',
    title: 'Digital Marketing & Growth',
    skills: ['Technical SEO', 'Google Analytics 4', 'Meta Ads', 'CRO', 'Content Marketing'],
    placement: '100% Guaranteed Production Internship with Dedicated Placement Assistance',
    desc: 'Optimize organic search acquisition, analyze conversion funnels, and manage targeted growth campaigns across digital channels.'
  },
  'generative-ai': {
    slug: 'generative-ai',
    title: 'Generative AI & LLM Systems',
    skills: ['PyTorch', 'Hybrid RAG', 'pgvector', 'vLLM', 'Ollama', 'FastAPI'],
    placement: '100% Guaranteed Production Internship with Dedicated Placement Assistance',
    desc: 'Build evaluated LLM applications using document ingestion, hybrid BM25 + vector retrieval, cross-encoder reranking, and streaming inference.'
  }
};

export const GEO_SHORT_DOMAIN_LABELS: Record<string, string> = {
  'full-stack-development': 'Full Stack',
  'ai-agent-development': 'AI Agent',
  'data-analytics': 'Data Analytics',
  'python-automation': 'Python Automation',
  'devops-cloud': 'DevOps & Cloud',
  'ui-ux-design': 'UI/UX Design',
  'cybersecurity': 'Cybersecurity',
  'mobile-app-development': 'Mobile App',
  'machine-learning': 'Machine Learning',
  'digital-marketing': 'Digital Marketing',
  'generative-ai': 'Generative AI',
};

export function generateCityHeadline(role?: string, city?: string): string {
  const r = role || 'Engineering & AI';
  const c = city || 'Pan-India';
  return `${r} in ${c} — 2-Month Production Track & Placement Assistance`;
}

export function buildGeoInternshipTitle(roleSlug: string, citySlug: string): string {
  const roleShort = GEO_SHORT_DOMAIN_LABELS[roleSlug] || GEO_ROLES[roleSlug]?.title || 'AI Engineering';
  const cityShort = GEO_CITIES[citySlug]?.shortName || 'India';
  const withYear = `${roleShort} Internship in ${cityShort} (2027)`;
  if (withYear.length <= 52) return withYear;
  return `${roleShort} Internship in ${cityShort}`.slice(0, 52).trim();
}

export function buildGeoInternshipDescription(roleSlug: string, citySlug: string): string {
  const roleTitle = GEO_ROLES[roleSlug]?.title || 'AI & Software Engineering';
  const cityShort = GEO_CITIES[citySlug]?.shortName || 'India';
  const candidate = `Apply for DBERT ${roleTitle} 2-month internship in ${cityShort}. Ship live client PRs with 1:1 mentor reviews and verified MSME credentials.`;
  if (candidate.length >= 140 && candidate.length <= 155) return candidate;
  if (candidate.length > 155) {
    const shorter = `Apply for ${GEO_SHORT_DOMAIN_LABELS[roleSlug] || roleTitle} 2-month internship in ${cityShort}. Ship production client PRs with 1:1 mentor code reviews and verified MSME credentials.`;
    return shorter.length > 155 ? shorter.slice(0, 152).trimEnd() + '...' : shorter;
  }
  return `${candidate} Guaranteed placement support included.`.slice(0, 155);
}

export function buildProgramCityTitle(
  tier: 'fellowship' | 'launchpad' | 'accelerate',
  domainSlug: string,
  citySlug: string
): string {
  const domainShort = GEO_SHORT_DOMAIN_LABELS[domainSlug] || domainSlug;
  const cityShort = GEO_CITIES[citySlug]?.shortName || 'India';
  const label = tier === 'launchpad' ? 'Launchpad' : tier === 'accelerate' ? 'Accelerate' : 'Course';
  const fee = tier === 'launchpad' ? '₹7,999' : tier === 'accelerate' ? '₹4,999' : '₹1,999';
  const candidate = `${domainShort} ${label} in ${cityShort} (${fee})`;
  if (candidate.length <= 52) return candidate;
  const compact = `${domainShort} ${label} ${cityShort} (${fee})`;
  return compact.length <= 52 ? compact : `${domainShort} ${label} in ${cityShort}`.slice(0, 52).trim();
}

export function buildProgramCityDescription(
  tier: 'fellowship' | 'launchpad' | 'accelerate',
  domainSlug: string,
  citySlug: string
): string {
  const domainShort = GEO_SHORT_DOMAIN_LABELS[domainSlug] || domainSlug;
  const cityShort = GEO_CITIES[citySlug]?.shortName || 'India';
  const fee = tier === 'launchpad' ? '₹7,999' : tier === 'accelerate' ? '₹4,999' : '₹1,999';
  const modeNote =
    tier === 'launchpad'
      ? '0-to-1 beginner foundations, Git & coding labs'
      : tier === 'accelerate'
      ? 'applied industrial sprints & senior PR reviews'
      : 'live client GitHub repos, 1:1 reviews & verified cert';
  const base = `Join DBERT 2-month ${domainShort} program in ${cityShort} (${fee}): ${modeNote}. Remote cohorts with verified outcomes.`;
  if (base.length >= 140 && base.length <= 155) return base;
  if (base.length > 155) {
    const trimmed = `Join 2-month ${domainShort} track in ${cityShort} (${fee}): ${modeNote}. Verified MSME outcomes and mentor guidance.`;
    if (trimmed.length >= 140 && trimmed.length <= 155) return trimmed;
    if (trimmed.length > 155) return trimmed.slice(0, 152).trimEnd() + '...';
    return (trimmed + ' Apply online now.').slice(0, 155);
  }
  const padded = `${base} Apply online for 2027 batches.`;
  return padded.length > 155 ? padded.slice(0, 155).trimEnd() : padded;
}

export function getAllGeoInternshipRoutes(): string[] {
  const routes: string[] = [];
  for (const role of Object.keys(GEO_ROLES)) {
    for (const city of Object.keys(GEO_CITIES)) {
      routes.push(`/internships/${role}/${city}`);
    }
  }
  return routes;
}

export function getAllProgramCityRoutes(): string[] {
  const domainSlugs = Object.keys(GEO_SHORT_DOMAIN_LABELS);
  const citySlugs = Object.keys(GEO_CITIES);
  const prefixes = ['/learners/courses', '/learners/launchpad', '/learners/accelerate'];
  const routes: string[] = [];
  for (const prefix of prefixes) {
    for (const slug of domainSlugs) {
      for (const city of citySlugs) {
        routes.push(`${prefix}/${slug}/${city}`);
      }
    }
  }
  return routes;
}
