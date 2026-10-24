import { NextResponse } from 'next/server';
import db from '@/lib/db';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const {
      name,
      email,
      organization,
      organizationType,
      researchArea,
      proposal
    } = body;

    if (!name || !email || !organization || !proposal) {
      return NextResponse.json({ error: 'Missing required parameters' }, { status: 400 });
    }

    const collaboration = await db.collaborationRequest.create({
      data: {
        name,
        email,
        organization,
        organizationType,
        researchArea,
        proposal
      }
    });

    return NextResponse.json({ success: true, id: collaboration.id }, { status: 201 });
  } catch (err) {
    console.error('Collaboration request error:', err);
    return NextResponse.json({ error: 'Failed to submit proposal' }, { status: 500 });
  }
}
