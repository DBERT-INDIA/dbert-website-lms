import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  const url = new URL('/admin/login', request.url);
  const response = NextResponse.redirect(url, 302);
  response.cookies.delete('admin_token');
  return response;
}
