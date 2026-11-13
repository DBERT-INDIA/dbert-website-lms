/**
 * DBERT Universal Interactive WhatsApp Widget for LMS
 * Load-balances inquiries 50/50 between +91 89580 06294 and +91 81929 11360.
 */
(function () {
  'use strict';

  const NUMBERS = ['918958006294', '918192911360'];

  const TOPICS = [
    {
      id: 'admissions',
      label: 'Admissions & ₹1,999 Program',
      icon: '🎓',
      defaultMsg: 'Hi, I want to know more about the ₹1,999 Incubation Program and guaranteed placement.'
    },
    {
      id: 'internship',
      label: 'Internship Status & Application',
      icon: '💼',
      defaultMsg: 'Hi, I want to check my internship application status and upcoming batch dates.'
    },
    {
      id: 'certificate',
      label: 'Certificate & LOR Verification',
      icon: '📜',
      defaultMsg: 'Hi, I have a question regarding my certificate verification and LOR dossier.'
    },
    {
      id: 'other',
      label: 'Other Inquiry',
      icon: '🛠️',
      defaultMsg: 'Hi DBERT Team, I have an inquiry regarding your programs.'
    }
  ];

  let currentTopic = TOPICS[0];
  let isOpen = false;
  let internContext = null;

  function initInternContext() {
    try {
      fetch('/intern/me', { credentials: 'include' })
        .then(function (r) { return r.json(); })
        .then(function (d) {
          if (d && d.status === 'success' && d.intern) {
            internContext = d.intern;
          }
        })
        .catch(function () {});
    } catch (e) {}
  }

  function createWidgetDOM() {
    if (document.getElementById('dbertWaWrapper')) return;

    const wrapper = document.createElement('div');
    wrapper.id = 'dbertWaWrapper';
    wrapper.className = 'dbert-wa-wrapper';

    const cleanTitle = (document.title || 'DBERT LMS')
      .replace(/— DBERT.*/, '')
      .replace(/\| DBERT.*/, '')
      .trim() || 'DBERT LMS';

    wrapper.innerHTML = `
      <!-- Popover Card -->
      <div class="dbert-wa-card" id="dbertWaCard" role="dialog" aria-modal="true" aria-label="WhatsApp Inquiry Desk">
        <div class="dbert-wa-header">
          <div class="dbert-wa-header-info">
            <div class="dbert-wa-avatar">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="#ffffff" aria-hidden="true">
                <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
              </svg>
              <span class="dbert-wa-online" title="Online"></span>
            </div>
            <div>
              <h4 class="dbert-wa-title">DBERT Admissions &amp; Support</h4>
              <p class="dbert-wa-sub">Online &middot; Typically replies in minutes</p>
            </div>
          </div>
          <button type="button" class="dbert-wa-close" id="dbertWaCloseBtn" aria-label="Close">&times;</button>
        </div>

        <div class="dbert-wa-body">
          <div class="dbert-wa-sec-label">What information are you looking for?</div>
          <div class="dbert-wa-chips" id="dbertWaChips"></div>

          <label for="dbertWaInput" class="dbert-wa-sec-label" style="display:block;margin-bottom:6px;">Your Question / Details</label>
          <textarea id="dbertWaInput" class="dbert-wa-textarea" rows="3" placeholder="Type your question here..."></textarea>

          <div class="dbert-wa-context" title="${window.location.href}">
            <span>📍</span>
            <span style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">Page: <strong>${cleanTitle}</strong></span>
          </div>

          <button type="button" class="dbert-wa-send" id="dbertWaSendBtn">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
            </svg>
            <span>Start Chat on WhatsApp &rarr;</span>
          </button>
          <div class="dbert-wa-note">🔒 Direct Admissions Line &middot; +91 89580 06294 / 81929 11360</div>
        </div>
      </div>

      <!-- Bubble Trigger -->
      <button type="button" class="dbert-wa-bubble" id="dbertWaBubble" aria-label="Chat on WhatsApp" aria-expanded="false">
        <div class="dbert-wa-pulse"></div>
        <svg width="30" height="30" viewBox="0 0 24 24" fill="#ffffff" aria-hidden="true" class="dbert-wa-icon">
          <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
        </svg>
        <span class="dbert-wa-tooltip">Chat with Admissions</span>
      </button>
    `;

    document.body.appendChild(wrapper);

    // Populate chips
    const chipsWrap = document.getElementById('dbertWaChips');
    const inputArea = document.getElementById('dbertWaInput');
    inputArea.value = currentTopic.defaultMsg;

    TOPICS.forEach(function (topic, idx) {
      const chip = document.createElement('button');
      chip.type = 'button';
      chip.className = 'dbert-wa-chip' + (idx === 0 ? ' active' : '');
      chip.innerHTML = `<span>${topic.icon}</span><span>${topic.label}</span>`;
      chip.addEventListener('click', function () {
        currentTopic = topic;
        document.querySelectorAll('.dbert-wa-chip').forEach(function (c) { c.classList.remove('active'); });
        chip.classList.add('active');
        inputArea.value = topic.defaultMsg;
      });
      chipsWrap.appendChild(chip);
    });

    const bubble = document.getElementById('dbertWaBubble');
    const card = document.getElementById('dbertWaCard');
    const closeBtn = document.getElementById('dbertWaCloseBtn');
    const sendBtn = document.getElementById('dbertWaSendBtn');

    function toggle(open) {
      isOpen = (open !== undefined) ? open : !isOpen;
      card.classList.toggle('open', isOpen);
      bubble.classList.toggle('active', isOpen);
      bubble.setAttribute('aria-expanded', String(isOpen));
      if (isOpen && window.dbertGA) {
        window.dbertGA('whatsapp_popup_open', {});
      }
    }

    bubble.addEventListener('click', function () { toggle(); });
    closeBtn.addEventListener('click', function () { toggle(false); });

    document.addEventListener('click', function (e) {
      if (isOpen && wrapper && !wrapper.contains(e.target)) {
        toggle(false);
      }
    });

    document.addEventListener('keydown', function (e) {
      if (isOpen && e.key === 'Escape') {
        toggle(false);
      }
    });

    sendBtn.addEventListener('click', function () {
      // 50/50 smart load-balance
      const activeNum = Math.random() < 0.5 ? NUMBERS[0] : NUMBERS[1];
      const userText = inputArea.value.trim() || currentTopic.defaultMsg;

      let payload =
        `Hi DBERT Team, I have an inquiry from your LMS platform:\n\n` +
        `• Topic: ${currentTopic.label}\n` +
        `• Inquiry: ${userText}\n` +
        `• Page: ${cleanTitle}\n` +
        `• URL: ${window.location.href}`;

      if (internContext && internContext.name) {
        payload += `\n• Candidate: ${internContext.name} (${internContext.email || ''})`;
      }

      if (window.dbertGA) {
        window.dbertGA('whatsapp_send_click', { topic: currentTopic.id, number: activeNum });
      }

      const waUrl = `https://wa.me/${activeNum}?text=${encodeURIComponent(payload)}`;
      window.open(waUrl, '_blank', 'noopener,noreferrer');
      toggle(false);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      initInternContext();
      createWidgetDOM();
    });
  } else {
    initInternContext();
    createWidgetDOM();
  }
})();
