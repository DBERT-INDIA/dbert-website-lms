/**
 * cohortCalendar.ts - Dynamic Rolling Cohort Calendar Engine
 * 
 * Eliminates hardcoded standup dates by computing the next weekly sprint cohort kickoff dynamically.
 * Standard Operating Rule: Cohorts kick off every Monday at 18:00:00 IST (UTC+05:30).
 */

export interface CohortStandupInfo {
  batchStartDate: string;      // e.g. "2026-11-16T18:00:00+05:30"
  batchStartDisplay: string;    // e.g. "Monday, 16 Nov 2026"
  batchStartTimestamp: number;  // Epoch ms for client countdowns
  kickoffTimeDisplay: string;   // e.g. "06:00 PM IST"
}

/**
 * Computes the upcoming cohort standup timestamp and formatted strings.
 * If today is Monday before 18:00 IST, returns today at 18:00 IST.
 * Otherwise, returns the upcoming Monday at 18:00 IST.
 */
export function getNextCohortStandup(now: Date = new Date()): CohortStandupInfo {
  // Convert current time to IST
  const utcMs = now.getTime() + (now.getTimezoneOffset() * 60000);
  const istOffsetMs = 5.5 * 3600000;
  const istDate = new Date(utcMs + istOffsetMs);

  const dayOfWeek = istDate.getDay(); // 0 = Sunday, 1 = Monday, ..., 6 = Saturday
  const hours = istDate.getHours();
  const minutes = istDate.getMinutes();

  let daysToAdd = 0;
  if (dayOfWeek === 1 && (hours < 18 || (hours === 18 && minutes === 0))) {
    daysToAdd = 0;
  } else {
    daysToAdd = (8 - dayOfWeek) % 7;
    if (daysToAdd === 0) {
      daysToAdd = 7;
    }
  }

  const targetIst = new Date(
    istDate.getFullYear(),
    istDate.getMonth(),
    istDate.getDate() + daysToAdd,
    18,
    0,
    0
  );

  const yyyy = targetIst.getFullYear();
  const mm = String(targetIst.getMonth() + 1).padStart(2, '0');
  const dd = String(targetIst.getDate()).padStart(2, '0');
  const iso = `${yyyy}-${mm}-${dd}T18:00:00+05:30`;

  const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const display = `${days[targetIst.getDay()]}, ${targetIst.getDate()} ${months[targetIst.getMonth()]} ${yyyy}`;

  return {
    batchStartDate: iso,
    batchStartDisplay: display,
    batchStartTimestamp: new Date(iso).getTime(),
    kickoffTimeDisplay: '06:00 PM IST',
  };
}
