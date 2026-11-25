export function lmsInternshipSignupUrl(domain: string, city?: string) {
  const destination = ['/internships', encodeURIComponent(domain)];
  if (city) destination.push(encodeURIComponent(city));

  const url = new URL('https://lms.dbert.in/');
  url.searchParams.set('domain', domain);
  url.searchParams.set('next', destination.join('/'));
  url.hash = 'signup';
  return url.href;
}
