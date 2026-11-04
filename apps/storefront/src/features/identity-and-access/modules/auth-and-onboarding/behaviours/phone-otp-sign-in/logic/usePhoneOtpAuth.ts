import { useState, useCallback, useEffect } from 'react';
import { PHONE_OTP_CONSTANTS } from '../constants/constants';
import { phoneOtpService } from '../services/phoneOtpService';

export interface UsePhoneOtpAuthProps {
  tenantId: string;
  onSuccess?: (token: string) => void;
}

export function usePhoneOtpAuth({ tenantId, onSuccess }: UsePhoneOtpAuthProps) {
  const [phoneNumber, setPhoneNumber] = useState('');
  const [otpCode, setOtpCode] = useState('');
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [step, setStep] = useState<'PHONE' | 'OTP'>('PHONE');
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [resendCountdown, setResendCountdown] = useState(0);

  useEffect(() => {
    if (resendCountdown <= 0) return;
    const timer = setInterval(() => {
      setResendCountdown((prev) => (prev > 0 ? prev - 1 : 0));
    }, 1000);
    return () => clearInterval(timer);
  }, [resendCountdown]);

  const handlePhoneNumberChange = useCallback((val: string) => {
    setPhoneNumber(val);
    setErrorMessage(null);
  }, []);

  const handleOtpCodeChange = useCallback((val: string) => {
    const clean = val.replace(/\D/g, '').slice(0, PHONE_OTP_CONSTANTS.OTP_LENGTH);
    setOtpCode(clean);
    setErrorMessage(null);
  }, []);

  const handleSendOtp = useCallback(async () => {
    if (!PHONE_OTP_CONSTANTS.PHONE_REGEX.test(phoneNumber.trim())) {
      setErrorMessage('Please enter a valid international phone number (e.g. +966501234567)');
      return;
    }

    setIsLoading(true);
    setErrorMessage(null);

    try {
      const result = await phoneOtpService.sendOtp({
        tenant_id: tenantId,
        phone_number: phoneNumber.trim(),
      });
      setSessionId(result.session_id);
      setStep('OTP');
      setResendCountdown(PHONE_OTP_CONSTANTS.RESEND_COOLDOWN_SECONDS);
    } catch (err: unknown) {
      setErrorMessage(err instanceof Error ? err.message : 'Failed to send OTP code');
    } finally {
      setIsLoading(false);
    }
  }, [phoneNumber, tenantId]);

  const handleVerifyOtp = useCallback(async () => {
    if (otpCode.length !== PHONE_OTP_CONSTANTS.OTP_LENGTH) {
      setErrorMessage(`OTP must be ${PHONE_OTP_CONSTANTS.OTP_LENGTH} digits`);
      return;
    }

    if (!sessionId) {
      setErrorMessage('Session expired. Please request a new OTP');
      setStep('PHONE');
      return;
    }

    setIsLoading(true);
    setErrorMessage(null);

    try {
      const result = await phoneOtpService.verifyOtp({
        tenant_id: tenantId,
        session_id: sessionId,
        code: otpCode,
      });

      if (result.success && result.auth_token) {
        onSuccess?.(result.auth_token);
      }
    } catch (err: unknown) {
      setErrorMessage(err instanceof Error ? err.message : 'Invalid OTP code');
    } finally {
      setIsLoading(false);
    }
  }, [otpCode, sessionId, tenantId, onSuccess]);

  return {
    phoneNumber,
    otpCode,
    step,
    isLoading,
    errorMessage,
    resendCountdown,
    onPhoneNumberChange: handlePhoneNumberChange,
    onOtpCodeChange: handleOtpCodeChange,
    onSendOtp: handleSendOtp,
    onVerifyOtp: handleVerifyOtp,
    onResendOtp: handleSendOtp,
  };
}
