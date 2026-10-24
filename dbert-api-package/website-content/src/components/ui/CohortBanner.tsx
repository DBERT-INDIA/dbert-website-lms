import React from 'react';
import { Hourglass } from 'lucide-react';
import s from './CohortBanner.module.css';

interface CohortBannerProps {
  deadlineDate: string;
}

export default function CohortBanner({ deadlineDate }: CohortBannerProps) {
  return (
    <div className={s.banner}>
      <Hourglass size={16} aria-hidden="true" />
      <span>Next incubation cohort review deadline: <strong>{deadlineDate}</strong></span>
    </div>
  );
}
