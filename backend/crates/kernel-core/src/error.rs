use thiserror::Error;

#[derive(Error, Debug)]
pub enum KernelError {
    #[error("Invalid currency operation: cannot combine {0} and {1}")]
    CurrencyMismatch(String, String),

    #[error("Arithmetic overflow in monetary calculation")]
    ArithmeticOverflow,

    #[error("Tenant validation failed: {0}")]
    InvalidTenant(String),

    #[error("Unauthorized action: {0}")]
    Unauthorized(String),

    #[error("Resource not found: {0}")]
    NotFound(String),

    #[error("Port error: {0}")]
    PortError(String),
}

pub type KernelResult<T> = Result<T, KernelError>;
