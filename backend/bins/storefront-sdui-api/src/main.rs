use lambda_http::{run, Error};
use some_commerce_backend::{build_master_router, AppContext};
use std::sync::Arc;
use tracing::info;

#[tokio::main]
async fn main() -> Result<(), Error> {
    tracing_subscriber::fmt()
        .with_env_filter(tracing_subscriber::EnvFilter::from_default_env())
        .json()
        .init();

    info!("Starting some-commerce storefront-sdui-api Cargo Lambda service...");

    let ctx = Arc::new(AppContext::new("storefront-sdui-api"));
    let app = build_master_router(ctx);

    run(app).await
}
