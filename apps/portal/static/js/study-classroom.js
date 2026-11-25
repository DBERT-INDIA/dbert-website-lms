(() => {
  'use strict';

  const byId = (id) => document.getElementById(id);
  const classroom = byId('study-classroom');
  if (!classroom) return;

  const endpoint = '/api/study-classroom/' + encodeURIComponent(classroom.dataset.courseId);
  const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content || '';
  const grid = classroom.querySelector('.study-grid');
  const desktop = window.matchMedia('(min-width: 1050px)');
  const tabs = [...classroom.querySelectorAll('[role="tab"]')];
  const panels = new Map(tabs.map((tab) => [tab, byId(tab.getAttribute('aria-controls'))]));
  const trailList = byId('study-trail-entries');
  const lessonSelect = byId('study-lesson-select');
  const lessonTitles = new Map([...lessonSelect.options].map((lesson) => [lesson.value, lesson.textContent]));
  const question = byId('study-question');
  const chatError = byId('study-chat-error');
  const lectureError = byId('study-lecture-error');
  const conversation = byId('study-conversation');
  const lessonSections = byId('study-lesson-sections');
  const chatLog = byId('study-chat-log');
  const send = byId('study-send');
  const noteForm = byId('study-notes-form');
  const noteField = byId('study-notes');
  const noteSave = byId('study-save-notes');
  const noteReload = byId('study-load-notes');
  const noteStatus = byId('study-notes-status');
  const noteError = byId('study-notes-error');
  const status = byId('study-status');
  const trail = new Map();
  const trailWrites = new Map();
  const noteDrafts = new Map();
  const noteConflicts = new Set();
  const noteSaves = new Set();
  const statusActions = new Map();
  const sectionNodes = new Map();
  const panelSizes = {};
  const widths = { trail: 200, chat: 300, lecture: 280 };

  let tab = tabs[1];
  let locationState;
  let lesson = null;
  let notes = null;
  let lessonRequest;
  let trailRevision = 0;
  let isLoading = true;
  let asking = false;
  let retryAsk = null;
  let reviewOnly = false;

  function element(tag, text, className) {
    const node = document.createElement(tag);
    if (text) node.textContent = text;
    if (className) node.className = className;
    return node;
  }

  async function request(path, method = 'GET', body, signal) {
    const headers = { Accept: 'application/json' };
    if (body !== undefined) {
      headers['Content-Type'] = 'application/json';
      headers['X-CSRF-Token'] = csrfToken;
    }
    const response = await fetch(endpoint + path, {
      method,
      headers,
      credentials: 'same-origin',
      body: body === undefined ? undefined : JSON.stringify(body),
      signal,
    });
    const data = await response.json().catch(() => null);
    if (!response.ok || !data) {
      const error = new Error(typeof data?.error === 'string' ? data.error : (
        response.status === 401 ? 'Your session expired. Sign in again to continue.' : 'The study classroom could not load this request. Try again.'
      ));
      error.status = response.status;
      throw error;
    }
    return data;
  }

  function localHref(raw) {
    if (typeof raw !== 'string' || !raw) return null;
    try {
      const url = new URL(raw, window.location.origin);
      return url.origin === window.location.origin && !url.username && !url.password
        ? url.pathname + url.search + url.hash
        : null;
    } catch {
      return null;
    }
  }

  function studyHref({ lessonId, entryId, sectionId, panel }) {
    const params = new URLSearchParams({ lesson_id: lessonId });
    if (entryId) params.set('entry_id', entryId);
    if (sectionId) params.set('section_id', sectionId);
    if (panel === 'lecture') params.set('panel', panel);
    return window.location.pathname + '?' + params.toString();
  }

  function readLocation() {
    const params = new URLSearchParams(window.location.search);
    const requested = params.get('lesson_id');
    return {
      lessonId: lessonTitles.has(requested) ? requested : classroom.dataset.lessonId,
      entryId: params.get('entry_id'),
      sectionId: params.get('section_id'),
      panel: params.get('panel'),
    };
  }

  function locationPanel(target) {
    return target.sectionId || target.panel === 'lecture' ? tabs[2] : tabs[1];
  }

  function selectTab(selected, focus = false) {
    tab = selected;
    for (const [button, panel] of panels) {
      const isSelected = button === tab;
      button.setAttribute('aria-selected', String(isSelected));
      button.tabIndex = isSelected ? 0 : -1;
      panel.hidden = !desktop.matches && !isSelected;
    }
    if (focus) selected.focus();
  }

  function applyLayout() {
    classroom.querySelector('.study-tabs').hidden = desktop.matches;
    for (const [button, panel] of panels) {
      if (desktop.matches) {
        panel.removeAttribute('role');
        panel.setAttribute('aria-labelledby', panel.id + '-heading');
      } else {
        panel.setAttribute('role', 'tabpanel');
        panel.setAttribute('aria-labelledby', button.id);
      }
    }
    selectTab(tab);
    if (desktop.matches) refreshSeparators();
  }

  for (const [index, button] of tabs.entries()) {
    button.addEventListener('click', () => selectTab(button));
    button.addEventListener('keydown', (event) => {
      const shifts = { ArrowLeft: -1, ArrowRight: 1 };
      let next;
      if (event.key in shifts) next = (index + shifts[event.key] + tabs.length) % tabs.length;
      else if (event.key === 'Home') next = 0;
      else if (event.key === 'End') next = tabs.length - 1;
      else return;
      event.preventDefault();
      selectTab(tabs[next], true);
    });
  }

  const separators = [...grid.querySelectorAll('[data-resize-panel]')];

  function panelWidth(side) {
    return Math.round(byId('study-' + side).getBoundingClientRect().width);
  }

  function maxWidth(side) {
    const other = side === 'trail' ? 'lecture' : 'trail';
    const bars = separators.reduce((total, bar) => total + bar.offsetWidth, 0);
    return Math.max(widths[side], grid.clientWidth - panelWidth(other) - widths.chat - bars);
  }

  function resizePanel(side, size) {
    const next = Math.round(Math.min(maxWidth(side), Math.max(widths[side], size)));
    panelSizes[side] = next;
    grid.style.setProperty('--study-' + side + '-width', next + 'px');
  }

  function refreshSeparators() {
    for (const separator of separators) {
      const side = separator.dataset.resizePanel;
      const width = panelWidth(side);
      separator.setAttribute('aria-valuemin', String(widths[side]));
      separator.setAttribute('aria-valuemax', String(maxWidth(side)));
      separator.setAttribute('aria-valuenow', String(width));
      separator.setAttribute('aria-valuetext', width + ' pixels');
    }
  }

  for (const separator of separators) {
    const side = separator.dataset.resizePanel;
    const direction = side === 'trail' ? 1 : -1;
    let pointer = null;

    separator.addEventListener('pointerdown', (event) => {
      if (event.button !== 0) return;
      pointer = { id: event.pointerId, x: event.clientX, width: panelWidth(side) };
      separator.focus();
      separator.setPointerCapture(event.pointerId);
      grid.setAttribute('data-resizing', '');
    });
    separator.addEventListener('pointermove', (event) => {
      if (pointer?.id !== event.pointerId) return;
      resizePanel(side, pointer.width + direction * (event.clientX - pointer.x));
      refreshSeparators();
    });
    separator.addEventListener('lostpointercapture', () => {
      pointer = null;
      grid.removeAttribute('data-resizing');
    });
    separator.addEventListener('keydown', (event) => {
      let size;
      if (event.key === 'ArrowLeft') size = panelWidth(side) - 24 * direction;
      else if (event.key === 'ArrowRight') size = panelWidth(side) + 24 * direction;
      else if (event.key === 'Home') size = widths[side];
      else if (event.key === 'End') size = maxWidth(side);
      else return;
      event.preventDefault();
      resizePanel(side, size);
      refreshSeparators();
    });
  }

  desktop.addEventListener('change', applyLayout);
  classroom.ownerDocument.querySelector('.study-skip')?.addEventListener('click', () => selectTab(tabs[1]));
  if ('ResizeObserver' in window) {
    const gridResize = new ResizeObserver(() => {
      if (!desktop.matches) return;
      for (const side of ['trail', 'lecture']) {
        if (panelSizes[side] !== undefined) resizePanel(side, panelSizes[side]);
      }
      refreshSeparators();
    });
    gridResize.observe(grid);
  }

  function onPlainClick(anchor, callback) {
    anchor.addEventListener('click', (event) => {
      if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      callback();
    });
  }

  function trailLink(entry) {
    const target = { lessonId: String(entry.lesson_id), entryId: String(entry.id) };
    const anchor = element('a', '', 'study-trail-link');
    anchor.href = studyHref(target);
    if (target.entryId === locationState.entryId) anchor.setAttribute('aria-current', 'true');
    const info = element('span', '', 'study-trail-info');
    const badge = element('span', entry.status === 'needs_review' ? 'Needs review' : 'Explored', 'study-badge');
    badge.dataset.status = entry.status;
    info.append(badge, element('span', lessonTitles.get(target.lessonId) || '', 'study-muted'));
    anchor.append(element('span', entry.question, 'study-trail-question'), info);
    onPlainClick(anchor, () => navigate(target, tabs[1]));
    return anchor;
  }

  function renderTrail() {
    const entries = [...trail.values()].sort((a, b) => Number(b.id) - Number(a.id));
    const count = entries.filter((entry) => entry.status === 'needs_review').length;
    byId('study-review-count').textContent = String(count);
    byId('study-filter-all').setAttribute('aria-pressed', String(!reviewOnly));
    byId('study-filter-review').setAttribute('aria-pressed', String(reviewOnly));

    const visible = reviewOnly ? entries.filter((entry) => entry.status === 'needs_review') : entries;
    trailList.replaceChildren(...visible.map((entry) => {
      const item = element('li');
      item.append(trailLink(entry));
      return item;
    }));
    const empty = byId('study-trail-empty');
    empty.hidden = visible.length !== 0;
    empty.textContent = reviewOnly
      ? 'Nothing is marked for review.'
      : 'Your questions will appear here.';
  }

  byId('study-filter-all').addEventListener('click', () => {
    reviewOnly = false;
    renderTrail();
  });
  byId('study-filter-review').addEventListener('click', () => {
    reviewOnly = true;
    renderTrail();
  });

  function appendReading(container, value) {
    const text = String(value ?? '');
    const parts = text.split(/(^\x60{3}[^\n]*\n[\s\S]*?^\x60{3}[ \t]*$)/gm);
    for (const chunk of parts) {
      const part = chunk.trimEnd();
      if (part.startsWith('\x60\x60\x60') && part.endsWith('\x60\x60\x60')) {
        const code = element('pre', '', 'study-code');
        code.append(element('code', part.slice(part.indexOf('\n') + 1, -3).trimEnd()));
        container.append(code);
      } else {
        for (const paragraph of part.split(/\n\s*\n/)) {
          if (paragraph.trim()) container.append(element('p', paragraph.trim()));
        }
      }
    }
  }

  function buildCitation(citation) {
    const target = { lessonId: String(citation.lesson_id), sectionId: String(citation.section_id) };
    if (!lessonTitles.has(target.lessonId)) return null;
    const item = element('li');
    const link = element('a', '', 'study-citation');
    link.href = studyHref(target);
    link.append(
      element('strong', citation.title),
      element('span', citation.excerpt),
    );
    onPlainClick(link, () => navigate(target, tabs[2]));
    item.append(link);
    return item;
  }

  function renderChat() {
    if (!lesson) return;
    byId('study-chat-context').textContent = 'Day ' + lesson.day_number + ' · ' + lesson.title;
    const entries = [...trail.values()].filter((entry) => String(entry.lesson_id) === String(lesson.id));
    entries.sort((a, b) => Number(a.id) - Number(b.id));
    const articles = [];
    statusActions.clear();
    for (const entry of entries) {
      const article = element('article', '', 'study-entry');
      article.id = 'study-entry-' + String(entry.id);
      article.tabIndex = -1;
      const yourQuestion = element('div', '', 'study-bubble study-bubble-user');
      yourQuestion.append(element('small', 'You'), element('p', entry.question));
      const answer = element('div', '', 'study-bubble study-bubble-tutor');
      answer.append(element('small', 'Course tutor'));
      appendReading(answer, entry.answer);
      const citations = (entry.citations || []).map(buildCitation).filter(Boolean);
      if (citations.length) {
        const list = element('ul', '', 'study-citations');
        list.append(...citations);
        answer.append(element('small', 'Sources'), list);
      }

      const actions = element('div', '', 'study-entry-actions');
      const marking = entry.status === 'needs_review' ? 'explored' : 'needs_review';
      const mark = element('button', marking === 'explored' ? 'Mark explored' : 'Mark for review', 'study-secondary');
      mark.type = 'button';
      statusActions.set(String(entry.id), mark);
      mark.addEventListener('click', () => setEntryStatus(entry, marking, mark));
      actions.append(mark);
      const practice = localHref(entry.practice_url);
      if (marking === 'explored' && practice) {
        const link = element('a', 'Practice this topic');
        link.href = practice;
        actions.append(link);
      }
      article.append(yourQuestion, answer, actions);
      articles.push(article);
    }
    conversation.replaceChildren(...articles);
    byId('study-chat-empty').hidden = entries.length > 0;
  }

  function renderLecture() {
    byId('study-lesson-title').textContent = lesson.title;
    byId('study-lesson-day').textContent = 'Day ' + lesson.day_number;
    sectionNodes.clear();
    const sections = lesson.sections.map((section) => {
      const node = element('section', '', 'study-source');
      node.tabIndex = -1;
      node.append(element('h4', section.title));
      appendReading(node, section.text);
      sectionNodes.set(String(section.id), node);
      return node;
    });
    lessonSections.replaceChildren(...sections);
  }

  function renderFollowups(followups) {
    const list = byId('study-followup-list');
    const entries = followups.filter((followup) => lessonTitles.has(String(followup.lesson_id)));
    list.replaceChildren(...entries.map((followup) => {
      const item = element('li');
      const link = element('a', followup.title);
      const target = { lessonId: String(followup.lesson_id), panel: 'lecture' };
      link.href = studyHref(target);
      onPlainClick(link, () => navigate(target, tabs[2]));
      item.append(link, element('p', followup.message, 'study-muted'));
      if (followup.due_on) {
        const due = element('time', followup.due_on, 'study-muted');
        due.dateTime = followup.due_on;
        item.append(due);
      }
      const practice = localHref(followup.practice_url);
      if (practice) {
        const practiceLink = element('a', 'Practice this lesson', 'study-followup-practice');
        practiceLink.href = practice;
        item.append(practiceLink);
      }
      return item;
    }));
    byId('study-followups').hidden = entries.length === 0;
  }

  function refreshNotes() {
    const id = String(lesson.id);
    const draft = noteDrafts.get(id);
    noteField.value = draft?.text ?? notes.text;
    noteField.readOnly = noteSaves.has(id);
    noteSave.disabled = !draft || noteSaves.has(id);
    noteReload.hidden = !noteConflicts.has(id);
    noteStatus.textContent = draft ? 'Unsaved draft in this tab.' : '';
    noteError.textContent = noteConflicts.has(id)
      ? 'Saved notes changed in another tab. Copy this draft before loading the saved version.'
      : '';
    noteForm.hidden = false;
  }

  function focusDestination() {
    const { sectionId, entryId } = locationState;
    for (const node of sectionNodes.values()) node.classList.remove('study-source-highlight');
    if (tab === tabs[2]) {
      const selected = sectionNodes.get(sectionId);
      if (selected) {
        selected.classList.add('study-source-highlight');
        selected.focus();
      } else {
        byId('study-lesson-title').focus();
        if (sectionId) status.textContent = 'The cited section is unavailable. The lesson is open.';
      }
    } else if (entryId) {
      const entry = byId('study-entry-' + entryId);
      if (entry) entry.focus();
      else status.textContent = 'That question is unavailable in this lesson.';
    }
  }

  function refreshComposer() {
    send.disabled = asking || isLoading || !lesson;
    send.textContent = asking ? 'Finding sources…' : 'Ask tutor';
    byId('study-chat-working').hidden = !asking;
    question.readOnly = asking;
  }

  async function loadLesson({ focus = true, clearDraft = false } = {}) {
    lessonRequest?.abort();
    const controller = new AbortController();
    lessonRequest = controller;
    const requestedId = locationState.lessonId;
    const params = new URLSearchParams({ lesson_id: requestedId });
    if (locationState.entryId) params.set('entry_id', locationState.entryId);
    const startRevision = trailRevision;
    isLoading = true;
    lesson = null;
    noteForm.hidden = true;
    byId('study-lesson-title').textContent = 'Loading lesson…';
    byId('study-lesson-day').textContent = '';
    byId('study-chat-context').textContent = 'Loading lesson context…';
    byId('study-retry-lecture').hidden = true;
    lectureError.textContent = '';
    lessonSections.replaceChildren();
    conversation.replaceChildren();
    refreshComposer();

    try {
      const data = await request('/state?' + params.toString(), 'GET', undefined, controller.signal);
      if (controller.signal.aborted) return;
      if (String(data.lesson?.id) !== requestedId) throw new Error('The selected lesson is unavailable.');
      lesson = data.lesson;
      notes = data.notes || { text: '', version: 0 };
      for (const entry of data.trail) {
        const id = String(entry.id);
        if ((trailWrites.get(id) || 0) <= startRevision) trail.set(id, entry);
      }
      if (clearDraft) {
        noteDrafts.delete(requestedId);
        noteConflicts.delete(requestedId);
      }
      renderTrail();
      renderChat();
      renderLecture();
      renderFollowups(data.followups || []);
      refreshNotes();
      if (focus) focusDestination();
    } catch (error) {
      if (controller.signal.aborted) return;
      lesson = null;
      lectureError.textContent = error.message;
      byId('study-lesson-title').textContent = 'Lesson unavailable';
      byId('study-chat-context').textContent = 'Open the lecture panel to reload the lesson.';
      byId('study-retry-lecture').hidden = false;
      status.textContent = error.message;
    } finally {
      if (!controller.signal.aborted) {
        isLoading = false;
        refreshComposer();
      }
    }
  }

  function navigate(target, panel, { updateHistory = true, focus = true } = {}) {
    if (!lessonTitles.has(target.lessonId)) return;
    locationState = target;
    lessonSelect.value = target.lessonId;
    chatError.textContent = '';
    status.textContent = '';
    selectTab(panel);
    if (updateHistory) {
      const next = studyHref(target);
      if (next !== window.location.pathname + window.location.search) window.history.pushState(null, '', next);
    }
    renderTrail();
    if (String(lesson?.id) === target.lessonId && (!target.entryId || trail.has(target.entryId))) {
      if (focus) focusDestination();
    } else {
      loadLesson({ focus });
    }
  }

  lessonSelect.addEventListener('change', () => {
    navigate({ lessonId: lessonSelect.value }, tab, { focus: false });
  });
  window.addEventListener('popstate', () => {
    const target = readLocation();
    navigate(target, locationPanel(target), { updateHistory: false });
  });
  byId('study-retry-lecture').addEventListener('click', () => loadLesson());
  noteReload.addEventListener('click', () => loadLesson({ clearDraft: true }));

  function saveEntry(entry) {
    const id = String(entry.id);
    trailWrites.set(id, ++trailRevision);
    trail.set(id, entry);
    renderTrail();
    renderChat();
  }

  async function setEntryStatus(entry, nextStatus, button) {
    button.disabled = true;
    chatError.textContent = '';
    try {
      const data = await request('/trail/' + encodeURIComponent(entry.id), 'PATCH', { status: nextStatus });
      saveEntry(data.entry);
      status.textContent = nextStatus === 'needs_review' ? 'Question marked for review.' : 'Question marked explored.';
      statusActions.get(String(entry.id))?.focus();
    } catch (error) {
      chatError.textContent = error.message;
    } finally {
      button.disabled = false;
    }
  }

  byId('study-chat-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const text = question.value.trim();
    if (asking || isLoading || !lesson) return;
    chatError.textContent = '';
    if (text.length < 3) {
      chatError.textContent = 'Enter a question of at least three characters.';
      question.focus();
      return;
    }

    const lessonId = String(lesson.id);
    const previous = retryAsk?.lessonId === lessonId && retryAsk?.question === text;
    const id = previous ? retryAsk.id : crypto.randomUUID();
    retryAsk = { id, lessonId, question: text };
    asking = true;
    refreshComposer();
    chatLog.scrollTop = chatLog.scrollHeight;
    try {
      const data = await request('/ask', 'POST', { lesson_id: Number(lessonId), question: text, request_id: id });
      retryAsk = null;
      question.value = '';
      saveEntry(data.entry);
      if (String(lesson?.id) === lessonId) {
        locationState = { lessonId, entryId: String(data.entry.id) };
        window.history.replaceState(null, '', studyHref(locationState));
        renderTrail();
        chatLog.scrollTop = chatLog.scrollHeight;
      }
      status.textContent = 'Answer added to your study trail.';
    } catch (error) {
      chatError.textContent = error.message;
    } finally {
      asking = false;
      refreshComposer();
      if (tab === tabs[1]) question.focus();
    }
  });

  noteField.addEventListener('input', () => {
    if (!lesson || !notes) return;
    const id = String(lesson.id);
    const draft = noteDrafts.get(id);
    if (noteField.value === notes.text && !noteConflicts.has(id)) noteDrafts.delete(id);
    else noteDrafts.set(id, { text: noteField.value, version: draft?.version ?? notes.version });
    noteSave.disabled = !noteDrafts.has(id);
    noteStatus.textContent = noteDrafts.has(id) ? 'Unsaved draft in this tab.' : '';
  });

  noteForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!lesson) return;
    const id = String(lesson.id);
    const draft = noteDrafts.get(id);
    if (!draft || noteSaves.has(id)) return;
    noteSaves.add(id);
    noteSave.disabled = true;
    noteField.readOnly = true;
    noteError.textContent = '';
    noteStatus.textContent = 'Saving notes…';

    try {
      const data = await request('/notes/' + encodeURIComponent(id), 'PUT', draft);
      noteDrafts.delete(id);
      noteConflicts.delete(id);
      if (String(lesson?.id) === id) {
        notes = data.notes;
        noteField.value = notes.text;
        noteReload.hidden = true;
        noteStatus.textContent = 'Notes saved.';
      }
    } catch (error) {
      if (error.status === 409) noteConflicts.add(id);
      if (String(lesson?.id) === id) {
        noteReload.hidden = error.status !== 409;
        noteError.textContent = error.status === 409
          ? 'Saved notes changed in another tab. Copy this draft before loading the saved version.'
          : error.message;
        noteStatus.textContent = 'Unsaved draft in this tab.';
      }
    } finally {
      noteSaves.delete(id);
      if (String(lesson?.id) === id) {
        noteField.readOnly = false;
        noteSave.disabled = !noteDrafts.has(id);
      }
    }
  });

  const initial = readLocation();
  applyLayout();
  if (!lessonTitles.size) {
    lessonSelect.disabled = true;
    byId('study-lesson-title').textContent = 'No lessons are available yet';
    byId('study-chat-context').textContent = 'The tutor will be available once this course has lessons.';
    return;
  }
  navigate(initial, locationPanel(initial), {
    updateHistory: false,
    focus: Boolean(initial.entryId || initial.sectionId || initial.panel === 'lecture'),
  });
})();
