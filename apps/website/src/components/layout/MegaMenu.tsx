'use client';

import React, { useCallback, useEffect, useRef, useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import styles from './MegaMenu.module.css';
import navConfigJson from '@/data/nav.config.json';
import NavDrawer, { type DrawerGroup, type DrawerLink } from './NavDrawer';

type NavColumn = { title: string; links: DrawerLink[] };

type NavItem =
  | { label: string; type: 'mega'; columns: NavColumn[] }
  | { label: string; type: 'dropdown'; links: DrawerLink[] }
  | { label: string; type: 'link'; href: string };

type NavConfig = {
  items: NavItem[];
  cta?: DrawerLink;
  /** Optional. Add a `signIn` entry to nav.config.json to surface the ghost
   *  action in the bar — see the Phase 2 note in CLAUDE-TASKS.md. */
  signIn?: DrawerLink;
};

const navConfig = navConfigJson as unknown as NavConfig;

/** Flattens the nav config into the drawer's grouped shape. */
function buildDrawerGroups(items: NavItem[]): DrawerGroup[] {
  const groups: DrawerGroup[] = [];
  const standalone: DrawerLink[] = [];

  items.forEach((item) => {
    if (item.type === 'mega') {
      groups.push({
        title: item.label,
        links: item.columns.flatMap((column) => column.links),
      });
    } else if (item.type === 'dropdown') {
      groups.push({ title: item.label, links: item.links });
    } else {
      standalone.push({ label: item.label, href: item.href });
    }
  });

  if (standalone.length > 0) {
    groups.push({ title: 'More', links: standalone });
  }

  return groups;
}

function renderNavLink(link: DrawerLink) {
  const className = link.highlight ? styles.highlightLink : undefined;

  if (link.external) {
    return (
      <a href={link.href} className={className} target="_blank" rel="noopener noreferrer">
        {link.label}
      </a>
    );
  }

  return (
    <Link href={link.href} className={className}>
      {link.label}
    </Link>
  );
}

export default function MegaMenu() {
  const pathname = usePathname();
  const [openIndex, setOpenIndex] = useState<number | null>(null);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const navRef = useRef<HTMLDivElement>(null);
  const hambRef = useRef<HTMLButtonElement>(null);

  // Close everything on route change. Adjusting state during render rather than
  // in an effect avoids a second render pass (and the set-state-in-effect rule).
  const [lastPathname, setLastPathname] = useState(pathname);
  if (pathname !== lastPathname) {
    setLastPathname(pathname);
    setOpenIndex(null);
    setDrawerOpen(false);
  }

  const closeDrawer = useCallback(() => setDrawerOpen(false), []);

  // Desktop dropdowns: close on outside click and on Escape.
  useEffect(() => {
    if (openIndex === null) return;

    const onPointerDown = (event: MouseEvent) => {
      if (!navRef.current?.contains(event.target as Node)) {
        setOpenIndex(null);
      }
    };

    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') setOpenIndex(null);
    };

    document.addEventListener('mousedown', onPointerDown);
    document.addEventListener('keydown', onKeyDown);
    return () => {
      document.removeEventListener('mousedown', onPointerDown);
      document.removeEventListener('keydown', onKeyDown);
    };
  }, [openIndex]);

  const drawerGroups = buildDrawerGroups(navConfig.items);

  return (
    <>
      <header className={styles.navbar}>
        <div className={styles.navContainer} ref={navRef}>
          <Link href="/" className={styles.navLogo}>
            <span className={styles.logoMark} aria-hidden="true">
              D
            </span>
            DBERT
          </Link>

          <nav className={styles.navLinks} aria-label="Primary">
            {navConfig.items.map((item, index) => {
              if (item.type === 'link') {
                return (
                  <Link key={item.label} href={item.href} className={styles.navLink}>
                    {item.label}
                  </Link>
                );
              }

              const isOpen = openIndex === index;
              const panelId = `nav-panel-${index}`;
              const isLast = index === navConfig.items.length - 1;

              return (
                <div
                  key={item.label}
                  className={`${styles.navItem}${item.type === 'mega' ? ` ${styles.navItemMega}` : ''}`}
                >
                  <button
                    type="button"
                    className={styles.navTrigger}
                    aria-expanded={isOpen}
                    aria-controls={panelId}
                    onClick={() => setOpenIndex(isOpen ? null : index)}
                  >
                    {item.label}
                    <svg
                      className={styles.caret}
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2.5"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      aria-hidden="true"
                    >
                      <path d="M6 9l6 6 6-6" />
                    </svg>
                  </button>

                  {isOpen && item.type === 'mega' && (
                    <div id={panelId} className={`${styles.panel} ${styles.panelMega}`}>
                      <div className={styles.megaGrid}>
                        {item.columns.map((column) => (
                          <div key={column.title}>
                            <h2 className={styles.megaColTitle}>{column.title}</h2>
                            <ul className={styles.linkList}>
                              {column.links.map((link) => (
                                <li key={`${link.href}-${link.label}`}>{renderNavLink(link)}</li>
                              ))}
                            </ul>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {isOpen && item.type === 'dropdown' && (
                    <div
                      id={panelId}
                      className={`${styles.panel} ${styles.panelDropdown}${isLast ? ` ${styles.panelAlignRight}` : ''}`}
                    >
                      <ul className={styles.linkList}>
                        {item.links.map((link) => (
                          <li key={`${link.href}-${link.label}`}>{renderNavLink(link)}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              );
            })}
          </nav>

          <div className={styles.navActions}>
            {navConfig.signIn && (
              <a
                href={navConfig.signIn.href}
                className={`btn btn-ghost btn-sm ${styles.ghostAction}`}
                target={navConfig.signIn.external ? '_blank' : undefined}
                rel={navConfig.signIn.external ? 'noopener noreferrer' : undefined}
              >
                {navConfig.signIn.label}
              </a>
            )}

            {navConfig.cta && (
              <a
                href={navConfig.cta.href}
                className="btn btn-primary btn-sm"
                target={navConfig.cta.external ? '_blank' : undefined}
                rel={navConfig.cta.external ? 'noopener noreferrer' : undefined}
              >
                {navConfig.cta.label}
              </a>
            )}

            <button
              ref={hambRef}
              type="button"
              className={styles.hamb}
              aria-label="Open menu"
              aria-expanded={drawerOpen}
              aria-controls="nav-drawer"
              onClick={() => setDrawerOpen(true)}
            >
              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                aria-hidden="true"
              >
                <path d="M4 7h16M4 12h16M4 17h16" />
              </svg>
            </button>
          </div>
        </div>
      </header>

      <div id="nav-drawer">
        <NavDrawer
          open={drawerOpen}
          groups={drawerGroups}
          cta={navConfig.cta}
          onClose={closeDrawer}
          returnFocusRef={hambRef}
        />
      </div>
    </>
  );
}
