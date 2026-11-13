'use client';

import React, { useState } from 'react';
import { Check, Copy, Terminal } from 'lucide-react';
import s from './StandardMarkdownRenderer.module.css';

interface StandardMarkdownRendererProps {
  content: string;
  titleToStrip?: string;
}

function CodeBlock({ code, lang }: { code: string; lang: string }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className={s.codeBlockWrap}>
      <div className={s.codeHeader}>
        <div className={s.codeLang}>
          <Terminal size={14} className={s.codeIcon} />
          <span>{lang ? lang.toUpperCase() : 'CODE'}</span>
        </div>
        <button
          onClick={handleCopy}
          className={s.copyBtn}
          title="Copy code to clipboard"
          aria-label="Copy code to clipboard"
        >
          {copied ? (
            <>
              <Check size={14} style={{ color: '#10B981' }} />
              <span style={{ color: '#10B981' }}>Copied!</span>
            </>
          ) : (
            <>
              <Copy size={14} />
              <span>Copy</span>
            </>
          )}
        </button>
      </div>
      <pre className={s.codePre}>
        <code className={s.codeText}>{code}</code>
      </pre>
    </div>
  );
}

function renderInline(text: string): React.ReactNode {
  // Regex to split by bold (**text**), inline code (`code`), links ([text](url)), and italic (*text*)
  const tokens = text.split(/(\*\*[^*]+\*\*|`[^`]+`|\[[^\]]+\]\([^)]+\)|\*[^*]+\*)/g);

  return tokens.map((tok, i) => {
    if (tok.startsWith('**') && tok.endsWith('**')) {
      return (
        <strong key={i} className={s.articleStrong}>
          {tok.slice(2, -2)}
        </strong>
      );
    }
    if (tok.startsWith('`') && tok.endsWith('`')) {
      return (
        <code key={i} className={s.articleInlineCode}>
          {tok.slice(1, -1)}
        </code>
      );
    }
    if (tok.startsWith('*') && tok.endsWith('*')) {
      return (
        <em key={i} className={s.articleEm}>
          {tok.slice(1, -1)}
        </em>
      );
    }
    const linkMatch = tok.match(/^\[([^\]]+)\]\(([^)]+)\)$/);
    if (linkMatch) {
      const href = linkMatch[2];
      const isExternal = href.startsWith('http');
      return (
        <a
          key={i}
          href={href}
          className={s.articleLink}
          target={isExternal ? '_blank' : undefined}
          rel={isExternal ? 'noopener noreferrer' : undefined}
        >
          {linkMatch[1]}
        </a>
      );
    }
    return tok;
  });
}

export default function StandardMarkdownRenderer({
  content,
  titleToStrip,
}: StandardMarkdownRendererProps) {
  if (!content) return null;

  // 1. Strip YAML frontmatter cleanly if present
  let clean = content.replace(/^---\s*[\r\n]+[\s\S]*?[\r\n]+---\s*[\r\n]*/, '').trim();

  // 1b. Ensure headers have breathing room (empty line after header if missing)
  clean = clean.replace(/^(#{1,6}\s+[^\r\n]+)[\r\n]+(?=[^\r\n#\-\*\d\>])/gm, '$1\n\n');

  // 2. Strip redundant initial # Header or metadata subtitle if present
  const lines = clean.split('\n');
  let startIdx = 0;

  while (startIdx < lines.length && !lines[startIdx].trim()) {
    startIdx++;
  }

  // If first non-empty line is an H1 that duplicates title
  if (startIdx < lines.length && lines[startIdx].trim().startsWith('# ')) {
    const headingText = lines[startIdx].trim().replace(/^#\s+/, '').trim();
    if (!titleToStrip || headingText.toLowerCase().includes(titleToStrip.toLowerCase().slice(0, 20)) || titleToStrip.toLowerCase().includes(headingText.toLowerCase().slice(0, 20))) {
      startIdx++; // Skip duplicate title
      // Also skip immediate subtitle like *Author: ...* or ---
      while (startIdx < lines.length) {
        const nextL = lines[startIdx].trim();
        if (nextL.startsWith('*Author:') || (nextL.startsWith('*') && nextL.endsWith('*')) || nextL === '---' || !nextL) {
          startIdx++;
        } else {
          break;
        }
      }
    }
  }

  clean = lines.slice(startIdx).join('\n').trim();

  // Recognize common standalone unhashed headings (e.g. from raw submissions)
  const commonHeaders = [
    'Introduction',
    'Understanding Microservices Architecture',
    'Why Choose Fast API?',
    'Why Choose FastAPI?',
    'Core Architecture & Design',
    'Key Architectural Advantages',
    'System Overview & Problem Statement',
    'Conclusion',
    'Summary & Next Steps',
  ];


  // 3. Split by blocks
  // Blocks can be: ```code blocks```, tables (|...|), lists, headers, blockquotes, or paragraphs
  const rawBlocks = clean.split(/\n\s*\n/);
  const elements: React.ReactNode[] = [];

  rawBlocks.forEach((block, bIdx) => {
    const trimmed = block.trim();
    if (!trimmed) return;

    // A. Code Block (```lang ... ```)
    if (trimmed.startsWith('```')) {
      const match = trimmed.match(/^```([a-zA-Z0-9_-]*)\n([\s\S]*?)```$/);
      if (match) {
        const lang = match[1] || '';
        const codeText = match[2].trimEnd();
        elements.push(<CodeBlock key={`code-${bIdx}`} lang={lang} code={codeText} />);
        return;
      }
      // Fallback for code block without closing or newline
      const codeLines = trimmed.replace(/^```[a-zA-Z0-9_-]*\n?/i, '').replace(/```$/, '');
      elements.push(<CodeBlock key={`code-${bIdx}`} lang="code" code={codeLines.trimEnd()} />);
      return;
    }

    // B. Horizontal Rule
    if (trimmed === '---' || trimmed === '***' || trimmed === '___') {
      elements.push(<hr key={`hr-${bIdx}`} className={s.articleHr} />);
      return;
    }

    // C. Markdown Headings (#, ##, ###, ####)
    if (trimmed.startsWith('#### ')) {
      elements.push(
        <h4 key={`h4-${bIdx}`} className={s.articleH4}>
          {renderInline(trimmed.replace(/^####\s+/, ''))}
        </h4>
      );
      return;
    }
    if (trimmed.startsWith('### ')) {
      elements.push(
        <h3 key={`h3-${bIdx}`} className={s.articleH3}>
          {renderInline(trimmed.replace(/^###\s+/, ''))}
        </h3>
      );
      return;
    }
    if (trimmed.startsWith('## ')) {
      elements.push(
        <h2 key={`h2-${bIdx}`} className={s.articleH2}>
          {renderInline(trimmed.replace(/^##\s+/, ''))}
        </h2>
      );
      return;
    }
    if (trimmed.startsWith('# ')) {
      elements.push(
        <h2 key={`h1-${bIdx}`} className={s.articleH2}>
          {renderInline(trimmed.replace(/^#\s+/, ''))}
        </h2>
      );
      return;
    }

    // D. Numbered Section Heading (e.g., "1. System Overview & Problem Statement") or Common Section Heading
    const numberedHeaderMatch = trimmed.match(/^(\d+\.\s+[A-Z][^\n]+)$/);
    if ((numberedHeaderMatch && trimmed.length < 100) || commonHeaders.includes(trimmed)) {
      elements.push(
        <h2 key={`nh-${bIdx}`} className={s.articleH2}>
          {renderInline(trimmed)}
        </h2>
      );
      return;
    }


    // E. Blockquote (> ...)
    if (trimmed.startsWith('>')) {
      const bqText = trimmed
        .split('\n')
        .map((l) => l.replace(/^>\s?/, ''))
        .join('\n');
      elements.push(
        <blockquote key={`bq-${bIdx}`} className={s.articleBlockquote}>
          {renderInline(bqText)}
        </blockquote>
      );
      return;
    }

    // F. Markdown Table (| Header 1 | Header 2 |)
    if (trimmed.startsWith('|') && trimmed.includes('\n|')) {
      const tableLines = trimmed.split('\n').filter((l) => l.trim().startsWith('|'));
      if (tableLines.length >= 2) {
        const headerRow = tableLines[0].split('|').slice(1, -1).map((c) => c.trim());
        const bodyRows = tableLines
          .slice(2)
          .map((row) => row.split('|').slice(1, -1).map((c) => c.trim()));

        elements.push(
          <div key={`table-${bIdx}`} className={s.tableWrap}>
            <table className={s.articleTable}>
              <thead>
                <tr>
                  {headerRow.map((cell, cIdx) => (
                    <th key={cIdx}>{renderInline(cell)}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {bodyRows.map((row, rIdx) => (
                  <tr key={rIdx}>
                    {row.map((cell, cIdx) => (
                      <td key={cIdx}>{renderInline(cell)}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        );
        return;
      }
    }

    // G. Unordered List (- or *)
    if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
      const items = trimmed.split('\n').filter(Boolean);
      elements.push(
        <ul key={`ul-${bIdx}`} className={s.articleUl}>
          {items.map((item, iIdx) => (
            <li key={iIdx} className={s.articleLi}>
              {renderInline(item.replace(/^[-*]\s+/, ''))}
            </li>
          ))}
        </ul>
      );
      return;
    }

    // H. Ordered List (1. , 2. )
    if (/^\d+\.\s+/.test(trimmed)) {
      const items = trimmed.split('\n').filter(Boolean);
      elements.push(
        <ol key={`ol-${bIdx}`} className={s.articleOl}>
          {items.map((item, iIdx) => (
            <li key={iIdx} className={s.articleLi}>
              {renderInline(item.replace(/^\d+\.\s+/, ''))}
            </li>
          ))}
        </ol>
      );
      return;
    }

    // I. Standard Paragraph
    elements.push(
      <p key={`p-${bIdx}`} className={s.articleP}>
        {renderInline(trimmed)}
      </p>
    );
  });

  return <div className={s.articleRoot}>{elements}</div>;
}
