import type { Metadata } from 'next';
import Link from 'next/link';
import navigation from '@/data/nav.config.json';
import { pageMetadata } from '@/lib/seo';
import { courses } from '../learners/courses/catalog';
import styles from './search.module.css';

export const metadata: Metadata = {
  ...pageMetadata('/search'),
  robots: { index: false, follow: true },
};

type SearchEntry = {
  href: string;
  label: string;
  area: string;
  description?: string;
  keywords?: string;
};

const popular: SearchEntry[] = [
  { href: '/learners/courses', label: 'Browse courses', area: 'Learners', keywords: 'classes skill tracks training' },
  { href: '/internships', label: 'Find internships', area: 'Careers', keywords: 'jobs roles remote application' },
  { href: '/verify', label: 'Verify a certificate', area: 'Credentials', keywords: 'check proof verify certification' },
  { href: '/about/contact', label: 'Contact DBERT', area: 'Support', keywords: 'help email support questions' },
];

const index = new Map(popular.map((entry) => [entry.href, entry]));
for (const item of navigation.items) {
  const links = item.columns?.flatMap((column) => column.links) ?? item.links ?? (item.href ? [item] : []);
  for (const { href, label } of links) {
    if (href?.startsWith('/') && !index.has(href)) {
      index.set(href, { href, label, area: item.label });
    }
  }
}
for (const course of courses) {
  index.set(course.href, {
    href: course.href,
    label: course.title,
    area: 'Course',
    description: course.description,
    keywords: course.tech,
  });
}

function findPages(query: string) {
  const terms = query.toLowerCase().split(/\s+/);
  return [...index.values()]
    .map((entry) => {
      const title = entry.label.toLowerCase();
      const text = `${title} ${entry.area} ${entry.description ?? ''} ${entry.keywords ?? ''}`.toLowerCase();
      const score = terms.every((term) => text.includes(term))
        ? terms.reduce((sum, term) => sum + (title.includes(term) ? 3 : 1), 0)
        : 0;
      return { entry, score };
    })
    .filter(({ score }) => score > 0)
    .sort((a, b) => b.score - a.score || a.entry.label.localeCompare(b.entry.label))
    .map(({ entry }) => entry);
}

type SearchPageProps = {
  searchParams: Promise<{ q?: string | string[] }>;
};

export default async function SearchPage({ searchParams }: SearchPageProps) {
  const { q } = await searchParams;
  const query = (Array.isArray(q) ? q[0] : q)?.trim().slice(0, 120) ?? '';
  const results = query ? findPages(query) : popular;

  return (
    <section className={`section ${styles.search}`}>
      <h1>Search DBERT</h1>
      <form className={styles.form} role="search" action="/search" method="get">
        <div className={styles.field}>
          <label htmlFor="site-query">Search the website</label>
          <input
            id="site-query"
            name="q"
            type="search"
            defaultValue={query}
            placeholder="Try Python, internships, or verify"
            maxLength={120}
          />
        </div>
        <button type="submit" className="btn btn-primary">Search</button>
      </form>

      <h2 className={styles.resultHeading}>
        {query ? `${results.length} ${results.length === 1 ? 'result' : 'results'} for “${query}”` : 'Popular destinations'}
      </h2>
      {results.length > 0 ? (
        <ul className={styles.results}>
          {results.map((result) => (
            <li key={result.href}>
              <span className="tag-chip">{result.area}</span>
              <Link href={result.href} prefetch={false}>{result.label}</Link>
              {result.description && <p>{result.description}</p>}
            </li>
          ))}
        </ul>
      ) : (
        <p className={styles.empty}>
          Try a different term or <Link href="/search" prefetch={false}>see popular destinations</Link>.
        </p>
      )}
    </section>
  );
}
