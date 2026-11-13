'use client';

import React, { useEffect, useState, useCallback } from 'react';
import Image from 'next/image';
import f from './forms.module.css';
import s from './ContributorCards.module.css';

interface Contributor {
  id: string;
  name: string;
  profilePicUrl: string;
  comment: string;
  linkedinUrl: string;
  githubUrl: string;
  domain: string;
  reviewedAt: string | null;
}

interface ApiResponse {
  contributors: Contributor[];
  page: number;
  totalPages: number;
  totalCount: number;
}

interface ContributorCardsProps {
  projectSlug?: string;
  projectName?: string;
}

export default function ContributorCards({
  projectSlug = 'alkame',
  projectName = 'Alkame',
}: ContributorCardsProps) {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState('');

  const fetchPage = useCallback(async (pageNum: number) => {
    setLoading(true);
    setErrorMsg('');
    try {
      const endpoint =
        projectSlug === 'alkame'
          ? `/api/alkame/contributors?page=${pageNum}`
          : `/api/projects/${projectSlug}/contributors?page=${pageNum}`;
      const res = await fetch(endpoint);
      if (!res.ok) throw new Error('Failed to load contributors');
      const json: ApiResponse = await res.json();
      setData(json);
    } catch (err) {
      setErrorMsg('Could not load contributors right now.');
    } finally {
      setLoading(false);
    }
  }, [projectSlug]);

  useEffect(() => {
    fetchPage(page);
  }, [page, fetchPage]);

  if (loading && !data) {
    return <p className={f.emptyState}>Loading contributors…</p>;
  }

  if (errorMsg) {
    return <p className={f.emptyState}>{errorMsg}</p>;
  }

  if (!data || data.contributors.length === 0) {
    return (
      <p className={f.emptyState}>
        No contributors have been published yet for {projectName}. Be the first to add yourself below.
      </p>
    );
  }

  return (
    <div>
      <div className={s.grid}>
        {data.contributors.map((c) => (
          <div key={c.id} className={`card ${s.card}`}>
            <div className={s.identity}>
              <div className={s.avatarFrame}>
                <Image src={c.profilePicUrl} alt={c.name} fill className={s.avatarImg} unoptimized />
              </div>
              <div>
                <p className={s.name}>{c.name}</p>
                <span className={s.domain}>
                  {c.domain}
                </span>
              </div>
            </div>
            <p className={s.comment}>{c.comment}</p>
            <div className={s.links}>
              <a href={c.linkedinUrl} target="_blank" rel="noopener noreferrer" className={f.caption}>LinkedIn ↗</a>
              <a href={c.githubUrl} target="_blank" rel="noopener noreferrer" className={f.caption}>GitHub ↗</a>
            </div>
          </div>
        ))}
      </div>

      {data.totalPages > 1 && (
        <div className={s.pager}>
          {Array.from({ length: data.totalPages }, (_, i) => i + 1).map((num) => (
            <button
              key={num}
              onClick={() => setPage(num)}
              disabled={loading}
              className={`${s.pageBtn}${num === page ? ` ${s.pageBtnActive}` : ''}`}
            >
              {num}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
