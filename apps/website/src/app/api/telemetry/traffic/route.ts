import { NextRequest, NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const {
      landingPage,
      referrer,
      referrerDomain,
      channel,
      aiSource,
      utmSource,
      utmMedium,
      utmCampaign,
      refCode,
      device,
      screenRes,
      timestamp,
    } = body || {};

    if (!landingPage) {
      return NextResponse.json({ status: 'ignored' }, { status: 400 });
    }

    const eventRecord = {
      landingPage: String(landingPage).substring(0, 255),
      referrer: String(referrer || '').substring(0, 255),
      referrerDomain: String(referrerDomain || '').substring(0, 100),
      channel: String(channel || 'direct').substring(0, 50),
      aiSource: aiSource ? String(aiSource).substring(0, 50) : undefined,
      utmSource: utmSource ? String(utmSource).substring(0, 50) : undefined,
      utmMedium: utmMedium ? String(utmMedium).substring(0, 50) : undefined,
      utmCampaign: utmCampaign ? String(utmCampaign).substring(0, 50) : undefined,
      refCode: refCode ? String(refCode).substring(0, 50) : undefined,
      device: String(device || 'Desktop').substring(0, 20),
      screenRes: String(screenRes || '').substring(0, 20),
      ip: req.headers.get('x-forwarded-for')?.split(',')[0].trim() || '127.0.0.1',
      userAgent: req.headers.get('user-agent')?.substring(0, 255) || '',
      timestamp: timestamp || new Date().toISOString(),
    };

    // Save to permanent buffer file in data directory
    const candidates = [
      path.resolve(process.cwd(), 'data', 'traffic_events_buffer.jsonl'),
      path.resolve(process.cwd(), '..', '..', 'data', 'traffic_events_buffer.jsonl'),
      '/var/www/dbert-website-lms/data/traffic_events_buffer.jsonl',
    ];

    let targetPath = candidates[0];
    for (const p of candidates) {
      const dir = path.dirname(p);
      if (fs.existsSync(dir)) {
        targetPath = p;
        break;
      }
    }

    fs.appendFileSync(targetPath, JSON.stringify(eventRecord) + '\n', 'utf8');

    return NextResponse.json({ status: 'ok' });
  } catch (err: any) {
    // Non-blocking fail-safe
    return NextResponse.json({ status: 'error', error: err?.message }, { status: 500 });
  }
}
