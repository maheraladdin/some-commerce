use crate::error::{KernelError, KernelResult};
use serde::{Deserialize, Serialize};

/// Zero-copy borrowed tenant identifier enforcing multi-tenant isolation.
#[derive(Debug, Copy, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct TenantRef<'a> {
    id: &'a str,
}

impl<'a> TenantRef<'a> {
    pub fn try_new(id: &'a str) -> KernelResult<Self> {
        let trimmed = id.trim();
        if trimmed.is_empty() {
            return Err(KernelError::InvalidTenant("Tenant ID cannot be empty".to_string()));
        }
        if !trimmed.chars().all(|c| c.is_ascii_alphanumeric() || c == '-' || c == '_') {
            return Err(KernelError::InvalidTenant(
                "Tenant ID contains invalid characters; must be alphanumeric, hyphen, or underscore".to_string(),
            ));
        }
        Ok(Self { id: trimmed })
    }

    #[inline]
    pub fn as_str(&self) -> &'a str {
        self.id
    }
}

/// Zero-copy borrowed actor / user identifier.
#[derive(Debug, Copy, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct UserRef<'a> {
    id: &'a str,
}

impl<'a> UserRef<'a> {
    pub fn try_new(id: &'a str) -> KernelResult<Self> {
        let trimmed = id.trim();
        if trimmed.is_empty() {
            return Err(KernelError::Unauthorized("User ID cannot be empty".to_string()));
        }
        Ok(Self { id: trimmed })
    }

    #[inline]
    pub fn as_str(&self) -> &'a str {
        self.id
    }
}
