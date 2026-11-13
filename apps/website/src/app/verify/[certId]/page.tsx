import React from 'react';
import type { Metadata } from 'next';
import fs from 'fs';
import path from 'path';
import Link from 'next/link';
import CandidateProfileClient, { type RegistryRecord } from './CandidateProfileClient';
import { getProjectRepoInfo, MENTOR_PROFILE, getIssueYearMonth } from '@/lib/verification';

function getCertificate(certId: string): RegistryRecord | null {
  try {
    const regPath = path.join(process.cwd(), 'src', 'data', 'certificates_registry.json');
    if (fs.existsSync(regPath)) {
      const registry: Record<string, RegistryRecord> = JSON.parse(fs.readFileSync(regPath, 'utf8'));
      const matchKey = Object.keys(registry).find(
        (k) => k.toLowerCase() === certId.toLowerCase()
      );
      if (matchKey) return registry[matchKey];
    }
    const provPath = path.join(process.cwd(), 'src', 'data', 'all_409_provisional_registry.json');
    if (fs.existsSync(provPath)) {
      const provList: RegistryRecord[] = JSON.parse(fs.readFileSync(provPath, 'utf8'));
      const pMatch = provList.find((p) => p.certId.toLowerCase() === certId.toLowerCase());
      if (pMatch) return pMatch;
    }
    const sheet1593Path = path.join(process.cwd(), 'src', 'data', 'sheet_1593_provisional_registry.json');
    if (fs.existsSync(sheet1593Path)) {
      const sheetList: RegistryRecord[] = JSON.parse(fs.readFileSync(sheet1593Path, 'utf8'));
      const sMatch = sheetList.find((p) => p.certId.toLowerCase() === certId.toLowerCase());
      if (sMatch) return sMatch;
    }
  } catch (err) {
    console.error('Error in getCertificate:', err);
  }
  return null;
}

export async function generateMetadata({
  params
}: {
  params: Promise<{ certId: string }>;
}): Promise<Metadata> {
  const { certId } = await params;
  const cert = getCertificate(certId);

  if (!cert) {
    return {
      title: 'Certificate Verification | DBERT',
      description: 'Verify official DBERT engineering and academic credentials.'
    };
  }

  const isVerified = !cert.isProvisional;
  const title = isVerified
    ? `Pre-Vetted ${cert.domain} Engineer: ${cert.holderName} | DBERT Proof Dossier`
    : `Credential Verification: ${cert.holderName} — ${cert.domain} | DBERT`;

  const desc = isVerified
    ? `Review verified evaluation rubrics, Turnitin originality, and production pull requests for ${cert.holderName} in ${cert.domain}. Score: ${cert.score || 84}/100. Ready for hire.`
    : `Official verified 2-month internship credential for ${cert.holderName} in ${cert.domain}. Project: ${cert.project}. Authenticity verified by DBERT.`;

  const previewImg = cert.previewUrl ? `https://dbert.in${cert.previewUrl}` : 'https://dbert.in/targets12.png';

  return {
    title,
    description: desc,
    alternates: {
      canonical: `https://dbert.in/verify/${cert.certId}`
    },
    openGraph: {
      title: `${cert.holderName} — Pre-Vetted ${cert.domain} Engineer | DBERT`,
      description: desc,
      url: `https://dbert.in/verify/${cert.certId}`,
      siteName: 'DBERT Pre-Vetted Talent Roster',
      images: [
        {
          url: previewImg,
          width: 1200,
          height: 630,
          alt: `DBERT Verified Dossier for ${cert.holderName}`
        }
      ],
      type: 'profile'
    },
    twitter: {
      card: 'summary_large_image',
      title,
      description: desc,
      images: [previewImg]
    }
  };
}

export default async function VerifiedCertificatePage({
  params
}: {
  params: Promise<{ certId: string }>;
}) {
  const { certId } = await params;
  const cert = getCertificate(certId);

  if (!cert) {
    return (
      <div className="container pad-block">
        <div className="card text-center p-8 max-w-lg mx-auto">
          <h1 className="text-xl font-bold mb-2 text-err">Certificate Not Found</h1>
          <p className="text-muted mb-4">No credential found matching ID: {certId}</p>
          <Link href="/verify" className="btn btn-primary btn-sm">
            Search Another Certificate
          </Link>
        </div>
      </div>
    );
  }

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'EducationalOccupationalCredential',
    name: `DBERT Certificate of Completion — ${cert.domain}`,
    credentialCategory: 'Pre-Vetted Technical Internship',
    educationalLevel: 'Production Internship & Technical Incubation',
    recognizedBy: {
      '@type': 'Organization',
      name: 'DBERT Labs Industrial Training & Venture Studio',
      url: 'https://dbert.in'
    },
    about: {
      '@type': 'Person',
      name: cert.holderName,
      jobTitle: `${cert.domain} Engineer`,
      award: `${cert.score || 84}/100 Evaluation Grade ${cert.grade || 'A'}`
    },
    description: `Successfully completed a rigorous 2-month technical incubation program in ${cert.domain} on project ${cert.project}.`
  };

  const { year: issueYear, month: issueMonth } = getIssueYearMonth(cert.issueDate);
  const linkedInUrl = `https://www.linkedin.com/profile/add?startTask=CERTIFICATION_NAME&name=${encodeURIComponent('DBERT Verified Engineer — ' + cert.domain)}&organizationName=DBERT&issueYear=${issueYear}&issueMonth=${issueMonth}&certUrl=${encodeURIComponent(`https://dbert.in/verify/${cert.certId}`)}&certId=${encodeURIComponent(cert.certId)}`;
  const whatsAppUrl = `https://api.whatsapp.com/send?text=${encodeURIComponent(`Review verified technical evaluation and production code dossier for ${cert.holderName} (${cert.domain}): https://dbert.in/verify/${cert.certId}`)}`;
  const repoInfo = getProjectRepoInfo(cert.project);
  const mentorUrl = MENTOR_PROFILE.githubUrl;

  return (
    <div className="container pad-block">
      {/* Schema.org Structured Data */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />

      <CandidateProfileClient
        cert={cert}
        repoInfo={repoInfo}
        mentorUrl={mentorUrl}
        linkedInUrl={linkedInUrl}
        whatsAppUrl={whatsAppUrl}
      />
    </div>
  );
}
