'use client';

import React, { useEffect, useRef, useState } from 'react';
import { X } from 'lucide-react';
import s from './modal.module.css';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  description?: string;
  children: React.ReactNode;
  maxWidth?: string;
}

export default function Modal({
  isOpen,
  onClose,
  title,
  description,
  children,
  maxWidth = '500px',
}: ModalProps) {
  const [mounted, setMounted] = useState(false);
  const modalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (!isOpen) return;
    const handleKeydown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    document.addEventListener('keydown', handleKeydown);
    const originalOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => {
      document.removeEventListener('keydown', handleKeydown);
      document.body.style.overflow = originalOverflow;
    };
  }, [isOpen, onClose]);

  if (!isOpen || !mounted) return null;

  return (
    <div className={s.overlay} role="dialog" aria-modal="true" aria-labelledby="modal-title">
      <div className={s.backdrop} onClick={onClose} />
      <div className={s.container} style={{ maxWidth }}>
        <div className={s.box} ref={modalRef}>
          <button className={s.closeBtn} onClick={onClose} aria-label="Close dialog">
            <X size={18} />
          </button>
          <div className={s.header}>
            <h3 id="modal-title" className={s.title}>
              {title}
            </h3>
            {description && <p className={s.desc}>{description}</p>}
          </div>
          <div className={s.content}>{children}</div>
        </div>
      </div>
    </div>
  );
}
