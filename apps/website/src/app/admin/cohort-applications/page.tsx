import React from 'react';
import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';
import jwt from 'jsonwebtoken';
import db from '@/lib/db';
import { getJwtSecret } from '@/lib/env';
import s from '../admin.module.css';
import CohortApplicationsClient from './CohortApplicationsClient';
import { pageMetadata } from '@/lib/seo';
import Link from 'next/link';

export const metadata = pageMetadata('/admin/cohort-applications');

export default async function CohortApplicationsPage() {
  const cookieStore = await cookies();
  const token = cookieStore.get('admin_token')?.value;

  if (!token) {
    redirect('/admin/login');
  }

  const jwtSecret = getJwtSecret();

  try {
    jwt.verify(token, jwtSecret);
  } catch {
    redirect('/admin/login');
  }

  const applications = await db.cohortApplication.findMany({
    where: { cohortSlug: 'aivara' },
    orderBy: { createdAt: 'desc' },
  });

  return (
    <div className={`container ${s.page}`}>
      <div className={s.pageHead}>
        <div>
          <h1 className={s.pageTitle}>Aivara Cohort Applications</h1>
          <p className={s.pageSub}>
            Review candidate applications, examine academics and family background, and trigger decision outcomes.
          </p>
        </div>
        <div className={s.headActions}>
          <Link href="/admin/leads" className="btn btn-outline btn-sm">
            ← Leads Dashboard
          </Link>
          <Link href="/admin/alkame-contributors" className="btn btn-outline btn-sm">
            Alkame Contribs
          </Link>
          <form action="/api/admin/logout" method="POST">
            <button type="submit" className="btn btn-outline btn-sm">
              Logout
            </button>
          </form>
        </div>
      </div>

      <CohortApplicationsClient initialApplications={applications} />
    </div>
  );
}
