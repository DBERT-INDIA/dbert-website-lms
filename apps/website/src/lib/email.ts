/**
 * Pluggable email dispatch utility for Cohort Applications.
 *
 * Supports calling an external email API / webhook when EMAIL_API_ENDPOINT is set.
 * Falls back to structured placeholder logging in development/staging so that
 * decisions can be executed and tested without requiring an active email provider.
 */

export type CohortDecisionType = 'approved' | 'approved_certified' | 'rejected';

export interface SendCohortEmailParams {
  to: string;
  applicantName: string;
  decision: CohortDecisionType;
  domain: string;
  adminNotes?: string;
  cohortName?: string;
}

export interface EmailDispatchResult {
  success: boolean;
  log: string;
  dispatchedAt: Date;
  provider: 'external_api' | 'placeholder';
}

interface EmailTemplate {
  subject: string;
  headline: string;
  bodyHtml: string;
  bodyText: string;
}

/**
 * Generates branded email content for each of the 3 cohort decisions.
 */
export function getCohortEmailTemplate(params: SendCohortEmailParams): EmailTemplate {
  const cohortName = params.cohortName || 'Aivara Technologies Hiring Cohort';
  const name = params.applicantName;
  const domain = params.domain;
  const notes = params.adminNotes ? `<p style="margin-top: 16px; padding: 12px; background: #f4f4f5; border-left: 4px solid #18181b; font-style: italic;"><strong>Reviewer Note:</strong> "${params.adminNotes}"</p>` : '';
  const notesText = params.adminNotes ? `\nReviewer Note: "${params.adminNotes}"\n` : '';

  switch (params.decision) {
    case 'approved':
      return {
        subject: `Selection Offer: ${cohortName} — ${domain}`,
        headline: `Welcome to the ${cohortName}`,
        bodyHtml: `
          <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; padding: 24px; color: #18181b; line-height: 1.6;">
            <div style="border-bottom: 2px solid #18181b; padding-bottom: 12px; margin-bottom: 24px;">
              <span style="font-size: 12px; letter-spacing: 0.1em; text-transform: uppercase; color: #71717a;">Aivara Technologies × DBERT Labs</span>
              <h1 style="font-size: 22px; margin: 6px 0 0; color: #18181b;">Application Approved</h1>
            </div>
            <p>Dear <strong>${name}</strong>,</p>
            <p>We are delighted to inform you that your application for the <strong>${cohortName}</strong> in the <strong>${domain}</strong> track has been <strong>Approved</strong>.</p>
            <p>Our technical review team evaluated your academics, project history, and profile. You have been selected to join our active engineering squads starting with the upcoming cohort cycle.</p>
            ${notes}
            <div style="background: #f4f4f5; border: 1px solid #e4e4e7; border-radius: 6px; padding: 16px; margin: 24px 0;">
              <h3 style="margin-top: 0; font-size: 15px;">Next Steps:</h3>
              <ul style="padding-left: 20px; margin-bottom: 0;">
                <li>Join the Cohort communication channels (invitation sent separately).</li>
                <li>Complete your squad technical onboarding questionnaire within 48 hours.</li>
                <li>Attend the technical orientation and repository setup session.</li>
              </ul>
            </div>
            <p>Congratulations on your selection. We look forward to building high-impact systems together.</p>
            <p style="margin-top: 32px; font-size: 13px; color: #71717a;">Warm regards,<br/><strong>Aivara Technologies Recruitment & Mentorship Team</strong><br/>Digital Blinc Education Research & Technology (DBERT)</p>
          </div>
        `,
        bodyText: `Dear ${name},\n\nWe are delighted to inform you that your application for the ${cohortName} in the ${domain} track has been Approved.\n\nOur technical team evaluated your profile and selected you for the upcoming squad sprint.${notesText}\n\nNext Steps:\n1. Join the cohort communication channels.\n2. Complete your technical onboarding questionnaire within 48 hours.\n3. Attend the technical orientation session.\n\nWarm regards,\nAivara Technologies & DBERT Team`
      };

    case 'approved_certified':
      return {
        subject: `Admission Offer: ${cohortName} (Certification Track) — ${domain}`,
        headline: `Selected for the Certified Cohort Track`,
        bodyHtml: `
          <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; padding: 24px; color: #18181b; line-height: 1.6;">
            <div style="border-bottom: 2px solid #7c3aed; padding-bottom: 12px; margin-bottom: 24px;">
              <span style="font-size: 12px; letter-spacing: 0.1em; text-transform: uppercase; color: #7c3aed; font-weight: 600;">Aivara Technologies × DBERT Labs</span>
              <h1 style="font-size: 22px; margin: 6px 0 0; color: #18181b;">Approved with Certification Track</h1>
            </div>
            <p>Dear <strong>${name}</strong>,</p>
            <p>Congratulations! Following our evaluation of your submission, you have been <strong>Approved for Admission with Certification</strong> in the <strong>${cohortName}</strong> (${domain} track).</p>
            <p>This dual track pairs active cohort sprint participation with structured milestone evaluation and an accredited DBERT experience credential independently verifiable at <code>dbert.online/verify</code>.</p>
            ${notes}
            <div style="background: #faf5ff; border: 1px solid #e9d5ff; border-radius: 6px; padding: 16px; margin: 24px 0;">
              <h3 style="margin-top: 0; font-size: 15px; color: #6b21a8;">Track Highlights:</h3>
              <ul style="padding-left: 20px; margin-bottom: 0; color: #374151;">
                <li>Verified Certificate of Internship & Engineering Experience Letter.</li>
                <li>Direct mentorship from senior production engineers on client repos.</li>
                <li>Code review logs recorded for partner hiring network recommendations.</li>
              </ul>
            </div>
            <p>Our program coordinators will reach out shortly with cohort onboarding credentials and timeline schedules.</p>
            <p style="margin-top: 32px; font-size: 13px; color: #71717a;">Warm regards,<br/><strong>Aivara Technologies Cohort Operations</strong><br/>DBERT Labs</p>
          </div>
        `,
        bodyText: `Dear ${name},\n\nCongratulations! You have been Approved for Admission with Certification in the ${cohortName} (${domain} track).\n\nThis track includes hands-on sprints alongside verified engineering certification checkable on dbert.online/verify.${notesText}\n\nOur coordinators will reach out shortly with onboarding details.\n\nWarm regards,\nAivara Technologies Cohort Operations`
      };

    case 'rejected':
      return {
        subject: `Application Update: ${cohortName}`,
        headline: `Cohort Application Status`,
        bodyHtml: `
          <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; padding: 24px; color: #18181b; line-height: 1.6;">
            <div style="border-bottom: 2px solid #e4e4e7; padding-bottom: 12px; margin-bottom: 24px;">
              <span style="font-size: 12px; letter-spacing: 0.1em; text-transform: uppercase; color: #71717a;">Aivara Technologies × DBERT Labs</span>
              <h1 style="font-size: 22px; margin: 6px 0 0; color: #18181b;">Application Update</h1>
            </div>
            <p>Dear <strong>${name}</strong>,</p>
            <p>Thank you for taking the time to apply for the <strong>${cohortName}</strong> in the <strong>${domain}</strong> track. We genuinely appreciate your interest and the effort put into your application.</p>
            <p>Due to squad capacity limits and high applicant volume for this cycle, we are unfortunately unable to offer you a cohort seat at this time.</p>
            ${notes}
            <p>Please note that this decision is specific to this cohort cycle and does not reflect on your potential. We strongly encourage you to continue building projects and apply for our next upcoming cohort intake.</p>
            <p style="margin-top: 32px; font-size: 13px; color: #71717a;">Sincerely,<br/><strong>Admissions Committee</strong><br/>Aivara Technologies & DBERT Labs</p>
          </div>
        `,
        bodyText: `Dear ${name},\n\nThank you for applying to the ${cohortName} (${domain} track).\n\nDue to cohort capacity limits, we are unable to offer you a seat for this intake.${notesText}\n\nWe encourage you to continue developing your projects and re-apply for upcoming cycles.\n\nSincerely,\nAdmissions Committee\nAivara Technologies & DBERT Labs`
      };
  }
}

/**
 * Executes email sending via configured external API or placeholder logging.
 */
export async function callCohortEmailApi(params: SendCohortEmailParams): Promise<EmailDispatchResult> {
  const endpoint = process.env.EMAIL_API_ENDPOINT;
  const apiKey = process.env.EMAIL_API_KEY;
  const template = getCohortEmailTemplate(params);
  const now = new Date();

  // If an external email API or webhook is configured in .env
  if (endpoint) {
    try {
      const payload = {
        to: params.to,
        recipientName: params.applicantName,
        subject: template.subject,
        html: template.bodyHtml,
        text: template.bodyText,
        decision: params.decision,
        domain: params.domain,
        adminNotes: params.adminNotes,
        timestamp: now.toISOString(),
      };

      const res = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(apiKey ? { Authorization: `Bearer ${apiKey}` } : {}),
        },
        body: JSON.stringify(payload),
      });

      const responseText = await res.text().catch(() => '');
      if (!res.ok) {
        return {
          success: false,
          log: `[External Email API Error ${res.status}]: ${responseText.slice(0, 300)}`,
          dispatchedAt: now,
          provider: 'external_api',
        };
      }

      return {
        success: true,
        log: `[External Email API Success]: Dispatched to ${params.to} via ${endpoint}. Response: ${responseText.slice(0, 200)}`,
        dispatchedAt: now,
        provider: 'external_api',
      };
    } catch (err) {
      return {
        success: false,
        log: `[External Email API Exception]: ${err instanceof Error ? err.message : String(err)}`,
        dispatchedAt: now,
        provider: 'external_api',
      };
    }
  }

  // Placeholder Mode: logs to server console and formats audit trail
  const logMessage = `[EMAIL API PLACEHOLDER] Decision '${params.decision}' queued for ${params.to} (${params.applicantName}) on track '${params.domain}'. Subject: "${template.subject}". (Plug real provider in .env via EMAIL_API_ENDPOINT)`;
  console.log(logMessage);

  return {
    success: true,
    log: logMessage,
    dispatchedAt: now,
    provider: 'placeholder',
  };
}
