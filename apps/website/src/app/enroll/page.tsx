import { redirect } from 'next/navigation';

export default async function EnrollRedirectPage({
  searchParams
}: {
  searchParams?: Promise<Record<string, string | string[] | undefined>> | Record<string, string | string[] | undefined>;
}) {
  const sp = searchParams ? await searchParams : {};
  const query = new URLSearchParams();
  for (const [key, val] of Object.entries(sp)) {
    if (typeof val === 'string') {
      query.set(key, val);
    }
  }
  const qs = query.toString();
  redirect(`/enroll/1999${qs ? `?${qs}` : ''}`);
}
