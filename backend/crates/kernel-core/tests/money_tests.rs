use kernel_core::{Currency, Money};

#[test]
fn test_minor_units_addition() {
    let m1 = Money::new(1000, Currency::SAR); // 10.00 SAR
    let m2 = Money::new(2550, Currency::SAR); // 25.50 SAR
    let sum = m1.add(&m2).expect("Addition should succeed");

    assert_eq!(sum.amount_minor(), 3550);
    assert_eq!(sum.currency(), Currency::SAR);
}

#[test]
fn test_currency_mismatch_prevention() {
    let sar = Money::new(1000, Currency::SAR);
    let usd = Money::new(1000, Currency::USD);

    assert!(sar.add(&usd).is_err());
}

#[test]
fn test_basis_points_vat_calculation() {
    let amount = Money::new(10_000, Currency::SAR); // 100.00 SAR
    let vat_15_percent = amount.apply_basis_points(1500).expect("BPS should succeed");

    assert_eq!(vat_15_percent.amount_minor(), 1500); // 15.00 SAR
}
