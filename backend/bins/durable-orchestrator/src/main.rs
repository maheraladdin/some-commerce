use lambda_runtime::{service_fn, Error, LambdaEvent};
use serde::{Deserialize, Serialize};
use tracing::info;

#[derive(Debug, Deserialize)]
pub struct SagaStepEvent {
    pub saga_id: String,
    pub tenant_id: String,
    pub step: String,
}

#[derive(Debug, Serialize)]
pub struct SagaStepResponse {
    pub saga_id: String,
    pub status: String,
}

async fn saga_handler(event: LambdaEvent<SagaStepEvent>) -> Result<SagaStepResponse, Error> {
    let payload = event.payload;
    info!(
        saga_id = %payload.saga_id,
        tenant_id = %payload.tenant_id,
        step = %payload.step,
        "Executing saga step in durable orchestrator"
    );

    Ok(SagaStepResponse {
        saga_id: payload.saga_id,
        status: "STEP_COMPLETED".to_string(),
    })
}

#[tokio::main]
async fn main() -> Result<(), Error> {
    tracing_subscriber::fmt()
        .with_env_filter(tracing_subscriber::EnvFilter::from_default_env())
        .json()
        .init();

    info!("Starting some-commerce durable-orchestrator Cargo Lambda service...");

    lambda_runtime::run(service_fn(saga_handler)).await
}
