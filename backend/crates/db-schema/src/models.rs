use serde::{Deserialize, Serialize};

/// Generic envelope for DynamoDB single-table items.
#[derive(Debug, Serialize, Deserialize)]
pub struct TableRecord<T> {
    pub pk: String,
    pub sk: String,
    pub gsi1pk: Option<String>,
    pub gsi1sk: Option<String>,
    pub entity_type: String,
    pub version: u64,
    pub created_at: i64,
    pub updated_at: i64,
    pub data: T,
}

impl<T> TableRecord<T> {
    pub fn new(
        pk: String,
        sk: String,
        entity_type: &str,
        data: T,
        now_epoch: i64,
    ) -> Self {
        Self {
            pk,
            sk,
            gsi1pk: None,
            gsi1sk: None,
            entity_type: entity_type.to_string(),
            version: 1,
            created_at: now_epoch,
            updated_at: now_epoch,
            data,
        }
    }
}
