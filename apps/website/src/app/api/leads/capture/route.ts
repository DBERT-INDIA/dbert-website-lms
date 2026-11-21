import { NextRequest, NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

interface InboundLeadRecord {
  id: string;
  submittedAt: string;
  fullName: string;
  email: string;
  phone: string;
  college?: string;
  graduationYear?: string;
  domain: string;
  programInterest: 'fellowship' | 'course' | 'both';
  city?: string;
  utmSource?: string;
  utmMedium?: string;
  utmCampaign?: string;
  ipAddress?: string;
  userAgent?: string;
}

function resolveLeadsFilePath(): string {
  const dataDir = path.join(process.cwd(), 'data');
  if (!fs.existsSync(dataDir)) {
    try {
      fs.mkdirSync(dataDir, { recursive: true });
    } catch {
      // ignore
    }
  }
  return path.join(dataDir, 'leads_inbound.json');
}

export async function POST(request: NextRequest) {
  try {
    let body: any;
    try {
      body = await request.json();
    } catch {
      return NextResponse.json({ success: false, error: 'Invalid JSON payload' }, { status: 400 });
    }

    const {
      fullName,
      name,
      email,
      phone,
      college,
      graduationYear,
      domain,
      track,
      programInterest,
      city,
      utmSource,
      utmMedium,
      utmCampaign
    } = body;

    const cleanName = (fullName || name || '').trim();
    const cleanEmail = (email || '').trim().toLowerCase();
    const cleanPhone = (phone || '').trim();
    const cleanDomain = (domain || track || 'Full Stack Web Development').trim();
    const cleanProgram = (programInterest || 'fellowship').toLowerCase();

    if (!cleanName || cleanName.length < 2) {
      return NextResponse.json({ success: false, error: 'Full Name is required (minimum 2 characters).' }, { status: 400 });
    }
    if (!cleanEmail || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(cleanEmail)) {
      return NextResponse.json({ success: false, error: 'A valid email address is required.' }, { status: 400 });
    }
    if (!cleanPhone || cleanPhone.replace(/\D/g, '').length < 10) {
      return NextResponse.json({ success: false, error: 'A valid 10-digit WhatsApp phone number is required.' }, { status: 400 });
    }

    const timestamp = new Date().toISOString();
    const randomHex = Math.random().toString(36).substring(2, 6).toUpperCase();
    const leadId = `DBERT-LEAD-${Date.now().toString().slice(-6)}-${randomHex}`;

    const newLead: InboundLeadRecord = {
      id: leadId,
      submittedAt: timestamp,
      fullName: cleanName,
      email: cleanEmail,
      phone: cleanPhone,
      college: (college || '').trim() || undefined,
      graduationYear: (graduationYear || '').trim() || undefined,
      domain: cleanDomain,
      programInterest: (cleanProgram === 'course' ? 'course' : cleanProgram === 'both' ? 'both' : 'fellowship'),
      city: (city || '').trim() || undefined,
      utmSource: (utmSource || '').trim() || undefined,
      utmMedium: (utmMedium || '').trim() || undefined,
      utmCampaign: (utmCampaign || '').trim() || undefined,
      ipAddress: request.headers.get('x-forwarded-for') || request.headers.get('x-real-ip') || undefined,
      userAgent: request.headers.get('user-agent') || undefined
    };

    const targetFile = resolveLeadsFilePath();
    let existing: InboundLeadRecord[] = [];
    if (fs.existsSync(targetFile)) {
      try {
        const raw = fs.readFileSync(targetFile, 'utf-8');
        existing = JSON.parse(raw);
        if (!Array.isArray(existing)) existing = [];
      } catch {
        existing = [];
      }
    }

    // Check recent duplicate by email + domain in last 24h
    const isDup = existing.some(
      (l) => l.email === cleanEmail && l.domain.toLowerCase() === cleanDomain.toLowerCase()
    );

    if (!isDup) {
      existing.unshift(newLead);
      const tmpPath = `${targetFile}.tmp.${Date.now()}`;
      fs.writeFileSync(tmpPath, JSON.stringify(existing, null, 2), 'utf-8');
      fs.renameSync(tmpPath, targetFile);
    }

    return NextResponse.json(
      {
        success: true,
        leadId,
        message: 'Lead captured successfully. Our admissions squad will connect on WhatsApp within 2 hours.',
        alreadyRegistered: isDup
      },
      { status: 201 }
    );
  } catch (err: any) {
    console.error('Lead capture API error:', err);
    return NextResponse.json(
      { success: false, error: 'Internal server error while capturing lead. Please try again.' },
      { status: 500 }
    );
  }
}
