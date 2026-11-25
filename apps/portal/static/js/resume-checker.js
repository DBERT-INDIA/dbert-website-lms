(() => {
  'use strict';

  const byId = (id) => document.getElementById(id);
  const categories = [
    { key: 'keywords', label: 'Keyword alignment', prefix: 'kw' },
    { key: 'impact_verbs', label: 'Impact and metrics', prefix: 'act' },
    { key: 'structure', label: 'Structure and contact', prefix: 'struct' },
    { key: 'length_hygiene', label: 'Length and formatting', prefix: 'len' },
    { key: 'domain_alignment', label: 'Role-specific skills', prefix: 'role' },
  ];
  const scoreLabels = ['ATS score', ...categories.map(({ label }) => label)];
  const domainButtons = [...byId('domainPills').querySelectorAll('button')];
  const uploadTabButton = byId('tabUploadBtn');
  const pasteTabButton = byId('tabPasteBtn');
  const pdfInput = byId('pdfInput');
  const dropZone = byId('dropZone');
  const scanButton = byId('btnScan');
  const scanError = byId('scanError');
  const unlockForm = byId('unlockForm');
  const unlockButton = byId('unlockButton');
  const unlockError = byId('unlockError');
  const saveBaseline = byId('saveBaseline');
  const clearBaseline = byId('clearBaseline');
  const comparisonStatus = byId('comparisonStatus');
  const comparisonTable = byId('comparisonTable');

  let selectedDomain = domainButtons.find((button) => button.classList.contains('active')).dataset.domain;
  let inputMode = 'pdf';
  let selectedFile = null;
  let latestAudit = null;
  let baseline = null;

  function setPressed(button, pressed) {
    button.classList.toggle('active', pressed);
    button.setAttribute('aria-pressed', String(pressed));
  }

  for (const button of domainButtons) {
    button.addEventListener('click', () => {
      selectedDomain = button.dataset.domain;
      domainButtons.forEach((option) => setPressed(option, option === button));
    });
  }

  function setInputMode(mode) {
    inputMode = mode;
    const isPdf = mode === 'pdf';
    byId('uploadTab').hidden = !isPdf;
    byId('pasteTab').hidden = isPdf;
    setPressed(uploadTabButton, isPdf);
    setPressed(pasteTabButton, !isPdf);
    scanError.textContent = '';
  }

  uploadTabButton.addEventListener('click', () => setInputMode('pdf'));
  pasteTabButton.addEventListener('click', () => setInputMode('text'));

  function selectPdf(file) {
    if (!file) return;
    scanError.textContent = '';
    selectedFile = null;
    byId('dropLabel').textContent = 'Choose or drop a PDF résumé';
    if (file.type !== 'application/pdf' && !/\.pdf$/i.test(file.name)) {
      scanError.textContent = 'Choose a PDF file.';
    } else if (file.size > 5 * 1024 * 1024) {
      scanError.textContent = 'Choose a PDF of 5 MB or less.';
    } else {
      selectedFile = file;
      byId('dropLabel').textContent = 'Selected: ' + file.name;
    }
  }

  dropZone.addEventListener('click', () => pdfInput.click());
  pdfInput.addEventListener('change', () => {
    selectPdf(pdfInput.files[0]);
    pdfInput.value = '';
  });
  dropZone.addEventListener('dragover', (event) => {
    event.preventDefault();
    dropZone.classList.add('dragging');
  });
  dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragging'));
  dropZone.addEventListener('drop', (event) => {
    event.preventDefault();
    dropZone.classList.remove('dragging');
    selectPdf(event.dataTransfer.files[0]);
  });

  function setBusy(busy) {
    scanButton.disabled = busy;
    unlockButton.disabled = busy;
  }

  async function requestAudit(subject, formData) {
    formData.set('domain', subject.domain);
    if (subject.jobDescription) formData.set('job_description', subject.jobDescription);
    if (subject.file) {
      formData.set('file', subject.file);
    } else {
      formData.set('text', subject.text);
    }
    const response = await fetch('/api/tools/ats-checker', { method: 'POST', body: formData });
    const data = await response.json().catch(() => null);
    if (!response.ok || data?.status !== 'success') {
      throw new Error(data?.message || 'The résumé audit could not be completed. Please try again.');
    }
    return data;
  }

  function scoreSnapshot(data, subject) {
    const values = [data.score, ...categories.map(({ key }) => data.breakdown?.[key]?.score)];
    if (!values.every(Number.isFinite)) {
      throw new Error('The audit returned incomplete scores. Please try again.');
    }
    return {
      domain: data.domain || subject.domain,
      inputLabel: subject.file ? 'PDF' : 'Pasted text',
      values,
    };
  }

  scanButton.addEventListener('click', async () => {
    scanError.textContent = '';
    const subject = { domain: selectedDomain, jobDescription: byId('atsJobDescription').value.trim() };
    if (inputMode === 'pdf') {
      if (!selectedFile) {
        scanError.textContent = 'Choose a PDF résumé or switch to pasted text.';
        return;
      }
      subject.file = selectedFile;
    } else {
      subject.text = byId('resumeText').value.trim();
      if (subject.text.length < 30) {
        scanError.textContent = 'Paste at least 30 characters of résumé text.';
        return;
      }
    }

    setBusy(true);
    byId('scanButtonLabel').textContent = 'Auditing résumé…';
    try {
      const data = await requestAudit(subject, new FormData());
      const scores = scoreSnapshot(data, subject);
      latestAudit = { scores, subject };
      renderAudit(data, scores);
      byId('resultsTitle').focus();
    } catch (error) {
      scanError.textContent = error.message || 'The résumé audit could not be completed. Please try again.';
    } finally {
      setBusy(false);
      byId('scanButtonLabel').textContent = 'Run Free AI ATS Audit';
    }
  });

  function renderAudit(data, scores) {
    byId('scoreNum').textContent = scores.values[0];
    byId('resultDomain').textContent = scores.domain;
    byId('scoreGauge').style.borderColor = data.color;
    byId('tierBadge').textContent = data.tier;
    byId('tierBadge').style.backgroundColor = data.color;

    for (const { key, prefix } of categories) {
      const percentage = data.breakdown[key].percentage + '%';
      byId(prefix + 'Percent').textContent = percentage;
      byId(prefix + 'Bar').style.width = percentage;
    }

    const strengths = (data.strengths || []).map((strength) => {
      const item = document.createElement('li');
      item.textContent = strength;
      return item;
    });
    byId('strengthsList').replaceChildren(...strengths);
    renderJobFit(data.job_fit);
    unlockError.textContent = '';
    byId('gateSection').hidden = !data.locked;
    byId('unlockedContent').hidden = !!data.locked;
    if (!data.locked) renderFullReport(data);
    byId('resultsWrap').hidden = false;
    renderComparison();
  }

  function renderJobFit(fit) {
    byId('atsJobFit').hidden = !fit;
    if (!fit) return;
    const total = fit.matched.length + fit.missing.length;
    byId('atsJobFitStatus').textContent = total
      ? fit.matched.length + ' of ' + total + ' recognized skills mentioned in your résumé.'
      : 'No known skills were found in this job description.';
    byId('atsJobFitSkills').replaceChildren(...[
      ...fit.matched.map(skill => [skill, 'Mentioned']),
      ...fit.missing.map(skill => [skill, 'Needs evidence']),
    ].map(([skill, status]) => {
      const item = document.createElement('li');
      item.textContent = skill + ' — ' + status;
      return item;
    }));
    byId('atsJobFitResources').replaceChildren(...fit.next_steps.map(({ href, label }) => {
      const item = document.createElement('li');
      const link = document.createElement('a');
      if (typeof href === 'string' && href.startsWith('/search?')) link.href = href;
      link.textContent = label;
      item.append(link);
      return item;
    }));
  }

  function renderComparison() {
    const current = latestAudit.scores;
    clearBaseline.hidden = !baseline;
    saveBaseline.disabled = baseline === current;
    comparisonTable.hidden = true;

    if (!baseline) {
      comparisonStatus.textContent = 'Set this audit as a baseline, then scan a revision for the same role. Comparison scores stay in this tab until you reload or close it.';
      return;
    }
    if (baseline === current) {
      comparisonStatus.textContent = 'Baseline saved for ' + baseline.domain + '. Scan a revision to see what changed.';
      return;
    }
    if (baseline.domain !== current.domain) {
      comparisonStatus.textContent = 'Choose the same target role to compare. Your baseline is for ' + baseline.domain + '.';
      return;
    }

    comparisonStatus.textContent = 'Comparing audits for ' + current.domain + '. Changes are shown in score points.';
    byId('baselineColumn').textContent = 'Baseline (' + baseline.inputLabel + ')';
    byId('revisionColumn').textContent = 'Revision (' + current.inputLabel + ')';
    const rows = scoreLabels.map((label, index) => {
      const before = baseline.values[index];
      const after = current.values[index];
      const change = after - before;
      const row = document.createElement('tr');
      const heading = document.createElement('th');
      heading.scope = 'row';
      heading.textContent = label;
      row.append(heading);
      row.insertCell().textContent = before;
      row.insertCell().textContent = after;
      const delta = row.insertCell();
      delta.textContent = change > 0 ? '+' + change : String(change).replace('-', '−');
      delta.classList.toggle('score-up', change > 0);
      delta.classList.toggle('score-down', change < 0);
      return row;
    });
    byId('comparisonRows').replaceChildren(...rows);
    comparisonTable.hidden = false;
  }

  saveBaseline.addEventListener('click', () => {
    baseline = latestAudit.scores;
    renderComparison();
    clearBaseline.focus();
  });
  clearBaseline.addEventListener('click', () => {
    baseline = null;
    byId('comparisonRows').replaceChildren();
    renderComparison();
    saveBaseline.focus();
  });

  unlockForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!latestAudit || unlockButton.disabled) return;
    unlockError.textContent = '';
    const contact = new FormData(unlockForm);
    if (!String(contact.get('name')).trim()) {
      unlockError.textContent = 'Enter your full name.';
      return;
    }

    setBusy(true);
    unlockButton.textContent = 'Unlocking report…';
    try {
      const data = await requestAudit(latestAudit.subject, contact);
      if (data.locked) throw new Error('The full report could not be unlocked. Check your details and try again.');
      renderFullReport(data);
      byId('gateSection').hidden = true;
      byId('unlockedContent').hidden = false;
      byId('fullReportTitle').focus();
    } catch (error) {
      unlockError.textContent = error.message || 'The full report could not be unlocked. Please try again.';
    } finally {
      setBusy(false);
      unlockButton.textContent = 'Unlock Full Report';
    }
  });

  function setReportItems(id, items, emptyMessage) {
    const container = byId(id);
    if (items.length) {
      container.replaceChildren(...items);
    } else {
      const message = document.createElement('p');
      message.className = 'checker-note';
      message.textContent = emptyMessage;
      container.replaceChildren(message);
    }
  }

  function renderFullReport(data) {
    const keywords = (data.critical_missing_keywords || []).map((keyword) => {
      const chip = document.createElement('span');
      chip.className = 'keyword-chip';
      chip.textContent = keyword;
      return chip;
    });
    setReportItems('missingKeywordsList', keywords, 'No missing keywords were reported.');

    const rewrites = (data.recommendations?.bullet_rewrites || []).map((rewrite) => {
      const item = document.createElement('div');
      item.className = 'rewrite-item';
      for (const [label, value] of [['Original', rewrite.original], ['Suggested', rewrite.improved], ['Why', rewrite.why]]) {
        if (!value) continue;
        const line = document.createElement('p');
        line.textContent = label + ': ' + value;
        item.append(line);
      }
      return item;
    });
    setReportItems('rewritesList', rewrites, 'No suggested rewrites were reported.');

    const jobs = (data.matched_jobs || []).map((job) => {
      const item = document.createElement('div');
      item.className = 'job-match';
      const summary = document.createElement('div');
      const title = document.createElement('strong');
      title.textContent = job.title;
      const company = document.createElement('p');
      company.className = 'checker-note';
      company.textContent = job.company_name + ' · ' + (job.location || 'Remote');
      summary.append(title, company);
      const link = document.createElement('a');
      link.href = '/apply/' + encodeURIComponent(job.id);
      link.className = 'btn btn-secondary';
      link.textContent = 'Apply now';
      link.setAttribute('aria-label', 'Apply for ' + job.title);
      item.append(summary, link);
      return item;
    });
    setReportItems('matchedJobsList', jobs, 'No matching roles were reported for this audit.');

    const cvBuilder = byId('lmsRedirectBtn');
    cvBuilder.href = '/portal/cv';
    if (!data.lms_signup_url) return;
    try {
      const signup = new URL(data.lms_signup_url, window.location.href);
      if (signup.origin === window.location.origin || signup.origin === 'https://lms.dbert.in') {
        cvBuilder.href = signup.href;
      }
    } catch {
      // Keep the CV builder link when the server returns an invalid URL.
    }
  }
})();
