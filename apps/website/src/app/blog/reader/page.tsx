import React, { Suspense } from 'react';
import type { Metadata } from 'next';
import DynamicBlogReader from '@/components/blog/DynamicBlogReader';

export const metadata: Metadata = {
  title: 'Technical Publication | DBERT Engineering Blog',
  description: 'Verified engineering publication and architectural benchmark from DBERT Labs.',
};

export default function BlogReaderPage() {
  return (
    <Suspense fallback={
      <div className="container pad-block" style={{ minHeight: '60vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <h1 className="visually-hidden">Technical Publication | DBERT Engineering Blog</h1>
        <p className="body-copy">Loading publication...</p>
      </div>
    }>
      <DynamicBlogReader />
    </Suspense>
  );
}
