import { NextResponse } from 'next/server';
import db from '@/lib/db';

export const VALID_DOMAINS = [
  'AI Agent Development',
  'Full Stack Development',
  'Python Automation',
  'Data Analytics',
  'Data Engineering / Machine Learning',
] as const;

function isPlausibleUrl(value: string): boolean {
  try {
    const parsed = new URL(value.trim());
    return parsed.protocol === 'http:' || parsed.protocol === 'https:';
  } catch {
    return false;
  }
}

function isValidEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim());
}

function isValidPhone(phone: string): boolean {
  // 10 digits mobile number format
  return /^[0-9]{10}$/.test(phone.replace(/[\s+-]/g, '').slice(-10));
}

export async function POST(request: Request) {
  try {
    const body = await request.json();

    const {
      fullName,
      email,
      phone,
      city,
      state,
      college,
      degree,
      graduationYear,
      cgpaOrPercentage,
      domain,
      cvUrl,
      linkedinUrl,
      githubUrl,
      portfolioUrl,
      familyBackground,
      motivation,
      availability,
      termsConsent,
      newsletterConsent,
      cohortSlug = 'aivara',
    } = body;

    // 1. Mandatory Step 1 fields
    if (!fullName || typeof fullName !== 'string' || fullName.trim().length < 2) {
      return NextResponse.json({ error: 'Please enter a valid full name.' }, { status: 400 });
    }

    if (!email || typeof email !== 'string' || !isValidEmail(email)) {
      return NextResponse.json({ error: 'Please enter a valid email address.' }, { status: 400 });
    }

    if (!phone || typeof phone !== 'string' || !isValidPhone(phone)) {
      return NextResponse.json({ error: 'Please enter a valid 10-digit phone/WhatsApp number.' }, { status: 400 });
    }

    if (!city || typeof city !== 'string' || city.trim().length === 0) {
      return NextResponse.json({ error: 'City is required.' }, { status: 400 });
    }

    if (!state || typeof state !== 'string' || state.trim().length === 0) {
      return NextResponse.json({ error: 'State is required.' }, { status: 400 });
    }

    if (!college || typeof college !== 'string' || college.trim().length === 0) {
      return NextResponse.json({ error: 'College / University name is required.' }, { status: 400 });
    }

    if (!degree || typeof degree !== 'string' || degree.trim().length === 0) {
      return NextResponse.json({ error: 'Degree and branch are required.' }, { status: 400 });
    }

    if (!graduationYear || typeof graduationYear !== 'string' || graduationYear.trim().length === 0) {
      return NextResponse.json({ error: 'Graduation year is required.' }, { status: 400 });
    }

    // 2. Mandatory Step 2 fields
    if (!domain || !VALID_DOMAINS.includes(domain as any)) {
      return NextResponse.json({ error: 'Please select a valid internship domain from the 5 options.' }, { status: 400 });
    }

    if (!cvUrl || typeof cvUrl !== 'string' || !isPlausibleUrl(cvUrl)) {
      return NextResponse.json({
        error: 'A valid CV / Resume link (Google Drive, Dropbox, OneDrive, or hosted PDF) is required.',
      }, { status: 400 });
    }

    // Optional URLs validation (if provided)
    if (linkedinUrl && typeof linkedinUrl === 'string' && linkedinUrl.trim() !== '') {
      if (!isPlausibleUrl(linkedinUrl)) {
        return NextResponse.json({ error: 'LinkedIn URL is invalid. Please enter a valid URL or leave it blank.' }, { status: 400 });
      }
    }

    if (githubUrl && typeof githubUrl === 'string' && githubUrl.trim() !== '') {
      if (!isPlausibleUrl(githubUrl)) {
        return NextResponse.json({ error: 'GitHub URL is invalid. Please enter a valid URL or leave it blank.' }, { status: 400 });
      }
    }

    if (portfolioUrl && typeof portfolioUrl === 'string' && portfolioUrl.trim() !== '') {
      if (!isPlausibleUrl(portfolioUrl)) {
        return NextResponse.json({ error: 'Portfolio URL is invalid.' }, { status: 400 });
      }
    }

    // 3. Mandatory Step 3 fields
    if (!familyBackground || typeof familyBackground !== 'string' || familyBackground.trim().length < 5) {
      return NextResponse.json({
        error: 'Please provide brief details on your family background (parents\' occupation / household context).',
      }, { status: 400 });
    }

    if (!termsConsent) {
      return NextResponse.json({
        error: 'You must agree to the Terms and Conditions to complete your application.',
      }, { status: 400 });
    }

    // 4. Save to Database
    const cleanPhone = phone.replace(/[\s+-]/g, '').slice(-10);

    const application = await db.cohortApplication.create({
      data: {
        cohortSlug,
        fullName: fullName.trim(),
        email: email.trim().toLowerCase(),
        phone: cleanPhone,
        city: city.trim(),
        state: state.trim(),
        college: college.trim(),
        degree: degree.trim(),
        graduationYear: graduationYear.trim(),
        cgpaOrPercentage: cgpaOrPercentage ? String(cgpaOrPercentage).trim() : null,
        domain,
        cvUrl: cvUrl.trim(),
        linkedinUrl: linkedinUrl && linkedinUrl.trim() ? linkedinUrl.trim() : null,
        githubUrl: githubUrl && githubUrl.trim() ? githubUrl.trim() : null,
        portfolioUrl: portfolioUrl && portfolioUrl.trim() ? portfolioUrl.trim() : null,
        familyBackground: familyBackground.trim(),
        motivation: motivation && motivation.trim() ? motivation.trim() : null,
        availability: availability && availability.trim() ? availability.trim() : null,
        termsConsent: Boolean(termsConsent),
        newsletterConsent: Boolean(newsletterConsent),
        status: 'pending',
      },
    });

    return NextResponse.json({
      success: true,
      id: application.id,
      message: 'Application submitted successfully.',
    }, { status: 201 });
  } catch (err) {
    console.error('Cohort application submission error:', err);
    return NextResponse.json({ error: 'Failed to process application. Please try again.' }, { status: 500 });
  }
}
