#!/usr/bin/env bash
# ==============================================================================
# agy_agent.sh - Antigravity CLI Launcher with 3 Google AI Pro Accounts
#
# Manages 3 authenticated Google AI Pro Account profiles:
#   - Account A (agent-a): All roles, shared quota pool
#   - Account B (agent-b): All roles, shared quota pool
#   - Account C (agent-c): All roles, shared quota pool
#
# All logical agents (Junior Authors, Senior Reviewers, PM, TL, CTO) execute
# by inheriting authentication from one of these 3 accounts.
# ==============================================================================

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

AGENTS_DIR="${REPO_ROOT}/.agents/agents"
AGENT_PROFILES_DIR="${REPO_ROOT}/.agent_profiles"
WORKSPACES_DIR="${REPO_ROOT}/.agents/workspaces"

AGY_BIN="${AGY_BIN:-$(command -v agy 2>/dev/null || echo "/Users/maheraladdin/.local/bin/agy")}"

function show_help() {
  cat << EOF
Usage: ./scripts/agents/agy_agent.sh [--account auto|a|b|c] <a|b|c|agent-name> [agy_options...]

1. Google AI Pro Account Sign-In / Interactive CLI:
  ./scripts/agents/agy_agent.sh a             # Interactive session for Account 1 (any role)
  ./scripts/agents/agy_agent.sh b             # Interactive session for Account 2 (any role)
  ./scripts/agents/agy_agent.sh c             # Interactive session for Account 3 (any role)

2. Run Single Prompt on an Account:
  ./scripts/agents/agy_agent.sh a -p "Review microkernel domain logic"
  ./scripts/agents/agy_agent.sh b -p "Inspect WatermelonDB offline schema"
  ./scripts/agents/agy_agent.sh c -p "Run Gate G2 security compliance audit"

3. Execute Any Specific Sprint Agent (Inherits Auth from Account A, B, or C):
  ./scripts/agents/agy_agent.sh sprint-1.1-junior-be-1
  ./scripts/agents/agy_agent.sh s11-us111-be-builder -p "Implement PR 1 domain logic"
  ./scripts/agents/agy_agent.sh sprint-1.1-tech-lead

4. All roles balance across all three accounts by default:
  ./scripts/agents/agy_agent.sh senior-backend-engineer -p "Review the assigned candidate"
  ./scripts/agents/agy_agent.sh --account b product-manager -p "Review assigned AC evidence"
  python3 scripts/agents/agent_account_pool.py status
  python3 scripts/agents/agent_account_pool.py configure agent-a --cooldown-seconds 3600
  python3 scripts/agents/agent_account_pool.py configure agent-b --budget 100 --used 25

Local estimated units balance usage; configure budgets/reset from actual provider evidence.
Quota errors require reporting cooldown/usage, reconciliation, then a new launch; no automatic replay.

5. Utilities:
  ./scripts/agents/agy_agent.sh --list        # List 3 Auth Accounts & all registered agents
  ./scripts/agents/agy_agent.sh --status      # Check authentication directory status
EOF
  exit 0
}

if [[ $# -lt 1 || "$1" == "-h" || "$1" == "--help" ]]; then
  show_help
fi

function show_status() {
  echo "================================================================================"
  echo "Google AI Pro Account Authentication Profiles (3 Physical Auth Homes)"
  echo "================================================================================"
  for acc in a b c; do
    acc_dir="${AGENT_PROFILES_DIR}/agent-${acc}"
    acc_upper=$(echo "${acc}" | tr '[:lower:]' '[:upper:]')
    echo "Account ${acc_upper} (agent-${acc}):"
    echo "  Auth Home Directory: ${acc_dir}"
    if [[ -d "${acc_dir}/.gemini" ]]; then
      echo "  Status:              INITIALIZED (Settings configured)"
    else
      echo "  Status:              NOT INITIALIZED (Run './scripts/agents/agy_agent.sh ${acc}' to sign in)"
    fi
  done
  echo "================================================================================"
}

if [[ "$1" == "--status" || "$1" == "status" ]]; then
  show_status
  exit 0
fi

if [[ "$1" == "--list" || "$1" == "list" ]]; then
  show_status
  echo ""
  echo "Available Registered Agents in Antigravity CLI:"
  cd "${REPO_ROOT}"
  exec "${AGY_BIN}" agents
fi

REQUESTED_ACCOUNT="auto"
if [[ "$1" == "--account" ]]; then
  if [[ $# -lt 3 ]]; then echo "--account needs an account and agent name" >&2; exit 2; fi
  REQUESTED_ACCOUNT="$2"
  shift 2
fi
case "${REQUESTED_ACCOUNT}" in
  a|b|c) REQUESTED_ACCOUNT="agent-${REQUESTED_ACCOUNT}" ;;
  auto|agent-a|agent-b|agent-c) ;;
  *) echo "Invalid account selection" >&2; exit 2 ;;
esac

if [[ ! -x "${AGY_BIN}" ]]; then
  echo "Error: Antigravity CLI binary 'agy' not found at ${AGY_BIN}." >&2
  exit 1
fi

INPUT="$1"
shift

# Normalize input for account shortcut: 'a', 'b', 'c', 'agent-a', 'agent-b', 'agent-c'
NORMALIZED=$(echo "${INPUT}" | tr '[:upper:]' '[:lower:]')

AUTH_ACCOUNT=""
AGENT_NAME=""

if [[ "${NORMALIZED}" == "a" || "${NORMALIZED}" == "agent-a" || "${NORMALIZED}" == "profile-a" ]]; then
  AUTH_ACCOUNT="agent-a"
  AGENT_NAME="agent-a"
elif [[ "${NORMALIZED}" == "b" || "${NORMALIZED}" == "agent-b" || "${NORMALIZED}" == "profile-b" ]]; then
  AUTH_ACCOUNT="agent-b"
  AGENT_NAME="agent-b"
elif [[ "${NORMALIZED}" == "c" || "${NORMALIZED}" == "agent-c" || "${NORMALIZED}" == "profile-c" ]]; then
  AUTH_ACCOUNT="agent-c"
  AGENT_NAME="agent-c"
else
  AGENT_NAME="${INPUT}"
fi

# Role names no longer select authentication accounts. Legacy account mappings
# in role .env files are intentionally ignored; use --account for an explicit pin.
if [[ -z "${AUTH_ACCOUNT}" && ! -d "${AGENTS_DIR}/${AGENT_NAME}" ]]; then
  echo "Error: Agent '${AGENT_NAME}' is not registered in ${AGENTS_DIR}." >&2
  exit 1
fi
if [[ -n "${AUTH_ACCOUNT}" ]]; then
  if [[ "${REQUESTED_ACCOUNT}" != "auto" && "${REQUESTED_ACCOUNT}" != "${AUTH_ACCOUNT}" ]]; then
    echo "Conflicting explicit account selections" >&2; exit 2
  fi
  REQUESTED_ACCOUNT="${AUTH_ACCOUNT}"
  # Explicit account shortcuts support initial sign-in before setup.
  mkdir -p "${AGENT_PROFILES_DIR}/${AUTH_ACCOUNT}"
fi
if [[ -z "${AGENT_POOL_RESERVATION:-}" ]]; then
  exec python3 "${REPO_ROOT}/scripts/agents/agent_account_pool.py" run \
    --role "${AGENT_NAME}" --account "${REQUESTED_ACCOUNT}" -- \
    "${BASH_SOURCE[0]}" "${INPUT}" "$@"
fi
AUTH_ACCOUNT="${AGENT_POOL_ACCOUNT:-}"
case "${AUTH_ACCOUNT}" in agent-a|agent-b|agent-c) ;; *) echo "Invalid reserved account" >&2; exit 2 ;; esac

# Set isolated HOME to the physical Google AI Pro Account home
PROFILE_HOME="${AGENT_PROFILES_DIR}/${AUTH_ACCOUNT}"
mkdir -p "${PROFILE_HOME}/.gemini/antigravity-cli"



# Load custom environment config from account env
MODEL="gemini-3.8-flash-high"
EFFORT="high"
GEMINI_API_KEY=""
ENV_FILE="${AGENT_PROFILES_DIR}/${AUTH_ACCOUNT}.env"
if [[ -f "${ENV_FILE}" ]]; then
  # shellcheck disable=SC1090
  source "${ENV_FILE}"
fi

# Preserve instance model/effort preferences without sourcing old account bindings.
INSTANCE_ENV="${AGENT_PROFILES_DIR}/${AGENT_NAME}.env"
if [[ "${AGENT_NAME}" != "${AUTH_ACCOUNT}" && -f "${INSTANCE_ENV}" ]]; then
  INSTANCE_MODEL=$(sed -n 's/^MODEL="\([^"]*\)"$/\1/p' "${INSTANCE_ENV}")
  INSTANCE_EFFORT=$(sed -n 's/^EFFORT="\([^"]*\)"$/\1/p' "${INSTANCE_ENV}")
  if [[ -n "${INSTANCE_MODEL}" ]]; then MODEL="${INSTANCE_MODEL}"; fi
  if [[ -n "${INSTANCE_EFFORT}" ]]; then EFFORT="${INSTANCE_EFFORT}"; fi
fi

SETTINGS_DIR="${PROFILE_HOME}/.gemini/antigravity-cli"
SETTINGS_FILE="${SETTINGS_DIR}/settings.json"
mkdir -p "${SETTINGS_DIR}"

if [[ -n "${GEMINI_API_KEY:-}" ]]; then
  export GEMINI_API_KEY="${GEMINI_API_KEY}"
  echo '{"modelProvider": "gemini"}' > "${SETTINGS_FILE}"
else
  # Use default backend to trigger browser OAuth sign-in for Google AI Pro accounts
  if [[ -f "${SETTINGS_FILE}" ]] && grep -q '"modelProvider"' "${SETTINGS_FILE}"; then
    echo '{}' > "${SETTINGS_FILE}"
  elif [[ ! -f "${SETTINGS_FILE}" ]]; then
    echo '{}' > "${SETTINGS_FILE}"
  fi
fi

# Determine Working Directory
TARGET_DIR="${REPO_ROOT}"
# Look for sprint workspace if this is a spawned agent
FOUND_WORKDIR=$(find "${WORKSPACES_DIR}" -mindepth 2 -maxdepth 2 -type d -name "${AGENT_NAME}" 2>/dev/null | head -n 1 || true)
if [[ -n "${FOUND_WORKDIR}" && -d "${FOUND_WORKDIR}" ]]; then
  TARGET_DIR="${FOUND_WORKDIR}"
fi

if [[ -d "${TARGET_DIR}/workspace" ]]; then
  TARGET_DIR="${TARGET_DIR}/workspace"
fi

ARGS=()
HAS_MODEL=false
HAS_EFFORT=false

for arg in "$@"; do
  if [[ "${arg}" == "--model" ]]; then HAS_MODEL=true; fi
  if [[ "${arg}" == "--effort" ]]; then HAS_EFFORT=true; fi
  ARGS+=("${arg}")
done

if [[ "${HAS_MODEL}" == false ]]; then
  ARGS+=(--model "${MODEL}")
fi

if [[ "${HAS_EFFORT}" == false ]]; then
  ARGS+=(--effort "${EFFORT}")
fi

ACCOUNT_LETTER=$(echo "${AUTH_ACCOUNT}" | sed 's/agent-//' | tr '[:lower:]' '[:upper:]')

echo "================================================================================"
echo "Starting Antigravity CLI for Agent: ${AGENT_NAME}"
echo "  Google AI Pro Auth: Account ${ACCOUNT_LETTER} (${AUTH_ACCOUNT})"
echo "  Auth HOME:          ${PROFILE_HOME}"
echo "  Working Directory:  ${TARGET_DIR}"
echo "  Model & Effort:     ${MODEL} (effort: ${EFFORT})"
echo "================================================================================"

cd "${TARGET_DIR}"
exec env HOME="${PROFILE_HOME}" "${AGY_BIN}" --agent "${AGENT_NAME}" "${ARGS[@]}"
