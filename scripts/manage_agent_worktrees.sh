#!/usr/bin/env bash
# ==============================================================================
# manage_agent_worktrees.sh - Git Worktree Manager for Roles & Agents
#
# Creates and manages isolated Git worktrees in .worktrees/ for:
#   - The 3 Google AI Pro Accounts (agent-a, agent-b, agent-c)
#   - Every Software Company Role (junior/senior backend, client, QA, PM, TL, CTO)
#   - Dynamic Sprint Agents (sprint-1.1-junior-be-1, etc.)
# ==============================================================================

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ "${REPO_ROOT}" =~ /\.worktrees ]]; then
  REPO_ROOT="${REPO_ROOT%%/.worktrees*}"
fi

WORKTREES_DIR="${REPO_ROOT}/.worktrees"
mkdir -p "${WORKTREES_DIR}"

ROLES=(
  "backend-engineer"
  "junior-backend-engineer"
  "senior-backend-engineer"
  "client-engineer"
  "junior-client-engineer"
  "senior-client-engineer"
  "testing-qa-engineer"
  "junior-testing-qa-engineer"
  "senior-security-qa-auditor"
  "product-manager"
  "tech-lead"
  "system-architect"
  "ui-ux-designer"
  "security-engineer"
  "devops-engineer"
  "release-gatekeeper"
  "chief-technology-officer"
)

ACCOUNTS=("agent-a" "agent-b" "agent-c")

function show_help() {
  cat << EOF
Usage: ./scripts/manage_agent_worktrees.sh <command> [args...]

Commands:
  status                          List all active worktrees, branches, and status
  init-accounts                   Initialize worktrees for the 3 Google AI Pro Accounts (agent-a, agent-b, agent-c)
  init-roles                      Initialize worktrees for all software company roles
  init-all                        Initialize worktrees for both accounts and all roles
  create <name> [branch]          Create a dedicated worktree for a specific agent or role
  switch <name> <story-id>        Switch a worktree to a story branch (e.g. switch agent-a US-1.1.1)
  reset <name>                    Reset a worktree to the latest origin/main
  remove <name>                   Remove a specific worktree safely
  remove-all                      Remove all worktrees inside .worktrees/

Examples:
  ./scripts/manage_agent_worktrees.sh init-accounts
  ./scripts/manage_agent_worktrees.sh init-roles
  ./scripts/manage_agent_worktrees.sh switch junior-backend-engineer US-1.1.1
  ./scripts/manage_agent_worktrees.sh status
EOF
  exit 0
}

function show_status() {
  echo "================================================================================"
  echo "Active Git Worktrees in .worktrees/"
  echo "================================================================================"
  git -C "${REPO_ROOT}" worktree list
  echo ""

  echo "Worktree Details & Status:"
  if [ -d "${WORKTREES_DIR}" ]; then
    found=0
    for dir in "${WORKTREES_DIR}"/*; do
      if [ -d "${dir}" ]; then
        found=1
        name=$(basename "${dir}")
        branch=$(git -C "${dir}" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "detached")
        dirty=$(git -C "${dir}" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
        echo "  - [${name}]"
        echo "      Path:   .worktrees/${name}"
        echo "      Branch: ${branch}"
        echo "      Dirty:  ${dirty} changed files"
      fi
    done
    if [ "${found}" -eq 0 ]; then
      echo "  (No worktrees currently initialized in .worktrees/)"
    fi
  fi
  echo "================================================================================"
}

function create_worktree() {
  local name="${1:-}"
  local branch="${2:-}"

  if [[ -z "${name}" ]]; then
    echo "Error: Worktree name required." >&2
    exit 1
  fi

  local target="${WORKTREES_DIR}/${name}"
  if [[ -z "${branch}" ]]; then
    branch="role/${name}"
  fi

  if [[ -d "${target}" ]]; then
    echo "Worktree for '${name}' already exists at ${target}."
    return 0
  fi

  echo "Creating isolated Git worktree for '${name}' on branch '${branch}'..."
  if git -C "${REPO_ROOT}" show-ref --verify --quiet "refs/heads/${branch}"; then
    git -C "${REPO_ROOT}" worktree add "${target}" "${branch}"
  else
    git -C "${REPO_ROOT}" worktree add -b "${branch}" "${target}" main
  fi
  echo "  [OK] Created .worktrees/${name} (branch: ${branch})"
}

function init_accounts() {
  echo "Initializing worktrees for 3 Google AI Pro Accounts..."
  for acc in "${ACCOUNTS[@]}"; do
    acc_letter=$(echo "${acc}" | sed 's/agent-//')
    create_worktree "${acc}" "agent/${acc_letter}"
  done
  echo "3 Google AI Pro Account worktrees ready."
}

function init_roles() {
  echo "Initializing worktrees for all ${#ROLES[@]} Software Company Roles..."
  for role in "${ROLES[@]}"; do
    create_worktree "${role}" "role/${role}"
  done
  echo "All role worktrees initialized."
}

function init_all() {
  init_accounts
  init_roles
}

function switch_story() {
  local name="${1:-}"
  local story="${2:-}"

  if [[ -z "${name}" || -z "${story}" ]]; then
    echo "Error: name and story required." >&2
    echo "Example: ./scripts/manage_agent_worktrees.sh switch junior-backend-engineer US-1.1.1" >&2
    exit 1
  fi

  local target="${WORKTREES_DIR}/${name}"
  local story_lower=$(echo "${story}" | tr '[:upper:]' '[:lower:]')
  local branch="${name}/${story_lower}"

  if [[ ! -d "${target}" ]]; then
    create_worktree "${name}" "${branch}"
    return 0
  fi

  local dirty=$(git -C "${target}" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
  if [[ "${dirty}" -gt 0 ]]; then
    echo "Warning: Worktree .worktrees/${name} has ${dirty} uncommitted changes." >&2
    echo "Commit or stash your changes before switching branches." >&2
    exit 1
  fi

  echo "Switching .worktrees/${name} to branch '${branch}'..."
  if git -C "${REPO_ROOT}" show-ref --verify --quiet "refs/heads/${branch}"; then
    git -C "${target}" checkout "${branch}"
  else
    git -C "${target}" checkout -b "${branch}" main
  fi
  echo "  [OK] .worktrees/${name} is now on branch '${branch}'."
}

function reset_worktree() {
  local name="${1:-}"
  if [[ -z "${name}" ]]; then
    echo "Error: name required." >&2
    exit 1
  fi

  local target="${WORKTREES_DIR}/${name}"
  if [[ ! -d "${target}" ]]; then
    echo "Worktree .worktrees/${name} does not exist." >&2
    exit 1
  fi

  echo "Resetting .worktrees/${name} to origin/main..."
  git -C "${target}" checkout main 2>/dev/null || true
  git -C "${target}" pull origin main 2>/dev/null || true
  echo "  [OK] Reset .worktrees/${name} to latest main."
}

function remove_worktree() {
  local name="${1:-}"
  if [[ -z "${name}" ]]; then
    echo "Error: name required." >&2
    exit 1
  fi

  local target="${WORKTREES_DIR}/${name}"
  if [[ -d "${target}" ]]; then
    echo "Removing worktree .worktrees/${name}..."
    git -C "${REPO_ROOT}" worktree remove --force "${target}" 2>/dev/null || rm -rf "${target}"
    git -C "${REPO_ROOT}" worktree prune
    echo "  [OK] Removed .worktrees/${name}."
  else
    echo "Worktree .worktrees/${name} does not exist."
  fi
}

function remove_all() {
  echo "Removing all worktrees from .worktrees/..."
  if [ -d "${WORKTREES_DIR}" ]; then
    for dir in "${WORKTREES_DIR}"/*; do
      if [ -d "${dir}" ]; then
        name=$(basename "${dir}")
        git -C "${REPO_ROOT}" worktree remove --force "${dir}" 2>/dev/null || rm -rf "${dir}"
      fi
    done
    git -C "${REPO_ROOT}" worktree prune
  fi
  echo "All worktrees removed."
}

cmd="${1:-status}"
shift || true

case "${cmd}" in
  status)
    show_status
    ;;
  init-accounts)
    init_accounts
    ;;
  init-roles)
    init_roles
    ;;
  init-all)
    init_all
    ;;
  create)
    create_worktree "${1:-}" "${2:-}"
    ;;
  switch)
    switch_story "${1:-}" "${2:-}"
    ;;
  reset)
    reset_worktree "${1:-}"
    ;;
  remove)
    remove_worktree "${1:-}"
    ;;
  remove-all)
    remove_all
    ;;
  help|--help|-h)
    show_help
    ;;
  *)
    show_help
    exit 1
    ;;
esac
