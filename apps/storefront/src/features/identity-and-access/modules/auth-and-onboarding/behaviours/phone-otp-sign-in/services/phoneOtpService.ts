import { PHONE_OTP_CONSTANTS } from '../constants/constants';
import type { SendOtpPayload, SendOtpResult, VerifyOtpPayload, VerifyOtpResult } from '../types/types';

export const phoneOtpService = {
  async sendOtp(payload: SendOtpPayload): Promise<SendOtpResult> {
    const res = await fetch(PHONE_OTP_CONSTANTS.ENDPOINTS.SEND_OTP, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Tenant-Id': payload.tenant_id,
      },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      throw new Error(`Failed to send OTP: ${res.statusText}`);
    }

    return res.json();
  },

  async verifyOtp(payload: VerifyOtpPayload): Promise<VerifyOtpResult> {
    const res = await fetch(PHONE_OTP_CONSTANTS.ENDPOINTS.VERIFY_OTP, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Tenant-Id': payload.tenant_id,
      },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      throw new Error(`Failed to verify OTP: ${res.statusText}`);
    }

    return res.json();
  },
};
