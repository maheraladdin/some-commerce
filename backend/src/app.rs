use axum::Router;
use std::sync::Arc;

use crate::features::identity_and_access::modules::auth_and_onboarding::behaviours::phone_otp_sign_in;
use crate::shared::AppContext;

/// Builds the portable Axum master router decoupled from Lambda runtime.
pub fn build_master_router(ctx: Arc<AppContext>) -> Router {
    let auth_state = Arc::new(phone_otp_sign_in::services::AuthAppState {
        app_name: ctx.app_name,
    });

    let auth_routes = phone_otp_sign_in::router(auth_state);

    Router::new()
        .merge(auth_routes)
        .route("/healthz", axum::routing::get(|| async { "ok" }))
}
