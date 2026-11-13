import React from 'react';
import { Hourglass } from 'lucide-react';
import s from './CohortBanner.module.css';

interface CohortBannerProps {
  deadlineDate: string;
}

function isPastDeadline(value: string) {
  const parts = value.match(/\b([A-Za-z]+\s+\d{1,2})(?:st|nd|rd|th)?[,]?\s+(\d{4})\b/);
  if (!parts) return false;

  const parsed = new Date(`${parts[1]}, ${parts[2]}`);
  if (Number.isNaN(parsed.getTime())) return false;

  const deadlineEndUtc = Date.UTC(
    parsed.getUTCFullYear(),
    parsed.getUTCMonth(),
    parsed.getUTCDate(),
    23,
    59,
    59,
  );

  return Date.now() > deadlineEndUtc;
}

export default function CohortBanner({ deadlineDate }: CohortBannerProps) {
  if (isPastDeadline(deadlineDate)) return null;

  return (
    <div className={s.banner}>
      <Hourglass size={16} aria-hidden="true" />
      <span>Next incubation cohort review deadline: <strong>{deadlineDate}</strong></span>
    </div>
  );
}
