#!/usr/bin/env python3
"""
Test suite for Gate M1 validator (validate_microkernel.py).
Provides negative controls:
1. Detects forbidden cloud SDKs in microkernel crate Cargo.toml
2. Detects forbidden lambda_http imports in Axum feature code
3. Detects forbidden .clone() calls in pure domain Rust code
4. Confirms that Arc::clone, Rc::clone, and // allow(clone) pass
"""

import sys
import unittest
import tempfile
import shutil
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_microkernel import (
    validate_crate_cargo_toml,
    validate_axum_feature_file,
    validate_rust_zero_clone,
)


class TestGateM1Validator(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_forbidden_crate_dependencies(self):
        # 1. Clean Cargo.toml should pass
        clean_cargo = self.test_dir / "clean_Cargo.toml"
        clean_cargo.write_text("""
[package]
name = "some-validation"
version = "0.1.0"

[dependencies]
serde = "1.0"
thiserror = "1.0"
regex = "1.10"
""", encoding="utf-8")
        errors = validate_crate_cargo_toml(clean_cargo)
        self.assertEqual(len(errors), 0, f"Expected 0 errors for clean cargo, got: {errors}")

        # 2. Cargo with aws-sdk-dynamodb and lambda_http should fail
        violating_cargo = self.test_dir / "violating_Cargo.toml"
        violating_cargo.write_text("""
[package]
name = "some-validation"
version = "0.1.0"

[dependencies]
serde = "1.0"
aws-sdk-dynamodb = "1.0"
lambda_http = "0.13"
mongodb = "2.8"
""", encoding="utf-8")
        errors = validate_crate_cargo_toml(violating_cargo)
        self.assertEqual(len(errors), 3, f"Expected 3 forbidden dep errors, got: {errors}")

    def test_forbidden_axum_feature_imports(self):
        # 1. Clean Axum handler should pass
        clean_rs = self.test_dir / "handler.rs"
        clean_rs.write_text("""
use axum::{routing::post, Router, Json};
use std::sync::Arc;

pub async fn login_handler() -> &'static str {
    "ok"
}
""", encoding="utf-8")
        errors = validate_axum_feature_file(clean_rs)
        self.assertEqual(len(errors), 0, f"Expected 0 errors, got: {errors}")

        # 2. Axum handler importing lambda_http should fail
        violating_rs = self.test_dir / "violating_handler.rs"
        violating_rs.write_text("""
use axum::{routing::post, Router};
use lambda_http::Request;
use aws_lambda_events::event::apigw::ApiGatewayProxyRequest;

pub async fn handler() {}
""", encoding="utf-8")
        errors = validate_axum_feature_file(violating_rs)
        self.assertEqual(len(errors), 2, f"Expected 2 transport import errors, got: {errors}")

    def test_rust_zero_clone_borrowing_enforcement(self):
        # 1. Clean borrowing and Arc::clone should pass
        clean_borrow_rs = self.test_dir / "borrow.rs"
        clean_borrow_rs.write_text("""
use std::sync::Arc;

pub fn process_order<'a>(order_id: &'a str, items: &'a [u8], shared_state: Arc<State>) {
    let state_handle = Arc::clone(&shared_state);
    let slice = &items[0..2];
    // allow(clone): explicitly permitted
    let copy = order_id.to_string().clone();
}

#[cfg(test)]
mod tests {
    fn test_helper() {
        let x = vec![1, 2].clone();
    }
}
""", encoding="utf-8")
        errors = validate_rust_zero_clone(clean_borrow_rs)
        self.assertEqual(len(errors), 0, f"Expected 0 errors for clean borrow, got: {errors}")

        # 2. Deep .clone() calls should fail
        violating_clone_rs = self.test_dir / "violating_clone.rs"
        violating_clone_rs.write_text("""
pub fn handle_order(payload: OrderPayload) {
    let duplicated_payload = payload.clone();
    let user_name = payload.user_name.clone();
}
""", encoding="utf-8")
        errors = validate_rust_zero_clone(violating_clone_rs)
        self.assertEqual(len(errors), 2, f"Expected 2 clone violation errors, got: {errors}")


if __name__ == "__main__":
    unittest.main()
