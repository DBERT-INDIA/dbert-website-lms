import { strict as assert } from 'node:assert';
import { test } from 'node:test';
import {
  matchesPaymentSignature,
  signWebsitePayment,
  validateWebsiteCapture,
  websiteProgramAmount,
  websiteReceiptPayload,
} from '../src/lib/website-payment-contract.ts';

const expected = {
  id: 'inquiry-test', email: 'buyer@example.test', amount: 150000,
  status: 'payment_pending', razorpayOrderId: 'order_test', razorpayPaymentId: null,
};
const capture = {
  id: 'pay_test', order_id: 'order_test', amount: 150000,
  currency: 'INR', status: 'captured',
};

test('amounts are selected by exact recognized program names', () => {
  assert.equal(websiteProgramAmount('Incubation Balance 1500'), 150000);
  assert.equal(websiteProgramAmount('Course'), 0);
  assert.equal(websiteProgramAmount(''), 0);
  assert.equal(websiteProgramAmount('__proto__'), 0);
});

test('checkout proof is scoped to the order and original buyer', () => {
  const secret = 'offline-test';
  const payload = websiteReceiptPayload(expected);
  const proof = signWebsitePayment(payload, secret);
  assert.equal(matchesPaymentSignature(payload, proof, secret), true);
  assert.equal(matchesPaymentSignature(payload, 'short', secret), false);
  assert.equal(matchesPaymentSignature(websiteReceiptPayload({ ...expected, email: 'other@example.test' }), proof, secret), false);
  assert.equal(matchesPaymentSignature(websiteReceiptPayload({ ...expected, id: 'inquiry-other' }), proof, secret), false);
});

test('the gateway capture must match the persisted order, amount, currency, and status', () => {
  assert.doesNotThrow(() => validateWebsiteCapture(expected, capture.id, capture));
  for (const override of [
    { order_id: 'order_other' }, { amount: 49900 }, { currency: 'USD' }, { status: 'authorized' },
  ]) {
    assert.throws(() => validateWebsiteCapture(expected, capture.id, { ...capture, ...override }), { status: 409 });
  }
});
