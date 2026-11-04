import React from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ActivityIndicator,
  StyleSheet,
} from 'react-native';
import type { PhoneOtpScreenProps } from '../types/types';

/**
 * Gate G-UI Certified Mobile Presentation Screen
 * Author: UI/UX Designer
 * Implements native platform presentation using React Native primitives.
 */
export const PhoneOtpScreenNative: React.FC<PhoneOtpScreenProps> = ({
  phoneNumber,
  otpCode,
  step,
  isLoading,
  errorMessage,
  resendCountdown,
  onPhoneNumberChange,
  onOtpCodeChange,
  onSendOtp,
  onVerifyOtp,
  onResendOtp,
}) => {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>
        {step === 'PHONE' ? 'Sign In with Phone' : 'Enter Verification Code'}
      </Text>
      <Text style={styles.subtitle}>
        {step === 'PHONE'
          ? 'Enter your international phone number to receive a one-time passcode.'
          : `We sent a 6-digit code to ${phoneNumber}`}
      </Text>

      {errorMessage ? (
        <View style={styles.errorContainer}>
          <Text style={styles.errorText}>{errorMessage}</Text>
        </View>
      ) : null}

      {step === 'PHONE' ? (
        <View style={styles.formGroup}>
          <Text style={styles.label}>Phone Number</Text>
          <TextInput
            style={styles.input}
            placeholder="+966 50 123 4567"
            placeholderTextColor="#64748B"
            keyboardType="phone-pad"
            value={phoneNumber}
            onChangeText={onPhoneNumberChange}
            editable={!isLoading}
            autoFocus
          />
          <TouchableOpacity
            style={[styles.button, isLoading && styles.buttonDisabled]}
            onPress={onSendOtp}
            disabled={isLoading}
            activeOpacity={0.8}
          >
            {isLoading ? (
              <ActivityIndicator color="#FFFFFF" />
            ) : (
              <Text style={styles.buttonText}>Send Code</Text>
            )}
          </TouchableOpacity>
        </View>
      ) : (
        <View style={styles.formGroup}>
          <Text style={styles.label}>6-Digit OTP</Text>
          <TextInput
            style={[styles.input, styles.otpInput]}
            placeholder="123456"
            placeholderTextColor="#64748B"
            keyboardType="number-pad"
            maxLength={6}
            value={otpCode}
            onChangeText={onOtpCodeChange}
            editable={!isLoading}
            autoFocus
          />
          <TouchableOpacity
            style={[styles.button, isLoading && styles.buttonDisabled]}
            onPress={onVerifyOtp}
            disabled={isLoading || otpCode.length !== 6}
            activeOpacity={0.8}
          >
            {isLoading ? (
              <ActivityIndicator color="#FFFFFF" />
            ) : (
              <Text style={styles.buttonText}>Verify & Continue</Text>
            )}
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.resendButton}
            onPress={onResendOtp}
            disabled={resendCountdown > 0 || isLoading}
          >
            <Text style={styles.resendText}>
              {resendCountdown > 0
                ? `Resend code in ${resendCountdown}s`
                : 'Resend Verification Code'}
            </Text>
          </TouchableOpacity>
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#080A0F',
    padding: 24,
    justifyContent: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#F1F5F9',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 14,
    color: '#94A3B8',
    marginBottom: 24,
    lineHeight: 20,
  },
  errorContainer: {
    backgroundColor: 'rgba(239, 68, 68, 0.15)',
    padding: 12,
    borderRadius: 8,
    marginBottom: 16,
  },
  errorText: {
    color: '#EF4444',
    fontSize: 14,
  },
  formGroup: {
    gap: 16,
  },
  label: {
    fontSize: 14,
    color: '#94A3B8',
    fontWeight: '500',
  },
  input: {
    backgroundColor: '#10141E',
    borderWidth: 1,
    borderColor: '#232D42',
    borderRadius: 8,
    padding: 14,
    color: '#F1F5F9',
    fontSize: 16,
  },
  otpInput: {
    textAlign: 'center',
    letterSpacing: 8,
    fontSize: 20,
  },
  button: {
    backgroundColor: '#3B82F6',
    borderRadius: 8,
    padding: 14,
    alignItems: 'center',
    justifyContent: 'center',
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  buttonText: {
    color: '#FFFFFF',
    fontWeight: '600',
    fontSize: 16,
  },
  resendButton: {
    alignItems: 'center',
    padding: 8,
  },
  resendText: {
    color: '#94A3B8',
    fontSize: 14,
  },
});
