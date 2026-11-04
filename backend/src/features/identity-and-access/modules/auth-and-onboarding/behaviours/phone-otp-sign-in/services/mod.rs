use axum::{
    extract::State,
    http::StatusCode,
    response::IntoResponse,
    routing::post,
    Json, Router,
};
use std::sync::Arc;

use super::constants::{OTP_EXPIRATION_SECONDS, ROUTE_SEND_OTP, ROUTE_VERIFY_OTP};
use super::logic::{guard_send_otp_request, guard_verify_otp_request};
use super::types::{SendOtpRequest, SendOtpResponse, VerifyOtpRequest, VerifyOtpResponse};

/// Pure Axum application state wrapping hexagonal ports or in-memory handlers.
pub struct AuthAppState {
    // In real implementation, stores Arc<dyn DocumentDbPort> and Arc<dyn EventBusPort>
    pub app_name: &'static str,
}

/// Handler for POST /v1/auth/otp/send (decoupled from lambda_http).
pub async fn send_otp_handler(
    State(_state): State<Arc<AuthAppState>>,
    Json(payload): Json<SendOtpRequest>,
) -> Result<impl IntoResponse, (StatusCode, &'static str)> {
    guard_send_otp_request(&payload).map_err(|err| (StatusCode::BAD_REQUEST, err))?;

    let session_id = uuid::Uuid::new_v4().to_string();

    Ok(Json(SendOtpResponse {
        success: true,
        session_id,
        expires_in_seconds: OTP_EXPIRATION_SECONDS,
    }))
}

/// Handler for POST /v1/auth/otp/verify (decoupled from lambda_http).
pub async fn verify_otp_handler(
    State(_state): State<Arc<AuthAppState>>,
    Json(payload): Json<VerifyOtpRequest>,
) -> Result<impl IntoResponse, (StatusCode, &'static str)> {
    guard_verify_otp_request(&payload).map_err(|err| (StatusCode::BAD_REQUEST, err))?;

    // In production, verifies against DynamoDB PK = TENANT#<id>, SK = OTP#<session_id>
    let auth_token = format!("tok_{}", uuid::Uuid::new_v4());

    Ok(Json(VerifyOtpResponse {
        success: true,
        auth_token: Some(auth_token),
        message: "OTP verified successfully".to_string(),
    }))
}

/// Constructs the pure Axum router for the Phone OTP behavior.
pub fn router(state: Arc<AuthAppState>) -> Router {
    Router::new()
        .route(ROUTE_SEND_OTP, post(send_otp_handler))
        .route(ROUTE_VERIFY_OTP, post(verify_otp_handler))
        .with_state(state)
}
