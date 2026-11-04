use crate::error::{KernelError, KernelResult};
use serde::{Deserialize, Serialize};
use std::fmt;

#[derive(Debug, Copy, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum Currency {
    SAR,
    USD,
    EGP,
    AED,
    EUR,
}

impl fmt::Display for Currency {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Currency::SAR => write!(f, "SAR"),
            Currency::USD => write!(f, "USD"),
            Currency::EGP => write!(f, "EGP"),
            Currency::AED => write!(f, "AED"),
            Currency::EUR => write!(f, "EUR"),
        }
    }
}

/// Zero-clone monetary value stored strictly in minor units (cents, halalas, piasters).
/// Implements Copy for primitive efficiency and strict borrowing across domain operations.
#[derive(Debug, Copy, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Money {
    amount_minor: i64,
    currency: Currency,
}

impl Money {
    #[inline]
    pub const fn new(amount_minor: i64, currency: Currency) -> Self {
        Self {
            amount_minor,
            currency,
        }
    }

    #[inline]
    pub const fn zero(currency: Currency) -> Self {
        Self {
            amount_minor: 0,
            currency,
        }
    }

    #[inline]
    pub const fn amount_minor(&self) -> i64 {
        self.amount_minor
    }

    #[inline]
    pub const fn currency(&self) -> Currency {
        self.currency
    }

    /// Add two monetary values with strict currency alignment check.
    pub fn add(&self, other: &Money) -> KernelResult<Money> {
        if self.currency != other.currency {
            return Err(KernelError::CurrencyMismatch(
                self.currency.to_string(),
                other.currency.to_string(),
            ));
        }

        let total = self
            .amount_minor
            .checked_add(other.amount_minor)
            .ok_or(KernelError::ArithmeticOverflow)?;

        Ok(Money::new(total, self.currency))
    }

    /// Subtract two monetary values with strict currency alignment check.
    pub fn sub(&self, other: &Money) -> KernelResult<Money> {
        if self.currency != other.currency {
            return Err(KernelError::CurrencyMismatch(
                self.currency.to_string(),
                other.currency.to_string(),
            ));
        }

        let diff = self
            .amount_minor
            .checked_sub(other.amount_minor)
            .ok_or(KernelError::ArithmeticOverflow)?;

        Ok(Money::new(diff, self.currency))
    }

    /// Multiply by an integer factor (e.g. quantity) without floating point imprecision.
    pub fn mul_qty(&self, quantity: i64) -> KernelResult<Money> {
        let total = self
            .amount_minor
            .checked_mul(quantity)
            .ok_or(KernelError::ArithmeticOverflow)?;

        Ok(Money::new(total, self.currency))
    }

    /// Calculate basis points (e.g. 1500 bps = 15.00% VAT) without floating point imprecision.
    pub fn apply_basis_points(&self, bps: u32) -> KernelResult<Money> {
        let multiplied = (self.amount_minor as i128)
            .checked_mul(bps as i128)
            .ok_or(KernelError::ArithmeticOverflow)?;

        let result = (multiplied / 10_000) as i64;
        Ok(Money::new(result, self.currency))
    }
}
