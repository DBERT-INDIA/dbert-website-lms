import { NextResponse } from 'next/server';

const LMS_BASE_URL = process.env.NODE_ENV === 'production' && process.env.LMS_INTERNAL_URL
  ? process.env.LMS_INTERNAL_URL
  : 'https://lms.dbert.in';

export async function POST(request: Request) {
  try {
    const contentType = request.headers.get('content-type') || '';
    const targetUrl = `${LMS_BASE_URL}/api/tools/ats-checker`;

    let res: Response;

    if (contentType.includes('multipart/form-data')) {
      const formData = await request.formData();
      res = await fetch(targetUrl, {
        method: 'POST',
        body: formData,
      });
    } else {
      const json = await request.json();
      res = await fetch(targetUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(json),
      });
    }

    const data = await res.json();
    return NextResponse.json(data, { status: res.status });
  } catch (error: any) {
    console.error('Error forwarding to ATS scanner service:', error);
    return NextResponse.json(
      { status: 'error', message: 'Unable to reach the AI ATS screening service. Please try again shortly.' },
      { status: 502 }
    );
  }
}
