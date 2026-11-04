use std::sync::Arc;
use cache_tier::L1MemoryCache;

/// Shared application context holding cache, database handles, and configuration.
pub struct AppContext {
    pub app_name: &'static str,
    pub cache: Arc<L1MemoryCache>,
}

impl AppContext {
    pub fn new(app_name: &'static str) -> Self {
        let cache = Arc::new(L1MemoryCache::new(10_000, std::time::Duration::from_secs(300)));
        Self { app_name, cache }
    }
}
