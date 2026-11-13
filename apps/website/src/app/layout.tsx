import type { Metadata, Viewport } from 'next'
import { Bricolage_Grotesque, Inter, JetBrains_Mono, Space_Grotesk } from 'next/font/google'
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
import { GA_MEASUREMENT_ID } from '@/lib/analytics'

/* Design system v2 typefaces with Option A Space Grotesk editorial precision. */
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

const spaceGrotesk = Space_Grotesk({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-space-src',
})

const jetbrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  style: ['normal', 'italic'],
  display: 'swap',
  preload: false,
  variable: '--font-jetbrains-src',
})

const fontVariables = `${bricolage.variable} ${inter.variable} ${jetbrainsMono.variable} ${spaceGrotesk.variable}`

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
}

export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL || 'https://dbert.in'),
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
        {/* GA4 Telemetry (G-MN7ME9X518) — loads seamlessly across static export */}
        <link rel="preconnect" href="https://www.googletagmanager.com" />
        <Script
          src={`https://www.googletagmanager.com/gtag/js?id=${GA_MEASUREMENT_ID}`}
          strategy="lazyOnload"
        />
        <Script id="ga4-init" strategy="lazyOnload">
          {`
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', '${GA_MEASUREMENT_ID}', {
              page_path: window.location.pathname,
              send_page_view: true
            });
          `}
        </Script>
        {/* Universal Cross-Domain Referral Attribution Script */}
        <Script id="dbert-referral-capture" strategy="afterInteractive">
          {`
            (function() {
              try {
                var m = window.location.search.match(/[?&]ref=([A-Za-z0-9_-]{3,40})/);
                if (m) {
                  var code = m[1];
                  var d = new Date(); d.setTime(d.getTime() + 30 * 864e5);
                  var isDbert = window.location.hostname.indexOf('dbert.in') !== -1;
                  var domain = isDbert ? ';domain=.dbert.in' : '';
                  document.cookie = 'dbert_ref=' + encodeURIComponent(code) + ';expires=' + d.toUTCString() + ';path=/' + domain + ';SameSite=Lax';
                  if (window.localStorage) {
                    localStorage.setItem('dbert_ref', code);
                    localStorage.setItem('dbert_ref_exp', d.getTime().toString());
                  }
                }
              } catch (e) {}
            })();
          `}
        </Script>
        <Script id="org-schema" type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify({
          "@context": "https://schema.org",
          "@type": "Organization",
          "name": "Digital Blinc Education Research And Technology",
          "alternateName": "DBERT",
          "url": process.env.NEXT_PUBLIC_SITE_URL || 'https://dbert.in',
          "logo": `${process.env.NEXT_PUBLIC_SITE_URL || 'https://dbert.in'}/logo.svg`,
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
            "email": "contactus@dbert.in",
            "availableLanguage": ["English", "Hindi"]
          }
        }) }} />
      </head>
      <body>
        <a href="#main-content" className="skip-link">
          Skip to main content
        </a>
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
