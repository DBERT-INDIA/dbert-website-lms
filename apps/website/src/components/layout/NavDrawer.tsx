'use client';

import React, { useEffect, useRef } from 'react';
import Link from 'next/link';
import styles from './MegaMenu.module.css';

export type DrawerLink = {
  label: string;
  href: string;
  external?: boolean;
  highlight?: boolean;
};

export type DrawerGroup = {
  title: string;
  links: DrawerLink[];
};

type NavDrawerProps = {
  open: boolean;
  groups: DrawerGroup[];
  cta?: DrawerLink;
  onClose: () => void;
  /** Focus returns here when the drawer closes. */
  returnFocusRef: React.RefObject<HTMLButtonElement | null>;
};

/**
 * Mobile navigation drawer.
 *
 * Replaces the v1 behaviour where every nav link was simply `display:none`
 * below 900px, leaving the site unnavigable on phones. Groups are built from
 * src/data/nav.config.json by the parent — nothing here is hardcoded.
 *
 * Closes on: scrim click, the button, Escape, any link click, and route
 * change (handled by the parent). Focus moves into the panel on open and
 * returns to the hamburger on close; Tab is trapped inside while open.
 */
export default function NavDrawer({
  open,
  groups,
  cta,
  onClose,
  returnFocusRef,
}: NavDrawerProps) {
  const panelRef = useRef<HTMLDivElement>(null);
  const closeRef = useRef<HTMLButtonElement>(null);

  // Lock body scroll while the drawer is open.
  useEffect(() => {
    if (!open) return;
    const previous = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => {
      document.body.style.overflow = previous;
    };
  }, [open]);

  // Move focus into the panel on open, and back to the hamburger on close.
  useEffect(() => {
    if (!open) return;
    const trigger = returnFocusRef.current;
    closeRef.current?.focus();
    return () => {
      trigger?.focus();
    };
  }, [open, returnFocusRef]);

  // Escape closes; Tab cycles within the panel.
  useEffect(() => {
    if (!open) return;

    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        event.preventDefault();
        onClose();
        return;
      }

      if (event.key !== 'Tab') return;

      const focusables = panelRef.current?.querySelectorAll<HTMLElement>(
        'a[href], button:not([disabled])'
      );
      if (!focusables || focusables.length === 0) return;

      const first = focusables[0];
      const last = focusables[focusables.length - 1];

      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    };

    document.addEventListener('keydown', onKeyDown);
    return () => document.removeEventListener('keydown', onKeyDown);
  }, [open, onClose]);

  const renderLink = (link: DrawerLink) => {
    const className = link.highlight ? styles.highlightLink : undefined;

    if (link.external) {
      return (
        <a
          key={`${link.href}-${link.label}`}
          href={link.href}
          className={className}
          target="_blank"
          rel="noopener noreferrer"
          onClick={onClose}
        >
          {link.label}
        </a>
      );
    }

    return (
      <Link
        key={`${link.href}-${link.label}`}
        href={link.href}
        className={className}
        onClick={onClose}
      >
        {link.label}
      </Link>
    );
  };

  return (
    <div
      className={`${styles.drawer}${open ? ` ${styles.drawerOpen}` : ''}`}
      aria-hidden={!open}
    >
      <button
        type="button"
        className={styles.drawerScrim}
        onClick={onClose}
        tabIndex={-1}
        aria-label="Close menu"
      />
      <div
        ref={panelRef}
        className={styles.drawerPanel}
        role="dialog"
        aria-modal="true"
        aria-label="Menu"
        inert={!open}
      >
        <div className={styles.drawerHead}>
          <span className={styles.navLogo}>
            <span className={styles.logoMark}>D</span>DBERT
          </span>
          <button
            ref={closeRef}
            type="button"
            className={styles.drawerClose}
            onClick={onClose}
            aria-label="Close menu"
          >
            <svg
              viewBox="0 0 24 24"
              width="18"
              height="18"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              aria-hidden="true"
            >
              <path d="M6 6l12 12M18 6L6 18" />
            </svg>
          </button>
        </div>

        {groups.map((group) => (
          <div key={group.title} className={styles.drawerGroup}>
            <div className={styles.gLabel}>{group.title}</div>
            {group.links.map(renderLink)}
          </div>
        ))}

        {cta && (
          <a
            href={cta.href}
            className={`btn btn-primary ${styles.drawerCta}`}
            target={cta.external ? '_blank' : undefined}
            rel={cta.external ? 'noopener noreferrer' : undefined}
            onClick={onClose}
          >
            {cta.label}
          </a>
        )}
      </div>
    </div>
  );
}
