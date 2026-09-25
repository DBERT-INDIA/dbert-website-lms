'use client';

import React, { useState } from 'react';
import s from '../admin.module.css';
import cs from '@/components/cohorts/cohort.module.css';
import { ExternalLink, CheckCircle, Award, XCircle, Search, Filter, Clock, FileText, X } from 'lucide-react';

interface CohortApp {
  id: string;
  cohortSlug: string;
  fullName: string;
  email: string;
  phone: string;
  city: string;
  state: string;
  college: string;
  degree: string;
  graduationYear: string;
  cgpaOrPercentage: string | null;
  domain: string;
  cvUrl: string;
  linkedinUrl: string | null;
  githubUrl: string | null;
  portfolioUrl: string | null;
  familyBackground: string;
  motivation: string | null;
  availability: string | null;
  termsConsent: boolean;
  newsletterConsent: boolean;
  status: string;
  adminNotes: string | null;
  reviewedAt: Date | string | null;
  reviewedBy: string | null;
  emailSent: boolean;
  emailSentAt: Date | string | null;
  emailTypeSent: string | null;
  emailResponseLog: string | null;
  createdAt: Date | string;
}

type TabType = 'all' | 'pending' | 'approved' | 'approved_certified' | 'rejected';

export default function CohortApplicationsClient({
  initialApplications,
}: {
  initialApplications: CohortApp[];
}) {
  const [applications, setApplications] = useState<CohortApp[]>(initialApplications);
  const [activeTab, setActiveTab] = useState<TabType>('pending');
  const [selectedDomain, setSelectedDomain] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedApp, setSelectedApp] = useState<CohortApp | null>(null);
  const [adminNotes, setAdminNotes] = useState<string>('');
  const [processingId, setProcessingId] = useState<string | null>(null);
  const [notification, setNotification] = useState<{ type: 'success' | 'error'; message: string } | null>(null);

  const counts = {
    all: applications.length,
    pending: applications.filter(a => a.status === 'pending').length,
    approved: applications.filter(a => a.status === 'approved').length,
    approved_certified: applications.filter(a => a.status === 'approved_certified').length,
    rejected: applications.filter(a => a.status === 'rejected').length,
  };

  const filteredApps = applications.filter(app => {
    // Status filter
    if (activeTab !== 'all' && app.status !== activeTab) {
      return false;
    }
    // Domain filter
    if (selectedDomain !== 'all' && app.domain !== selectedDomain) {
      return false;
    }
    // Search query
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      const matchName = app.fullName.toLowerCase().includes(q);
      const matchEmail = app.email.toLowerCase().includes(q);
      const matchCollege = app.college.toLowerCase().includes(q);
      const matchCity = app.city.toLowerCase().includes(q);
      if (!matchName && !matchEmail && !matchCollege && !matchCity) {
        return false;
      }
    }
    return true;
  });

  const openDetailModal = (app: CohortApp) => {
    setSelectedApp(app);
    setAdminNotes(app.adminNotes || '');
    setNotification(null);
  };

  const closeModal = () => {
    setSelectedApp(null);
    setAdminNotes('');
  };

  const handleDecision = async (
    id: string,
    decision: 'approved' | 'approved_certified' | 'rejected'
  ) => {
    setProcessingId(id);
    setNotification(null);

    try {
      const res = await fetch('/api/admin/cohort-applications', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          id,
          decision,
          adminNotes: adminNotes.trim() || undefined,
        }),
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.error || 'Failed to update cohort application decision.');
      }

      const updated = data.application;

      setApplications(prev =>
        prev.map(item => (item.id === id ? { ...item, ...updated } : item))
      );

      if (selectedApp && selectedApp.id === id) {
        setSelectedApp(prev => (prev ? { ...prev, ...updated } : null));
      }

      setNotification({
        type: 'success',
        message: `Decision marked as "${decision.replace('_', ' ')}". Email API dispatched.`,
      });
    } catch (err) {
      setNotification({
        type: 'error',
        message: err instanceof Error ? err.message : 'Error updating decision',
      });
    } finally {
      setProcessingId(null);
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'approved':
        return <span className={`${s.statusChip} ${cs.statusApproved}`}>Approved</span>;
      case 'approved_certified':
        return <span className={`${s.statusChip} ${cs.statusCertified}`}>Certified Track</span>;
      case 'rejected':
        return <span className={`${s.statusChip} ${cs.statusRejected}`}>Rejected</span>;
      default:
        return <span className={`${s.statusChip} ${cs.statusPending}`}>Pending Review</span>;
    }
  };

  return (
    <div>
      {/* Top Tabs */}
      <div className={s.tabBar}>
        {(['pending', 'approved', 'approved_certified', 'rejected', 'all'] as TabType[]).map(tab => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`${s.tab} ${activeTab === tab ? s.tabActive : ''}`}
          >
            {tab === 'approved_certified'
              ? 'Certified Track'
              : tab.charAt(0).toUpperCase() + tab.slice(1)}{' '}
            ({counts[tab]})
          </button>
        ))}
      </div>

      {/* Filter and Search Bar */}
      <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap', margin: '16px 0 24px' }}>
        <div style={{ position: 'relative', flex: '1', minWidth: '220px' }}>
          <input
            type="text"
            placeholder="Search candidate by name, email, or college..."
            value={searchQuery}
            onChange={e => setSearchQuery(e.target.value)}
            style={{
              width: '100%',
              padding: '8px 12px',
              background: 'rgba(255, 255, 255, 0.03)',
              border: '1px solid var(--line)',
              borderRadius: '6px',
              color: 'var(--fg)',
              fontSize: '0.88rem',
            }}
          />
        </div>

        <select
          value={selectedDomain}
          onChange={e => setSelectedDomain(e.target.value)}
          style={{
            padding: '8px 12px',
            background: 'rgba(255, 255, 255, 0.03)',
            border: '1px solid var(--line)',
            borderRadius: '6px',
            color: 'var(--fg)',
            fontSize: '0.88rem',
          }}
        >
          <option value="all">All Domains (5 tracks)</option>
          <option value="AI Agent Development">AI Agent Development</option>
          <option value="Full Stack Development">Full Stack Development</option>
          <option value="Python Automation">Python Automation</option>
          <option value="Data Analytics">Data Analytics</option>
          <option value="Data Engineering / Machine Learning">Data Engineering / ML</option>
        </select>
      </div>

      {notification && (
        <div
          style={{
            padding: '10px 14px',
            marginBottom: '16px',
            borderRadius: '6px',
            fontSize: '0.88rem',
            background:
              notification.type === 'success'
                ? 'rgba(34, 197, 94, 0.15)'
                : 'rgba(239, 68, 68, 0.15)',
            color: notification.type === 'success' ? '#4ade80' : '#f87171',
            border: `1px solid ${notification.type === 'success' ? 'rgba(34, 197, 94, 0.3)' : 'rgba(239, 68, 68, 0.3)'}`,
          }}
        >
          {notification.message}
        </div>
      )}

      {/* Applications Table */}
      {filteredApps.length === 0 ? (
        <p className={s.noResults}>No applications found under this view.</p>
      ) : (
        <div className={`card ${s.scrollCard}`}>
          <table className={s.leadsTable}>
            <thead>
              <tr>
                <th className="cell">Date</th>
                <th className="cell">Applicant</th>
                <th className="cell">Track / Domain</th>
                <th className="cell">College &amp; Degree</th>
                <th className="cell">CV / Links</th>
                <th className="cell">Status</th>
                <th className="cell">Action</th>
              </tr>
            </thead>
            <tbody>
              {filteredApps.map(app => (
                <tr key={app.id}>
                  <td className="cell-sm">
                    {new Date(app.createdAt).toLocaleDateString()}
                  </td>
                  <td className={s.nameCell}>
                    <strong>{app.fullName}</strong>
                    <div className="cell-xs" style={{ color: 'var(--muted)', marginTop: '2px' }}>
                      {app.email}
                      <br />
                      {app.phone} • {app.city}, {app.state}
                    </div>
                  </td>
                  <td className="cell-sm">
                    <span className={cs.adminDomainBadge}>{app.domain}</span>
                  </td>
                  <td className="cell-sm">
                    <div style={{ maxWidth: '200px' }}>
                      <strong>{app.college}</strong>
                      <div className="cell-xs" style={{ color: 'var(--muted)' }}>
                        {app.degree} ({app.graduationYear})
                        {app.cgpaOrPercentage ? ` • CGPA: ${app.cgpaOrPercentage}` : ''}
                      </div>
                    </div>
                  </td>
                  <td className="cell-sm">
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                      <a
                        href={app.cvUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="btn btn-outline btn-xs"
                        style={{ display: 'inline-flex', alignItems: 'center', gap: '4px' }}
                      >
                        <FileText size={12} /> View CV ↗
                      </a>
                      <div style={{ display: 'flex', gap: '6px' }}>
                        {app.linkedinUrl && (
                          <a
                            href={app.linkedinUrl}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="cell-xs"
                            style={{ color: 'var(--accent)' }}
                          >
                            LinkedIn
                          </a>
                        )}
                        {app.githubUrl && (
                          <a
                            href={app.githubUrl}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="cell-xs"
                            style={{ color: 'var(--accent)' }}
                          >
                            GitHub
                          </a>
                        )}
                      </div>
                    </div>
                  </td>
                  <td className="cell-sm">{getStatusBadge(app.status)}</td>
                  <td className="cell-sm">
                    <button
                      onClick={() => openDetailModal(app)}
                      className="btn btn-outline btn-sm"
                    >
                      Review
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Candidate Dossier Detail Modal */}
      {selectedApp && (
        <div className={cs.modalOverlay} onClick={closeModal}>
          <div className={cs.modalContent} onClick={e => e.stopPropagation()}>
            <div className={cs.modalHead}>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <h3 className={cs.modalTitle}>{selectedApp.fullName}</h3>
                  {getStatusBadge(selectedApp.status)}
                </div>
                <div className="cell-xs" style={{ color: 'var(--muted)', marginTop: '4px' }}>
                  Applied: {new Date(selectedApp.createdAt).toLocaleString()} • Ref: {selectedApp.id}
                </div>
              </div>
              <button
                onClick={closeModal}
                style={{
                  background: 'none',
                  border: 'none',
                  color: 'var(--muted)',
                  cursor: 'pointer',
                  padding: '4px',
                }}
              >
                <X size={20} />
              </button>
            </div>

            {/* Academic & Personal Profile */}
            <div className={cs.detailSection}>
              <div className={cs.detailSectionTitle}>Contact &amp; Academics</div>
              <div className={cs.detailBox}>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
                  <div><strong>Email:</strong> {selectedApp.email}</div>
                  <div><strong>Phone / WA:</strong> {selectedApp.phone}</div>
                  <div><strong>Location:</strong> {selectedApp.city}, {selectedApp.state}</div>
                  <div><strong>Graduation:</strong> {selectedApp.graduationYear}</div>
                  <div><strong>College:</strong> {selectedApp.college}</div>
                  <div><strong>Degree:</strong> {selectedApp.degree}</div>
                  <div><strong>CGPA / Score:</strong> {selectedApp.cgpaOrPercentage || 'Not specified'}</div>
                  <div><strong>Earliest Availability:</strong> {selectedApp.availability || 'Immediate'}</div>
                </div>
              </div>
            </div>

            {/* Track, CV & Online Links */}
            <div className={cs.detailSection}>
              <div className={cs.detailSectionTitle}>Internship Track &amp; Links</div>
              <div className={cs.detailBox}>
                <div style={{ marginBottom: '10px' }}>
                  <strong>Selected Domain:</strong>{' '}
                  <span className={cs.adminDomainBadge}>{selectedApp.domain}</span>
                </div>
                <div className={cs.linkRow}>
                  <a
                    href={selectedApp.cvUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn btn-primary btn-sm"
                    style={{ display: 'inline-flex', alignItems: 'center', gap: '6px' }}
                  >
                    <ExternalLink size={14} /> Open Candidate CV / Resume
                  </a>
                  {selectedApp.linkedinUrl && (
                    <a
                      href={selectedApp.linkedinUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="btn btn-outline btn-sm"
                    >
                      LinkedIn Profile ↗
                    </a>
                  )}
                  {selectedApp.githubUrl && (
                    <a
                      href={selectedApp.githubUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="btn btn-outline btn-sm"
                    >
                      GitHub Profile ↗
                    </a>
                  )}
                  {selectedApp.portfolioUrl && (
                    <a
                      href={selectedApp.portfolioUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="btn btn-outline btn-sm"
                    >
                      Portfolio / Work ↗
                    </a>
                  )}
                </div>
              </div>
            </div>

            {/* Family Background Statement */}
            <div className={cs.detailSection}>
              <div className={cs.detailSectionTitle}>Family Background Statement</div>
              <div className={cs.detailBox} style={{ whiteSpace: 'pre-wrap' }}>
                {selectedApp.familyBackground}
              </div>
            </div>

            {/* Motivation Statement */}
            {selectedApp.motivation && (
              <div className={cs.detailSection}>
                <div className={cs.detailSectionTitle}>Motivation / Purpose</div>
                <div className={cs.detailBox} style={{ whiteSpace: 'pre-wrap' }}>
                  {selectedApp.motivation}
                </div>
              </div>
            )}

            {/* Newsletter & Consents */}
            <div className={cs.detailSection}>
              <div className={cs.detailSectionTitle}>Consents &amp; Permissions</div>
              <div className="cell-sm" style={{ color: 'var(--muted)' }}>
                ✓ Terms &amp; Conditions Accepted: <strong>Yes</strong>
                <br />
                {selectedApp.newsletterConsent ? '✓' : '✗'} Future Contact &amp; Newsletter Consent:{' '}
                <strong>{selectedApp.newsletterConsent ? 'Subscribed' : 'No'}</strong>
              </div>
            </div>

            {/* Review Status & Email Audit Log */}
            {selectedApp.reviewedAt && (
              <div className={cs.detailSection}>
                <div className={cs.detailSectionTitle}>Review &amp; Email Dispatch Audit</div>
                <div className={cs.detailBox}>
                  <div><strong>Reviewed By:</strong> {selectedApp.reviewedBy || 'Admin'}</div>
                  <div><strong>Reviewed At:</strong> {new Date(selectedApp.reviewedAt).toLocaleString()}</div>
                  <div>
                    <strong>Email Status:</strong>{' '}
                    {selectedApp.emailSent ? 'Sent Successfully' : 'Not sent / Failed'} (Type: {selectedApp.emailTypeSent})
                  </div>
                  {selectedApp.emailResponseLog && (
                    <div className="cell-xs" style={{ color: 'var(--muted)', marginTop: '4px', fontFamily: 'monospace' }}>
                      Log: {selectedApp.emailResponseLog}
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* 3 Decision Actions Section */}
            <div className={cs.decisionSection}>
              <div className={cs.detailSectionTitle}>
                Admin Decision: Select 1 of 3 Actions
              </div>

              <div style={{ marginBottom: '12px' }}>
                <label style={{ fontSize: '0.82rem', color: 'var(--muted)', display: 'block', marginBottom: '4px' }}>
                  Reviewer Notes / Feedback (included in official notification email):
                </label>
                <textarea
                  rows={2}
                  value={adminNotes}
                  onChange={e => setAdminNotes(e.target.value)}
                  placeholder="Optional custom feedback or onboarding instruction..."
                  style={{
                    width: '100%',
                    padding: '8px 12px',
                    background: 'rgba(255, 255, 255, 0.03)',
                    border: '1px solid var(--line)',
                    borderRadius: '6px',
                    color: 'var(--fg)',
                    fontSize: '0.88rem',
                  }}
                />
              </div>

              <div className={cs.decisionButtons}>
                {/* 1. Approved */}
                <button
                  onClick={() => handleDecision(selectedApp.id, 'approved')}
                  disabled={processingId === selectedApp.id}
                  className="btn btn-primary btn-sm"
                  style={{ display: 'inline-flex', alignItems: 'center', gap: '6px' }}
                >
                  <CheckCircle size={15} />
                  1. Approve
                </button>

                {/* 2. Approved with Certification */}
                <button
                  onClick={() => handleDecision(selectedApp.id, 'approved_certified')}
                  disabled={processingId === selectedApp.id}
                  className="btn btn-outline btn-sm"
                  style={{
                    borderColor: '#a855f7',
                    color: '#c084fc',
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '6px',
                  }}
                >
                  <Award size={15} />
                  2. Approve with Certification
                </button>

                {/* 3. Rejected */}
                <button
                  onClick={() => handleDecision(selectedApp.id, 'rejected')}
                  disabled={processingId === selectedApp.id}
                  className="btn btn-outline btn-sm"
                  style={{
                    borderColor: 'rgba(239, 68, 68, 0.4)',
                    color: '#f87171',
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '6px',
                  }}
                >
                  <XCircle size={15} />
                  3. Reject
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
