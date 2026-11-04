import React from 'react';
import type { PhoneOtpScreenProps } from '../types/types';

/**
 * Gate G-UI Certified Web Presentation Screen
 * Author: UI/UX Designer
 * Implements semantic HTML5 + Tailwind CSS v4 presentation for web browsers.
 */
export const PhoneOtpScreenWeb: React.FC<PhoneOtpScreenProps> = ({
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
    <div className="min-h-screen bg-slate-950 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h1 className="text-center text-3xl font-extrabold text-white tracking-tight">
          {step === 'PHONE' ? 'Sign In with Phone' : 'Enter Verification Code'}
        </h1>
        <p className="mt-2 text-center text-sm text-slate-400">
          {step === 'PHONE'
            ? 'Enter your international phone number to receive a one-time passcode.'
            : `We sent a 6-digit code to ${phoneNumber}`}
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-slate-900 py-8 px-4 shadow sm:rounded-lg sm:px-10 border border-slate-800">
          {errorMessage ? (
            <div
              role="alert"
              className="mb-4 bg-red-950/50 border border-red-500/50 p-3 rounded text-sm text-red-400"
            >
              {errorMessage}
            </div>
          ) : null}

          {step === 'PHONE' ? (
            <form
              className="space-y-6"
              onSubmit={(e) => {
                e.preventDefault();
                onSendOtp();
              }}
            >
              <div>
                <label
                  htmlFor="phone-input"
                  className="block text-sm font-medium text-slate-300"
                >
                  Phone Number
                </label>
                <div className="mt-1">
                  <input
                    id="phone-input"
                    type="tel"
                    required
                    placeholder="+966 50 123 4567"
                    value={phoneNumber}
                    onChange={(e) => onPhoneNumberChange(e.target.value)}
                    disabled={isLoading}
                    className="appearance-none block w-full px-3 py-2 border border-slate-700 rounded-md shadow-sm bg-slate-950 text-white placeholder-slate-500 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  />
                </div>
              </div>

              <div>
                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
                >
                  {isLoading ? 'Sending...' : 'Send Verification Code'}
                </button>
              </div>
            </form>
          ) : (
            <form
              className="space-y-6"
              onSubmit={(e) => {
                e.preventDefault();
                onVerifyOtp();
              }}
            >
              <div>
                <label
                  htmlFor="otp-input"
                  className="block text-sm font-medium text-slate-300"
                >
                  6-Digit OTP Code
                </label>
                <div className="mt-1">
                  <input
                    id="otp-input"
                    type="text"
                    required
                    maxLength={6}
                    placeholder="123456"
                    value={otpCode}
                    onChange={(e) => onOtpCodeChange(e.target.value)}
                    disabled={isLoading}
                    className="appearance-none block w-full px-3 py-2 border border-slate-700 rounded-md shadow-sm bg-slate-950 text-white placeholder-slate-500 text-center tracking-widest text-lg font-mono focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>

              <div>
                <button
                  type="submit"
                  disabled={isLoading || otpCode.length !== 6}
                  className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
                >
                  {isLoading ? 'Verifying...' : 'Verify & Continue'}
                </button>
              </div>

              <div className="text-center">
                <button
                  type="button"
                  onClick={onResendOtp}
                  disabled={resendCountdown > 0 || isLoading}
                  className="text-sm font-medium text-slate-400 hover:text-slate-300 disabled:opacity-50"
                >
                  {resendCountdown > 0
                    ? `Resend code in ${resendCountdown}s`
                    : 'Resend Verification Code'}
                </button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};
