import { NextResponse } from 'next/server';
import db from '@/lib/db';
import fs from 'fs';
import path from 'path';

const PAGE_SIZE = 15; // 3x5 card grid per page
const VALID_DOMAINS = [
  'AI Agent Development',
  'Full Stack Development',
  'Python Automation',
  'Data Analytics',
  'Data Engineering / Quant Research',
];
const MAX_COMMENT_LENGTH = 500;

function isPlausibleUrl(value: string): boolean {
  try {
    const parsed = new URL(value);
    return parsed.protocol === 'http:' || parsed.protocol === 'https:';
  } catch {
    return false;
  }
}

async function isKnownDbertIntern(email: string): Promise<boolean> {
  const normEmail = email.trim().toLowerCase();
  try {
    const registryPath = path.join(process.cwd(), 'src', 'data', 'certificates_registry.json');
    if (fs.existsSync(registryPath)) {
      const raw = fs.readFileSync(registryPath, 'utf-8');
      const registry = JSON.parse(raw);
      for (const cert of Object.values(registry) as any[]) {
        if (cert?.holderEmail?.toLowerCase() === normEmail) {
          return true;
        }
      }
    }
  } catch (err) {
    console.warn('Could not inspect certificates_registry for auto-approval:', err);
  }

  try {
    const result: any = await db.$queryRaw`
      SELECT 1 FROM dbert_internship.intern_accounts WHERE LOWER(email) = ${normEmail}
      UNION
      SELECT 1 FROM dbert_internship.applications WHERE LOWER(email) = ${normEmail}
      LIMIT 1;
    `;
    if (Array.isArray(result) && result.length > 0) {
      return true;
    }
  } catch (err) {
    console.warn('Database intern lookup skipped:', err);
  }

  return false;
}

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { name, email, profilePicUrl, comment, linkedinUrl, githubUrl, domain } = body;

    if (!name || !email || !profilePicUrl || !comment || !linkedinUrl || !githubUrl || !domain) {
      return NextResponse.json({ error: 'Missing required parameters' }, { status: 400 });
    }

    if (typeof comment !== 'string' || comment.trim().length === 0) {
      return NextResponse.json({ error: 'Comment cannot be empty' }, { status: 400 });
    }

    if (comment.length > MAX_COMMENT_LENGTH) {
      return NextResponse.json(
        { error: `Comment must be ${MAX_COMMENT_LENGTH} characters or fewer` },
        { status: 400 }
      );
    }

    if (!VALID_DOMAINS.includes(domain)) {
      return NextResponse.json({ error: 'Invalid domain selection' }, { status: 400 });
    }

    if (!isPlausibleUrl(profilePicUrl) || !isPlausibleUrl(linkedinUrl) || !isPlausibleUrl(githubUrl)) {
      return NextResponse.json({ error: 'One or more URLs are invalid' }, { status: 400 });
    }

    const isEnrolled = await isKnownDbertIntern(email);
    const status = isEnrolled ? 'approved' : 'pending';
    const reviewedAt = isEnrolled ? new Date() : null;

    const contributor = await db.projectContributor.create({
      data: {
        projectSlug: 'alkame',
        name: name.trim(),
        email: email.trim().toLowerCase(),
        profilePicUrl: profilePicUrl.trim(),
        comment: comment.trim(),
        linkedinUrl: linkedinUrl.trim(),
        githubUrl: githubUrl.trim(),
        domain,
        status,
        reviewedAt,
      },
    });

    return NextResponse.json(
      {
        success: true,
        id: contributor.id,
        autoApproved: isEnrolled,
      },
      { status: 201 }
    );
  } catch (err) {
    console.error('Alkame contributor submission error:', err);
    return NextResponse.json({ error: 'Failed to submit contribution' }, { status: 500 });
  }
}

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const pageParam = parseInt(searchParams.get('page') || '1', 10);
    const page = Number.isFinite(pageParam) && pageParam > 0 ? pageParam : 1;

    const where = { projectSlug: 'alkame', status: 'approved' };

    const [totalCount, contributors] = await Promise.all([
      db.projectContributor.count({ where }),
      db.projectContributor.findMany({
        where,
        orderBy: [{ reviewedAt: 'desc' }, { createdAt: 'desc' }],
        skip: (page - 1) * PAGE_SIZE,
        take: PAGE_SIZE,
        select: {
          id: true,
          name: true,
          profilePicUrl: true,
          comment: true,
          linkedinUrl: true,
          githubUrl: true,
          domain: true,
          reviewedAt: true,
        },
      }),
    ]);

    return NextResponse.json({
      contributors,
      page,
      totalPages: Math.max(1, Math.ceil(totalCount / PAGE_SIZE)),
      totalCount,
    }, { status: 200 });
  } catch (err) {
    console.error('Alkame contributors list error:', err);
    return NextResponse.json({ error: 'Failed to load contributors' }, { status: 500 });
  }
}
