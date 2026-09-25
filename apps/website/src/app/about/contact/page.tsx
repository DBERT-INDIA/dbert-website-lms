import React from 'react';
import ContactForm from '@/components/ui/ContactForm';
import { pageMetadata } from '@/lib/seo';
import styles from '../about.module.css';


export const metadata = pageMetadata('/about/contact');

export default function ContactPage() {
  return (
    <div className="container pad-block">
      <div className="mb-lg">
        <div className="doclabel">
          § 01 — CONTACT &amp; SUPPORT CHANNELS <span className="rev">rev: 2026.2</span>
        </div>
        <h1>Let&apos;s Build Something Together</h1>
        <p>Get in touch with our incubation team, customer support, or academic advisors.</p>
      </div>

      <div className={styles.contactGrid}>
        
        {/* Contact Form Column */}
        <div>
          <div className="doclabel mb-2">§ 02 — INQUIRY SUBMISSION FORM</div>
          <ContactForm sourcePage="/about/contact" />
        </div>

        {/* Info Column */}
        <div className="stack">
          <div className="card card-lift">
            <h2 className={styles.cardTitleNudge}>Email</h2>
            <p><a href="mailto:contactus@dbert.online" className={styles.accentLink}>contactus@dbert.online</a></p>
            <p className={styles.contactNote}>Submit incubation inquiries, learner program questions, or enterprise collaboration proposals.</p>
          </div>

          <div className="card card-lift">
            <h2 className={styles.cardTitleNudge}>Phone &amp; WhatsApp</h2>
            <p><a href="tel:+918958006294" className={styles.accentLink}>+91 89580 06294</a></p>
            <p className={styles.contactNote}>Available Monday to Saturday, 10:00 AM to 7:00 PM IST. Direct WhatsApp connection available across the site.</p>
          </div>

          <div className="card card-lift">
            <h2 className={styles.cardTitleNudge}>Registered Entity &amp; Origin</h2>
            <address className={styles.address}>
              Digital Blinc Education Research And Technology<br />
              Ghaziabad, NCR, India<br /><br />
              <em>Operating as a 100% remote digital studio. All sprints, mentorship, and meetings are conducted online.</em>
            </address>
          </div>
        </div>

      </div>
    </div>
  );
}
