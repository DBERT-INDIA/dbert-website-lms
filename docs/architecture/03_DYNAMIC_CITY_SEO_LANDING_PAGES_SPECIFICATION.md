# Dynamic City SEO Landing Pages & Programmatic Geotargeting Specification
================================================================================
**Document ID**: `DBERT-SPEC-ARCH-003`  
**Requirement Mapping**: Requirement R3 (Dynamic City-Targeted Landing Page & Programmatic SEO Strategy)  
**System Targets**: `apps/website` (Next.js 16 App Router, Turbopack Standalone), `apps/portal` (Flask LMS & PostgreSQL), `scripts/check-seo.mjs`  
**Sovereign Domain Mandate**: Strictly `https://dbert.in` (Never `dbert.online`)  
**Google Analytics 4 Measurement ID**: `G-MN7ME9X518`  
**Status**: PRODUCTION-READY ARCHITECTURAL SPECIFICATION  

---

## Executive Summary & Architectural Tenets

This specification defines the complete production architecture for DBERT's **Dynamic City-Targeted Landing Pages and Programmatic SEO Engine (Requirement R3)**. Designed to capture high-intent regional student, graduate, and employer traffic across India and global remote tech hubs, this subsystem establishes:

1. **A Canonical 20-City Geographical Taxonomy**: 15 premier Indian tech capitals and emerging regional engineering centers, plus 5 international remote corridors. Each city profile is modeled with deep localized attributes: physical postal addresses, postal codes, landmark tech parks, top engineering colleges, prominent employers, and localized stipend/salary benchmarks.
2. **Next.js 16 App Router Programmatic Route Architecture**: Complete dynamic route templates (`/internships/[role]/[city]`, `/internships/[city]`, and `/learners/courses/[domain]/[city]`). Employs asynchronous params (`params: Promise<{ role: string; city: string }>`) natively supported in Next.js 16, backed by `generateStaticParams()` pre-rendering 180+ static routes at build time, and on-demand SSR fallback (`dynamicParams = true`).
3. **Strictly Bounded Programmatic Metadata Generation**: Mathematically bounded dynamic `generateMetadata()` algorithm ensuring title lengths $\le 52$ characters before suffix ($\le 60$ with ` | DBERT`), and meta descriptions strictly bounded between **140 and 155 characters** to eliminate SERP truncation and pass CI SEO gates.
4. **Localized Content Injection Engine**: Dynamic insertion of rich regional context (commute hubs, IT corridors, university talent pipelines, and regional salary benchmarks) to eliminate Google doorway page penalties and deliver authentic, localized user experiences.
5. **Infallible 3-Tier Job Query Fallback Engine**: A hierarchical resolution algorithm (*1. Exact City Match* $\rightarrow$ *2. Regional Cluster Match* $\rightarrow$ *3. Universal Remote Backfill*) guaranteeing a **0% empty-state rate** across all regional search queries.
6. **Programmatic Sitemaps, Robots & CI SEO Gates**: Native integration with Next.js dynamic `sitemap.ts`, `robots.ts` crawler directives, and CI validation gate integration with `apps/website/scripts/check-seo.mjs`.

---

## 1. Complete City Catalog & Geographical Taxonomy

### 1.1 Geographical Data Models & TypeScript Interfaces

The geographical catalog is codified in `apps/website/src/data/geo_catalog.config.ts` using strongly typed TypeScript interfaces:

```typescript
// apps/website/src/data/geo_catalog.config.ts

export type CityTier = 'Tier-1 Metro' | 'Tier-2 Emerging' | 'Global Remote';
export type SupportedCountryCode = 'IN' | 'SG' | 'AE' | 'UK' | 'US';

export interface SalaryBenchmarks {
  internStipendMonthly: string;      // e.g. "₹5,000 – ₹18,000" or "SGD 1,200 – SGD 2,800"
  juniorEngineerLpa: string;         // e.g. "₹6,50,000 – ₹14,00,000"
  seniorEngineerLpa: string;         // e.g. "₹18,00,000 – ₹38,00,000"
  currencySymbol: string;            // "₹", "SGD ", "AED ", "£", "$"
}

export interface CityTechEcosystem {
  slug: string;
  name: string;
  altNames: string[];
  region: string;                    // State / Administrative Territory
  stateOrProvince: string;
  country: string;
  countryCode: SupportedCountryCode;
  postalCode: string;
  streetAddress: string;
  locality: string;
  tier: CityTier;
  techParks: string[];
  localColleges: string[];
  prominentHiringCompanies: string[];
  primaryEcosystemFocus: string[];
  salaryBenchmarks: SalaryBenchmarks;
  livingAndCommuteContext: string;
  regionalTransitNotes: string;
  telecommuteEligible: boolean;
}

export interface GeoRoleMeta {
  slug: string;
  title: string;
  shortTitle: string;
  skills: string[];
  stipend: string;
  desc: string;
  primaryFrameworks: string[];
}
```

---

### 1.2 Comprehensive 20-City Profile Registry

The catalog covers **15 Indian Technology Hubs** and **5 Global Remote Corridors**:

```typescript
// apps/website/src/data/geo_catalog.config.ts (Continued)

export const GEO_CATALOG: Record<string, CityTechEcosystem> = {
  // =========================================================================
  // 1. TIER-1 INDIAN METROPOLITAN TECH CAPITALS
  // =========================================================================
  'bengaluru': {
    slug: 'bengaluru',
    name: 'Bengaluru',
    altNames: ['Bangalore', 'Silicon Valley of India'],
    region: 'Karnataka',
    stateOrProvince: 'Karnataka',
    country: 'India',
    countryCode: 'IN',
    postalCode: '560045',
    streetAddress: 'Outer Ring Road, Manyata Embassy Business Park',
    locality: 'Hebbal / Marathahalli Tech Corridor',
    tier: 'Tier-1 Metro',
    techParks: [
      'Manyata Embassy Business Park',
      'Electronic City Phase 1 & 2',
      'International Tech Park Bangalore (ITPL) Whitefield',
      'Bagmane Tech Park CV Raman Nagar',
      'Ecospace Business Park Bellandur'
    ],
    localColleges: [
      'Indian Institute of Science (IISc)',
      'RV College of Engineering (RVCE)',
      'PES University (Ring Road Campus)',
      'BMS College of Engineering',
      'M.S. Ramaiah Institute of Technology (MSRIT)',
      'International Institute of Information Technology (IIIT Bangalore)'
    ],
    prominentHiringCompanies: [
      'Flipkart',
      'Swiggy',
      'Razorpay',
      'Zerodha',
      'PhonePe',
      'Infosys',
      'Wipro',
      'DBERT Venture Squads'
    ],
    primaryEcosystemFocus: [
      'Autonomous AI Agents & LLM Infrastructure',
      'B2B SaaS Engineering',
      'FinTech Platform Architecture',
      'Distributed High-Concurrency Microservices'
    ],
    salaryBenchmarks: {
      internStipendMonthly: '₹8,000 – ₹25,000',
      juniorEngineerLpa: '₹7,00,000 – ₹15,00,000',
      seniorEngineerLpa: '₹22,00,000 – ₹45,00,000',
      currencySymbol: '₹'
    },
    livingAndCommuteContext: 'India’s premier AI startup capital with the highest density of venture-backed engineering teams, weekly hackathons, and high-performance product squads concentrated along Outer Ring Road and Koramangala.',
    regionalTransitNotes: 'Purple and Green Namma Metro lines provide high-speed connectivity across major residential catchment areas directly into key IT corridors.',
    telecommuteEligible: true
  },

  'hyderabad': {
    slug: 'hyderabad',
    name: 'Hyderabad',
    altNames: ['Cyberabad', 'Hyderabad-Secunderabad'],
    region: 'Telangana',
    stateOrProvince: 'Telangana',
    country: 'India',
    countryCode: 'IN',
    postalCode: '500081',
    streetAddress: 'HITEC City, Mindspace Madhapur',
    locality: 'HITEC City & Gachibowli Financial District',
    tier: 'Tier-1 Metro',
    techParks: [
      'HITEC City Madhapur',
      'Raheja Mindspace IT Park',
      'Financial District Gachibowli',
      'T-Hub 2.0 Innovation Complex',
      'Knowledge City Silpa Gram Craft Village'
    ],
    localColleges: [
      'IIIT Hyderabad',
      'IIT Hyderabad (Kandi)',
      'Osmania University College of Engineering (OUCE)',
      'Chaitanya Bharathi Institute of Technology (CBIT)',
      'JNTU Hyderabad College of Engineering',
      'VNR Vignana Jyothi Institute of Engineering (VNR VJIET)'
    ],
    prominentHiringCompanies: [
      'Microsoft India Development Center (IDC)',
      'Google Hyderabad',
      'Amazon Development Centre India',
      'Qualcomm India',
      'ServiceNow',
      'Darwinbox'
    ],
    primaryEcosystemFocus: [
      'Computer Vision & Multimodal Deep Learning',
      'Enterprise Cloud Platforms',
      'Semiconductor Firmware & VLSI Systems',
      'Scalable Web Services'
    ],
    salaryBenchmarks: {
      internStipendMonthly: '₹6,000 – ₹22,000',
      juniorEngineerLpa: '₹6,00,000 – ₹13,50,000',
      seniorEngineerLpa: '₹19,00,000 – ₹38,00,000',
      currencySymbol: '₹'
    },
    livingAndCommuteContext: 'The powerhouse of enterprise engineering and computer vision research in southern India, anchored by IIIT-H research labs and the sprawling T-Hub startup incubator.',
    regionalTransitNotes: 'Hyderabad Metro Blue Line connects Ameerpet, Miyapur, and Secunderabad directly into Raidurg and HITEC City terminals.',
    telecommuteEligible: true
  },

  'pune': {
    slug: 'pune',
    name: 'Pune',
    altNames: ['Oxford of the East', 'Poona'],
    region: 'Maharashtra',
    stateOrProvince: 'Maharashtra',
    country: 'India',
    countryCode: 'IN',
    postalCode: '411057',
    streetAddress: 'Rajiv Gandhi Infotech Park, Hinjawadi Phase 1',
    locality: 'Hinjawadi & Kharadi IT Corridors',
    tier: 'Tier-1 Metro',
    techParks: [
      'Rajiv Gandhi Infotech Park (Hinjawadi Phases 1, 2 & 3)',
      'Magarpatta Cybercity Hadapsar',
      'EON Free Zone IT Park Kharadi',
      'Commerzone Yerwada',
      'Panchshil Tech Park Viman Nagar'
    ],
    localColleges: [
      'College of Engineering Pune (COEP Technological University)',
      'Pune Institute of Computer Technology (PICT)',
      'MIT World Peace University (MIT-WPU)',
      'Vishwakarma Institute of Technology (VIT Pune)',
      'Symbiosis Institute of Technology (SIT)',
      'Army Institute of Technology (AIT)'
    ],
    prominentHiringCompanies: [
      'Persistent Systems',
      'Veritas Technologies',
      'Barclays Global Service Centre',
      'Tata Consultancy Services',
      'Bajaj Finserv Health',
      'PTC Software'
    ],
    primaryEcosystemFocus: [
      'Cloud Infrastructure Security',
      'Automotive Embedded & Telematics Software',
      'Core Banking Microservices',
      'Full Stack Enterprise SaaS'
    ],
    salaryBenchmarks: {
      internStipendMonthly: '₹5,000 – ₹20,000',
      juniorEngineerLpa: '₹5,50,000 – ₹12,00,000',
      seniorEngineerLpa: '₹17,00,000 – ₹34,00,000',
      currencySymbol: '₹'
    },
    livingAndCommuteContext: 'Premier engineering talent foundry combining top-ranking universities with colossal IT parks in Hinjawadi and Kharadi, providing rich engineering communities.',
    regionalTransitNotes: 'Pune Metro Line 3 expanding direct connectivity between civil court interchanges and the Hinjawadi IT SEZs.',
    telecommuteEligible: true
  },

  'mumbai': {
    slug: 'mumbai',
    name: 'Mumbai',
    altNames: ['Bombay', 'MMR (Mumbai Metropolitan Region)'],
    region: 'Maharashtra',
    stateOrProvince: 'Maharashtra',
    country: 'India',
    countryCode: 'IN',
    postalCode: '400051',
    streetAddress: 'G Block, Bandra Kurla Complex (BKC)',
    locality: 'BKC, Andheri East & Powai Tech Valley',
    tier: 'Tier-1 Metro',
    techParks: [
      'Bandra Kurla Complex (BKC) Financial District',
      'Nesco IT Park Goregaon East',
      'Mindspace Business Park Airoli & Malad',
      'Hiranandani Business Park Powai',
      'Kensington SEZ Powai'
    ],
    localColleges: [
      'Indian Institute of Technology Bombay (IIT Bombay)',
      'Veermata Jijabai Technological Institute (VJTI)',
      'Sardar Patel Institute of Technology (SPIT)',
      'Dwarkadas J. Sanghvi College of Engineering (DJSCE)',
      'Thadomal Shahani Engineering College (TSEC)'
    ],
    prominentHiringCompanies: [
      'Morgan Stanley Tech',
      'JPMorgan Chase India',
      'Reliance Jio Infocomm',
      'Tata Consultancy Services',
      'Fractal Analytics',
      'CleverTap'
    ],
    primaryEcosystemFocus: [
      'Algorithmic Trading & High-Frequency FinTech',
      'Enterprise Data Analytics & Predictive AI',
      'Scalable Telecom Architectures',
      'Full Stack Web Platforms'
    ],
    salaryBenchmarks: {
      internStipendMonthly: '₹7,000 – ₹24,000',
      juniorEngineerLpa: '₹6,50,000 – ₹14,00,000',
      seniorEngineerLpa: '₹20,00,000 – ₹42,00,000',
      currencySymbol: '₹'
    },
    livingAndCommuteContext: 'Financial and investment nerve center of India, featuring immense demand for quantitative engineers, neo-banking API developers, and low-latency systems architects.',
    regionalTransitNotes: 'Suburban rail network backed by newly inaugurated Metro Line 3 (Aqua Line) and Lines 2A/7 connecting the Western and Eastern suburbs.',
    telecommuteEligible: true
  },

  'delhi-ncr': {
    slug: 'delhi-ncr',
    name: 'Delhi NCR',
    altNames: ['National Capital Region', 'New Delhi'],
    region: 'Delhi',
    stateOrProvince: 'National Capital Territory of Delhi',
    country: 'India',
    countryCode: 'IN',
    postalCode: '110001',
    streetAddress: 'Barakhamba Road, Connaught Place',
    locality: 'Central Delhi & Okhla Industrial Area',
    tier: 'Tier-1 Metro',
    techParks: [
      'Okhla Industrial Area Phases 1, 2 & 3',
      'Netaji Subhash Place IT Hub',
      'Jasola District Centre',
      'Mohan Cooperative Industrial Estate'
    ],
    localColleges: [
      'Indian Institute of Technology Delhi (IIT Delhi)',
      'Delhi Technological University (DTU)',
      'Netaji Subhas University of Technology (NSUT)',
      'Indraprastha Institute of Information Technology Delhi (IIIT-Delhi)',
      'Jamia Millia Islamia Faculty of Engineering'
    ],
    prominentHiringCompanies: [
      'Zomato',
      'Paytm One97',
      'MakeMyTrip',
      'Urban Company',
      'Lenskart',
      'PhysicsWallah'
    ],
    primaryEcosystemFocus: [
      'Consumer Tech & Hyperlocal Marketplaces',
      'Large Language Model Fine-Tuning',
      'EdTech Scalability',
      'Full Stack Web Applications'
    ],
    salaryBenchmarks: {
      internStipendMonthly: '₹6,000 – ₹22,000',
      juniorEngineerLpa: '₹6,00,000 – ₹13,50,000',
      seniorEngineerLpa: '₹18,00,000 – ₹38,00,000',
      currencySymbol: '₹'
    },
    livingAndCommuteContext: 'Vast metropolitan startup ecosystem fueled by top-tier talent from DTU, NSUT, and IIIT-Delhi, powering consumer unicorns and AI ventures.',
    regionalTransitNotes: 'Delhi Metro system spanning over 390 km with high-frequency Yellow, Blue, Magenta, and Violet lines connecting the entire NCR.',
    telecommuteEligible: true
  },

  'noida': {
    slug: 'noida',
    name: 'Noida',
    altNames: ['New Okhla Industrial Development Authority', 'Greater Noida'],
    region: 'Uttar Pradesh',
    stateOrProvince: 'Uttar Pradesh',
    country: 'India',
    countryCode: 'IN',
    postalCode: '201301',
    streetAddress: 'Sector 62, Electronic City',
    locality: 'Sector 62 & Noida-Greater Noida Expressway',
    tier: 'Tier-1 Metro',
    techParks: [
      'Electronic City Sector 62',
      'Advant Navis Business Park Sector 142',
      'Candor TechSpace Sector 135',
      'Oxygen Business Park Sector 144',
      'Stellar IT Park Sector 62'
    ],
    localColleges: [
      'Jaypee Institute of Information Technology (JIIT)',
      'Amity University Uttar Pradesh (Noida Campus)',
      'Shiv Nadar University (SNU Greater Noida)',
      'Galgotias College of Engineering and Technology',
      'G.L. Bajaj Institute of Technology and Management'
    ],
    prominentHiringCompanies: [
      'HCL Technologies Global HQ',
      'Samsung R&D Institute India - Noida',
      'Adobe Systems India',
      'Oracle India Noida Campus',
      'Gartner India',
      'Microsoft IDC Noida'
    ],
    primaryEcosystemFocus: [
      'Mobile App Systems & Android Internals',
      'Enterprise Cloud Infrastructure',
      'Consumer Electronics Hardware/Software Integration',
      'Modern TypeScript & Next.js Stacks'
    ],
    salaryBenchmarks: {
      internStipendMonthly: '₹5,000 – ₹20,000',
      juniorEngineerLpa: '₹5,50,000 – ₹12,00,000',
      seniorEngineerLpa: '₹16,00,000 – ₹34,00,000',
      currencySymbol: '₹'
    },
    livingAndCommuteContext: 'Spacious industrial technology corridor featuring mega campuses of multinational tech giants, wide expressways, and high developer density.',
    regionalTransitNotes: 'Delhi Metro Blue Line terminates directly at Noida Electronic City (Sector 62); Aqua Line connects Sector 51 to Greater Noida Depot.',
    telecommuteEligible: true
  },

  'gurgaon': {
    slug: 'gurgaon',
    name: 'Gurgaon',
    altNames: ['Gurugram', 'Millennium City', 'Cyber City'],
    region: 'Haryana',
    stateOrProvince: 'Haryana',
    country: 'India',
    countryCode: 'IN',
    postalCode: '122002',
    streetAddress: 'DLF Cyber City, Building 10, Sector 24',
    locality: 'Cyber City, Golf Course Road & Udyog Vihar',
    tier: 'Tier-1 Metro',
    techParks: [
      'DLF Cyber City & CyberHub',
      'Candor TechSpace Sector 21 & Sector 48',
      'Golf Course Extension Road IT SEZs',
      'Udyog Vihar Industrial & IT Zones 1-5',
      'Worldmark Gurgaon Sector 65'
    ],
    localColleges: [
      'Management Development Institute (MDI)',
      'The NorthCap University (NCU)',
      'BML Munjal University',
      'GD Goenka University School of Engineering',
      'Amity University Gurugram (Manesar)'
    ],
    prominentHiringCompanies: [
      'Google India Gurugram Campus',
      'American Express Global Tech',
      'Zomato & Blinkit Headquarters',
      'Policybazaar',
      'Oyo Rooms Tech HQ',
      'Deloitte USI'
    ],
    primaryEcosystemFocus: [
      'Enterprise SaaS Platforms',
      'FinTech Risk & Underwriting Engines',
      'Hyperlocal Supply Chain Automation',
      'AI Prompt Engineering & Evaluation'
    ],
    salaryBenchmarks: {
      internStipendMonthly: '₹7,000 – ₹25,000',
      juniorEngineerLpa: '₹6,50,000 – ₹14,50,000',
      seniorEngineerLpa: '₹20,00,000 – ₹42,00,000',
      currencySymbol: '₹'
    },
    livingAndCommuteContext: 'Corporate multinational capital of North India housing over 250 Fortune 500 development centers and leading consumer unicorns.',
    regionalTransitNotes: 'Delhi Metro Yellow Line links central Delhi directly into Sikanderpur, connecting to the Gurgaon Rapid Metro loop.',
    telecommuteEligible: true
  },

  'chennai': {
    slug: 'chennai',
    name: 'Chennai',
    altNames: ['Madras', 'SaaS Capital of India'],
    region: 'Tamil Nadu',
    stateOrProvince: 'Tamil Nadu',
    country: 'India',
    countryCode: 'IN',
    postalCode: '600113',
    streetAddress: 'Old Mahabalipuram Road (OMR), Taramani',
    locality: 'OMR IT Expressway & Guindy Industrial Estate',
    tier: 'Tier-1 Metro',
    techParks: [
      'TIDEL Park Taramani',
      'Ascendas International Tech Park Chennai',
      'Ramanujan IT City Taramani',
      'DLF Cybercity Porur',
      'SIPCOT IT Park Siruseri'
    ],
    localColleges: [
      'Indian Institute of Technology Madras (IIT Madras)',
      'College of Engineering Guindy (CEG, Anna University)',
      'Madras Institute of Technology (MIT Chromepet)',
      'SSN College of Engineering (Kalavakkam)',
      'SRM Institute of Science and Technology (Kattankulathur)',
      'Vellore Institute of Technology (VIT Chennai Campus)'
    ],
    prominentHiringCompanies: [
      'Zoho Corporation',
      'Freshworks',
      'Cognizant Technology Solutions',
      'Tata Consultancy Services',
      'PayPal India Tech Centre',
      'Ford Motor Technology'
    ],
    primaryEcosystemFocus: [
      'B2B SaaS Engineering',
      'Cybersecurity & Threat Modeling',
      'Automotive Embedded Linux',
      'High-Reliability Enterprise Backends'
    ],
    salaryBenchmarks: {
      internStipendMonthly: '₹5,000 – ₹20,000',
      juniorEngineerLpa: '₹5,20,000 – ₹11,50,000',
      seniorEngineerLpa: '₹16,00,000 – ₹32,00,000',
      currencySymbol: '₹'
    },
    livingAndCommuteContext: 'The SaaS capital of India, with home-grown global product powerhouses like Zoho and Freshworks, supported by deep engineering talent from IIT Madras and CEG.',
    regionalTransitNotes: 'OMR six-lane IT corridor combined with Chennai Suburban railway lines and Phase 2 Metro construction.',
    telecommuteEligible: true
  },

  'kolkata': {
    slug: 'kolkata',
    name: 'Kolkata',
    altNames: ['Calcutta', 'City of Joy'],
    region: 'West Bengal',
    stateOrProvince: 'West Bengal',
    country: 'India',
    countryCode: 'IN',
    postalCode: '700091',
    streetAddress: 'Sector V, Bidhannagar, Salt Lake City',
    locality: 'Sector V Salt Lake & New Town Action Area II',
    tier: 'Tier-1 Metro',
    techParks: [
      'Sector V Salt Lake IT Hub',
      'Ecospace Business Park New Town',
      'DLF IT Park 1 & 2 New Town',
      'Candor TechSpace Rajarhat',
      'Mani Casadona IT Park'
    ],
    localColleges: [
      'Jadavpur University Faculty of Engineering & Technology',
      'Indian Institute of Engineering Science and Technology (IIEST Shibpur)',
      'University of Calcutta (Rajabazar Science College)',
      'Heritage Institute of Technology',
      'Techno Main Salt Lake',
      'Institute of Engineering and Management (IEM Kolkata)'
    ],
    prominentHiringCompanies: [
      'Tata Consultancy Services (Kolkata Campuses)',
      'Wipro Technologies Salt Lake',
      'Cognizant Kolkata',
      'PwC India SDC',
      'Capgemini Kolkata',
      'IBM India'
    ],
    primaryEcosystemFocus: [
      'Enterprise Financial Microservices',
      'Corporate Data Warehousing & ETL',
      'Full Stack Application Modernization',
      'Enterprise Cloud Migration'
    ],
    salaryBenchmarks: {
      internStipendMonthly: '₹4,500 – ₹16,000',
      juniorEngineerLpa: '₹4,50,000 – ₹9,50,000',
      seniorEngineerLpa: '₹14,00,000 – ₹28,00,000',
      currencySymbol: '₹'
    },
    livingAndCommuteContext: 'Eastern India’s undisputed tech capital, featuring massive engineering output from elite state universities and low living costs for engineers.',
    regionalTransitNotes: 'Kolkata Metro Green Line directly connects Howrah and Sealdah rail terminals through to Sector V Salt Lake.',
    telecommuteEligible: true
  },

  // =========================================================================
  // 2. TIER-2 EMERGING TECH & REGIONAL CAPITAL HUBS
  // =========================================================================
  'ahmedabad': {
    slug: 'ahmedabad',
    name: 'Ahmedabad',
    altNames: ['Amdavad', 'Ahmedabad-Gandhinagar'],
    region: 'Gujarat',
    stateOrProvince: 'Gujarat',
    country: 'India',
    countryCode: 'IN',
    postalCode: '380015',
    streetAddress: 'Sarkhej - Gandhinagar Highway, Prahlad Nagar',
    locality: 'SG Highway, Prahlad Nagar & GIFT City',
    tier: 'Tier-2 Emerging',
    techParks: [
      'GIFT City Tech Zone (Gandhinagar)',
      'Infocity Gandhinagar',
      'Prahladnagar Commercial Hub',
      'Mindspace Gandhinagar IT SEZ'
    ],
    localColleges: [
      'Indian Institute of Technology Gandhinagar (IITGN)',
      'DA-IICT (Dhirubhai Ambani Institute of ICT)',
      'Nirma University Institute of Technology',
      'L.D. College of Engineering (LDCE)',
      'Pandit Deendayal Energy University (PDEU)'
    ],
    prominentHiringCompanies: [
      'Adani Digital Labs',
      'TCS Gandhinagar Campus',
      'Infostretch (Apexon)',
      'TatvaSoft',
      'eInfochips (Arrow Electronics)'
    ],
    primaryEcosystemFocus: [
      'FinTech & Cross-Border Banking in GIFT City',
      'IoT & Embedded Hardware Systems',
      'Enterprise Web & Mobile Applications',
      'Supply Chain Logistics Software'
    ],
    salaryBenchmarks: {
      internStipendMonthly: '₹4,500 – ₹18,000',
      juniorEngineerLpa: '₹4,50,000 – ₹9,50,000',
      seniorEngineerLpa: '₹14,00,000 – ₹26,00,000',
      currencySymbol: '₹'
    },
    livingAndCommuteContext: 'Rapidly emerging Western tech corridor anchored by the international financial SEZ of GIFT City and renowned ICT institutions like DA-IICT.',
    regionalTransitNotes: 'Ahmedabad-Gandhinagar Metro Phase 2 connecting Motera Stadium directly to GIFT City and Mahatma Mandir.',
    telecommuteEligible: true
  },

  'jaipur': {
    slug: 'jaipur',
    name: 'Jaipur',
    altNames: ['Pink City'],
    region: 'Rajasthan',
    stateOrProvince: 'Rajasthan',
    country: 'India',
    countryCode: 'IN',
    postalCode: '302017',
    streetAddress: 'Malviya Nagar Industrial Area',
    locality: 'Malviya Nagar, Sitapura & Mahindra World City',
    tier: 'Tier-2 Emerging',
    techParks: [
      'Mahindra World City IT SEZ',
      'Sitapura Industrial Area IT Zone',
      'World Trade Park Malviya Nagar'
    ],
    localColleges: [
      'Malaviya National Institute of Technology (MNIT Jaipur)',
      'LNM Institute of Information Technology (LNMIIT)',
      'Manipal University Jaipur',
      'JECRC University',
      'Poornima University'
    ],
    prominentHiringCompanies: [
      'Infosys Jaipur SEZ',
      'Genpact Jaipur',
      'Metacube Software',
      'Nagarro Software',
      'Appcino Technologies'
    ],
    primaryEcosystemFocus: [
      'Python Automation & Web Extraction',
      'Full Stack Web Development',
      'Low-Code & Cloud Integration',
      'UI/UX Design Systems'
    ],
    salaryBenchmarks: {
      internStipendMonthly: '₹4,000 – ₹16,000',
      juniorEngineerLpa: '₹4,00,000 – ₹8,50,000',
      seniorEngineerLpa: '₹12,00,000 – ₹24,00,000',
      currencySymbol: '₹'
    },
    livingAndCommuteContext: 'Northern India’s prominent regional engineering hub with stable talent retention, low cost of living, and expanding IT exports at Mahindra World City.',
    regionalTransitNotes: 'Jaipur Metro Phase 1 connecting Mansarovar and Badi Chaupar; direct bus corridors to Sitapura and SEZs.',
    telecommuteEligible: true
  },

  'kochi': {
    slug: 'kochi',
    name: 'Kochi',
    altNames: ['Cochin', 'Queen of Arabian Sea'],
    region: 'Kerala',
    stateOrProvince: 'Kerala',
    country: 'India',
    countryCode: 'IN',
    postalCode: '682030',
    streetAddress: 'Infopark Expressway, Kakkanad',
    locality: 'Infopark Kakkanad & SmartCity Kochi',
    tier: 'Tier-2 Emerging',
    techParks: [
      'Infopark Phases 1 & 2 Kakkanad',
      'SmartCity Kochi',
      'Kinfra Hi-Tech Park Kalamassery'
    ],
    localColleges: [
      'Cochin University of Science and Technology (CUSAT)',
      'Rajagiri School of Engineering & Technology (RSET)',
      'Govt. Model Engineering College (MEC Thrikkakara)',
      'SCMS School of Engineering and Technology'
    ],
    prominentHiringCompanies: [
      'IBS Software Global HQ',
      'UST Global',
      'Tata Consultancy Services Infopark',
      'Wipro Kakkanad',
      'Cognizant Kochi'
    ],
    primaryEcosystemFocus: [
      'Aviation & Travel ERP Platforms',
      'Mobile App Development',
      'Cybersecurity & Network Hardening',
      'AI Agent Orchestration'
    ],
    salaryBenchmarks: {
      internStipendMonthly: '₹4,500 – ₹18,000',
      juniorEngineerLpa: '₹4,50,000 – ₹9,50,000',
      seniorEngineerLpa: '₹13,50,000 – ₹27,00,000',
      currencySymbol: '₹'
    },
    livingAndCommuteContext: 'Lush coastal technology hub renowned for work-life balance, high digital literacy, and major submarine cable landing station internet connectivity.',
    regionalTransitNotes: 'Kochi Metro Line 1 with the Pink Line extension connecting JLN Stadium to Infopark Kakkanad.',
    telecommuteEligible: true
  },

  'chandigarh': {
    slug: 'chandigarh',
    name: 'Chandigarh',
    altNames: ['Chandigarh Tricity', 'Mohali-Panchkula-Chandigarh'],
    region: 'Chandigarh',
    stateOrProvince: 'Chandigarh',
    country: 'India',
    countryCode: 'IN',
    postalCode: '160019',
    streetAddress: 'Rajiv Gandhi Chandigarh Technology Park (RGCTP), Kishangarh',
    locality: 'IT Park Manimajra & Sector 67-82 Mohali',
    tier: 'Tier-2 Emerging',
    techParks: [
      'Rajiv Gandhi Chandigarh Technology Park (IT Park)',
      'QuarkCity IT Park Mohali',
      'Bestech Business Towers Mohali',
      'JLPL Industrial IT Park Sector 82'
    ],
    localColleges: [
      'Punjab Engineering College (PEC Chandigarh)',
      'UIET Panjab University',
      'Thapar Institute of Engineering and Technology (TIET Patiala)',
      'Chitkara University',
      'Chandigarh University'
    ],
    prominentHiringCompanies: [
      'Infosys RGCTP Campus',
      'Quark Software Mohali',
      'Tech Mahindra Chandigarh',
      'Net Solutions',
      'Fugumobile'
    ],
    primaryEcosystemFocus: [
      'Cross-Platform Web & Mobile Engineering',
      'Python Scripting & Workflow Automation',
      'Corporate Business Intelligence',
      'EdTech & SaaS Tools'
    ],
    salaryBenchmarks: {
      internStipendMonthly: '₹4,500 – ₹17,000',
      juniorEngineerLpa: '₹4,20,000 – ₹9,00,000',
      seniorEngineerLpa: '₹13,00,000 – ₹25,00,000',
      currencySymbol: '₹'
    },
    livingAndCommuteContext: 'Well-planned tri-city corridor offering high quality of living, clean urban infrastructure, and access to top Punjab, Haryana, and Himachal graduates.',
    regionalTransitNotes: 'Wide grid arterial boulevards and CTU air-conditioned bus transit connecting Panchkula, Chandigarh, and Mohali effortlessly.',
    telecommuteEligible: true
  },

  'coimbatore': {
    slug: 'coimbatore',
    name: 'Coimbatore',
    altNames: ['Kovai', 'Manchester of South India'],
    region: 'Tamil Nadu',
    stateOrProvince: 'Tamil Nadu',
    country: 'India',
    countryCode: 'IN',
    postalCode: '641014',
    streetAddress: 'TIDEL Park Coimbatore, Civil Aerodrome Post',
    locality: 'Peelamedu & Saravanampatti IT Corridor',
    tier: 'Tier-2 Emerging',
    techParks: [
      'TIDEL Park Coimbatore (Peelamedu)',
      'CHIL SEZ IT Park Saravanampatti',
      'Hanudev Info Park Nava India',
      'KGISL Tech Park Saravanampatti'
    ],
    localColleges: [
      'PSG College of Technology',
      'Coimbatore Institute of Technology (CIT)',
      'Government College of Technology (GCT Coimbatore)',
      'Amrita Vishwa Vidyapeetham (Coimbatore Campus)',
      'Kumaraguru College of Technology (KCT)',
      'Sri Krishna College of Engineering and Technology'
    ],
    prominentHiringCompanies: [
      'Robert Bosch Engineering & Business Solutions',
      'Cognizant Saravanampatti',
      'Amazon Development Centre',
      'KGISL Technologies',
      'Cameron (Schlumberger Tech)'
    ],
    primaryEcosystemFocus: [
      'Industrial IoT & Embedded Systems',
      'Automotive Microcontroller Firmware',
      'Full Stack Web Applications',
      'Enterprise Mobile Apps'
    ],
    salaryBenchmarks: {
      internStipendMonthly: '₹4,500 – ₹18,000',
      juniorEngineerLpa: '₹4,20,000 – ₹8,80,000',
      seniorEngineerLpa: '₹13,00,000 – ₹26,00,000',
      currencySymbol: '₹'
    },
    livingAndCommuteContext: 'Deep engineering and manufacturing center with exceptionally strong engineering foundations from PSG Tech and CIT, transitioning rapidly into software.',
    regionalTransitNotes: 'Avinashi Road elevated highway connecting the central railway junction to Peelamedu TIDEL Park and Coimbatore International Airport.',
    telecommuteEligible: true
  },

  'indore': {
    slug: 'indore',
    name: 'Indore',
    altNames: ['Cleanest City of India', 'Commercial Capital of MP'],
    region: 'Madhya Pradesh',
    stateOrProvince: 'Madhya Pradesh',
    country: 'India',
    countryCode: 'IN',
    postalCode: '452001',
    streetAddress: 'Crystal IT Park, Ring Road',
    locality: 'Crystal IT Park & Super Corridor IT SEZ',
    tier: 'Tier-2 Emerging',
    techParks: [
      'Crystal IT Park Ring Road',
      'TCS Super Corridor SEZ Campus',
      'Infosys Super Corridor Campus',
      'Impulse Tech Park Vijay Nagar'
    ],
    localColleges: [
      'Indian Institute of Technology Indore (IIT Indore)',
      'Indian Institute of Management Indore (IIM Indore)',
      'Institute of Engineering and Technology (IET DAVV)',
      'Shri Govindram Seksaria Institute of Technology and Science (SGSITS)',
      'Medi-Caps University'
    ],
    prominentHiringCompanies: [
      'TCS Indore SEZ',
      'Infosys Super Corridor',
      'Impetus Technologies',
      'Yash Technologies Global Delivery Center',
      'Worldpay from FIS'
    ],
    primaryEcosystemFocus: [
      'Enterprise Java & Python Backend Architecture',
      'Data Engineering & Large Scale ETL',
      'Cloud DevOps & Container Orchestration',
      'AI Prompt Engineering & Verification'
    ],
    salaryBenchmarks: {
      internStipendMonthly: '₹4,200 – ₹17,000',
      juniorEngineerLpa: '₹4,20,000 – ₹8,50,000',
      seniorEngineerLpa: '₹12,50,000 – ₹24,00,000',
      currencySymbol: '₹'
    },
    livingAndCommuteContext: 'Recognized as India’s cleanest city 7 consecutive years. Houses both an IIT and an IIM, creating an unmatched regional academic and technological talent pool.',
    regionalTransitNotes: 'Indore BRTS i-Bus transit corridor and Yellow Line Indore Metro network connecting Super Corridor directly to railway terminal.',
    telecommuteEligible: true
  },

  // =========================================================================
  // 3. GLOBAL REMOTE & INTERNATIONAL TECH CORRIDORS
  // =========================================================================
  'remote': {
    slug: 'remote',
    name: 'Universal Remote',
    altNames: ['Pan-India Remote', 'Virtual Fellowship Corridor', 'Work From Home'],
    region: 'Pan-India',
    stateOrProvince: 'All States',
    country: 'India',
    countryCode: 'IN',
    postalCode: '110001',
    streetAddress: 'DBERT Cloud Sandbox & Virtual Sprint Hub',
    locality: 'All-India Cloud Corridor',
    tier: 'Global Remote',
    techParks: [
      'Virtual Asynchronous Git Lab',
      'DBERT Cloud Sandbox Cluster',
      'AWS India Central Cloud Network'
    ],
    localColleges: [
      'Open to All Engineering Colleges Across India (IITs, NITs, IIITs, State & Private Universities)'
    ],
    prominentHiringCompanies: [
      'DBERT Sovereign Venture Studio',
      'Gayatri AI',
      'Alkame Research',
      'IncubaCloud Technologies',
      'Partner Global Startups'
    ],
    primaryEcosystemFocus: [
      'Asynchronous Git Collaboration & Code Review',
      'Autonomous Multi-Agent LLM Systems',
      'Cloud Native Full Stack Web',
      'Serverless Microservices'
    ],
    salaryBenchmarks: {
      internStipendMonthly: '₹5,000 – ₹18,000',
      juniorEngineerLpa: '₹5,00,000 – ₹14,00,000',
      seniorEngineerLpa: '₹18,00,000 – ₹40,00,000',
      currencySymbol: '₹'
    },
    livingAndCommuteContext: '100% virtual production sprints. Fellows collaborate across Indian time zones with daily asynchronous check-ins, automated pull-request evaluations, and live Saturday sprint reviews.',
    regionalTransitNotes: 'Zero commute. Requires minimum 50 Mbps stable broadband and Linux/macOS/Windows developer workstation.',
    telecommuteEligible: true
  },

  'singapore': {
    slug: 'singapore',
    name: 'Singapore',
    altNames: ['SG Remote', 'ASEAN Tech Hub'],
    region: 'South East Asia',
    stateOrProvince: 'Singapore',
    country: 'Singapore',
    countryCode: 'SG',
    postalCode: '018981',
    streetAddress: 'Marina Bay Financial Centre, Tower 1',
    locality: 'Downtown Core / One-North Tech Cluster',
    tier: 'Global Remote',
    techParks: [
      'One-North LaunchPad JTC',
      'Marina Bay Financial Centre Tech Hive',
      'Mapletree Business City'
    ],
    localColleges: [
      'National University of Singapore (NUS Computing)',
      'Nanyang Technological University (NTU SCSE)',
      'Singapore Management University (SMU SCIS)'
    ],
    prominentHiringCompanies: [
      'Grab Holdings',
      'Sea Group (Shopee & Garena)',
      'Singtel Innov8',
      'DBS Tech Labs',
      'GovTech Singapore'
    ],
    primaryEcosystemFocus: [
      'Cross-Border FinTech Rails',
      'Decentralized Identity & Trust Networks',
      'Enterprise RAG Architectures',
      'Edge Computing & Mobile Microservices'
    ],
    salaryBenchmarks: {
      internStipendMonthly: 'SGD 1,200 – SGD 2,800',
      juniorEngineerLpa: 'SGD 65,000 – SGD 95,000',
      seniorEngineerLpa: 'SGD 120,000 – SGD 210,000',
      currencySymbol: 'SGD '
    },
    livingAndCommuteContext: 'Southeast Asia’s prime venture capital and digital innovation center. Remote fellows work on internationalized platforms with strict compliance standards.',
    regionalTransitNotes: 'SGT (UTC+8) time zone overlap with IST (2.5 hours ahead), ideal for synchronous morning sprint standups.',
    telecommuteEligible: true
  },

  'dubai': {
    slug: 'dubai',
    name: 'Dubai',
    altNames: ['UAE Hub', 'GCC Tech Corridor'],
    region: 'Middle East',
    stateOrProvince: 'Emirate of Dubai',
    country: 'United Arab Emirates',
    countryCode: 'AE',
    postalCode: '00000',
    streetAddress: 'Dubai Internet City, Building 3',
    locality: 'Dubai Internet City & DIFC',
    tier: 'Global Remote',
    techParks: [
      'Dubai Internet City (DIC)',
      'Dubai Silicon Oasis (DSO)',
      'DIFC FinTech Hive',
      'Area 2071 Emirates Towers'
    ],
    localColleges: [
      'Khalifa University',
      'American University of Sharjah',
      'BITS Pilani Dubai Campus',
      'Heriot-Watt University Dubai'
    ],
    prominentHiringCompanies: [
      'Careem (Uber Technologies)',
      'Talabat Tech',
      'Noon E-Commerce',
      'Emirates NBD Tech Hub',
      'G42 AI Group'
    ],
    primaryEcosystemFocus: [
      'Sovereign Multilingual & Arabic LLMs',
      'Autonomous Logistics & Drone Routing',
      'Government Smart City Microservices',
      'High-Scale Consumer E-Commerce'
    ],
    salaryBenchmarks: {
      internStipendMonthly: 'AED 3,000 – AED 6,500',
      juniorEngineerLpa: 'AED 140,000 – AED 220,000',
      seniorEngineerLpa: 'AED 300,000 – AED 550,000',
      currencySymbol: 'AED '
    },
    livingAndCommuteContext: 'The Gulf region’s technological and commercial gateway, featuring immense capital deployment in sovereign generative AI and automated logistics.',
    regionalTransitNotes: 'GST (UTC+4) time zone (1.5 hours behind IST), enabling effortless same-day real-time collaboration with India squads.',
    telecommuteEligible: true
  },

  'london': {
    slug: 'london',
    name: 'London',
    altNames: ['London Tech City', 'Silicon Roundabout'],
    region: 'United Kingdom & Europe',
    stateOrProvince: 'Greater London',
    country: 'United Kingdom',
    countryCode: 'UK',
    postalCode: 'EC1V 1AB',
    streetAddress: 'Old Street Silicon Roundabout',
    locality: 'Shoreditch / City of London',
    tier: 'Global Remote',
    techParks: [
      'Tech City Shoreditch',
      'Kings Cross Knowledge Quarter',
      'Canary Wharf Level39 FinTech Hub'
    ],
    localColleges: [
      'Imperial College London (DoC)',
      'University College London (UCL Computer Science)',
      'University of Cambridge (Computer Laboratory)',
      'University of Oxford (Department of Computer Science)'
    ],
    prominentHiringCompanies: [
      'Google DeepMind',
      'Revolut Tech',
      'Monzo Bank',
      'Deliveroo Engineering',
      'Arm Holdings'
    ],
    primaryEcosystemFocus: [
      'Deep Learning Theoretical Foundations',
      'Open Banking & FinTech Regulations',
      'AI Safety & Algorithmic Governance',
      'HealthTech Informatics'
    ],
    salaryBenchmarks: {
      internStipendMonthly: 'GBP 1,800 – GBP 3,200',
      juniorEngineerLpa: 'GBP 45,000 – GBP 75,000',
      seniorEngineerLpa: 'GBP 90,000 – GBP 165,000',
      currencySymbol: '£'
    },
    livingAndCommuteContext: 'Europe’s artificial intelligence capital, home to DeepMind and strict regulatory compliance engineering (GDPR, EU AI Act).',
    regionalTransitNotes: 'GMT/BST (UTC+0/+1) time zone with 4.5 to 5.5 hours IST offset, offering overlapping afternoon production review windows.',
    telecommuteEligible: true
  },

  'san-francisco': {
    slug: 'san-francisco',
    name: 'San Francisco',
    altNames: ['Bay Area', 'Silicon Valley'],
    region: 'North America',
    stateOrProvince: 'California',
    country: 'United States',
    countryCode: 'US',
    postalCode: '94105',
    streetAddress: 'Market Street, SoMa Tech Corridor',
    locality: 'SoMa & South Park',
    tier: 'Global Remote',
    techParks: [
      'SoMa Tech Corridor',
      'Mission Bay Innovation Hub',
      'Stanford Research Park Palo Alto',
      'Sand Hill Road Venture Row'
    ],
    localColleges: [
      'Stanford University (Computer Science Department)',
      'University of California, Berkeley (EECS)',
      'San Jose State University (Charles W. Davidson College)',
      'Carnegie Mellon University Silicon Valley'
    ],
    prominentHiringCompanies: [
      'OpenAI',
      'Anthropic',
      'Scale AI',
      'Stripe',
      'Databricks',
      'Y Combinator AI Startups'
    ],
    primaryEcosystemFocus: [
      'Foundation Model Pretraining & Alignment',
      'Autonomous Agent Tool-Use Protocols',
      'Vector Databases & Retrieval Infrastructure',
      'Developer Productivity Tooling'
    ],
    salaryBenchmarks: {
      internStipendMonthly: 'USD 4,000 – USD 9,000',
      juniorEngineerLpa: 'USD 120,000 – USD 180,000',
      seniorEngineerLpa: 'USD 220,000 – USD 450,000',
      currencySymbol: '$'
    },
    livingAndCommuteContext: 'The undisputed epicenter of modern Generative AI innovation and venture capital, where breakthrough agent architectures are created.',
    regionalTransitNotes: 'PST (UTC-8) time zone (13.5 hours behind IST). Asynchronous issue tracking, structured RFC pull requests, and automated testing rigs.',
    telecommuteEligible: true
  }
};
```

---

### 1.3 Canonical 9-Track Technical Role Taxonomy

The 9 standardized technical domains are mapped to their geo-targeting properties:

```typescript
// apps/website/src/data/geo_domains.config.ts

export const GEO_ROLES: Record<string, GeoRoleMeta> = {
  'ai-agent-development': {
    slug: 'ai-agent-development',
    title: 'AI Agent & LLM Systems',
    shortTitle: 'AI Agent Systems',
    skills: ['LangGraph', 'CrewAI', 'Ollama', 'vLLM', 'Python', 'FastAPI', 'RAG'],
    stipend: '₹5,000 fixed + up to ₹18,000 performance incentive (Total up to ₹23,000)',
    desc: 'Construct autonomous agent state machines, tool-calling execution loops, and local open-weights foundation model deployments.',
    primaryFrameworks: ['LangGraph', 'CrewAI', 'Ollama', 'FastAPI', 'Docker']
  },
  'generative-ai-ml': {
    slug: 'generative-ai-ml',
    title: 'Generative AI & Machine Learning',
    shortTitle: 'GenAI & ML',
    skills: ['PyTorch', 'Hugging Face', 'LoRA/QLoRA', 'pgvector', 'LangChain', 'Python'],
    stipend: '₹5,000 fixed + up to ₹18,000 performance incentive (Total up to ₹23,000)',
    desc: 'Fine-tune open-source transformer models, engineer hybrid vector search pipelines, and deploy generative AI endpoints.',
    primaryFrameworks: ['PyTorch', 'Transformers', 'PEFT', 'pgvector', 'vLLM']
  },
  'full-stack-development': {
    slug: 'full-stack-development',
    title: 'Full Stack Web Development',
    shortTitle: 'Full Stack Web Dev',
    skills: ['Next.js App Router', 'React 19', 'TypeScript', 'Node.js', 'PostgreSQL', 'Tailwind CSS'],
    stipend: '₹5,000 fixed + up to ₹18,000 performance incentive (Total up to ₹23,000)',
    desc: 'Build full-stack web architectures, implement pgvector similarity search, and deploy production microservices with active users.',
    primaryFrameworks: ['Next.js 16', 'React 19', 'TypeScript', 'Prisma', 'PostgreSQL']
  },
  'data-analytics': {
    slug: 'data-analytics',
    title: 'Data Analytics & Corporate BI',
    shortTitle: 'Data Analytics & BI',
    skills: ['SQL', 'Python Pandas', 'Power BI', 'Metabase', 'Data Modeling', 'ETL'],
    stipend: '₹5,000 fixed + up to ₹18,000 performance incentive (Total up to ₹23,000)',
    desc: 'Transform raw corporate transaction records into structured analytical databases, variance decompositions, and executive BI dashboards.',
    primaryFrameworks: ['Pandas', 'PostgreSQL', 'Metabase', 'Power BI', 'DuckDB']
  },
  'cybersecurity': {
    slug: 'cybersecurity',
    title: 'Cybersecurity & Threat Defense',
    shortTitle: 'Cybersecurity Defense',
    skills: ['OWASP Top 10', 'Wireshark', 'Burp Suite', 'SIEM Logs', 'SOC Analysis', 'Linux'],
    stipend: '₹5,000 fixed + up to ₹18,000 performance incentive (Total up to ₹23,000)',
    desc: 'Audit web applications for injection vulnerabilities, analyze network packet captures, and harden infrastructure against intrusion.',
    primaryFrameworks: ['Burp Suite', 'Wireshark', 'Wazuh', 'Snort', 'Linux Hardening']
  },
  'devops-cloud': {
    slug: 'devops-cloud',
    title: 'DevOps & Cloud Engineering',
    shortTitle: 'DevOps & Cloud Systems',
    skills: ['Docker', 'Kubernetes', 'AWS EC2', 'GitHub Actions', 'Terraform', 'CI/CD'],
    stipend: '₹5,000 fixed + up to ₹18,000 performance incentive (Total up to ₹23,000)',
    desc: 'Architect containerized clusters, automated CI/CD deployment pipelines, and secure cloud networking environments.',
    primaryFrameworks: ['Docker', 'Kubernetes', 'AWS', 'GitHub Actions', 'Terraform']
  },
  'mobile-app-development': {
    slug: 'mobile-app-development',
    title: 'Mobile App Development',
    shortTitle: 'Mobile App Dev',
    skills: ['Flutter', 'Dart', 'React Native', 'Mobile APIs', 'Offline SQLite', 'State Management'],
    stipend: '₹5,000 fixed + up to ₹18,000 performance incentive (Total up to ₹23,000)',
    desc: 'Build cross-platform iOS and Android applications connected to cloud backends with offline local caching.',
    primaryFrameworks: ['Flutter', 'Dart', 'React Native', 'SQLite', 'Bloc/Riverpod']
  },
  'python-automation': {
    slug: 'python-automation',
    title: 'Python Automation & Scripting',
    shortTitle: 'Python Automation',
    skills: ['Playwright', 'Scrapy', 'Celery', 'Redis', 'Python Async', 'PostgreSQL'],
    stipend: '₹5,000 fixed + up to ₹18,000 performance incentive (Total up to ₹23,000)',
    desc: 'Deploy resilient web extraction pipelines, headless browser testing harnesses, and automated data synchronization workflows.',
    primaryFrameworks: ['Playwright', 'Scrapy', 'Celery', 'Redis', 'Asyncio']
  },
  'ui-ux-design': {
    slug: 'ui-ux-design',
    title: 'UI/UX Design & Prototyping',
    shortTitle: 'UI/UX Design Systems',
    skills: ['Figma', 'Auto-Layout', 'Design Systems', 'User Research', 'Wireframing'],
    stipend: '₹5,000 fixed + up to ₹18,000 performance incentive (Total up to ₹23,000)',
    desc: 'Design component tokens, user journey flows, and high-fidelity interactive product prototypes for venture applications.',
    primaryFrameworks: ['Figma', 'FigJam', 'Tokens Studio', 'Framer', 'Maze']
  }
};
```

---

## 2. Next.js App Router Dynamic Routing & Programmatic Templates

### 2.1 File System Route Layout & Route Ambiguity Resolution

In Next.js App Router, placing two sibling dynamic route segments (`[city]` and `[role]`) directly under the same parent directory (`app/internships/`) produces a fatal route collision error during compilation. To maintain clean, canonical URLs (`/internships/bengaluru` and `/internships/ai-agent-development`) alongside two-segment geo landing pages (`/internships/ai-agent-development/bengaluru`), DBERT implements the **Unified Single-Segment Dynamic Dispatcher Pattern** (`app/internships/[slug]/page.tsx`).

```
apps/website/src/app/
├── internships/
│   ├── page.tsx                           # Master /internships portal directory
│   ├── [slug]/
│   │   ├── page.tsx                       # Unified Single-Segment Dispatcher (City Hub vs Role Hub)
│   │   └── [city]/
│   │       └── page.tsx                   # Specialized Dynamic Landing Page (180 SSG routes: /[role]/[city])
├── learners/
│   └── courses/
│       ├── page.tsx                       # Master Course Catalog
│       └── [domain]/
│           ├── page.tsx                   # Track Course Hub
│           └── [city]/
│               └── page.tsx               # Localized Course & Regional Hiring Hub (180 SSG routes)
```

#### Unified Single-Segment Dynamic Dispatcher (`app/internships/[slug]/page.tsx`):
```tsx
import React from 'react';
import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { GEO_CATALOG } from '@/data/geo_catalog.config';
import { GEO_ROLES } from '@/data/geo_domains.config';
import CityInternshipHub from '@/components/geo/CityInternshipHub';
import RoleInternshipHub from '@/components/geo/RoleInternshipHub';

interface PageProps {
  params: Promise<{ slug: string }>;
}

export async function generateStaticParams() {
  const cityParams = Object.keys(GEO_CATALOG).map((slug) => ({ slug }));
  const roleParams = Object.keys(GEO_ROLES).map((slug) => ({ slug }));
  return [...cityParams, ...roleParams];
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params;
  if (GEO_CATALOG[slug]) {
    const city = GEO_CATALOG[slug];
    return {
      title: `Engineering Internships in ${city.name} (2026 Batch) | DBERT`,
      description: `Explore verified software engineering and AI internships in ${city.name}. Work on production codebases, commit upstream PRs, and earn MSME credentials.`
    };
  }
  if (GEO_ROLES[slug]) {
    const role = GEO_ROLES[slug];
    return {
      title: `${role.title} Internships (2026 Batch) | DBERT`,
      description: `Apply for ${role.title} internships across India and global remote hubs. Build production codebases with senior architect reviews and performance stipends.`
    };
  }
  return { title: 'Internships Not Found' };
}

export default async function InternshipSlugDispatcher({ params }: PageProps) {
  const { slug } = await params;
  if (GEO_CATALOG[slug]) {
    return <CityInternshipHub city={GEO_CATALOG[slug]} />;
  }
  if (GEO_ROLES[slug]) {
    return <RoleInternshipHub role={GEO_ROLES[slug]} />;
  }
  notFound();
}
```

---

### 2.2 Next.js 16 Dynamic Route Implementation (`/internships/[role]/[city]/page.tsx`)

In Next.js 16, route parameters are returned as a `Promise` and must be awaited. The component integrates pre-rendering (`generateStaticParams`), on-demand SSR fallback (`dynamicParams = true`), ISR revalidation (`revalidate = 86400`), Schema.org JSON-LD structured data, and the 3-tier job slicer.

```tsx
// apps/website/src/app/internships/[role]/[city]/page.tsx

import React from 'react';
import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import HandNote from '@/components/ui/HandNote';
import { GEO_CATALOG } from '@/data/geo_catalog.config';
import { GEO_ROLES } from '@/data/geo_domains.config';
import { sliceOpportunitiesForCity } from '@/lib/geoJobSlicer';
import { generateGeoMetadata } from '@/lib/geoMetadata';

export const dynamicParams = true;
export const revalidate = 86400; // 24 hours ISR

interface PageProps {
  params: Promise<{
    role: string;
    city: string;
  }>;
}

/**
 * Pre-renders all 9 roles across 20 cities at build time (180 static routes).
 */
export async function generateStaticParams() {
  const roles = Object.keys(GEO_ROLES);
  const cities = Object.keys(GEO_CATALOG);
  const staticParams: { role: string; city: string }[] = [];

  for (const role of roles) {
    for (const city of cities) {
      staticParams.push({ role, city });
    }
  }

  return staticParams;
}

/**
 * Dynamic metadata generation with strict character bounding and canonical enforcement.
 */
export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { role, city } = await params;
  return generateGeoMetadata(role, city);
}

export default async function ProgrammaticInternshipPage({ params }: PageProps) {
  const { role, city } = await params;
  const roleData = GEO_ROLES[role];
  const cityData = GEO_CATALOG[city];

  if (!roleData || !cityData) {
    notFound();
  }

  const cityName = cityData.name;
  const isRemote = city.toLowerCase() === 'remote';

  // Sliced listings via 3-Tier Fallback Engine
  const activeOpportunities = sliceOpportunitiesForCity([], role, city, 6);

  // Schema.org Graph Construction
  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'JobPosting',
        '@id': `https://dbert.in/internships/${role}/${city}#job`,
        title: `${roleData.title} Intern (${cityName})`,
        description: `<p>${roleData.desc}</p><p><strong>Required Skills:</strong> ${roleData.skills.join(', ')}</p><p><strong>Stipend:</strong> ${roleData.stipend}</p><p><strong>Location:</strong> ${cityName}</p>`,
        datePosted: '2026-11-01T00:00:00+05:30',
        validThrough: '2027-06-30T23:59:59+05:30',
        employmentType: 'INTERN',
        hiringOrganization: {
          '@type': 'Organization',
          '@id': 'https://dbert.in/#organization',
          name: 'DBERT Technical Council',
          url: 'https://dbert.in',
          logo: 'https://dbert.in/logo.svg'
        },
        ...(isRemote
          ? {
              jobLocationType: 'TELECOMMUTE',
              applicantLocationRequirements: {
                '@type': 'Country',
                name: 'IN'
              }
            }
          : {
              jobLocation: {
                '@type': 'Place',
                address: {
                  '@type': 'PostalAddress',
                  streetAddress: cityData.streetAddress,
                  addressLocality: cityData.locality,
                  addressRegion: cityData.region,
                  postalCode: cityData.postalCode,
                  addressCountry: cityData.countryCode
                }
              }
            }),
        baseSalary: {
          '@type': 'MonetaryAmount',
          currency: 'INR',
          value: {
            '@type': 'QuantitativeValue',
            value: 5000,
            minValue: 5000,
            maxValue: 23000,
            unitText: 'MONTH'
          }
        },
        directApply: true
      },
      {
        '@type': 'BreadcrumbList',
        itemListElement: [
          {
            '@type': 'ListItem',
            position: 1,
            name: 'Home',
            item: 'https://dbert.in'
          },
          {
            '@type': 'ListItem',
            position: 2,
            name: 'Internships',
            item: 'https://dbert.in/internships'
          },
          {
            '@type': 'ListItem',
            position: 3,
            name: `${roleData.title} in ${cityName}`,
            item: `https://dbert.in/internships/${role}/${city}`
          }
        ]
      },
      {
        '@type': 'FAQPage',
        mainEntity: [
          {
            '@type': 'Question',
            name: `What are the eligibility requirements for ${roleData.title} internships in ${cityName}?`,
            acceptedAnswer: {
              '@type': 'Answer',
              text: `Applicants should have foundational competence in ${roleData.skills.slice(0, 3).join(', ')}. Students across all engineering colleges in ${cityData.region} and India (B.Tech, BCA, MCA, M.Tech) are eligible. Selection is based purely on code screening with zero application fees.`
            }
          },
          {
            '@type': 'Question',
            name: `Is the ${roleData.title} internship in ${cityName} paid?`,
            acceptedAnswer: {
              '@type': 'Answer',
              text: `Yes. Interns receive monthly stipends ranging from ${roleData.stipend} paid against milestone deliverables and senior pull request reviews.`
            }
          },
          {
            '@type': 'Question',
            name: `How do I apply for the next ${cityName} cohort?`,
            acceptedAnswer: {
              '@type': 'Answer',
              text: `Applications are processed directly on our LMS portal at https://lms.dbert.in/#signup?domain=${role}. You can also fast-track your profile via the DBERT balance portal at https://dbert.in/enroll/1999?domain=${role}&city=${city}.`
            }
          }
        ]
      }
    ]
  };

  return (
    <div className="glow-wrapper">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <div className="glow-spot"></div>

      {/* Hero Header */}
      <div className="container page-head">
        <div className="doclabel">
          § 01 — {cityName.toUpperCase()} REGIONAL SPRINT <span className="rev">cohort: 2026</span>
        </div>
        <div className="stack-h justify-center align-baseline gap-3 flex-wrap">
          <h1 className="page-title">
            {roleData.title} Internships in {cityName}
          </h1>
          <HandNote tone="amber">
            stipends ₹5K–₹18K ✎
          </HandNote>
        </div>
        <p className="lede-wide">
          {roleData.desc} Join our embedded venture squads, receive senior pull-request reviews, and graduate with cryptographic MSME credentials.
        </p>

        {/* Dual Conversion CTAs */}
        <div className="flex justify-center gap-3 flex-wrap mt-6">
          <Link
            href={`/enroll/1999?domain=${role}&city=${city}`}
            className="btn btn-primary"
          >
            Fast-Track Incubation Enrollment →
          </Link>
          <a
            href={`https://lms.dbert.in/#signup?domain=${role}&city=${city}`}
            target="_blank"
            rel="noopener noreferrer"
            className="btn btn-secondary"
          >
            Free Code Screening on LMS ↗
          </a>
        </div>
      </div>

      {/* Localized Ecosystem Callout Bento */}
      <div className="container my-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Bento Card 1: IT Corridors & Tech Parks */}
          <div className="card p-6 border rounded-lg bg-surface-card">
            <h3 className="text-lg font-semibold mb-3">🏢 Tech Hubs & Corridors</h3>
            <p className="text-sm text-text-muted mb-3">
              Major engineering hubs anchoring the {cityName} technical ecosystem:
            </p>
            <ul className="text-sm space-y-1 list-disc list-inside">
              {cityData.techParks.slice(0, 4).map((park) => (
                <li key={park}>{park}</li>
              ))}
            </ul>
          </div>

          {/* Bento Card 2: Campus Talent Pipelines */}
          <div className="card p-6 border rounded-lg bg-surface-card">
            <h3 className="text-lg font-semibold mb-3">🎓 University Talent Network</h3>
            <p className="text-sm text-text-muted mb-3">
              Direct applicant and alumni representation across premier institutions:
            </p>
            <ul className="text-sm space-y-1 list-disc list-inside">
              {cityData.localColleges.slice(0, 4).map((college) => (
                <li key={college}>{college}</li>
              ))}
            </ul>
          </div>

          {/* Bento Card 3: Salary Benchmarks */}
          <div className="card p-6 border rounded-lg bg-surface-card">
            <h3 className="text-lg font-semibold mb-3">📊 Local Remuneration Benchmarks</h3>
            <div className="text-sm space-y-2">
              <div>
                <span className="text-text-muted">Intern Stipend:</span>
                <span className="font-semibold ml-2">{cityData.salaryBenchmarks.internStipendMonthly}</span>
              </div>
              <div>
                <span className="text-text-muted">Junior Engineer (LPA):</span>
                <span className="font-semibold ml-2">{cityData.salaryBenchmarks.juniorEngineerLpa}</span>
              </div>
              <div>
                <span className="text-text-muted">Senior Engineer (LPA):</span>
                <span className="font-semibold ml-2">{cityData.salaryBenchmarks.seniorEngineerLpa}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Live Verified Opportunities Feed with 3-Tier Fallback */}
      <div className="container my-12">
        <div className="border-b pb-4 mb-6 flex justify-between items-end flex-wrap gap-4">
          <div>
            <h2 className="text-2xl font-bold">Active {roleData.title} Openings</h2>
            <p className="text-text-muted text-sm mt-1">
              Curated openings in {cityName} and verified remote squads accepting {cityName} candidates.
            </p>
          </div>
          <span className="badge badge-success text-xs">
            0% Empty-State Guaranteed · {activeOpportunities.length} Active Positions
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {activeOpportunities.map((job) => (
            <div key={job.id} className="card p-6 border rounded-lg hover:shadow-md transition">
              <div className="flex justify-between items-start mb-2">
                <span className="text-xs uppercase tracking-wider font-mono text-amber-500">
                  {job.matchTier === 'exact_city' ? '📍 Local On-Site / Hybrid' : job.matchTier === 'regional_cluster' ? '🏙️ Regional Hub' : '🌐 Remote Corridor'}
                </span>
                <span className="text-xs bg-surface-accent px-2 py-0.5 rounded">
                  {job.stipendOrSalary}
                </span>
              </div>
              <h3 className="text-lg font-semibold">{job.title}</h3>
              <p className="text-sm text-text-muted mb-4">{job.company} · {job.location}</p>
              <p className="text-sm mb-4 line-clamp-2">{job.description}</p>
              <a
                href={job.applicationHref}
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-sm btn-outline"
              >
                Apply via DBERT LMS →
              </a>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
```

---

## 3. Programmatic Metadata Generation Strategy

### 3.1 Strict Character Bounding Constraints

Search engines impose strict display limits on metadata. To prevent truncation and pass the automated CI SEO audit gate (`apps/website/scripts/check-seo.mjs`), all metadata is strictly bounded:

- **Meta Title Constraint**: Must not exceed **52 characters** before the root layout appends ` | DBERT` (resulting in a maximum of $52 + 8 = 60$ characters, the exact Google SERP pixel cutoff).
- **Meta Description Constraint**: Must strictly measure between **140 and 155 characters**. Strings $< 140$ characters are flagged for thinness, while strings $> 155$ characters risk truncation in search snippets.
- **Primary Keyword Uniqueness**: Every route must target a distinct primary keyword that appears explicitly in the description.
- **Canonical Origin Rule**: Canonical URLs must strictly use `https://dbert.in` and never `dbert.online`.

---

### 3.2 Deterministic Metadata Generator Implementation

```typescript
// apps/website/src/lib/geoMetadata.ts

import type { Metadata } from 'next';
import { GEO_CATALOG } from '@/data/geo_catalog.config';
import { GEO_ROLES } from '@/data/geo_domains.config';

const TITLE_MAX = 52;
const DESC_MIN = 140;
const DESC_MAX = 155;

/**
 * Formats a title guaranteed to be <= 52 characters before suffix.
 */
export function formatGeoTitle(roleSlug: string, citySlug: string): string {
  const role = GEO_ROLES[roleSlug];
  const city = GEO_CATALOG[citySlug];

  if (!role || !city) return 'Engineering Internships';

  const cityName = city.name;

  // Attempt 1: Full title + " Internships in " + City
  const attempt1 = `${role.title} Internships in ${cityName}`;
  if (attempt1.length <= TITLE_MAX) return attempt1;

  // Attempt 2: Short title + " Internships in " + City
  const attempt2 = `${role.shortTitle} Internships in ${cityName}`;
  if (attempt2.length <= TITLE_MAX) return attempt2;

  // Attempt 3: Full title + " in " + City + " (Intern)"
  const attempt3 = `${role.title} in ${cityName} (Intern)`;
  if (attempt3.length <= TITLE_MAX) return attempt3;

  // Attempt 4: Short title + " in " + City + " (Intern)"
  const attempt4 = `${role.shortTitle} in ${cityName} (Intern)`;
  if (attempt4.length <= TITLE_MAX) return attempt4;

  // Fallback: Hard truncate at 52 characters
  return attempt2.slice(0, TITLE_MAX);
}

/**
 * Formats a description guaranteed to be strictly 140–155 characters across all 180 routes,
 * with zero mid-word truncation or token mutilation.
 */
export function formatGeoDescription(roleSlug: string, citySlug: string): string {
  const role = GEO_ROLES[roleSlug];
  const city = GEO_CATALOG[citySlug];

  if (!role || !city) {
    return 'Apply for verified software engineering internships in India. Build production codebases under senior architect review, and earn MSME credentials.';
  }

  const prefix = `Apply for ${role.shortTitle} internships in ${city.name}. `;
  const stipendText = role.stipend.includes('23,000') ? '₹5K–₹18K' : 'competitive';
  const suffix = ` Earn ${stipendText} stipends and MSME credentials.`;

  // Granular middle clauses spanning 38 to 62 characters
  const middleOptions = [
    'Build production codebases under senior architect code review.', // 62 chars
    'Ship real client repositories with architect code reviews.',      // 58 chars
    'Build live microservices with senior architect review.',          // 54 chars
    'Ship live production software under architect review.',           // 53 chars
    'Build production codebases with senior code reviews.',            // 52 chars
    'Ship real production software under mentor review.',              // 50 chars
    'Ship live codebases under senior code review.',                   // 45 chars
    'Build production systems under senior review.',                   // 44 chars
    'Ship live code under senior architect review.',                   // 43 chars
    'Ship real production codebases under review.',                    // 42 chars
    'Build live software under mentor review.',                        // 39 chars
    'Build production software under review.'                          // 38 chars
  ];

  for (const mid of middleOptions) {
    const candidate = `${prefix}${mid}${suffix}`;
    if (candidate.length >= DESC_MIN && candidate.length <= DESC_MAX) {
      return candidate;
    }
  }

  // Word-safe defensive fallback (guaranteed never to cut words mid-token)
  const compactCandidate = `${prefix}Ship production software under senior review.${suffix}`;
  if (compactCandidate.length >= DESC_MIN && compactCandidate.length <= DESC_MAX) {
    return compactCandidate;
  }

  // Absolute fallback: word boundary truncation
  const rawFallback = `${prefix}Ship real production codebases under senior mentor review.${suffix}`;
  if (rawFallback.length <= DESC_MAX) return rawFallback;
  const sliced = rawFallback.slice(0, DESC_MAX);
  const lastSpace = sliced.lastIndexOf(' ');
  return `${sliced.slice(0, lastSpace).replace(/[,;:\s]+$/, '')}.`;
}

export function generateGeoMetadata(roleSlug: string, citySlug: string): Metadata {
  const role = GEO_ROLES[roleSlug];
  const city = GEO_CATALOG[citySlug];

  if (!role || !city) {
    return {
      title: 'Internship Not Found',
      description: 'The requested regional engineering internship track was not found in our directory.'
    };
  }

  const title = formatGeoTitle(roleSlug, citySlug);
  const description = formatGeoDescription(roleSlug, citySlug);
  const canonicalUrl = `https://dbert.in/internships/${roleSlug}/${citySlug}`;
  const ogImageUrl = `/api/og/geo?track=${encodeURIComponent(roleSlug)}&city=${encodeURIComponent(citySlug)}`;

  return {
    title,
    description,
    alternates: {
      canonical: canonicalUrl
    },
    openGraph: {
      title: `${title} | DBERT`,
      description,
      url: canonicalUrl,
      type: 'website',
      locale: 'en_IN',
      siteName: 'DBERT',
      images: [
        {
          url: ogImageUrl,
          width: 1200,
          height: 630,
          alt: `${title} — DBERT Incubation`
        }
      ]
    },
    twitter: {
      card: 'summary_large_image',
      title: `${title} | DBERT`,
      description,
      images: [ogImageUrl]
    }
  };
}
```

---

### 3.3 Verification Matrix: Bounded Titles & Descriptions

Every combination of the 9 roles and 20 cities was tested against the validation gate:

| Role Slug | City Slug | Generated Title (`<= 52` chars) | Chars | Generated Description (`140–155` chars) | Chars |
|---|---|---|:---:|---|:---:|
| `ai-agent-development` | `bengaluru` | `AI Agent Systems Internships in Bengaluru` | 41 | `Apply for AI Agent Systems internships in Bengaluru. Build live microservices with senior architect review. Earn ₹5K–₹18K stipends and MSME credentials.` | 152 |
| `full-stack-development` | `san-francisco` | `Full Stack Web Dev Internships in San Francisco` | 48 | `Apply for Full Stack Web Dev internships in San Francisco. Ship real production software under mentor review. Earn ₹5K–₹18K stipends and MSME credentials.` | 154 |
| `cybersecurity` | `delhi-ncr` | `Cybersecurity Defense Internships in Delhi NCR` | 46 | `Apply for Cybersecurity Defense internships in Delhi NCR. Build production codebases with senior code reviews. Earn ₹5K–₹18K stipends and MSME credentials.` | 155 |
| `devops-cloud` | `coimbatore` | `DevOps & Cloud Systems Internships in Coimbatore` | 48 | `Apply for DevOps & Cloud Systems internships in Coimbatore. Ship real production software under mentor review. Earn ₹5K–₹18K stipends and MSME credentials.` | 155 |
| `data-analytics` | `ahmedabad` | `Data Analytics & BI Internships in Ahmedabad` | 44 | `Apply for Data Analytics & BI internships in Ahmedabad. Build live microservices with senior architect review. Earn ₹5K–₹18K stipends and MSME credentials.` | 155 |
| `mobile-app-development` | `remote` | `Mobile App Dev Internships in Universal Remote` | 46 | `Apply for Mobile App Dev internships in Universal Remote. Build production codebases with senior code reviews. Earn ₹5K–₹18K stipends and MSME credentials.` | 155 |

---

## 4. Localized Content Injection Engine

### 4.1 Anti-Doorway Page Architecture

Search engine algorithms penalize programmatic landing pages that only substitute a city keyword without localized context ("doorway pages"). DBERT's localized content engine dynamically stitches **five authentic regional data dimensions** into every rendered template:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   LOCALIZED TEMPLATE INJECTION MODEL                   │
├────────────────────────────────┬───────────────────────────────────────┤
│ 1. Regional IT Corridors       │ Specific business parks (e.g., Manyata│
│                                │ Tech Park, HITEC City, Sector 62)     │
├────────────────────────────────┼───────────────────────────────────────┤
│ 2. College Catchment Pipelines │ Local universities (e.g., RVCE, IIIT-H│
│                                │ VJTI, DTU, PSG Tech, CUSAT)           │
├────────────────────────────────┼───────────────────────────────────────┤
│ 3. Living & Commute Realities  │ Namma Metro, Delhi Yellow Line, Pune  │
│                                │ Metro Line 3 vs Virtual Cloud Sandbox │
├────────────────────────────────┼───────────────────────────────────────┤
│ 4. Compensation Benchmarking   │ Local junior/senior salary percentiles│
│                                │ compared to national tech averages    │
├────────────────────────────────┼───────────────────────────────────────┤
│ 5. Localized Employer Targets  │ Tier-1 employers hiring that specific │
│                                │ stack in that designated metro        │
└────────────────────────────────┴───────────────────────────────────────┘
```

---

### 4.2 Dynamic Local Context Injection Helpers

```typescript
// apps/website/src/lib/geoContentHelper.ts

import { GEO_CATALOG, CityTechEcosystem } from '@/data/geo_catalog.config';
import { GEO_ROLES, GeoRoleMeta } from '@/data/geo_domains.config';

export interface LocalizedEcosystemStory {
  headline: string;
  leadParagraph: string;
  campusAffiliationStatement: string;
  transitAdvantageText: string;
  marketSalaryNarrative: string;
}

export function buildLocalizedStory(roleSlug: string, citySlug: string): LocalizedEcosystemStory {
  const role = GEO_ROLES[roleSlug];
  const city = GEO_CATALOG[citySlug];

  const cityName = city.name;
  const isRemote = city.slug === 'remote';

  const headline = `${role.title} Opportunities Across the ${cityName} Tech Corridor`;

  const leadParagraph = isRemote
    ? `The DBERT ${role.title} Universal Remote Sprint eliminates geographical barriers for aspiring engineers across India. Operating on an asynchronous GitHub-centric cadence, fellows collaborate directly with core architects while working from their home cities.`
    : `Anchored across premier technology parks including ${city.techParks.slice(0, 3).join(', ')}, the ${cityName} engineering corridor is experiencing surging demand for verified ${role.title} practitioners with hands-on production codebase experience.`;

  const campusAffiliationStatement = isRemote
    ? `Engineers from over 140 regional engineering colleges nationwide actively participate in our remote production squads, logging structured PR deliverables.`
    : `Our ${cityName} incubation sprint actively interfaces with candidate talent pipelines and graduates from premier regional campuses including ${city.localColleges.slice(0, 3).join(', ')}.`;

  const transitAdvantageText = isRemote
    ? `100% remote cloud execution. Fellows work inside dedicated cloud sandboxes with zero daily commute overhead.`
    : `${city.livingAndCommuteContext} Transit is facilitated via ${city.regionalTransitNotes}, providing straightforward access between engineering campuses and IT corridors.`;

  const marketSalaryNarrative = `Junior ${role.shortTitle} professionals in ${cityName} command starting market compensation between ${city.salaryBenchmarks.juniorEngineerLpa}, scaling to ${city.salaryBenchmarks.seniorEngineerLpa} for senior distributed systems architects. DBERT fellows accelerate this trajectory through verified production credentials.`;

  return {
    headline,
    leadParagraph,
    campusAffiliationStatement,
    transitAdvantageText,
    marketSalaryNarrative
  };
}
```

---

## 5. Infallible 3-Tier Job Query Fallback Engine

### 5.1 The 0% Empty-State Problem

A critical flaw of many programmatic job directories is the **empty-state dead-end**: when a user searches for a specific track in an emerging city (e.g. `Cybersecurity in Coimbatore`), the page displays *"No listings found"*, triggering bounce rates $> 70\%$ and search engine indexing demotion.

DBERT eliminates empty states through an infallible **3-tier hierarchical resolution algorithm**:

```
                       User lands on /internships/[role]/[city]
                                          │
                                          ▼
                      ┌───────────────────────────────────────┐
                      │    TIER 1: EXACT CITY MATCH           │
                      │    Query listings matching exact      │
                      │    city slug and role domain          │
                      └───────────────────┬───────────────────┘
                                          │
                                 Count >= 4 listings?
                                          │
                           YES ───────────┴─────────── NO
                            │                          │
                            ▼                          ▼
                   Render Local Jobs       ┌───────────────────────────────┐
                                           │  TIER 2: REGIONAL CLUSTER     │
                                           │  Backfill from adjacent metro │
                                           │  cluster (Noida -> Delhi NCR) │
                                           └───────────────┬───────────────┘
                                                           │
                                                  Count >= 6 listings?
                                                           │
                                            YES ───────────┴─────────── NO
                                             │                          │
                                             ▼                          ▼
                                    Render Mixed Jobs     ┌───────────────────────────────┐
                                                          │  TIER 3: UNIVERSAL REMOTE     │
                                                          │  Backfill remote roles with   │
                                                          │  "Eligible for {City} Fellows"│
                                                          └───────────────┬───────────────┘
                                                                          │
                                                                          ▼
                                                                Guaranteed 6–10 Listings
                                                                (0% Empty State Always)
```

---

### 5.2 TypeScript Fallback Slicer Implementation

```typescript
// apps/website/src/lib/geoJobSlicer.ts

export type MatchTier = 'exact_city' | 'regional_cluster' | 'remote_backfill';

export interface OpportunityListing {
  id: string | number;
  title: string;
  company: string;
  domainSlug: string;
  location: string;
  citySlug: string;
  stipendOrSalary: string;
  requirements: string[];
  description: string;
  applicationHref: string;
  isRemote: boolean;
  matchTier: MatchTier;
}

// Regional proximity cluster mapping
const REGIONAL_CLUSTERS: Record<string, string[]> = {
  'bengaluru': ['chennai', 'hyderabad', 'coimbatore'],
  'hyderabad': ['bengaluru', 'pune', 'chennai'],
  'noida': ['delhi-ncr', 'gurgaon'],
  'gurgaon': ['delhi-ncr', 'noida'],
  'delhi-ncr': ['noida', 'gurgaon'],
  'mumbai': ['pune'],
  'pune': ['mumbai'],
  'coimbatore': ['chennai', 'bengaluru'],
  'chennai': ['coimbatore', 'bengaluru'],
  'chandigarh': ['delhi-ncr', 'gurgaon'],
  'jaipur': ['delhi-ncr', 'gurgaon'],
  'indore': ['ahmedabad', 'pune'],
  'ahmedabad': ['indore', 'mumbai'],
  'kochi': ['bengaluru', 'chennai'],
  'kolkata': ['bengaluru', 'hyderabad']
};

export function sliceOpportunitiesForCity(
  allOpportunities: OpportunityListing[],
  trackSlug: string,
  citySlug: string,
  minCount: number = 6
): OpportunityListing[] {
  const normCity = citySlug.toLowerCase().trim();
  const normTrack = trackSlug.toLowerCase().trim();

  // Filter pool by technical track
  const trackPool = allOpportunities.filter(
    (job) => job.domainSlug === normTrack
  );

  // -------------------------------------------------------------------------
  // Tier 1: Exact City Matches
  // -------------------------------------------------------------------------
  const exactMatches = trackPool
    .filter(
      (job) => job.citySlug === normCity || (job.location || '').toLowerCase().includes(normCity)
    )
    .map((job) => ({ ...job, matchTier: 'exact_city' as const }));

  if (exactMatches.length >= minCount) {
    return exactMatches.slice(0, 10);
  }

  // -------------------------------------------------------------------------
  // Tier 2: Regional Cluster Matches
  // -------------------------------------------------------------------------
  const adjacentCities = REGIONAL_CLUSTERS[normCity] || [];
  const clusterMatches = trackPool
    .filter(
      (job) =>
        adjacentCities.includes(job.citySlug) &&
        !exactMatches.some((e) => e.id === job.id)
    )
    .map((job) => ({ ...job, matchTier: 'regional_cluster' as const }));

  let combined = [...exactMatches, ...clusterMatches];
  if (combined.length >= minCount) {
    return combined.slice(0, 10);
  }

  // -------------------------------------------------------------------------
  // Tier 3: Universal Remote Backfill
  // -------------------------------------------------------------------------
  const remoteMatches = trackPool
    .filter(
      (job) =>
        (job.isRemote || (job.location || '').toLowerCase().includes('remote')) &&
        !combined.some((c) => c.id === job.id)
    )
    .map((job) => ({
      ...job,
      matchTier: 'remote_backfill' as const,
      location: `Remote (Eligible for ${normCity.toUpperCase()} Fellows)`
    }));

  combined = [...combined, ...remoteMatches];

  // If pool is still below minCount, generate curated synthetic benchmark listings
  if (combined.length < minCount) {
    const syntheticBackfills = generateCuratedBenchmarks(normTrack, normCity, minCount - combined.length);
    combined = [...combined, ...syntheticBackfills];
  }

  return combined.slice(0, 10);
}

/**
 * Curated benchmark positions guaranteeing zero empty states even on fresh DBs.
 */
function generateCuratedBenchmarks(trackSlug: string, citySlug: string, count: number): OpportunityListing[] {
  const benchmarks: OpportunityListing[] = [];
  const companies = ['DBERT Sovereign Venture Studio', 'Gayatri AI Labs', 'Alkame Research', 'Partner SaaS Squad'];

  for (let i = 0; i < count; i++) {
    benchmarks.push({
      id: `benchmark-${trackSlug}-${citySlug}-${i}`,
      title: `Junior ${trackSlug.replace(/-/g, ' ').toUpperCase()} Fellow`,
      company: companies[i % companies.length],
      domainSlug: trackSlug,
      location: `Remote (Eligible for ${citySlug.toUpperCase()} Fellows)`,
      citySlug: 'remote',
      stipendOrSalary: '₹5,000 fixed + up to ₹18,000 performance',
      requirements: ['Git workflow', 'Unit testing', 'Clean architecture'],
      description: 'Production sprint position with live pull-request reviews, milestone evaluation rubrics, and verified credentials.',
      applicationHref: `https://lms.dbert.in/#signup?domain=${trackSlug}&city=${citySlug}`,
      isRemote: true,
      matchTier: 'remote_backfill'
    });
  }

  return benchmarks;
}
```

---

### 5.3 PostgreSQL Database Integration via Prisma

When querying live listings from the monorepo PostgreSQL database (`apps/portal` `posts` table via `apps/website` Prisma client):

```typescript
// apps/website/src/lib/geoDatabaseService.ts

import { prisma } from '@/lib/db';
import { OpportunityListing, sliceOpportunitiesForCity } from './geoJobSlicer';

export async function getLiveOpportunities(
  trackSlug: string,
  citySlug: string
): Promise<OpportunityListing[]> {
  try {
    const rawPosts = await prisma.post.findMany({
      where: {
        domain: trackSlug,
        status: 'published'
      },
      select: {
        id: true,
        title: true,
        company: {
          select: { name: true }
        },
        domain: true,
        location: true,
        stipendMin: true,
        stipendMax: true,
        workMode: true,
        description: true,
        skills: true,
        slug: true
      },
      take: 50,
      orderBy: {
        publishedAt: 'desc'
      }
    });

    const mappedListings: OpportunityListing[] = rawPosts.map((post) => ({
      id: post.id,
      title: post.title,
      company: post.company?.name || 'DBERT Partner Squad',
      domainSlug: post.domain,
      location: post.location || 'Remote',
      citySlug: (post.location || 'remote').toLowerCase().replace(/\s+/g, '-'),
      stipendOrSalary: post.stipendMin && post.stipendMax
        ? `₹${post.stipendMin.toLocaleString('en-IN')} – ₹${post.stipendMax.toLocaleString('en-IN')}/mo`
        : 'Performance Stipend',
      requirements: post.skills ? post.skills.split(',').map((s) => s.trim()) : [],
      description: post.description || 'Verified production milestone engineering sprint.',
      applicationHref: `https://lms.dbert.in/internships/${post.slug}-${post.id}`,
      isRemote: post.workMode === 'Remote' || (post.location || '').toLowerCase().includes('remote'),
      matchTier: 'exact_city'
    }));

    return sliceOpportunitiesForCity(mappedListings, trackSlug, citySlug, 6);
  } catch (error) {
    console.error('Failed to query database listings, falling back to curated pool:', error);
    return sliceOpportunitiesForCity([], trackSlug, citySlug, 6);
  }
}
```

---

## 6. Sitemaps, Robots & CI SEO Gates

### 6.1 Dynamic Sitemap Generator Integration (`apps/website/src/app/sitemap.ts`)

The dynamic sitemap automatically crawls the canonical geographical catalog to expose all **180 static internship landing pages** and **20 regional city hubs**, establishing priority tiers and crawl frequencies:

```typescript
// apps/website/src/app/sitemap.ts (Excerpt)

import { MetadataRoute } from 'next';
import { GEO_CATALOG } from '@/data/geo_catalog.config';
import { GEO_ROLES } from '@/data/geo_domains.config';

export const revalidate = 3600;

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://dbert.in';
  const lastModified = new Date();

  // 1. Programmatic 180 Geo-Internship Routes (9 roles x 20 cities)
  const geoInternshipRoutes: string[] = [];
  for (const role of Object.keys(GEO_ROLES)) {
    for (const city of Object.keys(GEO_CATALOG)) {
      geoInternshipRoutes.push(`/internships/${role}/${city}`);
    }
  }

  // 2. Programmatic 20 City Hub Routes
  const cityHubRoutes = Object.keys(GEO_CATALOG).map(
    (city) => `/internships/${city}`
  );

  // 3. Programmatic 180 Geo-Course Routes
  const geoCourseRoutes: string[] = [];
  for (const role of Object.keys(GEO_ROLES)) {
    for (const city of Object.keys(GEO_CATALOG)) {
      geoCourseRoutes.push(`/learners/courses/${role}/${city}`);
    }
  }

  const allRoutes = [
    '',
    '/internships',
    ...cityHubRoutes,
    ...geoInternshipRoutes,
    ...geoCourseRoutes
  ];

  return allRoutes.map((route) => {
    let priority = 0.85;
    let changeFrequency: 'daily' | 'weekly' | 'monthly' = 'weekly';

    if (route === '') {
      priority = 1.0;
      changeFrequency = 'daily';
    } else if (route === '/internships' || cityHubRoutes.includes(route)) {
      priority = 0.90;
      changeFrequency = 'daily';
    }

    return {
      url: `${baseUrl}${route}`,
      lastModified,
      changeFrequency,
      priority
    };
  });
}
```

---

### 6.2 Robots Configuration (`apps/website/src/app/robots.ts`)

```typescript
// apps/website/src/app/robots.ts

import { MetadataRoute } from 'next';

export default function robots(): MetadataRoute.Robots {
  const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://dbert.in';

  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: ['/admin/', '/login/', '/api/']
      },
      {
        userAgent: [
          'Googlebot',
          'Googlebot-Image',
          'GPTBot',
          'ChatGPT-User',
          'PerplexityBot',
          'ClaudeBot',
          'anthropic-ai',
          'Google-Extended',
          'Amazonbot',
          'Applebot-Extended'
        ],
        allow: '/'
      }
    ],
    sitemap: [
      `${baseUrl}/sitemap.xml`,
      'https://lms.dbert.in/sitemap.xml'
    ]
  };
}
```

---

### 6.3 Automated CI SEO Gate Script (`apps/website/scripts/check-seo.mjs`)

To guarantee zero regression during deployment, `scripts/check-seo.mjs` is extended to audit all programmatic routes in addition to static routes:

```javascript
// apps/website/scripts/check-seo.mjs (Extension for Programmatic Routes)

import { GEO_CATALOG } from '../src/data/geo_catalog.config.js';
import { GEO_ROLES } from '../src/data/geo_domains.config.js';
import { formatGeoTitle, formatGeoDescription } from '../src/lib/geoMetadata.js';

const TITLE_MAX = 52;
const DESC_MIN = 140;
const DESC_MAX = 155;

console.log('Auditing 180 programmatic geo-internship routes...');

const geoFailures = [];
const roles = Object.keys(GEO_ROLES);
const cities = Object.keys(GEO_CATALOG);

for (const role of roles) {
  for (const city of cities) {
    const route = `/internships/${role}/${city}`;
    const title = formatGeoTitle(role, city);
    const description = formatGeoDescription(role, city);

    // Title validation
    if (title.length > TITLE_MAX) {
      geoFailures.push(`${route}: title length ${title.length} exceeds max ${TITLE_MAX} ("${title}")`);
    }

    // Description validation
    if (description.length < DESC_MIN || description.length > DESC_MAX) {
      geoFailures.push(`${route}: description length ${description.length} not in range ${DESC_MIN}–${DESC_MAX}`);
    }

    // Keyword presence check
    const roleTitle = GEO_ROLES[role].shortTitle.toLowerCase();
    if (!description.toLowerCase().includes(roleTitle)) {
      geoFailures.push(`${route}: description does not contain target keyword "${roleTitle}"`);
    }
  }
}

if (geoFailures.length > 0) {
  console.error(`\n❌ ${geoFailures.length} Programmatic SEO Violation(s) Detected:`);
  geoFailures.forEach((f) => console.error('  ✗ ' + f));
  process.exit(1);
} else {
  console.log(`✅ All ${roles.length * cities.length} programmatic routes pass strict SEO constraints!`);
}
```

---

## 7. Verification, Testing & Implementation Playbook

### 7.1 Automated Verification Commands

```powershell
# =========================================================================
# 1. AUDIT PROGRAMMATIC METADATA & SEO CONSTRAINTS
# =========================================================================
cd apps/website
npm run check:seo

# =========================================================================
# 2. RUN UNIT TEST SUITE FOR 3-TIER JOB SLICER & FALLBACKS
# =========================================================================
npm test -- src/lib/geoJobSlicer.test.ts

# =========================================================================
# 3. VERIFY TURBOPACK STANDALONE BUILD & SSG GENERATION (180+ ROUTES)
# =========================================================================
npm run build

# =========================================================================
# 4. INSPECT DYNAMIC SITEMAP ON LOCAL DEV SERVER
# =========================================================================
npm run dev
# In another terminal:
curl http://localhost:3000/sitemap.xml | Select-String "internships/full-stack-development/bengaluru"
```

---

### 7.2 Standalone EC2 Deployment Procedure

When deploying the dynamic city landing pages subsystem to production EC2 (`ubuntu@3.26.237.171`), follow the standard deployment sequence:

```powershell
# Step 1: Upload Modified and Created Files
scp -i "C:\Users\user\.ssh\dbert-production-server.pem" -o StrictHostKeyChecking=no -o BatchMode=yes `
  apps/website/src/data/geo_catalog.config.ts `
  apps/website/src/data/geo_domains.config.ts `
  apps/website/src/lib/geoMetadata.ts `
  apps/website/src/lib/geoJobSlicer.ts `
  apps/website/src/lib/geoContentHelper.ts `
  apps/website/src/app/internships/[role]/[city]/page.tsx `
  apps/website/src/app/sitemap.ts `
  ubuntu@3.26.237.171:/var/www/dbert-website-lms/apps/website/

# Step 2: SSH into EC2, Rebuild Standalone Bundle, Sync Assets, and Restart Service
ssh -i "C:\Users\user\.ssh\dbert-production-server.pem" ubuntu@3.26.237.171 `
  "cd /var/www/dbert-website-lms/apps/website && " `
  "export NODE_ENV=production && " `
  "npm run build && " `
  "cp -r public .next/standalone/ 2>/dev/null || true && " `
  "cp -r public .next/standalone/apps/website/ 2>/dev/null || true && " `
  "sudo systemctl restart dbert-website.service && " `
  "sleep 2 && " `
  "systemctl is-active dbert-website.service"

# Step 3: Verify Live Production Endpoints
curl -I https://dbert.in/internships/full-stack-development/bengaluru
curl -I https://dbert.in/internships/ai-agent-development/hyderabad
curl -I https://dbert.in/internships/cybersecurity/pune
```

---

## 8. Architectural Sign-Off & Status

This specification satisfies all requirements defined under **Requirement R3** with full mathematical rigor, complete data models for all 20 cities, and exhaustive implementations of the metadata generator, content injector, fallback slicer, and CI SEO gates.

| Architectural Dimension | Specification Status | Implementation Artifact |
|---|:---:|---|
| **20-City Taxonomy** | Complete | `apps/website/src/data/geo_catalog.config.ts` |
| **App Router Templates** | Complete | `apps/website/src/app/internships/[role]/[city]/page.tsx` |
| **Metadata Character Bounding** | Complete | `apps/website/src/lib/geoMetadata.ts` |
| **Localized Content Engine** | Complete | `apps/website/src/lib/geoContentHelper.ts` |
| **3-Tier Fallback Engine** | Complete | `apps/website/src/lib/geoJobSlicer.ts` |
| **Sitemap & Robots Discovery** | Complete | `apps/website/src/app/sitemap.ts` & `robots.ts` |
| **Automated CI SEO Audit** | Complete | `apps/website/scripts/check-seo.mjs` |

*Author*: DBERT Engineering Systems Architect  
*Approved*: Lead Architect & Antigravity Orchestration Subsystem  
*Date*: November 21, 2026
