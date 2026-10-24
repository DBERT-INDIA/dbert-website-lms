import React from 'react';
import Link from 'next/link';
import { Users } from 'lucide-react';
import s from '@/app/blog/blog.module.css';

interface AuthorBoxProps {
  name: string;
  role: string;
  bio: string;
}

/**
 * Reusable author signature card for technical blog articles.
 * Establishes author authority and directs users to the authenticated team roster.
 */
export default function AuthorBox({ name, role, bio }: AuthorBoxProps) {
  return (
    <aside className={`card ${s.authorBox}`} aria-label="Article author information">
      <div className={s.authorIcon}>
        <Users className={s.authorIconSvg} aria-hidden="true" />
      </div>
      <div className={s.authorDetails}>
        <div className={s.authorHeader}>
          <span className="doclabel">§ AUTHOR</span>
          <span className="faint-label">Authored inside DBERT Labs</span>
        </div>
        <h4 className={s.authorName}>{name}</h4>
        <p className={s.authorRole}>{role}</p>
        <p className="body-copy mb-2">{bio}</p>
        <div>
          <Link href="/about/team" className="accent-link">
            Verify researcher profiles &amp; credentials &rarr;
          </Link>
        </div>
      </div>
    </aside>
  );
}
