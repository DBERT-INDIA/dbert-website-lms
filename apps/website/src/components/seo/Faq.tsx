import React from 'react';
import FAQAccordion from '@/components/ui/FAQAccordion';

export type FaqItem = {
  question: string;
  answer: string;
};

type FaqProps = {
  items: FaqItem[];
  /** Heading above the accordion. Defaults to a plain "Questions" heading. */
  heading?: string;
  /** Anchor id, so a page can link straight to its own FAQ. */
  id?: string;
};

/**
 * FAQ block + FAQPage structured data, as one unit (spec 7.10).
 *
 * The schema and the visible copy come from the same array on purpose. Google's
 * structured-data guidelines require the marked-up answer to be the answer the
 * user actually sees; keeping two lists in sync by hand is how that breaks.
 *
 * This is a **server** component wrapping the client-side accordion, so the
 * questions and answers ship in the HTML for crawlers rather than appearing
 * only after hydration.
 *
 * Answers are plain strings, not JSX: FAQPage `acceptedAnswer.text` has to be
 * text, and `JSON.stringify` here would happily emit `[object Object]` for an
 * element without erroring.
 */
export default function Faq({ items, heading = 'Common questions', id = 'faq' }: FaqProps) {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: items.map((item) => ({
      '@type': 'Question',
      name: item.question,
      acceptedAnswer: {
        '@type': 'Answer',
        text: item.answer,
      },
    })),
  };

  return (
    <section id={id} className="faq-block" aria-labelledby={`${id}-heading`}>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
      />
      <h2 id={`${id}-heading`} className="section-heading">{heading}</h2>
      <FAQAccordion items={items} />
    </section>
  );
}
