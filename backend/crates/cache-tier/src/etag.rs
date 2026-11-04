/// Computes an HTTP ETag string using BLAKE3 cryptographic hash.
pub fn compute_etag(payload: &[u8]) -> String {
    let hash = blake3::hash(payload);
    format!("\"{}\"", hash.to_hex())
}

/// Checks if client If-None-Match header matches the computed ETag.
pub fn is_etag_match(client_if_none_match: Option<&str>, current_etag: &str) -> bool {
    match client_if_none_match {
        Some(header_val) => {
            let clean = header_val.trim();
            clean == current_etag || clean == "*"
        }
        None => false,
    }
}
