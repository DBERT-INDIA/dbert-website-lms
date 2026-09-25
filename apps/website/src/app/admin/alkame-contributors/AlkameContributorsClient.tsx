'use client';

import s from '../admin.module.css';

import React, { useState } from 'react';

interface Contributor {
  id: string;
  name: string;
  email: string;
  profilePicUrl: string;
  comment: string;
  linkedinUrl: string;
  githubUrl: string;
  domain: string;
  status: string;
  createdAt: Date;
  reviewedAt: Date | null;
}

type Tab = 'pending' | 'approved' | 'rejected';

export default function AlkameContributorsClient({ contributors: initialContributors }: { contributors: Contributor[] }) {
  const [contributors, setContributors] = useState<Contributor[]>(initialContributors);
  const [activeTab, setActiveTab] = useState<Tab>('pending');
  const [pendingActionId, setPendingActionId] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const filtered = contributors.filter((c) => c.status === activeTab);
  const counts = {
    pending: contributors.filter((c) => c.status === 'pending').length,
    approved: contributors.filter((c) => c.status === 'approved').length,
    rejected: contributors.filter((c) => c.status === 'rejected').length,
  };

  async function handleDecision(id: string, status: 'approved' | 'rejected') {
    setPendingActionId(id);
    setErrorMessage(null);
    try {
      const res = await fetch('/api/admin/alkame-contributors', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id, status }),
      });

      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.error || 'Failed to update status');
      }

      setContributors((prev) =>
        prev.map((c) => (c.id === id ? { ...c, status, reviewedAt: new Date() } : c))
      );
    } catch (err) {
      setErrorMessage(err instanceof Error ? err.message : 'Something went wrong');
    } finally {
      setPendingActionId(null);
    }
  }

  const tabs: Tab[] = ['pending', 'approved', 'rejected'];

  return (
    <div>
      <div className={s.tabBar}>
        {tabs.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`${s.tab}${activeTab === tab ? ` ${s.tabActive}` : ''}`}
          >
            {tab} ({counts[tab]})
          </button>
        ))}
      </div>

      {errorMessage && (
        <div className={s.errorBanner}>
          {errorMessage}
        </div>
      )}

      {filtered.length === 0 ? (
        <p className={s.noResults}>No {activeTab} submissions.</p>
      ) : (
        <div className={s.scroll}>
          <table className={s.contribTable}>
            <thead>
              <tr>
                <th className="cell-xs">Name</th>
                <th className="cell-xs">Email</th>
                <th className="cell-xs">Domain</th>
                <th className="cell-xs">Comment</th>
                <th className="cell-xs">Links</th>
                <th className="cell-xs">Submitted</th>
                {activeTab === 'pending' && (
                  <th className="cell-xs">Actions</th>
                )}
              </tr>
            </thead>
            <tbody>
              {filtered.map((c) => (
                <tr key={c.id}>
                  <td className={s.contribCell}>{c.name}</td>
                  <td className={s.contribCell}>{c.email}</td>
                  <td className={s.contribCell}>{c.domain}</td>
                  <td className={`${s.contribCell} ${s.commentCell}`}>{c.comment}</td>
                  <td className={s.contribCell}>
                    <a href={c.linkedinUrl} target="_blank" rel="noopener noreferrer" className={`${s.rowLink} ${s.rowLinkSpaced}`}>LinkedIn ↗</a>
                    <a href={c.githubUrl} target="_blank" rel="noopener noreferrer" className={s.rowLink}>GitHub ↗</a>
                  </td>
                  <td className="cell-xs">
                    {new Date(c.createdAt).toLocaleDateString()}
                  </td>
                  {activeTab === 'pending' && (
                    <td className={s.actionCell}>
                      <button
                        onClick={() => handleDecision(c.id, 'approved')}
                        disabled={pendingActionId === c.id}
                        className={`btn btn-primary btn-sm ${s.actionGap}`}
                      >
                        Approve
                      </button>
                      <button
                        onClick={() => handleDecision(c.id, 'rejected')}
                        disabled={pendingActionId === c.id}
                        className="btn btn-outline btn-sm"
                      >
                        Reject
                      </button>
                    </td>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
