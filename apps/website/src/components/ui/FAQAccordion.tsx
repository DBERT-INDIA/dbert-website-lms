'use client';

import React, { useState } from 'react';
import { ChevronDown } from 'lucide-react';
import { trackEvent } from '@/lib/analytics';
import styles from './FAQAccordion.module.css';

interface FAQItem {
  question: string;
  answer: string;
}

interface FAQAccordionProps {
  items: FAQItem[];
  trackingContext?: string;
}

export default function FAQAccordion({ items, trackingContext }: FAQAccordionProps) {
  const [activeIndex, setActiveIndex] = useState<number | null>(null);

  const toggleAccordion = (index: number, question: string) => {
    const isOpening = activeIndex !== index;
    setActiveIndex(prevIndex => (prevIndex === index ? null : index));
    if (isOpening) {
      const eventName = trackingContext === 'blog-faq' ? 'blog_faq_expand' : 'faq_expand';
      trackEvent(eventName, {
        context: trackingContext || 'faq',
        question: question.slice(0, 120),
      });
    }
  };

  return (
    <div className={styles.faqList}>
      {items.map((item, index) => {
        const isOpen = activeIndex === index;
        const answerId = `faq-answer-${index}`;
        return (
          <div 
            key={index} 
            className={`${styles.faqItem} ${isOpen ? styles.open : ''}`}
          >
            <button 
              type="button"
              className={styles.faqQuestion} 
              aria-expanded={isOpen}
              aria-controls={answerId}
              onClick={() => toggleAccordion(index, item.question)}
            >
              <span>{item.question}</span>
              <ChevronDown 
                size={18} 
                className={`${styles.faqArrow} ${isOpen ? styles.faqArrowOpen : ''}`} 
                aria-hidden="true"
              />
            </button>
            <div 
              id={answerId}
              role="region"
              className={`${styles.faqAnswer}${isOpen ? ` ${styles.faqAnswerOpen}` : ''}`}
            >
              <p>{item.answer}</p>
            </div>
          </div>
        );
      })}
    </div>
  );
}
