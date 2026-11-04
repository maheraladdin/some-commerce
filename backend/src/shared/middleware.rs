use axum::{
    body::Body,
    http::{Request, StatusCode},
    middleware::Next,
    response::Response,
};

/// Middleware ensuring X-Tenant-Id header is present on multi-tenant requests.
pub async fn enforce_tenant_header(
    req: Request<Body>,
    next: Next,
) -> Result<Response, (StatusCode, &'static str)> {
    if !req.headers().contains_key("x-tenant-id") {
        return Err((StatusCode::BAD_REQUEST, "Missing required X-Tenant-Id header"));
    }
    Ok(next.run(req).await)
}
