use bytes::Bytes;
use moka::future::Cache;
use std::time::Duration;

/// In-memory L1 cache wrapper powered by Moka.
pub struct L1MemoryCache {
    cache: Cache<String, Bytes>,
}

impl L1MemoryCache {
    pub fn new(max_capacity: u64, ttl: Duration) -> Self {
        let cache = Cache::builder()
            .max_capacity(max_capacity)
            .time_to_live(ttl)
            .build();
        Self { cache }
    }

    pub async fn get(&self, key: &str) -> Option<Bytes> {
        self.cache.get(key).await
    }

    pub async fn insert(&self, key: String, value: Bytes) {
        self.cache.insert(key, value).await;
    }

    pub async fn invalidate(&self, key: &str) {
        self.cache.invalidate(key).await;
    }
}
