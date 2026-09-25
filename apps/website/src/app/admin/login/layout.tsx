import React from 'react';
import { pageMetadata } from '@/lib/seo';

/* This route's page is a client component, so it cannot export
   `metadata` itself. The layout carries it instead. */
export const metadata = pageMetadata('/admin/login');

export default function AdminLoginLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
