import React from 'react';
import Link from 'next/link';
import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';
import jwt from 'jsonwebtoken';
import db from '@/lib/db';
import { getJwtSecret } from '@/lib/env';
import s from '../admin.module.css';
import LeadsDashboardClient from './LeadsDashboardClient';
import { pageMetadata } from '@/lib/seo';


export const metadata = pageMetadata('/admin/leads');

export default async function AdminLeadsPage() {
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

  // Fetch all leads
  const [startups, contacts, consultations, demos, enrollments, collaborations, pendingCohorts] = await Promise.all([
    db.startupRegistration.findMany({ orderBy: { createdAt: 'desc' } }),
    db.contactSubmission.findMany({ orderBy: { createdAt: 'desc' } }),
    db.consultationBooking.findMany({ orderBy: { createdAt: 'desc' } }),
    db.demoRequest.findMany({ orderBy: { createdAt: 'desc' } }),
    db.enrollmentInquiry.findMany({ orderBy: { createdAt: 'desc' } }),
    db.collaborationRequest.findMany({ orderBy: { createdAt: 'desc' } }),
    db.cohortApplication.count({ where: { cohortSlug: 'aivara', status: 'pending' } }),
  ]);

  return (
    <div className={`container ${s.page}`}>
      <div className={s.pageHead}>
        <div>
          <h1 className={s.pageTitle}>DBERT Admin Dashboard</h1>
        </div>
        <div className={s.headActions}>
          <Link href="/admin/cohort-applications" className="btn btn-primary btn-sm">
            Aivara Cohort ({pendingCohorts})
          </Link>
          <Link href="/admin/alkame-contributors" className="btn btn-outline btn-sm">
            Alkame Contribs
          </Link>
          <form action="/api/admin/logout" method="POST">
            <button type="submit" className="btn btn-outline btn-sm">Logout</button>
          </form>
        </div>
      </div>
      
      <LeadsDashboardClient 
        startups={startups} 
        contacts={contacts}
        consultations={consultations}
        demos={demos}
        enrollments={enrollments}
        collaborations={collaborations}
      />
    </div>
  );
}
