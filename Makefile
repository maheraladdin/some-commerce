# ==============================================================================
# some-commerce Enterprise White-Label E-Commerce Monorepo
# Master Orchestration Makefile v1.0.0
# ==============================================================================

SHELL := /bin/bash
.DEFAULT_GOAL := help

# --- Directories ---
ROOT_DIR     := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
BACKEND_DIR  := $(ROOT_DIR)/backend
FRONTEND_DIR := $(ROOT_DIR)/apps/storefront
INFRA_DIR    := $(ROOT_DIR)/infra
DEPLOY_DIR   := $(ROOT_DIR)/deploy

# --- Tooling ---
CARGO   := cargo
BUN     := bun
PYTHON  := python3
DOCKER  := docker
COMPOSE := docker compose

# --- Color Scheme for Help Output ---
COLOR_RESET   := \033[0m
COLOR_CYAN    := \033[36m
COLOR_GREEN   := \033[32m
COLOR_YELLOW  := \033[33m
COLOR_MAGENTA := \033[35m
COLOR_BOLD    := \033[1m

# ==============================================================================
# 1. HELP & DIAGNOSTICS
# ==============================================================================

.PHONY: help
help: ## Show this interactive command catalog with complete command descriptions
	@echo ""
	@echo -e "$(COLOR_BOLD)$(COLOR_CYAN)==============================================================================$(COLOR_RESET)"
	@echo -e "$(COLOR_BOLD)$(COLOR_CYAN)some-commerce Enterprise Architecture Monorepo (v1.0.0)$(COLOR_RESET)"
	@echo -e "$(COLOR_BOLD)$(COLOR_CYAN)==============================================================================$(COLOR_RESET)"
	@echo -e "$(COLOR_YELLOW)Usage:$(COLOR_RESET) make $(COLOR_GREEN)<target>$(COLOR_RESET)"
	@echo ""
	@echo -e "$(COLOR_BOLD)1. Environment & Setup:$(COLOR_RESET)"
	@printf "  $(COLOR_GREEN)%-26s$(COLOR_RESET) %s\n" "doctor" "Inspect local environment toolchains (Cargo, Bun, Python3, Docker)"
	@printf "  $(COLOR_GREEN)%-26s$(COLOR_RESET) %s\n" "info" "Display repository metadata, crate statistics, and platform architecture"
	@printf "  $(COLOR_GREEN)%-26s$(COLOR_RESET) %s\n" "install" "Install all dependencies across tiers (storefront, packages, infra)"
	@printf "  $(COLOR_GREEN)%-26s$(COLOR_RESET) %s\n" "setup" "Complete workspace initialization (install dependencies + run validators)"
	@echo ""
	@echo -e "$(COLOR_BOLD)2. Development Servers & Runtime:$(COLOR_RESET)"
	@printf "  $(COLOR_GREEN)%-26s$(COLOR_RESET) %s\n" "dev-storefront" "Launch the Expo universal mobile/web client dev server with Bun"
	@printf "  $(COLOR_GREEN)%-26s$(COLOR_RESET) %s\n" "dev-web" "Launch the Expo storefront in web browser mode"
	@printf "  $(COLOR_GREEN)%-26s$(COLOR_RESET) %s\n" "dev-backend" "Launch the Axum storefront-sdui-api server on port 8080"
	@echo ""
	@echo -e "$(COLOR_BOLD)3. Quality Assurance & Static Analysis:$(COLOR_RESET)"
	@printf "  $(COLOR_GREEN)%-26s$(COLOR_RESET) %s\n" "check" "Run typecheck and compiler validations (Rust cargo check + TypeScript tsc)"
	@printf "  $(COLOR_GREEN)%-26s$(COLOR_RESET) %s\n" "check-backend" "Run cargo check across all backend workspace crates and binaries"
	@printf "  $(COLOR_GREEN)%-26s$(COLOR_RESET) %s\n" "check-storefront" "Run TypeScript compiler check (bun run typecheck) on storefront"
	@printf "  $(COLOR_GREEN)%-26s$(COLOR_RESET) %s\n" "lint" "Execute static code analysis and clippy checks on backend"
	@printf "  $(COLOR_GREEN)%-26s$(COLOR_RESET) %s\n" "fmt" "Auto-format all Rust workspace source files (cargo fmt --all)"
	@printf "  $(COLOR_GREEN)%-26s$(COLOR_RESET) %s\n" "fmt-check" "Verify Rust formatting compliance (cargo fmt --all --check)"
	@echo ""
	@echo -e "$(COLOR_BOLD)4. Quality Gates & Validation Suites:$(COLOR_RESET)"
	@printf "  $(COLOR_GREEN)%-26s$(COLOR_RESET) %s\n" "validate" "Execute all 8 monorepo quality gate validators"
	@printf "  $(COLOR_GREEN)%-26s$(COLOR_RESET) %s\n" "gate-l1" "Run Gate L1: Constitutional & Global E-Commerce Law validator"
	@printf "  $(COLOR_GREEN)%-26s$(COLOR_RESET) %s\n" "gate-r1" "Run Gate R1: Rust Zero-Clone Borrowing Discipline validator"
	@printf "  $(COLOR_GREEN)%-26s$(COLOR_RESET) %s\n" "gate-f1" "Run Gate F1: Platform Presentation & UI/UX Separation validator"
	@printf "  $(COLOR_GREEN)%-26s$(COLOR_RESET) %s\n" "gate-m1" "Run Gate M1: Microkernel Logic Abstraction validator"
	@printf "  $(COLOR_GREEN)%-26s$(COLOR_RESET) %s\n" "gate-a1" "Run Gate A1: System Architecture Conformance validator"
	@printf "  $(COLOR_GREEN)%-26s$(COLOR_RESET) %s\n" "gate-a2" "Run Gate A2: Folder Architecture & LoB Conformance validator"
	@printf "  $(COLOR_GREEN)%-26s$(COLOR_RESET) %s\n" "gate-speckit" "Run GitHub Spec Kit Configuration validator"
	@printf "  $(COLOR_GREEN)%-26s$(COLOR_RESET) %s\n" "gate-docs" "Run User Stories & Spec Kit Documentation validator"
	@echo ""
	@echo -e "$(COLOR_BOLD)5. Automated Testing Suites:$(COLOR_RESET)"
	@printf "  $(COLOR_GREEN)%-26s$(COLOR_RESET) %s\n" "test" "Execute comprehensive test suites (backend cargo test + validation unit tests)"
	@printf "  $(COLOR_GREEN)%-26s$(COLOR_RESET) %s\n" "test-backend" "Run cargo test across all backend crates and integration suites"
	@printf "  $(COLOR_GREEN)%-26s$(COLOR_RESET) %s\n" "test-storefront" "Execute storefront unit, component, and hook tests using Bun"
	@printf "  $(COLOR_GREEN)%-26s$(COLOR_RESET) %s\n" "test-validation" "Execute Python unit tests and negative controls for all gates"
	@echo ""
	@echo -e "$(COLOR_BOLD)6. Compilation, CDK & Production Packaging:$(COLOR_RESET)"
	@printf "  $(COLOR_GREEN)%-26s$(COLOR_RESET) %s\n" "build" "Build release artifacts for both backend and storefront"
	@printf "  $(COLOR_GREEN)%-26s$(COLOR_RESET) %s\n" "build-backend" "Compile optimized production release binaries (storefront-sdui-api, etc.)"
	@printf "  $(COLOR_GREEN)%-26s$(COLOR_RESET) %s\n" "build-storefront" "Export static production Expo web bundle to apps/storefront/dist"
	@printf "  $(COLOR_GREEN)%-26s$(COLOR_RESET) %s\n" "cdk-synth" "Synthesize AWS CDK CloudFormation templates"
	@echo ""
	@echo -e "$(COLOR_BOLD)7. Infrastructure & Local Containers (deploy/):$(COLOR_RESET)"
	@printf "  $(COLOR_GREEN)%-26s$(COLOR_RESET) %s\n" "docker-up" "Start local development stack: Redis L2 cache, LocalStack DynamoDB"
	@printf "  $(COLOR_GREEN)%-26s$(COLOR_RESET) %s\n" "docker-down" "Stop local development stack containers"
	@printf "  $(COLOR_GREEN)%-26s$(COLOR_RESET) %s\n" "docker-ps" "List all running some-commerce containers"
	@echo ""
	@echo -e "$(COLOR_BOLD)8. Workspace Maintenance & Cleanup:$(COLOR_RESET)"
	@printf "  $(COLOR_GREEN)%-26s$(COLOR_RESET) %s\n" "clean" "Clean compiled build artifacts across backend and storefront"
	@echo ""

# ==============================================================================
# 2. ENVIRONMENT & SETUP
# ==============================================================================

.PHONY: doctor
doctor: ## Inspect local environment toolchains
	@echo -e "$(COLOR_BOLD)$(COLOR_CYAN)Checking environment toolchains...$(COLOR_RESET)"
	@which $(CARGO) > /dev/null && echo -e "  $(COLOR_GREEN)✓$(COLOR_RESET) Cargo: $$($(CARGO) --version)" || echo -e "  $(COLOR_YELLOW)✗$(COLOR_RESET) Cargo not found"
	@which $(BUN) > /dev/null && echo -e "  $(COLOR_GREEN)✓$(COLOR_RESET) Bun: $$($(BUN) --version)" || echo -e "  $(COLOR_YELLOW)✗$(COLOR_RESET) Bun not found"
	@which $(PYTHON) > /dev/null && echo -e "  $(COLOR_GREEN)✓$(COLOR_RESET) Python3: $$($(PYTHON) --version)" || echo -e "  $(COLOR_YELLOW)✗$(COLOR_RESET) Python3 not found"
	@which $(DOCKER) > /dev/null && echo -e "  $(COLOR_GREEN)✓$(COLOR_RESET) Docker: $$($(DOCKER) --version)" || echo -e "  $(COLOR_YELLOW)✗$(COLOR_RESET) Docker not found"

.PHONY: info
info: ## Display repository metadata and statistics
	@echo -e "$(COLOR_BOLD)$(COLOR_CYAN)some-commerce Architecture Summary$(COLOR_RESET)"
	@echo "  • Framework: Universal Expo SDK 58 (Client) + Rust 2024 Axum 0.8 (Backend)"
	@echo "  • User Stories: 51 Spec Kit Specifications (13 Modules)"
	@echo "  • Quality Gates: G0–G4 + G-Review + G-Borrow + G-UI + G-Law (Mandatory)"
	@echo "  • Slicing Standard: 10-PR Vertical Slicing Framework"

.PHONY: install
install: ## Install dependencies across storefront, packages, and infra
	@echo -e "$(COLOR_BOLD)$(COLOR_CYAN)Installing dependencies...$(COLOR_RESET)"
	@if [ -d "$(FRONTEND_DIR)" ] && [ -f "$(FRONTEND_DIR)/package.json" ]; then cd $(FRONTEND_DIR) && $(BUN) install; fi
	@if [ -d "$(INFRA_DIR)" ] && [ -f "$(INFRA_DIR)/package.json" ]; then cd $(INFRA_DIR) && $(BUN) install; fi

.PHONY: setup
setup: install validate ## Setup workspace and run all gate validations

# ==============================================================================
# 3. DEVELOPMENT SERVERS
# ==============================================================================

.PHONY: dev-storefront
dev-storefront: ## Launch Expo dev server
	@cd $(FRONTEND_DIR) && $(BUN) dev

.PHONY: dev-web
dev-web: ## Launch Expo storefront in web mode
	@cd $(FRONTEND_DIR) && $(BUN) run web

.PHONY: dev-backend
dev-backend: ## Launch Axum server
	@cd $(BACKEND_DIR) && $(CARGO) run --bin storefront-sdui-api

# ==============================================================================
# 4. QUALITY ASSURANCE & GATES
# ==============================================================================

.PHONY: check
check: check-backend check-storefront ## Run typecheck and compiler validations

.PHONY: check-backend
check-backend: ## Run cargo check on backend
	@if [ -d "$(BACKEND_DIR)" ] && [ -f "$(BACKEND_DIR)/Cargo.toml" ]; then cd $(BACKEND_DIR) && $(CARGO) check --workspace; fi

.PHONY: check-storefront
check-storefront: ## Run TypeScript typecheck on storefront
	@if [ -d "$(FRONTEND_DIR)" ] && [ -f "$(FRONTEND_DIR)/package.json" ]; then cd $(FRONTEND_DIR) && $(BUN) run typecheck; fi

.PHONY: lint
lint: ## Run cargo clippy on backend
	@if [ -d "$(BACKEND_DIR)" ] && [ -f "$(BACKEND_DIR)/Cargo.toml" ]; then cd $(BACKEND_DIR) && $(CARGO) clippy --workspace -- -D warnings; fi

.PHONY: fmt
fmt: ## Auto-format Rust files
	@if [ -d "$(BACKEND_DIR)" ] && [ -f "$(BACKEND_DIR)/Cargo.toml" ]; then cd $(BACKEND_DIR) && $(CARGO) fmt --all; fi

.PHONY: fmt-check
fmt-check: ## Verify Rust formatting
	@if [ -d "$(BACKEND_DIR)" ] && [ -f "$(BACKEND_DIR)/Cargo.toml" ]; then cd $(BACKEND_DIR) && $(CARGO) fmt --all -- --check; fi

# --- Quality Gates Targets ---

.PHONY: validate
validate: gate-speckit gate-docs gate-l1 gate-r1 gate-f1 gate-m1 gate-a1 gate-a2 ## Run all 8 quality gate validators
	@echo -e "$(COLOR_BOLD)$(COLOR_GREEN)All 8 Quality Gates Verified Successfully!$(COLOR_RESET)"

.PHONY: gate-l1
gate-l1: ## Run Gate L1 validator
	@$(PYTHON) scripts/validation/validate_laws.py

.PHONY: gate-r1
gate-r1: ## Run Gate R1 validator
	@$(PYTHON) scripts/validation/validate_rust_borrowing.py

.PHONY: gate-f1
gate-f1: ## Run Gate F1 validator
	@$(PYTHON) scripts/validation/validate_platform_presentation.py

.PHONY: gate-m1
gate-m1: ## Run Gate M1 validator
	@$(PYTHON) scripts/validation/validate_microkernel.py

.PHONY: gate-a1
gate-a1: ## Run Gate A1 validator
	@$(PYTHON) scripts/validation/validate_system_architecture.py

.PHONY: gate-a2
gate-a2: ## Run Gate A2 validator
	@$(PYTHON) scripts/validation/validate_folder_architecture.py

.PHONY: gate-speckit
gate-speckit: ## Run Spec Kit validator
	@$(PYTHON) scripts/validation/validate_speckit.py

.PHONY: gate-docs
gate-docs: ## Run Spec Kit user story documentation validator
	@$(PYTHON) scripts/validation/validate_docs.py

# ==============================================================================
# 5. TESTING SUITES
# ==============================================================================

.PHONY: test
test: test-validation test-backend ## Execute comprehensive test suites

.PHONY: test-backend
test-backend: ## Run cargo test on backend
	@if [ -d "$(BACKEND_DIR)" ] && [ -f "$(BACKEND_DIR)/Cargo.toml" ]; then cd $(BACKEND_DIR) && $(CARGO) test --workspace; fi

.PHONY: test-storefront
test-storefront: ## Run bun test on storefront
	@if [ -d "$(FRONTEND_DIR)" ] && [ -f "$(FRONTEND_DIR)/package.json" ]; then cd $(FRONTEND_DIR) && $(BUN) test; fi

.PHONY: test-validation
test-validation: ## Run validation unit tests
	@$(PYTHON) -m unittest discover -s scripts

# ==============================================================================
# 6. BUILD & PRODUCTION
# ==============================================================================

.PHONY: build
build: build-backend build-storefront ## Build release artifacts

.PHONY: build-backend
build-backend: ## Build release Rust binaries
	@if [ -d "$(BACKEND_DIR)" ] && [ -f "$(BACKEND_DIR)/Cargo.toml" ]; then cd $(BACKEND_DIR) && $(CARGO) build --release; fi

.PHONY: build-storefront
build-storefront: ## Build production Expo web bundle
	@if [ -d "$(FRONTEND_DIR)" ] && [ -f "$(FRONTEND_DIR)/package.json" ]; then cd $(FRONTEND_DIR) && $(BUN) run build:web; fi

.PHONY: cdk-synth
cdk-synth: ## Synthesize AWS CDK CloudFormation
	@if [ -d "$(INFRA_DIR)" ] && [ -f "$(INFRA_DIR)/package.json" ]; then cd $(INFRA_DIR) && $(BUN) run cdk synth; fi

# ==============================================================================
# 7. INFRASTRUCTURE & CONTAINERS
# ==============================================================================

.PHONY: docker-up
docker-up: ## Start local Redis and LocalStack containers
	@if [ -f "$(DEPLOY_DIR)/docker-compose.yml" ]; then $(COMPOSE) -f $(DEPLOY_DIR)/docker-compose.yml up -d; fi

.PHONY: docker-down
docker-down: ## Stop local containers
	@if [ -f "$(DEPLOY_DIR)/docker-compose.yml" ]; then $(COMPOSE) -f $(DEPLOY_DIR)/docker-compose.yml down; fi

.PHONY: docker-ps
docker-ps: ## List running containers
	@if [ -f "$(DEPLOY_DIR)/docker-compose.yml" ]; then $(COMPOSE) -f $(DEPLOY_DIR)/docker-compose.yml ps; fi

# ==============================================================================
# 8. CLEANUP
# ==============================================================================

.PHONY: clean
clean: ## Clean build outputs across backend and storefront
	@if [ -d "$(BACKEND_DIR)" ]; then cd $(BACKEND_DIR) && $(CARGO) clean 2>/dev/null || true; fi
	@if [ -d "$(FRONTEND_DIR)/dist" ]; then rm -rf $(FRONTEND_DIR)/dist; fi
