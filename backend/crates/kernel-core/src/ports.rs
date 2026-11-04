use crate::error::KernelResult;
use async_trait::async_trait;
use bytes::Bytes;

/// Hexagonal port for document / key-value storage (implemented by DynamoDB in AWS or In-Memory/Redis for testing).
#[async_trait]
pub trait DocumentDbPort: Send + Sync {
    async fn get_item(&self, pk: &str, sk: &str) -> KernelResult<Option<Bytes>>;
    async fn put_item(&self, pk: &str, sk: &str, payload: &[u8]) -> KernelResult<()>;
    async fn delete_item(&self, pk: &str, sk: &str) -> KernelResult<()>;
}

/// Hexagonal port for binary object storage (implemented by S3 in AWS or Local filesystem).
#[async_trait]
pub trait BlobStoragePort: Send + Sync {
    async fn put_blob(&self, key: &str, data: &[u8], content_type: &str) -> KernelResult<()>;
    async fn get_blob(&self, key: &str) -> KernelResult<Bytes>;
    async fn delete_blob(&self, key: &str) -> KernelResult<()>;
}

/// Hexagonal port for event messaging / bus (implemented by SNS/SQS/EventBridge in AWS or Mock channel).
#[async_trait]
pub trait EventBusPort: Send + Sync {
    async fn publish_event(&self, topic: &str, event_type: &str, payload: &[u8]) -> KernelResult<()>;
}

/// Hexagonal port for KMS / envelope encryption.
#[async_trait]
pub trait KeyManagementPort: Send + Sync {
    async fn encrypt(&self, key_id: &str, plaintext: &[u8]) -> KernelResult<Bytes>;
    async fn decrypt(&self, key_id: &str, ciphertext: &[u8]) -> KernelResult<Bytes>;
}
