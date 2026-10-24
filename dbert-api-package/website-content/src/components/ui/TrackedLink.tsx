'use client';

import React from 'react';
import Link, { type LinkProps } from 'next/link';
import { trackEvent } from '@/lib/analytics';

interface TrackedLinkProps extends LinkProps {
  eventName: string;
  eventParams?: Record<string, string | number | boolean>;
  className?: string;
  children: React.ReactNode;
  target?: string;
  rel?: string;
  id?: string;
  'aria-label'?: string;
  style?: React.CSSProperties;
}

export default function TrackedLink({
  eventName,
  eventParams = {},
  onClick,
  children,
  ...props
}: TrackedLinkProps & { onClick?: (e: React.MouseEvent<HTMLAnchorElement>) => void }) {
  return (
    <Link
      {...props}
      onClick={(e) => {
        trackEvent(eventName, eventParams);
        if (onClick) onClick(e);
      }}
    >
      {children}
    </Link>
  );
}
