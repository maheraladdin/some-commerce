use std::borrow::Cow;

/// Multi-tenant partition and sort key builders adhering to Constitutional Law 8.
/// Strictly enforces PK = TENANT#<tenant_id> to guarantee zero cross-tenant leakage.
pub struct KeyBuilder;

impl KeyBuilder {
    #[inline]
    pub fn tenant_pk<'a>(tenant_id: &'a str) -> Cow<'a, str> {
        if tenant_id.starts_with("TENANT#") {
            Cow::Borrowed(tenant_id)
        } else {
            Cow::Owned(format!("TENANT#{}", tenant_id))
        }
    }

    #[inline]
    pub fn user_sk<'a>(user_id: &'a str) -> Cow<'a, str> {
        if user_id.starts_with("USER#") {
            Cow::Borrowed(user_id)
        } else {
            Cow::Owned(format!("USER#{}", user_id))
        }
    }

    #[inline]
    pub fn otp_sk<'a>(phone_e164: &'a str) -> Cow<'a, str> {
        Cow::Owned(format!("OTP#{}", phone_e164))
    }

    #[inline]
    pub fn product_sk<'a>(product_id: &'a str) -> Cow<'a, str> {
        if product_id.starts_with("PRODUCT#") {
            Cow::Borrowed(product_id)
        } else {
            Cow::Owned(format!("PRODUCT#{}", product_id))
        }
    }

    #[inline]
    pub fn order_sk<'a>(order_id: &'a str) -> Cow<'a, str> {
        if order_id.starts_with("ORDER#") {
            Cow::Borrowed(order_id)
        } else {
            Cow::Owned(format!("ORDER#{}", order_id))
        }
    }
}
