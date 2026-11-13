'use client';

import React, { useState, useEffect, useRef } from 'react';
import styles from './WhatsAppFloat.module.css';
import { trackEvent } from '@/lib/analytics';

const NUMBERS = ['918958006294', '918192911360'];

interface TopicOption {
  id: string;
  label: string;
  icon: string;
  defaultMsg: string;
}

const TOPICS: TopicOption[] = [
  {
    id: 'admissions',
    label: 'Admissions & ₹1,999 Program',
    icon: '🎓',
    defaultMsg: 'Hi, I want to know more about the ₹1,999 Incubation Program and guaranteed placement.',
  },
  {
    id: 'internship',
    label: 'Internship Status & Application',
    icon: '💼',
    defaultMsg: 'Hi, I want to check my internship application status and upcoming batch dates.',
  },
  {
    id: 'certificate',
    label: 'Certificate & LOR Verification',
    icon: '📜',
    defaultMsg: 'Hi, I have a question regarding my certificate verification and LOR dossier.',
  },
  {
    id: 'other',
    label: 'Other Inquiry',
    icon: '🛠️',
    defaultMsg: 'Hi DBERT Team, I have an inquiry regarding your programs.',
  },
];

export default function WhatsAppFloat() {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedTopic, setSelectedTopic] = useState<TopicOption>(TOPICS[0]);
  const [userQuery, setUserQuery] = useState(TOPICS[0].defaultMsg);
  const [targetNumber, setTargetNumber] = useState(NUMBERS[0]);
  const [currentUrl, setCurrentUrl] = useState('');
  const [pageTitle, setPageTitle] = useState('');
  const popoverRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // 50/50 smart distribution between 8958006294 and 8192911360
    const chosen = NUMBERS[Math.floor(Math.random() * NUMBERS.length)];
    setTargetNumber(chosen);

    if (typeof window !== 'undefined') {
      setCurrentUrl(window.location.href);
      setPageTitle(document.title || 'DBERT Sovereign Platform');
    }

    const handleClickOutside = (e: MouseEvent) => {
      if (popoverRef.current && !popoverRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    document.addEventListener('keydown', handleKeyDown);

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, []);

  const handleSelectTopic = (topic: TopicOption) => {
    setSelectedTopic(topic);
    setUserQuery(topic.defaultMsg);
  };

  const handleOpenToggle = () => {
    const nextState = !isOpen;
    setIsOpen(nextState);
    if (nextState) {
      if (typeof window !== 'undefined') {
        setCurrentUrl(window.location.href);
        setPageTitle(document.title || 'DBERT Sovereign Platform');
      }
      trackEvent('whatsapp_popup_open');
    }
  };

  const handleSend = () => {
    // Re-roll 50/50 on submission to balance live sessions
    const activeNum = Math.random() < 0.5 ? NUMBERS[0] : NUMBERS[1];

    const cleanTitle = pageTitle.replace(/— DBERT.*/, '').replace(/\| DBERT.*/, '').trim() || 'DBERT Platform';
    const payload = 
      `Hi DBERT Team, I have an inquiry from your platform:\n\n` +
      `• Topic: ${selectedTopic.label}\n` +
      `• Inquiry: ${userQuery.trim()}\n` +
      `• Page: ${cleanTitle}\n` +
      `• URL: ${currentUrl}`;

    trackEvent('whatsapp_send_click', { topic: selectedTopic.id, number: activeNum });

    const waUrl = `https://wa.me/${activeNum}?text=${encodeURIComponent(payload)}`;
    window.open(waUrl, '_blank', 'noopener,noreferrer');
    setIsOpen(false);
  };

  return (
    <div className={styles.widgetWrapper} ref={popoverRef}>
      {/* Interactive Popover Card */}
      {isOpen && (
        <div className={styles.popoverCard} role="dialog" aria-modal="true" aria-label="WhatsApp Inquiry Desk">
          <div className={styles.popoverHeader}>
            <div className={styles.headerInfo}>
              <div className={styles.avatarWrap}>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="#ffffff" aria-hidden="true">
                  <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
                </svg>
                <span className={styles.onlineDot} title="Online"></span>
              </div>
              <div>
                <h4 className={styles.headerTitle}>DBERT Admissions &amp; Support</h4>
                <p className={styles.headerSubtitle}>Online &middot; Typically replies in minutes</p>
              </div>
            </div>
            <button 
              className={styles.closeBtn} 
              onClick={() => setIsOpen(false)}
              aria-label="Close WhatsApp dialogue"
            >
              &times;
            </button>
          </div>

          <div className={styles.popoverBody}>
            <div className={styles.sectionLabel}>What information are you looking for?</div>
            <div className={styles.topicChips}>
              {TOPICS.map((topic) => (
                <button
                  key={topic.id}
                  type="button"
                  className={`${styles.topicChip} ${selectedTopic.id === topic.id ? styles.topicChipActive : ''}`}
                  onClick={() => handleSelectTopic(topic)}
                >
                  <span className={styles.chipIcon}>{topic.icon}</span>
                  <span>{topic.label}</span>
                </button>
              ))}
            </div>

            <div className={styles.inputWrap}>
              <label htmlFor="waUserQuery" className={styles.fieldLabel}>Your Question / Details</label>
              <textarea
                id="waUserQuery"
                className={styles.queryTextarea}
                rows={3}
                value={userQuery}
                onChange={(e) => setUserQuery(e.target.value)}
                placeholder="Type your question here..."
              />
            </div>

            {currentUrl && (
              <div className={styles.pageContextPill} title={currentUrl}>
                <span className={styles.contextIcon}>📍</span>
                <span className={styles.contextText}>
                  Page: <strong>{pageTitle.replace(/— DBERT.*/, '').replace(/\| DBERT.*/, '').trim() || 'dbert.in'}</strong>
                </span>
              </div>
            )}

            <button 
              type="button" 
              className={styles.sendBtn}
              onClick={handleSend}
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
              </svg>
              <span>Start Chat on WhatsApp &rarr;</span>
            </button>
            <div className={styles.secureNote}>
              🔒 Encrypted Direct Desk &middot; +91 89580 06294 / 81929 11360
            </div>
          </div>
        </div>
      )}

      {/* Floating Scroll Bubble */}
      <button
        type="button"
        className={`${styles.whatsappBubble} ${isOpen ? styles.bubbleActive : ''}`}
        onClick={handleOpenToggle}
        aria-label="Chat on WhatsApp"
        aria-expanded={isOpen}
      >
        <div className={styles.pulseRing}></div>
        <svg 
          width="30" 
          height="30" 
          viewBox="0 0 24 24" 
          fill="#ffffff" 
          aria-hidden="true"
          className={styles.bubbleIcon}
        >
          <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
        </svg>
        <span className={styles.bubbleTooltip}>Chat with Admissions</span>
      </button>
    </div>
  );
}
