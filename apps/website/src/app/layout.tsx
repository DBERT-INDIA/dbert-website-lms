import type { Metadata, Viewport } from 'next'
import { Bricolage_Grotesque, Inter, JetBrains_Mono, Caveat } from 'next/font/google'
import './globals.css'
import Script from 'next/script'
import MegaMenu from '@/components/layout/MegaMenu'
import Footer from '@/components/layout/Footer'
import WhatsAppFloat from '@/components/layout/WhatsAppFloat'
import ThemeSetter from '@/components/layout/ThemeSetter'
import RevealObserver from '@/components/ui/RevealObserver'
import Breadcrumbs from '@/components/seo/Breadcrumbs'
import ScrollProgress from '@/components/ui/ScrollProgress'
import BackToTop from '@/components/ui/BackToTop'

/* Design system v2 typefaces. All four are variable fonts, so no `weight` is
   specified — the full axis ships in one file. Self-hosted and preloaded by
   next/font, which removes the render-blocking Google Fonts @import that
   globals.css used to carry. */
const bricolage = Bricolage_Grotesque({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-bricolage-src',
})

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter-src',
})

/* Mono and Caveat set micro-copy and margin annotations, never the LCP element.
   Preloading all four families put ~244KB on the critical path and pushed mobile
   LCP to 6.9s; these two now load lazily instead. */
const jetbrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  style: ['normal', 'italic'], // italic sets the `born from:` provenance lines
  display: 'swap',
  preload: false,
  variable: '--font-jetbrains-src',
})

const caveat = Caveat({
  subsets: ['latin'],
  display: 'swap',
  preload: false,
  variable: '--font-caveat-src',
})

const fontVariables = `${bricolage.variable} ${inter.variable} ${jetbrainsMono.variable} ${caveat.variable}`

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
}

export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000'),
  title: {
    default: 'DBERT — AI Incubation Platform for Startups & Learners',
    template: '%s | DBERT'
  },
  description: "India's AI-powered incubation platform. Startup support, paid internships, AI consultation, and custom LLM training.",
  icons: {
    icon: '/favicon.svg',
    shortcut: '/favicon.svg',
    apple: '/favicon.svg',
  },
  openGraph: {
    type: 'website',
    locale: 'en_IN',
    siteName: 'DBERT',
    images: [
      {
        url: '/og-image.jpg',
        width: 1200,
        height: 630,
        alt: 'DBERT - AI Venture Studio & Educational Hub'
      }
    ]
  },
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={fontVariables}>
      <head>
        {/* GA4 — insert ONCE here, NOT on individual pages.
            lazyOnload rather than afterInteractive: the gtag bundle is ~163KB,
            the single largest transfer on the page, and loading it during
            hydration cost ~290ms of blocking time on mobile. */}
        {process.env.NEXT_PUBLIC_GA_ID && (
          <>
            <link rel="preconnect" href="https://www.googletagmanager.com" />
            <Script
              src={`https://www.googletagmanager.com/gtag/js?id=${process.env.NEXT_PUBLIC_GA_ID}`}
              strategy="lazyOnload"
            />
            <Script id="ga4-init" strategy="lazyOnload">
              {`
                window.dataLayer = window.dataLayer || [];
                function gtag(){dataLayer.push(arguments);}
                gtag('js', new Date());
                gtag('config', '${process.env.NEXT_PUBLIC_GA_ID}');
              `}
            </Script>
          </>
        )}
        <Script id="org-schema" type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify({
          "@context": "https://schema.org",
          "@type": "Organization",
          "name": "Digital Blinc Education Research And Technology",
          "alternateName": "DBERT",
          "url": process.env.NEXT_PUBLIC_SITE_URL || 'https://dbert.online',
          "logo": `${process.env.NEXT_PUBLIC_SITE_URL || 'https://dbert.online'}/logo.png`,
          // TODO-CONFIRM: founder's full legal name for the `founder` property.
          "founder": {
            "@type": "Person",
            "name": "Abhinav"
          },
          "sameAs": [
            "https://www.linkedin.com/company/dbert",
            "https://www.youtube.com/@dbert-india",
            "https://github.com/DBERT-INDIA"
          ],
          "address": {
            "@type": "PostalAddress",
            "addressLocality": "Delhi",
            "addressCountry": "IN"
          },
          "contactPoint": {
            "@type": "ContactPoint",
            "telephone": "+918958006294",
            "contactType": "customer service",
            "email": "contactus@dbert.online",
            "availableLanguage": ["English", "Hindi"]
          }
        }) }} />
      </head>
      <body>
        <ThemeSetter />
        <RevealObserver />
        <ScrollProgress />
        <Breadcrumbs />
        <div className="app-shell">
          <MegaMenu />
          
          <main id="main-content" className="app-main">
            {children}
          </main>

          <Footer />
          <WhatsAppFloat />
          <BackToTop />
        </div>
      </body>
    </html>
  )
}
