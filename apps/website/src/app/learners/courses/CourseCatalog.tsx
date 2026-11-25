'use client';

import { useId, useRef, useState } from 'react';
import Link from 'next/link';
import { courseCategories, courses } from './catalog';
import styles from './catalog.module.css';

export default function CourseCatalog() {
  const id = useId();
  const search = useRef<HTMLInputElement>(null);
  const [query, setQuery] = useState('');
  const [category, setCategory] = useState('');
  const terms = query.trim().toLowerCase().split(/\s+/).filter(Boolean);
  const results = courses.filter((course) => {
    const searchable = `${course.title} ${course.tech} ${course.description}`.toLowerCase();
    return (!category || course.category === category) && terms.every((term) => searchable.includes(term));
  });
  const isFiltered = Boolean(query || category);

  return (
    <section className={styles.catalog} aria-labelledby="catalog-heading">
      <h2 id="catalog-heading">Find a course</h2>
      <div className={styles.controls}>
        <div className={styles.field}>
          <label htmlFor={id + '-query'}>Search by course or technology</label>
          <input
            ref={search}
            id={id + '-query'}
            type="search"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Search Python, React, or Figma"
          />
        </div>
        <div className={styles.field}>
          <label htmlFor={id + '-category'}>Category</label>
          <select id={id + '-category'} value={category} onChange={(event) => setCategory(event.target.value)}>
            <option value="">All categories</option>
            {Object.entries(courseCategories).map(([key, label]) => (
              <option key={key} value={key}>{label}</option>
            ))}
          </select>
        </div>
        <button
          type="button"
          className="btn btn-outline btn-sm"
          disabled={!isFiltered}
          onClick={() => { setQuery(''); setCategory(''); search.current?.focus(); }}
        >
          Clear filters
        </button>
      </div>
      <p className={styles.summary} role="status">
        {results.length} {results.length === 1 ? 'course' : 'courses'}
        {isFiltered && ' found'}
      </p>
      {results.length > 0 ? (
        <ul className={styles.grid}>
          {results.map((course) => (
            <li key={course.href}>
              <Link href={course.href} prefetch={false} className={`card ${styles.card}`}>
                <div className={styles.meta}>
                  <span className="tag-chip">{courseCategories[course.category]}</span>
                  <span>{course.duration}</span>
                </div>
                <h3>{course.title}</h3>
                <p>{course.description}</p>
                <div className={styles.technologies}>{course.tech}</div>
                <span className={styles.syllabus}>View syllabus <span aria-hidden="true">→</span></span>
              </Link>
            </li>
          ))}
        </ul>
      ) : (
        <div className={styles.empty}>
          <p>Try a different technology or choose another category.</p>
        </div>
      )}
    </section>
  );
}
