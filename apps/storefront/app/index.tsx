import React from 'react';
import { Platform } from 'react-native';
import { usePhoneOtpAuth } from '@/features/identity-and-access/modules/auth-and-onboarding/behaviours/phone-otp-sign-in/logic/usePhoneOtpAuth';
import { PhoneOtpScreenNative } from '@/features/identity-and-access/modules/auth-and-onboarding/behaviours/phone-otp-sign-in/designs/PhoneOtpScreen.native';
import { PhoneOtpScreenWeb } from '@/features/identity-and-access/modules/auth-and-onboarding/behaviours/phone-otp-sign-in/designs/PhoneOtpScreen.web';

export default function HomeScreen() {
  const authState = usePhoneOtpAuth({
    tenantId: 'default',
    onSuccess: (token) => {
      console.log('Successfully authenticated with token:', token);
    },
  });

  if (Platform.OS === 'web') {
    return <PhoneOtpScreenWeb {...authState} />;
  }

  return <PhoneOtpScreenNative {...authState} />;
}
