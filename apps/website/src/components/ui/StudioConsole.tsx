import React from 'react';
import styles from './StudioConsole.module.css';

export type FeedTag = 'build' | 'ship' | 'cohort';

export type FeedLine = {
  /** Timestamp, e.g. "09:41:07". */
  time: string;
  tag: FeedTag;
  message: string;
  /** Trailing dimmed detail, e.g. "· sprint 14". */
  detail?: string;
};

type StudioConsoleProps = {
  /** Window title, e.g. "dbert-studio · live feed". */
  title: string;
  lines: FeedLine[];
  footLeft?: string;
  footRight?: string;
  /** Handwritten annotation pinned above the console. */
  note?: React.ReactNode;
};

const tagClass: Record<FeedTag, string> = {
  build: styles.tagBuild,
  ship: styles.tagShip,
  cohort: styles.tagCohort,
};

/**
 * The hero live-feed terminal.
 *
 * The staggered reveal is pure CSS (`animation-delay` off a `--i` index), so
 * this stays a server component: no timers, no hydration, and the feed content
 * is in the HTML for crawlers. The reference implementation used setTimeout,
 * which meant the lines did not exist until JS ran.
 */
export default function StudioConsole({
  title,
  lines,
  footLeft,
  footRight,
  note,
}: StudioConsoleProps) {
  return (
    <div className={styles.wrap}>
      {note && (
        <div className={styles.note} aria-hidden="true">
          {note}
        </div>
      )}

      <div className={styles.console} aria-label="Studio activity feed" role="img">
        <div className={styles.bar}>
          <span className={`${styles.dot} ${styles.dotRed}`} />
          <span className={`${styles.dot} ${styles.dotAmber}`} />
          <span className={`${styles.dot} ${styles.dotGreen}`} />
          <span className={styles.barTitle}>{title}</span>
        </div>

        <div className={styles.body}>
          {lines.map((line, index) => (
            <div
              key={`${line.time}-${index}`}
              className={styles.line}
              style={{ '--i': index } as React.CSSProperties}
            >
              <span className={styles.st}>{line.time}</span>
              <span className={`${styles.tag} ${tagClass[line.tag]}`}>{line.tag}</span>
              <span className={styles.msg}>
                {line.message}
                {line.detail && <em> {line.detail}</em>}
              </span>
            </div>
          ))}

          <div
            className={`${styles.line} ${styles.cursorRow}`}
            style={{ '--i': lines.length } as React.CSSProperties}
          >
            <span className={`${styles.st} ${styles.prompt}`}>▸</span>
            <span className={`${styles.msg} ${styles.listening}`}>
              listening
              <span className={styles.caret} />
            </span>
          </div>
        </div>

        {(footLeft || footRight) && (
          <div className={styles.foot}>
            <span>{footLeft}</span>
            <span className={styles.live}>{footRight}</span>
          </div>
        )}
      </div>
    </div>
  );
}
