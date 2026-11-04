pub const ROUTE_SEND_OTP: &str = "/v1/auth/otp/send";
pub const ROUTE_VERIFY_OTP: &str = "/v1/auth/otp/verify";

pub const OTP_EXPIRATION_SECONDS: u64 = 300; // 5 minutes
pub const MAX_OTP_ATTEMPTS: u8 = 3;
pub const DYNAMODB_OTP_PREFIX: &str = "OTP#";
