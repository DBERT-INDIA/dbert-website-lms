'use client';

import { CircleCheck } from 'lucide-react';
import { trackEvent } from '@/lib/analytics';
import PublicForm from './PublicForm';
import f from './forms.module.css';
import styles from './MultiStepForm.module.css';

export default function ContactForm({ sourcePage = '/about/contact' }: { sourcePage?: string }) {
  return (
    <PublicForm
      endpoint="/api/contact"
      title="Send us a message"
      submitLabel="Send message"
      pendingLabel="Sending message…"
      confirmationTitle="Message sent"
      confirmationCopy="Thank you for reaching out. A member of the DBERT team will get back to you."
      confirmationIcon={<CircleCheck aria-hidden="true" />}
      restartLabel="Send another message"
      context={{ sourcePage }}
      onSuccess={() => trackEvent('contact_form_submit', { source_page: sourcePage })}
    >
      {(id) => (
        <>
          <div className={styles.fieldGroup}>
            <label htmlFor={id + '-name'}>Full name *</label>
            <input id={id + '-name'} name="name" autoComplete="name" minLength={2} maxLength={150} required />
          </div>
          <div className={styles.fieldGroup}>
            <label htmlFor={id + '-email'}>Email address *</label>
            <input id={id + '-email'} type="email" name="email" autoComplete="email" maxLength={254} required />
          </div>
          <div className={styles.fieldGroup}>
            <label htmlFor={id + '-phone'}>Phone or WhatsApp</label>
            <input id={id + '-phone'} type="tel" name="phone" autoComplete="tel" maxLength={30} />
          </div>
          <div className={styles.fieldGroup}>
            <label htmlFor={id + '-subject'}>Subject *</label>
            <input id={id + '-subject'} name="subject" minLength={2} maxLength={200} required />
          </div>
          <div className={[styles.fieldGroup, f.publicFieldWide].join(' ')}>
            <label htmlFor={id + '-message'}>Message *</label>
            <textarea id={id + '-message'} name="message" minLength={5} maxLength={5000} rows={5} required />
          </div>
        </>
      )}
    </PublicForm>
  );
}
