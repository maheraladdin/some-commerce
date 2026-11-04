use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize)]
pub struct SendOtpRequest {
    pub tenant_id: String,
    pub phone_number: String,
}

#[derive(Debug, Serialize)]
pub struct SendOtpResponse {
    pub success: bool,
    pub session_id: String,
    pub expires_in_seconds: u64,
}

#[derive(Debug, Deserialize)]
pub struct VerifyOtpRequest {
    pub tenant_id: String,
    pub session_id: String,
    pub code: String,
}

#[derive(Debug, Serialize)]
pub struct VerifyOtpResponse {
    pub success: bool,
    pub auth_token: Option<String>,
    pub message: String,
}
