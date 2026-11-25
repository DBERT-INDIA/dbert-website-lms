'use client';

import { Rocket } from 'lucide-react';
import { trackEvent } from '@/lib/analytics';
import PublicForm from './PublicForm';
import f from './forms.module.css';
import styles from './MultiStepForm.module.css';

export default function DemoRequestForm({ productName }: { productName: string }) {
  return (
    <PublicForm
      endpoint="/api/demo-request"
      title="Request a demo"
      description={'See how ' + productName + ' could work for your team.'}
      submitLabel="Request demo"
      pendingLabel="Submitting request…"
      confirmationTitle="Demo requested"
      confirmationCopy={'The DBERT product team will contact you to schedule your ' + productName + ' demo.'}
      confirmationIcon={<Rocket aria-hidden="true" />}
      restartLabel="Request another demo"
      context={{ productName }}
      onSuccess={() => trackEvent('generate_lead', { form_name: 'demo_request', product_name: productName })}
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
            <label htmlFor={id + '-phone'}>Phone number</label>
            <input id={id + '-phone'} type="tel" name="phone" autoComplete="tel" maxLength={30} />
          </div>
          <div className={styles.fieldGroup}>
            <label htmlFor={id + '-company'}>Company name</label>
            <input id={id + '-company'} name="companyName" autoComplete="organization" maxLength={200} />
          </div>
          <div className={[styles.fieldGroup, f.publicFieldWide].join(' ')}>
            <label htmlFor={id + '-message'}>What would you like to see in the demo?</label>
            <textarea id={id + '-message'} name="message" maxLength={4000} rows={3} />
          </div>
        </>
      )}
    </PublicForm>
  );
}
