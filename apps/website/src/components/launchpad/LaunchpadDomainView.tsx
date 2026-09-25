'use client';

import React, { useState, useEffect, Suspense } from 'react';
import { useSearchParams, useRouter, usePathname } from 'next/navigation';
import { Bot, Sparkles, Cpu, Terminal, Layout, BarChart3 } from 'lucide-react';
import ProgramDetailTemplate from '@/components/layout/ProgramDetailTemplate';
import { LAUNCHPAD_DOMAINS, LaunchpadDomain } from '@/data/launchpadDomains';
import s from './LaunchpadDomainView.module.css';

const DOMAIN_ICONS: Record<string, React.ReactNode> = {
  'ai-agent-development': <Bot className="w-4 h-4" />,
  'generative-ai': <Sparkles className="w-4 h-4" />,
  'machine-learning': <Cpu className="w-4 h-4" />,
  'python-automation': <Terminal className="w-4 h-4" />,
  'full-stack-development': <Layout className="w-4 h-4" />,
  'data-analytics': <BarChart3 className="w-4 h-4" />
};

const DOMAIN_KEYS = Object.keys(LAUNCHPAD_DOMAINS);

function DomainSelectorContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const pathname = usePathname();

  const domainParam = searchParams.get('domain') || searchParams.get('track');
  const initialDomainId = domainParam && LAUNCHPAD_DOMAINS[domainParam] 
    ? domainParam 
    : 'ai-agent-development';

  const [selectedDomainId, setSelectedDomainId] = useState<string>(initialDomainId);

  useEffect(() => {
    if (domainParam && LAUNCHPAD_DOMAINS[domainParam]) {
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setSelectedDomainId(domainParam);
    }
  }, [domainParam]);

  const handleSelectDomain = (domainId: string) => {
    setSelectedDomainId(domainId);
    const params = new URLSearchParams(searchParams.toString());
    params.set('domain', domainId);
    router.replace(`${pathname}?${params.toString()}`, { scroll: false });
  };

  const currentDomain: LaunchpadDomain = LAUNCHPAD_DOMAINS[selectedDomainId] || LAUNCHPAD_DOMAINS['ai-agent-development'];

  const selectorSlot = (
    <div className={s.tabContainer}>
      <div className={s.selectorTitle}>Select Your Internship Domain Track (2 Months)</div>
      <div className={s.tabList} role="tablist" aria-label="Internship domain tracks">
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
    </div>
  );

  return (
    <ProgramDetailTemplate
      title={`DBERT Launchpad: ${currentDomain.name}`}
      subtitle={`2-Month Intensive Industrial Track · ${currentDomain.tagline}`}
      price={currentDomain.price}
      duration={currentDomain.duration}
      audience={currentDomain.audience}
      outcome={currentDomain.outcome}
      curriculum={currentDomain.curriculum}
      headerSlot={selectorSlot}
      repoReferences={currentDomain.githubRepos}
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
