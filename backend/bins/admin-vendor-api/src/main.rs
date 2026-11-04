use axum::{routing::get, Json, Router};
use lambda_http::{run, Error};
use serde_json::json;
use tracing::info;

async fn vendor_status_handler() -> Json<serde_json::Value> {
    info!("Vendor status queried");
    Json(json!({
        "status": "operational",
        "service": "admin-vendor-api"
    }))
}

#[tokio::main]
async fn main() -> Result<(), Error> {
    tracing_subscriber::fmt()
        .with_env_filter(tracing_subscriber::EnvFilter::from_default_env())
        .json()
        .init();

    info!("Starting some-commerce admin-vendor-api Cargo Lambda service...");

    let app = Router::new()
        .route("/admin/health", get(vendor_status_handler));

    run(app).await
}
