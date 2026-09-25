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
        return (
          <div 
            key={index} 
            className={`${styles.faqItem} ${isOpen ? styles.open : ''}`}
            onClick={() => toggleAccordion(index)}
          >
            <button 
              className={styles.faqQuestion} 
              aria-expanded={isOpen}
            >
              <span>{item.question}</span>
              <ChevronDown 
                size={18} 
                className={styles.faqArrow} 
                style={{ 
                  transform: isOpen ? 'rotate(180deg)' : 'rotate(0deg)', 
                  transition: 'transform 0.25s var(--ease)' 
                }}
              />
            </button>
            <div className={`${styles.faqAnswer}${isOpen ? ` ${styles.faqAnswerOpen}` : ''}`}>
              <p>{item.answer}</p>
            </div>
          </div>
        );
      })}
    </div>
  );
}
