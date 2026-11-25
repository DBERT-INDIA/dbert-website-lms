'use client';

import { Calendar } from 'lucide-react';
import { trackEvent } from '@/lib/analytics';
import PublicForm from './PublicForm';
import f from './forms.module.css';
import styles from './MultiStepForm.module.css';

export default function ConsultationForm() {
  return (
    <PublicForm
      endpoint="/api/consultation"
      title="Request an AI consultation"
      submitLabel="Request consultation"
      pendingLabel="Submitting request…"
      confirmationTitle="Consultation requested"
      confirmationCopy="Our enterprise team will review your request and contact you to confirm a time."
      confirmationIcon={<Calendar aria-hidden="true" />}
      restartLabel="Request another consultation"
      onSuccess={(fields) => trackEvent('generate_lead', {
        form_name: 'consultation_form',
        service_type: fields.serviceType,
        company_size: fields.companySize,
      })}
    >
      {(id) => (
        <>
          <div className={styles.fieldGroup}>
            <label htmlFor={id + '-name'}>Full name *</label>
            <input id={id + '-name'} name="name" autoComplete="name" minLength={2} maxLength={150} required />
          </div>
          <div className={styles.fieldGroup}>
            <label htmlFor={id + '-email'}>Work email *</label>
            <input id={id + '-email'} type="email" name="email" autoComplete="email" maxLength={254} required />
          </div>
          <div className={styles.fieldGroup}>
            <label htmlFor={id + '-phone'}>Phone number *</label>
            <input id={id + '-phone'} type="tel" name="phone" autoComplete="tel" maxLength={30} required />
          </div>
          <div className={styles.fieldGroup}>
            <label htmlFor={id + '-company'}>Company name</label>
            <input id={id + '-company'} name="companyName" autoComplete="organization" maxLength={200} />
          </div>
          <div className={styles.fieldGroup}>
            <label htmlFor={id + '-company-size'}>Company size</label>
            <select id={id + '-company-size'} name="companySize" defaultValue="">
              <option value="">Select company size</option>
              <option value="1-10">1–10 employees</option>
              <option value="11-50">11–50 employees</option>
              <option value="51-200">51–200 employees</option>
              <option value="201-500">201–500 employees</option>
              <option value="500+">500+ employees</option>
            </select>
          </div>
          <div className={styles.fieldGroup}>
            <label htmlFor={id + '-service'}>Service type *</label>
            <select id={id + '-service'} name="serviceType" defaultValue="Discovery" required>
              <option value="Discovery">Discovery &amp; strategy</option>
              <option value="Architecture">System architecture</option>
              <option value="Implementation">Custom implementation</option>
              <option value="Optimization">Model optimization</option>
            </select>
          </div>
          <div className={styles.fieldGroup}>
            <label htmlFor={id + '-date'}>Preferred date</label>
            <input id={id + '-date'} type="date" name="preferredDate" />
          </div>
          <div className={[styles.fieldGroup, f.publicFieldWide].join(' ')}>
            <label htmlFor={id + '-description'}>Project description</label>
            <textarea id={id + '-description'} name="description" maxLength={4000} rows={4} />
          </div>
        </>
      )}
    </PublicForm>
  );
}
