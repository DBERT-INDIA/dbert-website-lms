import React from 'react';
import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';
import jwt from 'jsonwebtoken';
import db from '@/lib/db';
import { getJwtSecret } from '@/lib/env';
import s from '../admin.module.css';
import AlkameContributorsClient from './AlkameContributorsClient';
import { pageMetadata } from '@/lib/seo';


export const metadata = pageMetadata('/admin/alkame-contributors');

export default async function AlkameContributorsPage() {
  const cookieStore = await cookies();
  const token = cookieStore.get('admin_token')?.value;

  if (!token) {
    redirect('/admin/login');
  }

  // Read the secret outside the try: a missing JWT_SECRET is a server
  // misconfiguration, not a failed login, and must not redirect to the form.
  const jwtSecret = getJwtSecret();

  try {
    jwt.verify(token, jwtSecret);
  } catch {
    redirect('/admin/login');
  }

  const contributors = await db.projectContributor.findMany({
    where: { projectSlug: 'alkame' },
    orderBy: { createdAt: 'desc' },
  });

  return (
    <div className={`container ${s.page}`}>
      <div className={s.pageHead}>
        <div>
          <h1 className={s.pageTitle}>Alkame Contributors</h1>
          <p className={s.pageSub}>
            Review intern submissions before they appear publicly on the Alkame case study page.
          </p>
        </div>
        <div className={s.headActions}>
          <a href="/admin/leads" className="btn btn-outline btn-sm">← Back to Leads</a>
          <form action="/api/admin/logout" method="POST">
            <button type="submit" className="btn btn-outline btn-sm">Logout</button>
          </form>
        </div>
      </div>

      <AlkameContributorsClient contributors={contributors} />
    </div>
  );
}
