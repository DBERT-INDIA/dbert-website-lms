export interface ProjectRepoInfo {
  url: string;
  label: string;
  org: string;
  repo: string;
  description: string;
  defaultBranch: string;
}

export const MENTOR_PROFILE = {
  name: 'Mr. Abhinav Sharma',
  title: 'Program Head & Project Mentor',
  organization: 'DBERT (Digital Blinc Education Research and Technology)',
  githubUrl: 'https://github.com/ainabhinavsharma',
  githubHandle: 'ainabhinavsharma',
  bio: 'AI Product Developer and Mentor at DBERT. Leading sovereign AI product development, multi-agent architectures, and guiding engineering cohorts through production-level system design and delivery.',
};

export function getProjectRepoInfo(project?: string): ProjectRepoInfo {
  const p = (project || '').toLowerCase();

  if (p.includes('gayatri')) {
    return {
      url: 'https://github.com/Gayatri-Education/Gayatri-Demo',
      label: 'Gayatri-Education / Gayatri-Demo',
      org: 'Gayatri-Education',
      repo: 'Gayatri-Demo',
      description: 'Autonomous Socratic tutoring, multi-agent RAG engine, and adaptive educational intelligence architecture.',
      defaultBranch: 'main',
    };
  }

  if (p.includes('alkame')) {
    return {
      url: 'https://github.com/ainabhinavsharma/alkame-nifty-50-educational',
      label: 'ainabhinavsharma / alkame-nifty-50-educational',
      org: 'ainabhinavsharma',
      repo: 'alkame-nifty-50-educational',
      description: 'Quantitative market analytics, conformal prediction risk models, and algorithmic time-series backtesting.',
      defaultBranch: 'main',
    };
  }

  if (p.includes('aivara')) {
    return {
      url: 'https://github.com/DBERT-INDIA/dbert-agent',
      label: 'DBERT-INDIA / dbert-agent',
      org: 'DBERT-INDIA',
      repo: 'dbert-agent',
      description: 'Autonomous AI operations, local-first agentic orchestration, and LLM-driven insight workflows.',
      defaultBranch: 'main',
    };
  }

  // Default / DBERT Cloud / Incubation Platform
  return {
    url: 'https://github.com/DBERT-INDIA/Internshipportal',
    label: 'DBERT-INDIA / Internshipportal',
    org: 'DBERT-INDIA',
    repo: 'Internshipportal',
    description: 'Production internship portal, enterprise applicant lifecycle, and scalable technical workflow engine.',
    defaultBranch: 'main',
  };
}

export function getIssueYearMonth(issueDate?: string): { year: number; month: number } {
  if (issueDate && issueDate.includes('-')) {
    const parts = issueDate.split('-');
    const year = parseInt(parts[0], 10);
    const month = parseInt(parts[1], 10);
    if (!isNaN(year) && !isNaN(month)) {
      return { year, month };
    }
  }
  return { year: 2026, month: 10 };
}
