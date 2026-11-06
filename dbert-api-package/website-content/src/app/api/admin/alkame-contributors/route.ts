import { NextResponse } from 'next/server';
import { cookies } from 'next/headers';
import jwt from 'jsonwebtoken';
import db from '@/lib/db';
import { getJwtSecret } from '@/lib/env';

async function requireAdmin(): Promise<boolean> {
  const cookieStore = await cookies();
  const token = cookieStore.get('admin_token')?.value;

  if (!token) return false;

  try {
    jwt.verify(token, getJwtSecret());
    return true;
  } catch {
    return false;
  }
}

export async function PATCH(request: Request) {
  const isAdmin = await requireAdmin();
  if (!isAdmin) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  try {
    const { id, status } = await request.json();

    if (!id || !status) {
      return NextResponse.json({ error: 'Missing id or status' }, { status: 400 });
    }

    if (status !== 'approved' && status !== 'rejected') {
      return NextResponse.json({ error: 'Status must be "approved" or "rejected"' }, { status: 400 });
    }

    const updated = await db.projectContributor.update({
      where: { id },
      data: {
        status,
        reviewedAt: new Date(),
      },
    });

    return NextResponse.json({ success: true, id: updated.id, status: updated.status }, { status: 200 });
  } catch (err) {
    console.error('Alkame contributor moderation error:', err);
    return NextResponse.json({ error: 'Failed to update contributor status' }, { status: 500 });
  }
}
