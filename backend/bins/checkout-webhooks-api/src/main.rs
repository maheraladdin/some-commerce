use axum::{routing::post, Json, Router};
use lambda_http::{run, Error};
use serde_json::Value;
use tracing::info;

async fn webhook_handler(Json(payload): Json<Value>) -> &'static str {
    info!("Received checkout payment webhook event");
    let _ = payload;
    "accepted"
}

#[tokio::main]
async fn main() -> Result<(), Error> {
    tracing_subscriber::fmt()
        .with_env_filter(tracing_subscriber::EnvFilter::from_default_env())
        .json()
        .init();

    info!("Starting some-commerce checkout-webhooks-api Cargo Lambda service...");

    let app = Router::new()
        .route("/webhooks/paymob", post(webhook_handler))
        .route("/webhooks/stripe", post(webhook_handler))
        .route("/webhooks/zatca", post(webhook_handler));

    run(app).await
}
