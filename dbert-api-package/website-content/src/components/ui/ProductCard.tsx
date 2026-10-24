import React from 'react';
import Link from 'next/link';
import type { LucideIcon } from 'lucide-react';
import styles from './ProductCard.module.css';
import Reveal from './Reveal';

export type ProductCardProps = {
  /** Stroke icon from lucide-react. No emoji anywhere on the site. */
  icon: LucideIcon;
  title: string;
  description: string;
  /** The provenance story: what forced this product to exist. */
  bornFrom?: string;
  /** Short mono facts, e.g. ["SOC2-ready", "self-host"]. */
  meta?: string[];
  /** Renders a green dot + "live" as the first meta item. */
  isLive?: boolean;
  href?: string;
  /** Dashed outline treatment for the trailing "custom work" card. */
  variant?: 'default' | 'custom';
};

/**
 * A single product card: icon chip, description, provenance line, and a
 * bordered meta row. The `born from:` line is the point of the card — it is
 * what separates "software we run" from "software we sell".
 */
export default function ProductCard({
  icon: Icon,
  title,
  description,
  bornFrom,
  meta = [],
  isLive = false,
  href,
  variant = 'default',
}: ProductCardProps) {
  const body = (
    <>
      <div className={styles.ic}>
        <Icon strokeWidth={1.8} aria-hidden="true" />
      </div>
      <h3>{title}</h3>
      <p>{description}</p>
      {bornFrom && (
        <div className={styles.born}>
          born from: <b>{bornFrom}</b>
        </div>
      )}
      {(isLive || meta.length > 0) && (
        <div className={styles.meta}>
          {isLive && (
            <span>
              <b className={styles.live}>●</b> live
            </span>
          )}
          {meta.map((item) => (
            <span key={item}>{item}</span>
          ))}
        </div>
      )}
    </>
  );

  const className = `${styles.prod}${variant === 'custom' ? ` ${styles.custom}` : ''}`;

  return (
    <Reveal as="div">
      {href ? (
        <Link href={href} className={className}>
          {body}
        </Link>
      ) : (
        <div className={className}>{body}</div>
      )}
    </Reveal>
  );
}

/** Grid wrapper so pages do not re-declare the column rules. */
export function ProductGrid({ children }: { children: React.ReactNode }) {
  return <div className={styles.grid}>{children}</div>;
}
