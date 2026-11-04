export const PHONE_OTP_CONSTANTS = {
  ENDPOINTS: {
    SEND_OTP: '/v1/auth/otp/send',
    VERIFY_OTP: '/v1/auth/otp/verify',
  },
  MUTATION_KEYS: {
    SEND: ['auth', 'phone-otp', 'send'] as const,
    VERIFY: ['auth', 'phone-otp', 'verify'] as const,
  },
  RESEND_COOLDOWN_SECONDS: 60,
  OTP_LENGTH: 6,
  PHONE_REGEX: /^\+[1-9]\d{7,14}$/,
} as const;
