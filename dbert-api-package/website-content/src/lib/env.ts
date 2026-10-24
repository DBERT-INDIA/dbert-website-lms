/**
 * Single place where required server-side environment variables are read.
 *
 * Several call sites previously fell back to a hardcoded development secret
 * when JWT_SECRET was unset, which meant a deploy missing that variable would
 * sign and verify admin sessions with a string committed to this repo. Reading
 * through these accessors turns a missing variable into a loud failure instead
 * of a silent downgrade.
 *
 * The accessors are lazy on purpose: `next build` compiles pages that never
 * touch the database or admin auth, and should not require production secrets
 * to be present just to produce those pages.
 */

function requireEnv(name: string): string {
  const value = process.env[name];
  if (!value) {
    throw new Error(
      `Missing required environment variable: ${name}. Set it in .env — see .env.example for the full list.`
    );
  }
  return value;
}

/** Secret used to sign and verify the admin session cookie. */
export function getJwtSecret(): string {
  return requireEnv('JWT_SECRET');
}

/** Postgres connection string consumed by the Prisma driver adapter. */
export function getDatabaseUrl(): string {
  return requireEnv('DATABASE_URL');
}
