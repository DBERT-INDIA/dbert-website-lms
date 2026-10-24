'use client';

import styles from '../admin.module.css';

import React, { useState } from 'react';

type Tab = 'startups' | 'contacts' | 'consultations' | 'demos' | 'enrollments' | 'collaborations';

interface LeadsDashboardClientProps {
  startups: any[];
  contacts: any[];
  consultations: any[];
  demos: any[];
  enrollments: any[];
  collaborations: any[];
}

export default function LeadsDashboardClient({
  startups,
  contacts,
  consultations,
  demos,
  enrollments,
  collaborations
}: LeadsDashboardClientProps) {
  const [activeTab, setActiveTab] = useState<Tab>('startups');

  const tabs: { key: Tab, label: string, count: number }[] = [
    { key: 'startups', label: 'Startup Incubation', count: startups.length },
    { key: 'demos', label: 'SaaS Demos', count: demos.length },
    { key: 'enrollments', label: 'Learner Enrollments', count: enrollments.length },
    { key: 'consultations', label: 'Consultations', count: consultations.length },
    { key: 'contacts', label: 'General Contacts', count: contacts.length },
    { key: 'collaborations', label: 'Labs Collaboration', count: collaborations.length }
  ];

  return (
    <div>
      <div className={styles.buttonTabs}>
        {tabs.map(tab => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key)}
            className={`btn ${activeTab === tab.key ? 'btn-primary' : 'btn-outline'} ${styles.buttonTab}`}
          >
            {tab.label} <span className={styles.tabCount}>({tab.count})</span>
          </button>
        ))}
      </div>

      <div className={`card ${styles.scrollCard}`}>
        {activeTab === 'startups' && (
          <table className={styles.leadsTable}>
            <thead>
              <tr>
                <th className="cell">Date</th>
                <th className="cell">Startup</th>
                <th className="cell">Founder</th>
                <th className="cell">Contact</th>
                <th className="cell">Stage</th>
                <th className="cell">Status</th>
              </tr>
            </thead>
            <tbody>
              {startups.length === 0 ? <tr><td colSpan={6} className={styles.emptyRow}>No leads yet.</td></tr> : null}
              {startups.map(s => (
                <tr key={s.id}>
                  <td className="cell-sm">{new Date(s.createdAt).toLocaleDateString()}</td>
                  <td className={styles.nameCell}>{s.startupName}</td>
                  <td className="cell-sm">{s.founderName}</td>
                  <td className="cell-sm">{s.email}<br/>{s.phone}</td>
                  <td className="cell-sm">{s.stage}</td>
                  <td className="cell-sm"><span className={styles.statusChip}>{s.status}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        )}

        {activeTab === 'demos' && (
          <table className={styles.leadsTable}>
            <thead>
              <tr>
                <th className="cell">Date</th>
                <th className="cell">Product</th>
                <th className="cell">Name</th>
                <th className="cell">Contact</th>
                <th className="cell">Company</th>
                <th className="cell">Status</th>
              </tr>
            </thead>
            <tbody>
              {demos.length === 0 ? <tr><td colSpan={6} className={styles.emptyRow}>No leads yet.</td></tr> : null}
              {demos.map(d => (
                <tr key={d.id}>
                  <td className="cell-sm">{new Date(d.createdAt).toLocaleDateString()}</td>
                  <td className={`${styles.nameCell} ${styles.accentCell}`}>{d.productName}</td>
                  <td className="cell-sm">{d.name}</td>
                  <td className="cell-sm">{d.email}<br/>{d.phone}</td>
                  <td className="cell-sm">{d.companyName || '-'}</td>
                  <td className="cell-sm"><span className={styles.statusChip}>{d.status}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        )}

        {activeTab === 'enrollments' && (
          <table className={styles.leadsTable}>
            <thead>
              <tr>
                <th className="cell">Date</th>
                <th className="cell">Program</th>
                <th className="cell">Name</th>
                <th className="cell">Contact</th>
                <th className="cell">Payment Status</th>
              </tr>
            </thead>
            <tbody>
              {enrollments.length === 0 ? <tr><td colSpan={5} className={styles.emptyRow}>No leads yet.</td></tr> : null}
              {enrollments.map(e => (
                <tr key={e.id}>
                  <td className="cell-sm">{new Date(e.createdAt).toLocaleDateString()}</td>
                  <td className={styles.nameCell}>{e.programName}</td>
                  <td className="cell-sm">{e.name}</td>
                  <td className="cell-sm">{e.email}<br/>{e.phone}</td>
                  <td className="cell-sm">
                    <span className={`${styles.statusChip}${e.status === 'paid' ? ` ${styles.statusPaid}` : ''}`}>
                      {e.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}

        {/* Other tabs follow the same simple table pattern */}
        {(activeTab === 'consultations' || activeTab === 'contacts' || activeTab === 'collaborations') && (
          <div className={styles.placeholder}>
            Render remaining tables here based on the active tab...
          </div>
        )}
      </div>
    </div>
  );
}
