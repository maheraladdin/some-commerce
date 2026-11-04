export interface SendOtpPayload {
  tenant_id: string;
  phone_number: string;
}

export interface SendOtpResult {
  success: boolean;
  session_id: string;
  expires_in_seconds: number;
}

export interface VerifyOtpPayload {
  tenant_id: string;
  session_id: string;
  code: string;
}

export interface VerifyOtpResult {
  success: boolean;
  auth_token?: string;
  message: string;
}

export interface PhoneOtpScreenProps {
  phoneNumber: string;
  otpCode: string;
  step: 'PHONE' | 'OTP';
  isLoading: boolean;
  errorMessage: string | null;
  resendCountdown: number;
  onPhoneNumberChange: (val: string) => void;
  onOtpCodeChange: (val: string) => void;
  onSendOtp: () => void;
  onVerifyOtp: () => void;
  onResendOtp: () => void;
}
