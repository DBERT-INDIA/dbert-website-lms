import { strict as assert } from 'node:assert';
import { test } from 'node:test';
import { submitEnrollmentPaymentClaim } from '../src/lib/enrollment-payment-claim.ts';

const input = {
  fullName: 'Sample Student',
  email: 'learner@example.test',
  phone: '1111111111',
  domain: 'Data Analyst',
  utrNumber: 'demo00000001',
};

test('uses the LMS receipt and never labels a pending claim as verified', async (t) => {
  const previousEndpoint = process.env.INTERNAL_LMS_SYNC_URL;
  const previousSecret = process.env.INTERNAL_SYNC_SECRET;
  process.env.INTERNAL_LMS_SYNC_URL = 'https://offline.test/claim';
  process.env.INTERNAL_SYNC_SECRET = 'test-placeholder';
  t.after(() => {
    if (previousEndpoint === undefined) delete process.env.INTERNAL_LMS_SYNC_URL;
    else process.env.INTERNAL_LMS_SYNC_URL = previousEndpoint;
    if (previousSecret === undefined) delete process.env.INTERNAL_SYNC_SECRET;
    else process.env.INTERNAL_SYNC_SECRET = previousSecret;
  });

  const fetchFixture = t.mock.method(globalThis, 'fetch', async (url, opts) => {
    assert.equal(url, 'https://offline.test/claim');
    assert.equal(opts.method, 'POST');
    assert.equal(opts.redirect, 'error');
    const claim = JSON.parse(opts.body);
    assert.equal(claim.utr, 'DEMO00000001');
    assert.equal(claim.amount, 1500);
    assert.equal(claim.payment_type, 'balance');
    return Response.json({
      status: 'success',
      submission_id: 'canonical-receipt',
      submitted_at: '2026-01-01 01:02:03',
      claim_status: 'pending',
      amount: 1500,
      duplicate: true,
    });
  });
  const receipt = await submitEnrollmentPaymentClaim(input, 'balance', 1500);
  assert.equal(receipt.submissionId, 'canonical-receipt');
  assert.equal(receipt.claimStatus, 'pending');
  assert.equal(receipt.alreadySubmitted, true);

  fetchFixture.mock.mockImplementation(async () => Response.json({ status: 'error' }, { status: 503 }));
  await assert.rejects(
    submitEnrollmentPaymentClaim(input, 'balance', 1500),
    { status: 503, message: /Retry with the same transaction reference/ },
  );
  assert.equal(fetchFixture.mock.callCount(), 2);
  await assert.rejects(submitEnrollmentPaymentClaim([], 'balance', 1500), { status: 400 });
  assert.equal(fetchFixture.mock.callCount(), 2);
});
