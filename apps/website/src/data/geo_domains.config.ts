/**
 * Canonical Geo-Targeted Programmatic SEO Taxonomy for DBERT Internships.
 * Covers 9 technical tracks across 18 major Indian technology hubs and college corridors.
 */

export interface GeoCityMeta {
  slug: string;
  name: string;
  street: string;
  locality: string;
  region: string;
  postalCode: string;
}

export const GEO_CITIES: Record<string, GeoCityMeta> = {
  'remote': { slug: 'remote', name: 'Remote / Work From Home', street: 'Cloud Sandbox Hub', locality: 'Pan-India', region: 'India', postalCode: '110001' },
  'bengaluru': { slug: 'bengaluru', name: 'Bengaluru', street: 'Outer Ring Road, Manyata Tech Park', locality: 'Bengaluru', region: 'Karnataka', postalCode: '560001' },
  'delhi-ncr': { slug: 'delhi-ncr', name: 'Delhi NCR', street: 'Connaught Place / Barakhamba Road', locality: 'Delhi NCR', region: 'Delhi', postalCode: '110001' },
  'mumbai': { slug: 'mumbai', name: 'Mumbai', street: 'Bandra Kurla Complex (BKC)', locality: 'Mumbai', region: 'Maharashtra', postalCode: '400051' },
  'pune': { slug: 'pune', name: 'Pune', street: 'Hinjawadi Rajiv Gandhi Infotech Park', locality: 'Pune', region: 'Maharashtra', postalCode: '411057' },
  'hyderabad': { slug: 'hyderabad', name: 'Hyderabad', street: 'HITEC City, Madhapur', locality: 'Hyderabad', region: 'Telangana', postalCode: '500081' },
  'chennai': { slug: 'chennai', name: 'Chennai', street: 'Old Mahabalipuram Rd, Tech Corridor', locality: 'Chennai', region: 'Tamil Nadu', postalCode: '600001' },
  'kolkata': { slug: 'kolkata', name: 'Kolkata', street: 'Sector V, Salt Lake City', locality: 'Kolkata', region: 'West Bengal', postalCode: '700091' },
  'ahmedabad': { slug: 'ahmedabad', name: 'Ahmedabad', street: 'SG Highway, Prahlad Nagar', locality: 'Ahmedabad', region: 'Gujarat', postalCode: '380015' },
  'jaipur': { slug: 'jaipur', name: 'Jaipur', street: 'Malviya Nagar Industrial Area', locality: 'Jaipur', region: 'Rajasthan', postalCode: '302017' },
  'lucknow': { slug: 'lucknow', name: 'Lucknow', street: 'Vibhuti Khand, Gomti Nagar', locality: 'Lucknow', region: 'Uttar Pradesh', postalCode: '226010' },
  'chandigarh': { slug: 'chandigarh', name: 'Chandigarh', street: 'Rajiv Gandhi Chandigarh Technology Park', locality: 'Chandigarh', region: 'Chandigarh', postalCode: '160019' },
  'indore': { slug: 'indore', name: 'Indore', street: 'Crystal IT Park, Ring Road', locality: 'Indore', region: 'Madhya Pradesh', postalCode: '452001' },
  'coimbatore': { slug: 'coimbatore', name: 'Coimbatore', street: 'TIDEL Park, Civil Aerodrome Post', locality: 'Coimbatore', region: 'Tamil Nadu', postalCode: '641014' },
  'kochi': { slug: 'kochi', name: 'Kochi', street: 'Infopark, Kakkanad', locality: 'Kochi', region: 'Kerala', postalCode: '682030' },
  'bhubaneswar': { slug: 'bhubaneswar', name: 'Bhubaneswar', street: 'Infocity, Chandaka Industrial Estate', locality: 'Bhubaneswar', region: 'Odisha', postalCode: '751024' },
  'noida': { slug: 'noida', name: 'Noida', street: 'Sector 62, Electronic City', locality: 'Noida', region: 'Uttar Pradesh', postalCode: '201301' },
  'gurgaon': { slug: 'gurgaon', name: 'Gurgaon', street: 'DLF Cyber City, Sector 24', locality: 'Gurugram', region: 'Haryana', postalCode: '122002' },
};

export interface GeoRoleMeta {
  slug: string;
  title: string;
  skills: string[];
  stipend: string;
  desc: string;
}

export const GEO_ROLES: Record<string, GeoRoleMeta> = {
  'full-stack-development': {
    slug: 'full-stack-development',
    title: 'Full Stack Web Development',
    skills: ['Next.js App Router', 'React 19', 'TypeScript', 'Node.js', 'PostgreSQL', 'Tailwind CSS'],
    stipend: '₹5,000 fixed + up to ₹18,000 performance incentive (Total up to ₹23,000)',
    desc: 'Build full-stack web architectures, implement pgvector similarity search, and deploy production microservices with active users.'
  },
  'ai-agent-development': {
    slug: 'ai-agent-development',
    title: 'AI Agent & LLM Systems',
    skills: ['LangGraph', 'CrewAI', 'Ollama', 'vLLM', 'Python', 'FastAPI', 'RAG'],
    stipend: '₹5,000 fixed + up to ₹18,000 performance incentive (Total up to ₹23,000)',
    desc: 'Construct autonomous agent state machines, tool-calling execution loops, and local open-weights foundation model deployments.'
  },
  'data-analytics': {
    slug: 'data-analytics',
    title: 'Data Analytics & Corporate BI',
    skills: ['SQL', 'Python Pandas', 'Power BI', 'Metabase', 'Data Modeling', 'ETL'],
    stipend: '₹5,000 fixed + up to ₹18,000 performance incentive (Total up to ₹23,000)',
    desc: 'Transform raw corporate transaction records into structured analytical databases, variance decompositions, and executive BI dashboards.'
  },
  'python-automation': {
    slug: 'python-automation',
    title: 'Python Automation & Scraping',
    skills: ['Playwright', 'Scrapy', 'Celery', 'Redis', 'Python Async', 'PostgreSQL'],
    stipend: '₹5,000 fixed + up to ₹18,000 performance incentive (Total up to ₹23,000)',
    desc: 'Deploy resilient web extraction pipelines, headless browser testing harnesses, and automated data synchronization workflows.'
  },
  'devops-cloud': {
    slug: 'devops-cloud',
    title: 'DevOps & Cloud Engineering',
    skills: ['Docker', 'Kubernetes', 'AWS EC2', 'GitHub Actions', 'Terraform', 'CI/CD'],
    stipend: '₹5,000 fixed + up to ₹18,000 performance incentive (Total up to ₹23,000)',
    desc: 'Architect containerized clusters, automated CI/CD deployment pipelines, and secure cloud networking environments.'
  },
  'ui-ux-design': {
    slug: 'ui-ux-design',
    title: 'UI/UX Design & Prototyping',
    skills: ['Figma', 'Auto-Layout', 'Design Systems', 'User Research', 'Wireframing'],
    stipend: '₹5,000 fixed + up to ₹18,000 performance incentive (Total up to ₹23,000)',
    desc: 'Design component tokens, user journey flows, and high-fidelity interactive product prototypes for venture applications.'
  },
  'cybersecurity': {
    slug: 'cybersecurity',
    title: 'Cybersecurity & Threat Defense',
    skills: ['OWASP Top 10', 'Wireshark', 'Burp Suite', 'SIEM Logs', 'SOC Analysis', 'Linux'],
    stipend: '₹5,000 fixed + up to ₹18,000 performance incentive (Total up to ₹23,000)',
    desc: 'Audit web applications for injection vulnerabilities, analyze network packet captures, and harden infrastructure against intrusion.'
  },
  'mobile-app-development': {
    slug: 'mobile-app-development',
    title: 'Mobile App Development',
    skills: ['Flutter', 'Dart', 'React Native', 'Mobile APIs', 'Offline SQLite', 'State Management'],
    stipend: '₹5,000 fixed + up to ₹18,000 performance incentive (Total up to ₹23,000)',
    desc: 'Build cross-platform iOS and Android applications connected to cloud backends with offline local caching.'
  },
  'machine-learning': {
    slug: 'machine-learning',
    title: 'Machine Learning & Generative AI',
    skills: ['PyTorch', 'Transformers', 'LoRA / QLoRA', 'LangChain', 'FastAPI', 'RAG'],
    stipend: '₹5,000 fixed + up to ₹18,000 performance incentive (Total up to ₹23,000)',
    desc: 'Fine-tune open-weights LLMs, construct production RAG vector pipelines, and deploy low-latency inference endpoints.'
  },
  'digital-marketing': {
    slug: 'digital-marketing',
    title: 'Digital Marketing & Growth',
    skills: ['Technical SEO', 'Google Analytics 4', 'Meta Ads', 'CRO', 'Content Marketing'],
    stipend: '₹5,000 fixed + up to ₹18,000 performance incentive (Total up to ₹23,000)',
    desc: 'Optimize organic search acquisition, analyze conversion funnels, and manage targeted growth campaigns across digital channels.'
  }
};

export function getAllGeoInternshipRoutes(): string[] {
  const routes: string[] = [];
  for (const role of Object.keys(GEO_ROLES)) {
    for (const city of Object.keys(GEO_CITIES)) {
      routes.push(`/internships/${role}/${city}`);
    }
  }
  return routes;
}
