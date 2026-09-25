import { defineConfig, globalIgnores } from 'eslint/config'
import nextVitals from 'eslint-config-next/core-web-vitals'

// Next.js 16 removed `next lint` and no longer lints during `next build`,
// so ESLint runs on its own via `npm run lint`.
const eslintConfig = defineConfig([
  ...nextVitals,
  globalIgnores([
    '.next/**',
    'out/**',
    'build/**',
    'next-env.d.ts',
    'src/generated/**', // Prisma client output — regenerated, never hand-edited
  ]),
])

export default eslintConfig
