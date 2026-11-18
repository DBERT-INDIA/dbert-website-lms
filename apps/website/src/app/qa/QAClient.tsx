'use client';

import React, { useState, useMemo } from 'react';
import Link from 'next/link';
import { Search, ChevronDown, Sparkles, ArrowRight, ShieldCheck, GraduationCap, ExternalLink } from 'lucide-react';
import { trackEvent } from '@/lib/analytics';
import s from './qa.module.css';

export interface QAItem {
  id: string;
  domain: string;
  domainSlug: string;
  question: string;
  shortAnswer: string;
  detailedMarkdown: string;
  relatedBlogSlug: string;
  relatedBlogTitle: string;
  relatedCertId: string;
  author: string;
  tags: string[];
  ctaText: string;
  ctaUrl: string;
}

interface QAClientProps {
  initialItems: QAItem[];
}

const DOMAINS = [
  'All',
  'AI Agent Development',
  'Data Analytics',
  'Full Stack Development',
  'Legitimacy & Accreditation',
  'Incubation & Careers'
];

export default function QAClient({ initialItems }: QAClientProps) {
  const [selectedDomain, setSelectedDomain] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');
  const [openIds, setOpenIds] = useState<string[]>(['gayatri-ai-architecture', 'dbert-legitimacy-verification']);

  const toggleItem = (id: string, question: string) => {
    setOpenIds(prev => {
      const isOpen = prev.includes(id);
      if (!isOpen) {
        trackEvent('qa_question_expand', { questionId: id, questionTitle: question.slice(0, 50) });
        return [...prev, id];
      } else {
        return prev.filter(item => item !== id);
      }
    });
  };

  const filteredItems = useMemo(() => {
    return initialItems.filter(item => {
      const matchesDomain = selectedDomain === 'All' || item.domain === selectedDomain;
      const q = searchQuery.toLowerCase().trim();
      const matchesSearch =
        !q ||
        item.question.toLowerCase().includes(q) ||
        item.shortAnswer.toLowerCase().includes(q) ||
        item.tags.some(t => t.toLowerCase().includes(q)) ||
        item.author.toLowerCase().includes(q);
      return matchesDomain && matchesSearch;
    });
  }, [initialItems, selectedDomain, searchQuery]);

  return (
    <div className={s.pageWrapper}>
      <div className={s.glowOrb} />
      <div className={s.container}>
        
        {/* Hero Section */}
        <header className={s.heroSection}>
          <div className={s.badge}>
            <Sparkles size={14} />
            <span>AI Knowledge & Career Intelligence</span>
          </div>
          <h1 className={s.mainTitle}>
            Technical Knowledge &amp; <span className={s.goldGradient}>Career Q&amp;A Hub</span>
          </h1>
          <p className={s.subtitle}>
            Explore peer-reviewed architectural case studies, production AI agent blueprints, financial data pipelines, and verified career pathways directly from DBERT Engineering.
          </p>
        </header>

        {/* Learner-First CTA Banner */}
        <section className={s.ctaBanner}>
          <div className={s.ctaText}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
              <GraduationCap size={20} color="#e5b842" />
              <h3>Looking to Build Production Systems Like These?</h3>
            </div>
            <p>
              Join the 2-Month Technical Incubation Fellowship for <strong>₹1,999</strong> (Pay ₹1,500 balance if ₹499 caution deposit is paid). Build in public, get mentor reviews, and earn 5,000 coins stipend eligibility.
            </p>
          </div>
          <div className={s.ctaActions}>
            <Link
              href="/enroll/1999"
              className={s.primaryCta}
              onClick={() => trackEvent('qa_banner_enroll_click', { destination: '/enroll/1999' })}
            >
              <span>Enroll / Pay Balance</span>
              <ArrowRight size={16} />
            </Link>
            <Link
              href="/verify"
              className={s.secondaryCta}
              onClick={() => trackEvent('qa_banner_verify_click', { destination: '/verify' })}
            >
              <ShieldCheck size={16} />
              <span>Verify Credential</span>
            </Link>
          </div>
        </section>

        {/* Controls Section: Search & Filters */}
        <div className={s.controlsSection}>
          <div className={s.searchBox}>
            <Search className={s.searchIcon} size={18} />
            <input
              type="text"
              className={s.searchInput}
              placeholder="Search by topic, architecture, technology (FastAPI, Redis, RAG, Streamlit, Legitimacy)..."
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
            />
          </div>

          <div className={s.filterPills}>
            {DOMAINS.map(domain => (
              <button
                key={domain}
                type="button"
                className={`${s.filterBtn} ${selectedDomain === domain ? s.filterBtnActive : ''}`}
                onClick={() => {
                  setSelectedDomain(domain);
                  trackEvent('qa_domain_filter_select', { domain });
                }}
              >
                {domain}
              </button>
            ))}
          </div>
        </div>

        {/* QA Accordion List */}
        <div className={s.qaList}>
          {filteredItems.length === 0 ? (
            <div className={s.emptyState}>
              <p>No questions found matching &ldquo;{searchQuery}&rdquo;.</p>
              <button
                type="button"
                className={s.filterBtn}
                style={{ marginTop: '12px' }}
                onClick={() => {
                  setSearchQuery('');
                  setSelectedDomain('All');
                }}
              >
                Reset Filters
              </button>
            </div>
          ) : (
            filteredItems.map(item => {
              const isOpen = openIds.includes(item.id);
              return (
                <article key={item.id} className={`${s.qaCard} ${isOpen ? s.qaCardOpen : ''}`}>
                  <button
                    type="button"
                    className={s.qaHeader}
                    onClick={() => toggleItem(item.id, item.question)}
                    aria-expanded={isOpen}
                  >
                    <div>
                      <div className={s.questionMeta}>
                        <span className={s.domainTag}>{item.domain}</span>
                        {item.author && <span className={s.authorTag}>By {item.author}</span>}
                      </div>
                      <h2 className={s.questionText}>{item.question}</h2>
                    </div>
                    <ChevronDown className={`${s.toggleIcon} ${isOpen ? s.toggleIconRotated : ''}`} size={20} />
                  </button>

                  {isOpen && (
                    <div className={s.qaBody}>
                      <div className={s.shortAnswerBox}>
                        <strong>Executive Summary:</strong> {item.shortAnswer}
                      </div>

                      <div className={s.detailedText}>{item.detailedMarkdown}</div>

                      <div className={s.qaFooter}>
                        <div className={s.tagGroup}>
                          {item.tags.map(t => (
                            <span key={t} className={s.tagPill}>
                              #{t}
                            </span>
                          ))}
                        </div>

                        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                          {item.relatedBlogSlug && (
                            <Link
                              href={`/blog/${item.relatedBlogSlug}`}
                              className={s.qaCtaLink}
                              style={{ color: '#38bdf8' }}
                              onClick={() => trackEvent('qa_related_blog_click', { slug: item.relatedBlogSlug })}
                            >
                              <span>Read Case Study</span>
                              <ExternalLink size={13} />
                            </Link>
                          )}
                          <Link
                            href={item.ctaUrl}
                            className={s.qaCtaLink}
                            onClick={() => trackEvent('qa_card_cta_click', { ctaUrl: item.ctaUrl, questionId: item.id })}
                          >
                            <span>{item.ctaText}</span>
                            <ArrowRight size={14} />
                          </Link>
                        </div>
                      </div>
                    </div>
                  )}
                </article>
              );
            })
          )}
        </div>

      </div>
    </div>
  );
}
