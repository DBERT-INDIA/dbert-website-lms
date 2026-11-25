(() => {
  'use strict';

  const storageKey = 'dbert-saved-opportunities-v1';
  const saveButton = document.querySelector('[data-save-opportunity]');
  const list = document.getElementById('savedOpportunityList');
  const status = document.getElementById('savedOpportunityStatus');
  const isValid = item => item && /^[1-9]\d{0,11}$/.test(item.id)
    && ['job', 'internship'].includes(item.kind) && typeof item.title === 'string';

  function read() {
    const entries = JSON.parse(localStorage.getItem(storageKey) || '[]');
    return Array.isArray(entries) ? entries.filter(isValid).slice(0, 50) : [];
  }

  function write(entries) {
    localStorage.setItem(storageKey, JSON.stringify(entries));
  }

  if (saveButton) {
    const record = {
      id: saveButton.dataset.saveOpportunity,
      kind: saveButton.dataset.opportunityKind,
      title: saveButton.dataset.opportunityTitle.slice(0, 220),
    };
    const error = document.getElementById('saveOpportunityStatus');
    if (!isValid(record)) return;
    const updateButton = entries => {
      const saved = entries.some(item => item.id === record.id);
      saveButton.textContent = saved ? 'Saved' : 'Save opportunity';
      saveButton.setAttribute('aria-pressed', String(saved));
    };
    try {
      updateButton(read());
      saveButton.hidden = false;
    } catch {
      error.textContent = 'Saved opportunities are unavailable in this browser.';
    }
    saveButton.addEventListener('click', () => {
      try {
        const entries = read();
        const next = entries.some(item => item.id === record.id)
          ? entries.filter(item => item.id !== record.id) : [record, ...entries].slice(0, 50);
        write(next);
        updateButton(next);
      } catch {
        error.textContent = 'This opportunity could not be saved in this browser.';
      }
    });
  }

  if (list) loadSaved();

  async function loadSaved() {
    let entries;
    try {
      entries = read();
    } catch {
      status.textContent = 'Saved opportunities are unavailable in this browser.';
      return;
    }
    if (!entries.length) {
      status.textContent = 'You haven’t saved any opportunities yet.';
      return;
    }
    status.textContent = 'Checking availability…';
    let open = null;
    try {
      const response = await fetch('/api/opportunities/availability?ids=' + entries.map(item => item.id).join(','));
      if (response.ok) open = new Set((await response.json()).open_ids.map(String));
    } catch {
      // Keep the shortlist available if the connection drops.
    }
    status.textContent = open ? 'Saved in this browser.' : 'Saved in this browser. Current availability could not be checked.';
    list.replaceChildren(...entries.map(item => {
      const li = document.createElement('li');
      const link = document.createElement('a');
      link.href = `/${item.kind === 'internship' ? 'internships' : 'jobs'}/${item.id}`;
      link.textContent = item.title;
      const details = document.createElement('span');
      const type = item.kind === 'internship' ? 'Internship' : 'Job';
      details.textContent = open ? `${type} · ${open.has(item.id) ? 'Open' : 'Closed or unavailable'}` : type;
      const remove = document.createElement('button');
      remove.type = 'button';
      remove.className = 'btn btn-secondary';
      remove.textContent = 'Remove';
      remove.setAttribute('aria-label', 'Remove ' + item.title);
      remove.addEventListener('click', () => {
        try {
          write(read().filter(entry => entry.id !== item.id));
          li.remove();
          if (!list.children.length) status.textContent = 'You haven’t saved any opportunities yet.';
          (list.querySelector('a') || document.getElementById('savedOpportunityBrowse')).focus();
        } catch {
          status.textContent = 'This opportunity could not be removed.';
        }
      });
      li.append(link, details, remove);
      return li;
    }));
  }
})();
