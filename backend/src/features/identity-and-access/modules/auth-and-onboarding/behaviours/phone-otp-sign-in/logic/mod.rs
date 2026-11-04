use super::types::{SendOtpRequest, VerifyOtpRequest};

/// Validates E.164 international phone number format (+ followed by 8-15 digits).
pub fn validate_e164_phone(phone: &str) -> bool {
    let trimmed = phone.trim();
    if !trimmed.starts_with('+') {
        return false;
    }
    let digits = &trimmed[1..];
    digits.len() >= 8 && digits.len() <= 15 && digits.chars().all(|c| c.is_ascii_digit())
}

/// Validates a 6-digit numeric OTP code.
pub fn validate_otp_code(code: &str) -> bool {
    let trimmed = code.trim();
    trimmed.len() == 6 && trimmed.chars().all(|c| c.is_ascii_digit())
}

/// Pure validation guard for SendOtpRequest.
pub fn guard_send_otp_request(req: &SendOtpRequest) -> Result<(), &'static str> {
    if req.tenant_id.trim().is_empty() {
        return Err("Tenant ID is required");
    }
    if !validate_e164_phone(&req.phone_number) {
        return Err("Phone number must be a valid E.164 format (e.g. +966501234567)");
    }
    Ok(())
}

/// Pure validation guard for VerifyOtpRequest.
pub fn guard_verify_otp_request(req: &VerifyOtpRequest) -> Result<(), &'static str> {
    if req.tenant_id.trim().is_empty() {
        return Err("Tenant ID is required");
    }
    if req.session_id.trim().is_empty() {
        return Err("Session ID is required");
    }
    if !validate_otp_code(&req.code) {
        return Err("OTP code must be 6 digits");
    }
    Ok(())
}
