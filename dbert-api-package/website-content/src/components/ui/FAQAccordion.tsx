'use client';

import React, { useState } from 'react';
import { ChevronDown } from 'lucide-react';
import styles from './FAQAccordion.module.css';

interface FAQItem {
  question: string;
  answer: string;
}

interface FAQAccordionProps {
  items: FAQItem[];
}

export default function FAQAccordion({ items }: FAQAccordionProps) {
  const [activeIndex, setActiveIndex] = useState<number | null>(null);

  const toggleAccordion = (index: number) => {
    setActiveIndex(prevIndex => (prevIndex === index ? null : index));
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
              onClick={() => toggleAccordion(index)}
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
