'use client';

import { useId, useRef, useState, type FormEvent, type ReactNode } from 'react';
import f from './forms.module.css';
import styles from './MultiStepForm.module.css';

interface PublicFormProps {
  endpoint: string;
  title: string;
  description?: string;
  submitLabel: string;
  pendingLabel: string;
  confirmationTitle: string;
  confirmationCopy: string;
  confirmationIcon: ReactNode;
  restartLabel: string;
  context?: Record<string, string>;
  onSuccess: (fields: Record<string, string>) => void;
  children: (id: string) => ReactNode;
}

export default function PublicForm({
  endpoint,
  title,
  description,
  submitLabel,
  pendingLabel,
  confirmationTitle,
  confirmationCopy,
  confirmationIcon,
  restartLabel,
  context,
  onSuccess,
  children,
}: PublicFormProps) {
  const id = useId();
  const pending = useRef(false);
  const restarting = useRef(false);
  const [status, setStatus] = useState<'ready' | 'pending' | 'success'>('ready');
  const [error, setError] = useState('');

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (pending.current) return;

    const fields = { ...context };
    for (const [name, value] of new FormData(event.currentTarget)) {
      if (typeof value === 'string') fields[name] = value.trim();
    }

    setStatus('pending');
    setError('');
    pending.current = true;
    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(fields),
      });
      const data: { success?: unknown; error?: unknown } | null = await response.json().catch(() => null);
      if (!response.ok || data?.success !== true) {
        setError(typeof data?.error === 'string' ? data.error : 'Your request could not be confirmed. Please try again.');
        setStatus('ready');
        return;
      }
    } catch {
      setError('We could not reach DBERT. Check your connection and try again.');
      setStatus('ready');
      return;
    } finally {
      pending.current = false;
    }

    setStatus('success');
    onSuccess(fields);
  }

  if (status === 'success') {
    return (
      <div className={`card ${f.statePanel}`}>
        <span className="icon-chip">{confirmationIcon}</span>
        <h2 className="card-title" tabIndex={-1} ref={(heading) => { heading?.focus(); }}>
          {confirmationTitle}
        </h2>
        <p className={f.hint}>{confirmationCopy}</p>
        <button
          type="button"
          className="btn btn-outline btn-sm"
          onClick={() => { restarting.current = true; setStatus('ready'); }}
        >
          {restartLabel}
        </button>
      </div>
    );
  }

  return (
    <div className={f.narrowForm}>
      <form
        className={`card ${f.publicForm}`}
        method="post"
        onSubmit={handleSubmit}
        aria-labelledby={`${id}-title`}
      >
        <div>
          <h2
            className={styles.stepTitle}
            id={`${id}-title`}
            tabIndex={-1}
            ref={(heading) => {
              if (heading && restarting.current) {
                restarting.current = false;
                heading.focus();
              }
            }}
          >
            {title}
          </h2>
          {description && <p className={f.mutedCopy}>{description}</p>}
          <p className={f.requiredHint}>Fields marked * are required.</p>
        </div>
        <div className={error ? styles.errorAlert : undefined} role="alert">{error}</div>
        <div className={f.publicFields}>{children(id)}</div>
        <button type="submit" className="btn btn-primary" aria-disabled={status === 'pending'}>
          {status === 'pending' ? pendingLabel : submitLabel}
        </button>
        <span className="sr-only" role="status">{status === 'pending' ? pendingLabel : ''}</span>
      </form>
    </div>
  );
}
