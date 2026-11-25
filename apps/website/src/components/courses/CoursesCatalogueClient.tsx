'use client';

import React, { useMemo, useState } from 'react';
import Link from 'next/link';
import type { FellowshipTrack } from '@/data/courses.types';

interface CoursesCatalogueClientProps {
  tracks: FellowshipTrack[];
  formattedFee: string;
}

const CATEGORIES = ['All', 'AI & Data', 'Software & Cloud', 'Product & Growth'] as const;

export default function CoursesCatalogueClient({ tracks, formattedFee }: CoursesCatalogueClientProps) {
  const [category, setCategory] = useState<(typeof CATEGORIES)[number]>('All');
  const [query, setQuery] = useState('');

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return tracks.filter((t) => {
      const catOk = category === 'All' || t.category === category;
      if (!catOk) return false;
      if (!q) return true;
      const haystack = [
        t.name,
        t.shortDescription,
        ...t.technologies.map((tech) => tech.name),
      ]
        .join(' ')
        .toLowerCase();
      return haystack.includes(q);
    });
  }, [tracks, category, query]);

  return (
    <div className="my-8">
      <div className="flex flex-col md:flex-row gap-4 justify-between items-stretch md:items-center mb-6">
        <div className="flex gap-2 flex-wrap" role="group" aria-label="Filter tracks by category">
          {CATEGORIES.map((cat) => {
            const active = category === cat;
            return (
              <button
                key={cat}
                type="button"
                aria-pressed={active}
                onClick={() => setCategory(cat)}
                className={`px-3 py-1.5 rounded text-xs font-mono border transition-colors ${
                  active
                    ? 'bg-accent text-zinc-950 border-accent font-bold'
                    : 'bg-card text-[var(--text-secondary)] border-line hover:border-accent'
                }`}
              >
                {cat}
              </button>
            );
          })}
        </div>

        <div className="w-full md:w-72">
          <label htmlFor="catalogue-search" className="sr-only">
            Search fellowship tracks or technologies
          </label>
          <input
            id="catalogue-search"
            type="search"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search tracks or stack (e.g. LangGraph, SQL)..."
            className="w-full px-3 py-2 rounded bg-card border border-line text-xs font-mono text-white placeholder:text-muted focus:outline-none focus:border-accent"
          />
        </div>
      </div>

      {filtered.length === 0 ? (
        <div className="card p-8 bg-card border border-line text-center">
          <p className="text-sm text-muted mb-3">No fellowship tracks matched &ldquo;{query}&rdquo;.</p>
          <button
            type="button"
            onClick={() => {
              setCategory('All');
              setQuery('');
            }}
            className="btn btn-outline text-xs"
          >
            Reset Filters
          </button>
        </div>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {filtered.map((course) => (
            <Link
              key={course.id}
              href={course.canonicalPath}
              className="card card-lift p-6 bg-card border border-line flex flex-col justify-between h-full group"
            >
              <div>
                <div className="flex justify-between items-center mb-3 gap-2">
                  <span className="tag-chip text-xs font-mono">{course.badge}</span>
                  <span className="text-xs font-mono text-muted">
                    {course.duration} · {formattedFee}
                  </span>
                </div>
                <h2 className="font-mono text-xl font-bold text-white group-hover:text-accent transition-colors mb-2">
                  {course.name}
                </h2>
                <p className="text-xs leading-relaxed mb-4 text-[var(--text-secondary)]">
                  {course.shortDescription}
                </p>
              </div>
              <div className="pt-4 border-t border-line/50 mt-auto">
                <div className="text-[11px] font-mono text-accent mb-2">
                  {course.technologies.slice(0, 3).map((t) => t.name).join(', ')}
                </div>
                <div className="text-xs font-mono font-medium text-[var(--text-primary)] flex items-center justify-between">
                  <span>Explore Curriculum</span>
                  <span className="group-hover:translate-x-1 transition-transform" aria-hidden="true">
                    &rarr;
                  </span>
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
