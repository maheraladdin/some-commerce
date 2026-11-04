use cache_tier::{compute_etag, is_etag_match};

#[test]
fn test_etag_generation_and_match() {
    let payload = b"{\"products\": [{\"id\": \"p1\"}]}";
    let etag = compute_etag(payload);

    assert!(etag.starts_with('"'));
    assert!(etag.ends_with('"'));

    assert!(is_etag_match(Some(&etag), &etag));
    assert!(is_etag_match(Some("*"), &etag));
    assert!(!is_etag_match(Some("\"different\""), &etag));
    assert!(!is_etag_match(None, &etag));
}
