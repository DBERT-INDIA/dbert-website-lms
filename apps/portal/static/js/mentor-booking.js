(() => {
  const strip = document.getElementById('dateStrip');
  const dateInput = document.getElementById('mentorBookingDate');
  const mentorInput = document.getElementById('mentorSelect');
  const domainGroup = document.getElementById('domainPills');
  const cards = [...document.querySelectorAll('[data-session-card]')];
  const title = document.getElementById('step3Title');
  const empty = document.getElementById('mentorNoSessions');
  const status = document.getElementById('bookingStatus');
  const today = strip.dataset.today;
  const weekday = new Intl.DateTimeFormat(undefined, {weekday: 'short', timeZone: 'UTC'});
  const shortDate = new Intl.DateTimeFormat(undefined, {month: 'short', day: 'numeric', timeZone: 'UTC'});
  const fullDate = new Intl.DateTimeFormat(undefined, {dateStyle: 'long', timeZone: 'UTC'});
  const localTime = new Intl.DateTimeFormat(undefined, {
    month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit', timeZoneName: 'short',
  });
  let domain = domainGroup.querySelector('[aria-pressed=true]')?.dataset.domain || 'All Tracks';
  let pending = false;

  document.querySelectorAll('time[data-mentor-time]').forEach(element => {
    const time = new Date(element.dateTime);
    if (!Number.isNaN(time.getTime())) element.textContent = localTime.format(time);
  });

  function matchingCards() {
    return cards.filter(card => {
      const trackMatches = domain === 'All Tracks' || card.dataset.domain === domain || card.dataset.domain === 'All Tracks';
      const mentorMatches = mentorInput.value === 'all' || card.dataset.mentor === mentorInput.value;
      return trackMatches && mentorMatches;
    });
  }

  function showDay(date) {
    const day = new Date(`${date}T00:00:00Z`);
    if (Number.isNaN(day.getTime())) return;
    dateInput.value = date;
    title.textContent = `Sessions on ${fullDate.format(day)} (IST)`;
    const visible = new Set(matchingCards().filter(card => card.dataset.date === date));
    cards.forEach(card => { card.hidden = !visible.has(card); });
    empty.hidden = visible.size > 0;
    strip.querySelectorAll('[data-date]').forEach(button => {
      const isCurrent = button.dataset.date === date;
      button.classList.toggle('active', isCurrent);
      button.setAttribute('aria-pressed', String(isCurrent));
    });
  }

  function renderDateStrip() {
    const matches = matchingCards();
    const counts = new Map();
    for (const card of matches) {
      if (Number(card.dataset.seats) > 0) {
        counts.set(card.dataset.date, (counts.get(card.dataset.date) || 0) + 1);
      }
    }
    const options = document.createDocumentFragment();
    const day = new Date(`${today}T00:00:00Z`);
    for (let i = 0; i < 14; i += 1) {
      const date = day.toISOString().slice(0, 10);
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'date-card';
      button.dataset.date = date;
      const label = document.createElement('span');
      label.className = 'date-day-name';
      label.textContent = `${weekday.format(day)} ${shortDate.format(day)}`;
      const count = document.createElement('span');
      const open = counts.get(date) || 0;
      count.className = `date-badge ${open ? 'has-slots' : 'none'}`;
      count.textContent = open ? `${open} open` : 'No availability';
      button.append(label, count);
      options.append(button);
      day.setUTCDate(day.getUTCDate() + 1);
    }
    strip.replaceChildren(options);
    showDay(counts.keys().next().value || matches[0]?.dataset.date || today);
  }

  domainGroup.addEventListener('click', event => {
    const button = event.target.closest('[data-domain]');
    if (!button) return;
    domain = button.dataset.domain;
    domainGroup.querySelectorAll('[data-domain]').forEach(item => {
      item.classList.toggle('active', item === button);
      item.setAttribute('aria-pressed', String(item === button));
    });
    renderDateStrip();
  });
  mentorInput.addEventListener('change', renderDateStrip);
  dateInput.addEventListener('change', () => {
    if (dateInput.value && dateInput.validity.valid) showDay(dateInput.value);
  });
  strip.addEventListener('click', event => {
    const button = event.target.closest('[data-date]');
    if (button) showDay(button.dataset.date);
  });

  document.addEventListener('click', async event => {
    const button = event.target.closest('[data-reservation-action]');
    if (!button || pending) return;
    const isBooking = button.dataset.reservationAction === 'book';
    if (!window.confirm(isBooking ? 'Reserve a seat in this session?' : 'Cancel your reservation and release your seat?')) return;
    const feedback = button.closest('.mentor-reservation')?.querySelector('[data-reservation-feedback]') || status;
    pending = true;
    button.disabled = true;
    feedback.textContent = isBooking ? 'Reserving your seat…' : 'Cancelling your reservation…';
    try {
      const token = document.querySelector('meta[name=csrf-token]')?.content;
      const headers = token ? {'X-CSRF-Token': token} : {};
      const response = await fetch(button.dataset.endpoint, {method: 'POST', credentials: 'same-origin', headers});
      const result = await response.json();
      if (!response.ok || result.status !== 'success') {
        feedback.textContent = result.message || 'The reservation could not be updated.';
        return;
      }
      const anchor = isBooking ? `mentor-reservation-${button.dataset.slotId}` : 'scheduledMentorship';
      window.history.replaceState(window.history.state, '', `#${anchor}`);
      window.location.reload();
    } catch {
      feedback.textContent = 'The reservation could not be updated. Try again.';
    } finally {
      pending = false;
      button.disabled = false;
    }
  });

  renderDateStrip();
})();
