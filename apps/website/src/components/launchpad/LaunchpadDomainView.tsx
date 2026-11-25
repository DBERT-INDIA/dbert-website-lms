'use client';

import React, { Suspense } from 'react';
import Link from 'next/link';
import { useSearchParams, useRouter, usePathname } from 'next/navigation';
import {
  Bot,
  Sparkles,
  Cpu,
  Terminal,
  Layout,
  BarChart3,
  Palette,
  Cloud,
  Smartphone,
  Shield,
  TrendingUp
} from 'lucide-react';
import ProgramDetailTemplate from '@/components/layout/ProgramDetailTemplate';
import { LAUNCHPAD_DOMAINS, LaunchpadDomain } from '@/data/launchpadDomains';
import { GEO_CITIES } from '@/data/geo_domains.config';
import s from './LaunchpadDomainView.module.css';

const DOMAIN_ICONS: Record<string, React.ReactNode> = {
  'data-analytics': <BarChart3 className="w-4 h-4" />,
  'ai-agent-development': <Bot className="w-4 h-4" />,
  'generative-ai': <Sparkles className="w-4 h-4" />,
  'machine-learning': <Cpu className="w-4 h-4" />,
  'python-automation': <Terminal className="w-4 h-4" />,
  'full-stack-development': <Layout className="w-4 h-4" />,
  'ui-ux-design': <Palette className="w-4 h-4" />,
  'devops-cloud': <Cloud className="w-4 h-4" />,
  'mobile-app-development': <Smartphone className="w-4 h-4" />,
  'cybersecurity': <Shield className="w-4 h-4" />,
  'digital-marketing': <TrendingUp className="w-4 h-4" />
};

const DOMAIN_KEYS = Object.keys(LAUNCHPAD_DOMAINS);

function DomainSelectorContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const pathname = usePathname();

  const domainParam = searchParams.get('domain') || searchParams.get('track');
  const selectedDomainId = domainParam && LAUNCHPAD_DOMAINS[domainParam] 
    ? domainParam 
    : 'ai-agent-development';

  const handleSelectDomain = (domainId: string) => {
    const params = new URLSearchParams(searchParams.toString());
    params.set('domain', domainId);
    router.replace(`${pathname}?${params.toString()}`, { scroll: false });
  };

  const currentDomain: LaunchpadDomain = LAUNCHPAD_DOMAINS[selectedDomainId] || LAUNCHPAD_DOMAINS['ai-agent-development'];

  const selectorSlot = (
    <div className={s.tabContainer}>
      <div className={s.selectorTitle}>Select Launchpad Beginner Domain Track (2 Months · ₹7,999 · 0-to-1 Foundations)</div>
      <div className={s.tabList} role="tablist" aria-label="Launchpad domain tracks">
        {DOMAIN_KEYS.map((key) => {
          const domain = LAUNCHPAD_DOMAINS[key];
          const isActive = selectedDomainId === key;
          return (
            <button
              key={key}
              role="tab"
              aria-selected={isActive}
              onClick={() => handleSelectDomain(key)}
              className={`${s.tabItem} ${isActive ? s.tabItemActive : ''}`}
            >
              {DOMAIN_ICONS[key]}
              <span>{domain.shortName}</span>
              {isActive && <span className={s.activeDot} aria-hidden="true" />}
            </button>
          );
        })}
      </div>
      <div className="mt-3 flex flex-wrap gap-1.5 items-center text-xs">
        <span className="font-mono text-muted mr-1">City Pages ({currentDomain.shortName}):</span>
        {Object.values(GEO_CITIES).map((c) => (
          <Link
            key={c.slug}
            href={`/learners/launchpad/${selectedDomainId}/${c.slug}`}
            className="tag-chip text-[11px] font-mono hover:border-accent hover:text-accent"
          >
            {c.shortName}
          </Link>
        ))}
      </div>
    </div>
  );

  return (
    <ProgramDetailTemplate
      title={`DBERT Launchpad: ${currentDomain.name}`}
      subtitle={`Beginner 0-to-1 Track (2 Months · ₹7,999) · ${currentDomain.tagline}`}
      price={currentDomain.price}
      duration={currentDomain.duration}
      audience={currentDomain.audience}
      outcome={currentDomain.outcome}
      curriculum={currentDomain.curriculum}
      headerSlot={selectorSlot}
      repoReferences={currentDomain.githubRepos}
      programKey="launchpad"
      domainSlug={selectedDomainId}
    />
  );
}

export default function LaunchpadDomainView() {
  return (
    <Suspense fallback={
      <div className="container pad-block text-center text-muted">
        Loading domain curriculum...
      </div>
    }>
      <DomainSelectorContent />
    </Suspense>
  );
}
