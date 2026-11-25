import React from 'react';

type RevealProps = {
  children: React.ReactNode;
  /** Element to render. Defaults to a div. */
  as?: React.ElementType;
  className?: string;
  /** Stagger in milliseconds for the optional entry animation. */
  delay?: number;
} & React.HTMLAttributes<HTMLElement>;

/**
 * Marks an element for scroll reveal.
 *
 * This is a **server** component and ships no JavaScript of its own — it only
 * adds the `.rv` class. A single `RevealObserver` mounted in the root layout
 * watches every `.rv` on the page and adds `.in` as they enter the viewport.
 *
 * An earlier version made each Reveal its own client component with its own
 * IntersectionObserver. The homepage alone renders 29 of them, so that was 29
 * hydration roots and 29 observers for one behaviour.
 *
 * Content is visible by default. The observer skips optional motion when
 * scripting support, motion preferences, or data-saving settings call for it.
 */
export default function Reveal({
  children,
  as: Tag = 'div',
  className = '',
  delay,
  ...rest
}: RevealProps) {
  return (
    <Tag
      className={`rv${className ? ` ${className}` : ''}`}
      style={delay ? { animationDelay: `${delay}ms` } : undefined}
      {...rest}
    >
      {children}
    </Tag>
  );
}
