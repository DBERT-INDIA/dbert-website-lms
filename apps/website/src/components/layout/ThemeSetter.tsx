'use client';

import { useEffect } from 'react';
import { usePathname } from 'next/navigation';

export default function ThemeSetter() {
  const pathname = usePathname();

  useEffect(() => {
    if (!pathname) return;

    const isEnterprise = 
      pathname.startsWith('/startups') || 
      pathname.startsWith('/ai-solutions') || 
      pathname.startsWith('/admin');

    const theme = isEnterprise ? 'enterprise' : 'learner';
    document.body.setAttribute('data-theme', theme);
  }, [pathname]);

  return null;
}
