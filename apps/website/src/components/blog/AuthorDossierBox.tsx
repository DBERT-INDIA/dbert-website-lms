import React from 'react';
import Link from 'next/link';
import { Award, CheckCircle2, Code2, ExternalLink, Share2, ShieldCheck, Sparkles } from 'lucide-react';
import certificatesRegistry from '@/data/certificates_registry.json';

function GithubIcon({ size = 15 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22" />
    </svg>
  );
}

interface AuthorDossierProps {
  name: string;
  role: string;
  domain?: string;
  certId?: string;
  githubRepoUrl?: string;
  liveDemoUrl?: string;
  rubricScore?: number | null;
  stipendStatus?: string;
  slug: string;
}

export default function AuthorDossierBox({
  name,
  role,
  domain,
  certId,
  githubRepoUrl,
  liveDemoUrl,
  rubricScore,
  stipendStatus,
  slug,
}: AuthorDossierProps) {
  const shareUrl = typeof window !== 'undefined' ? window.location.href : `https://dbert.in/blog/${slug}`;
  const linkedInShareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(`https://dbert.in/blog/${slug}`)}`;

  const certRecord = certId ? (certificatesRegistry as Record<string, any>)[certId] : null;
  const certifiedScore = certRecord?.score || (rubricScore ?? null);
  const certifiedGrade = certRecord?.grade || 'Grade: A+ (Outstanding Performance)';
  const showPreScreenSeparately = rubricScore && certRecord?.score && rubricScore !== certRecord.score;

  return (
    <div className="author-dossier-wrap my-8" style={{
      background: 'linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(22, 29, 51, 0.95) 100%)',
      border: '1px solid rgba(99, 102, 241, 0.35)',
      borderRadius: '16px',
      padding: '1.75rem',
      boxShadow: '0 12px 32px rgba(0, 0, 0, 0.4), 0 0 20px rgba(99, 102, 241, 0.1)',
    }}>
      {/* 1. Header with Author and Verified Pill */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem', borderBottom: '1px solid rgba(255, 255, 255, 0.08)', paddingBottom: '1.25rem', marginBottom: '1.25rem' }}>
        <div>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.75rem', fontWeight: 700, color: '#A5B4FC', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '0.35rem' }}>
            <Sparkles size={13} /> DBERT Verified Contributor Dossier
          </div>
          <h3 style={{ fontSize: '1.35rem', color: '#fff', margin: 0, fontWeight: 800 }}>{name}</h3>
          <p style={{ color: '#94A3B8', fontSize: '0.875rem', margin: '0.2rem 0 0' }}>{role} &bull; {domain || 'AI & Full Stack Engineering'}</p>
        </div>

        {certId && (
          <Link
            href={`/verify/${certId}`}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '0.45rem',
              background: 'rgba(16, 185, 129, 0.15)',
              border: '1px solid rgba(16, 185, 129, 0.4)',
              borderRadius: '9999px',
              padding: '0.4rem 0.9rem',
              color: '#34D399',
              fontSize: '0.8125rem',
              fontWeight: 700,
              textDecoration: 'none',
              transition: 'all 0.2s',
            }}
          >
            <ShieldCheck size={16} /> Verified Credential: {certId} &rarr;
          </Link>
        )}
      </div>

      {/* 2. Interactive Proof-of-Work Pills */}
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.75rem', marginBottom: '1.5rem' }}>
        {githubRepoUrl && (
          <a
            href={githubRepoUrl}
            target="_blank"
            rel="noopener noreferrer"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '0.5rem',
              background: 'rgba(255, 255, 255, 0.08)',
              border: '1px solid rgba(255, 255, 255, 0.18)',
              borderRadius: '8px',
              padding: '0.55rem 0.95rem',
              color: '#F8FAFC',
              fontSize: '0.8125rem',
              fontWeight: 700,
              textDecoration: 'none',
              transition: 'all 0.2s',
            }}
          >
            <GithubIcon size={15} /> Source Code on GitHub ↗
          </a>
        )}

        {liveDemoUrl && (
          <a
            href={liveDemoUrl}
            target="_blank"
            rel="noopener noreferrer"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '0.5rem',
              background: 'rgba(56, 189, 248, 0.15)',
              border: '1px solid rgba(56, 189, 248, 0.4)',
              borderRadius: '8px',
              padding: '0.55rem 0.95rem',
              color: '#38BDF8',
              fontSize: '0.8125rem',
              fontWeight: 700,
              textDecoration: 'none',
              transition: 'all 0.2s',
            }}
          >
            <ExternalLink size={15} /> Launch Working Application ↗
          </a>
        )}

        {certifiedScore && (
          <span
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '0.45rem',
              background: 'rgba(245, 158, 11, 0.15)',
              border: '1px solid rgba(245, 158, 11, 0.4)',
              borderRadius: '8px',
              padding: '0.55rem 0.95rem',
              color: '#FBBF24',
              fontSize: '0.8125rem',
              fontWeight: 700,
            }}
          >
            <Award size={15} /> Official Certified Evaluation: {certifiedScore}/100 ({certifiedGrade.replace(/^Grade:\s*/i, '')})
          </span>
        )}

        {showPreScreenSeparately && (
          <span
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '0.45rem',
              background: 'rgba(56, 189, 248, 0.15)',
              border: '1px solid rgba(56, 189, 248, 0.4)',
              borderRadius: '8px',
              padding: '0.55rem 0.95rem',
              color: '#38BDF8',
              fontSize: '0.8125rem',
              fontWeight: 700,
            }}
          >
            <CheckCircle2 size={15} /> Technical Contribution Pre-Screen: {rubricScore}/100
          </span>
        )}


        <span
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.45rem',
            background: 'rgba(99, 102, 241, 0.15)',
            border: '1px solid rgba(99, 102, 241, 0.4)',
            borderRadius: '8px',
            padding: '0.55rem 0.95rem',
            color: '#A5B4FC',
            fontSize: '0.8125rem',
            fontWeight: 700,
          }}
        >
          <CheckCircle2 size={15} /> ₹5,000 Production Milestone Disbursed
        </span>
      </div>

      {/* 3. Conversion Lead Magnet Banner */}
      <div style={{
        background: 'rgba(0, 0, 0, 0.35)',
        border: '1px solid rgba(255, 255, 255, 0.08)',
        borderRadius: '12px',
        padding: '1.25rem 1.5rem',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '1rem',
      }}>
        <div style={{ maxWidth: '540px' }}>
          <h4 style={{ color: '#fff', fontSize: '0.95rem', margin: '0 0 0.25rem', fontWeight: 700 }}>
            Want to build production projects like {name}?
          </h4>
          <p style={{ color: '#94A3B8', fontSize: '0.8125rem', margin: 0, lineHeight: 1.5 }}>
            Work 1:1 with practicing Delhi NCR engineers, build verified GitHub codebases, and earn production stipends up to ₹5,000.
          </p>
        </div>

        <div style={{ display: 'flex', gap: '0.65rem', flexWrap: 'wrap' }}>
          <a
            href={linkedInShareUrl}
            target="_blank"
            rel="noopener noreferrer"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '0.4rem',
              background: 'rgba(255, 255, 255, 0.06)',
              border: '1px solid rgba(255, 255, 255, 0.15)',
              borderRadius: '8px',
              padding: '0.6rem 0.95rem',
              color: '#CBD5E1',
              fontSize: '0.8125rem',
              fontWeight: 600,
              textDecoration: 'none',
            }}
          >
            <Share2 size={14} /> Share on LinkedIn
          </a>

          <a
            href={`https://lms.dbert.in/#signup?domain=${encodeURIComponent(domain || 'AI')}&ref=article_${slug}`}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '0.4rem',
              background: 'linear-gradient(135deg, #6366F1 0%, #4F46E5 100%)',
              border: 'none',
              borderRadius: '8px',
              padding: '0.6rem 1.25rem',
              color: '#fff',
              fontSize: '0.8125rem',
              fontWeight: 700,
              textDecoration: 'none',
              boxShadow: '0 4px 14px rgba(79, 70, 229, 0.4)',
            }}
          >
            Apply for Fellowship &rarr;
          </a>
        </div>
      </div>
    </div>
  );
}
