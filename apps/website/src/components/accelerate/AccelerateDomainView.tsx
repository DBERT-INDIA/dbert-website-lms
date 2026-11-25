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
import { ACCELERATE_DOMAINS, AccelerateDomain } from '@/data/accelerateDomains';
import { GEO_CITIES } from '@/data/geo_domains.config';
import s from '@/components/launchpad/LaunchpadDomainView.module.css';

const DOMAIN_ICONS: Record<string, React.ReactNode> = {
  'ai-agent-development': <Bot className="w-4 h-4" />,
  'generative-ai': <Sparkles className="w-4 h-4" />,
  'machine-learning': <Cpu className="w-4 h-4" />,
  'data-analytics': <BarChart3 className="w-4 h-4" />,
  'full-stack-development': <Layout className="w-4 h-4" />,
  'python-automation': <Terminal className="w-4 h-4" />,
  'ui-ux-design': <Palette className="w-4 h-4" />,
  'devops-cloud': <Cloud className="w-4 h-4" />,
  'mobile-app-development': <Smartphone className="w-4 h-4" />,
  'cybersecurity': <Shield className="w-4 h-4" />,
  'digital-marketing': <TrendingUp className="w-4 h-4" />
};

const DOMAIN_KEYS = Object.keys(ACCELERATE_DOMAINS);

function AccelerateDomainContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const pathname = usePathname();

  const domainParam = searchParams.get('domain') || searchParams.get('track');
  const selectedDomainId = domainParam && ACCELERATE_DOMAINS[domainParam]
    ? domainParam
    : 'ai-agent-development';

  const handleSelectDomain = (domainId: string) => {
    const params = new URLSearchParams(searchParams.toString());
    params.set('domain', domainId);
    router.replace(`${pathname}?${params.toString()}`, { scroll: false });
  };

  const currentDomain: AccelerateDomain =
    ACCELERATE_DOMAINS[selectedDomainId] || ACCELERATE_DOMAINS['ai-agent-development'];

  const selectorSlot = (
    <div className={s.tabContainer}>
      <div className={s.selectorTitle}>
        Select Accelerate Intermediate Sprint Track (2 Months · ₹4,999 · Applied Engineering)
      </div>
      <div className={s.tabList} role="tablist" aria-label="Accelerate domain tracks">
        {DOMAIN_KEYS.map((key) => {
          const domain = ACCELERATE_DOMAINS[key];
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
            href={`/learners/accelerate/${selectedDomainId}/${c.slug}`}
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
      title={`DBERT Accelerate: ${currentDomain.name}`}
      subtitle={`Applied Industrial Sprint Track (2 Months · ₹4,999) · ${currentDomain.tagline}`}
      price={currentDomain.price}
      duration={currentDomain.duration}
      audience={currentDomain.audience}
      outcome={currentDomain.outcome}
      curriculum={currentDomain.curriculum}
      headerSlot={selectorSlot}
      repoReferences={currentDomain.githubRepos}
      programKey="accelerate"
      domainSlug={selectedDomainId}
    />
  );
}

export default function AccelerateDomainView() {
  return (
    <Suspense
      fallback={
        <div className="container pad-block text-center text-muted">
          Loading Accelerate domain curriculum...
        </div>
      }
    >
      <AccelerateDomainContent />
    </Suspense>
  );
}
