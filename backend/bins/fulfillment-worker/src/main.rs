use lambda_runtime::{service_fn, Error, LambdaEvent};
use serde::{Deserialize, Serialize};
use tracing::info;

#[derive(Debug, Deserialize)]
pub struct FulfillmentEvent {
    pub tenant_id: String,
    pub order_id: String,
    pub carrier: String,
}

#[derive(Debug, Serialize)]
pub struct FulfillmentResponse {
    pub tracking_number: String,
    pub status: String,
}

async fn function_handler(event: LambdaEvent<FulfillmentEvent>) -> Result<FulfillmentResponse, Error> {
    let payload = event.payload;
    info!(
        tenant_id = %payload.tenant_id,
        order_id = %payload.order_id,
        carrier = %payload.carrier,
        "Processing fulfillment event in worker"
    );

    Ok(FulfillmentResponse {
        tracking_number: format!("TRK-{}", uuid::Uuid::new_v4()),
        status: "DISPATCHED".to_string(),
    })
}

#[tokio::main]
async fn main() -> Result<(), Error> {
    tracing_subscriber::fmt()
        .with_env_filter(tracing_subscriber::EnvFilter::from_default_env())
        .json()
        .init();

    info!("Starting some-commerce fulfillment-worker Cargo Lambda service...");

    lambda_runtime::run(service_fn(function_handler)).await
}
