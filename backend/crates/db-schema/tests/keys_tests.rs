use db_schema::KeyBuilder;

#[test]
fn test_tenant_partition_key_law_8() {
    let pk = KeyBuilder::tenant_pk("tenant_123");
    assert_eq!(pk, "TENANT#tenant_123");

    // Idempotent if prefix already present
    let pk_already = KeyBuilder::tenant_pk("TENANT#tenant_123");
    assert_eq!(pk_already, "TENANT#tenant_123");
}

#[test]
fn test_otp_sort_key() {
    let sk = KeyBuilder::otp_sk("+966501234567");
    assert_eq!(sk, "OTP#+966501234567");
}
