import Razorpay from 'razorpay';

if (!process.env.RAZORPAY_KEY_ID || !process.env.RAZORPAY_KEY_SECRET) {
  console.warn("Razorpay keys are missing from environment variables.");
}

export const razorpay = new Razorpay({
  key_id: process.env.RAZORPAY_KEY_ID || 'dummy_key_id_for_build',
  key_secret: process.env.RAZORPAY_KEY_SECRET || 'dummy_key_secret_for_build',
});
