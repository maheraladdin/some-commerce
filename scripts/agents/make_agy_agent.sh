#!/usr/bin/env bash
# ==============================================================================
# make_agy_agent.sh - Antigravity CLI Agent Generator for some-commerce
#
# Generates an Antigravity CLI agent with:
#  1. Native Antigravity CLI agent definition: .agents/agents/<name>/agent.md
#  2. Isolated agent profile home & env:       .agent_profiles/<name>/
#  3. Sprint-level working directory:          .agents/workspaces/<sprint>/<name>/
#  4. Tailored context, rules & tasks:         context.md, agent.yaml, tasks.md, run.sh
#  5. Optional isolated Git worktree:          .worktrees/<name> or workspace/
# ==============================================================================

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

PROFILES_DIR="${REPO_ROOT}/.agents/profiles"
AGENTS_DIR="${REPO_ROOT}/.agents/agents"
AGENT_PROFILES_DIR="${REPO_ROOT}/.agent_profiles"
WORKSPACES_DIR="${REPO_ROOT}/.agents/workspaces"
WORKTREES_DIR="${REPO_ROOT}/.worktrees"

NAME=""
PROFILE=""
ROLE=""
SENIORITY=""
SPRINT="sprint-1.1"
STORY="us-1.1.1"
PR=""
WORKDIR=""
CREATE_WORKTREE=false
MODEL="gemini-3.8-flash-high"
EFFORT="high"
API_KEY=""

function show_help() {
  cat << EOF
Usage: ./scripts/agents/make_agy_agent.sh [OPTIONS]

Required Options:
  -n, --name <name>         Unique name for the agent (e.g. sprint-1.1-junior-be-1, s11-us111-be-builder)
  -p, --profile <profile>   Agent profile (e.g. backend-engineer, client-engineer, testing-qa-engineer,
                            product-manager, tech-lead, system-architect, cto, etc.)

Configuration Options:
  -r, --role <role>         Specialized role (builder, reviewer, tester, auditor, lead, pm, cto)
  -s, --seniority <level>   Seniority tier (junior, senior, lead, executive)
      --sprint <sprint-id>  Target sprint (default: sprint-1.1)
      --story <story-id>    Assigned User Story ID (default: us-1.1.1)
      --pr <1-10>           Assigned 10-PR Vertical Slice (1 to 10)
  -w, --workdir <path>      Custom working directory (default: .agents/workspaces/<sprint>/<name>)
      --create-git-worktree Create isolated Git worktree on branch agent/<sprint>/<name>
      --model <model>       Gemini model (default: gemini-3.8-flash-high)
      --effort <level>      Reasoning effort: low | medium | high | xhigh | max (default: high)
      --api-key <key>       Optional Gemini API key

Help:
  -h, --help                Show this help message and exit

Examples:
  # Generate a Junior Backend Builder for Sprint 1.1, Story US-1.1.1, PR 1:
  ./scripts/agents/make_agy_agent.sh -n s11-us111-be-builder -p backend-engineer -s junior -r builder --sprint sprint-1.1 --story us-1.1.1 --pr 1

  # Generate a Senior Backend Reviewer:
  ./scripts/agents/make_agy_agent.sh -n s11-sr-be-reviewer -p senior-backend-engineer --sprint sprint-1.1 --story us-1.1.1

  # Generate an agent with isolated Git worktree:
  ./scripts/agents/make_agy_agent.sh -n s11-fe-builder -p client-engineer --sprint sprint-1.1 --story us-1.1.1 --pr 5 --create-git-worktree
EOF
  exit 0
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    -n|--name)
      NAME="$2"
      shift 2
      ;;
    -p|--profile)
      PROFILE="$2"
      shift 2
      ;;
    -r|--role)
      ROLE="$2"
      shift 2
      ;;
    -s|--seniority)
      SENIORITY="$2"
      shift 2
      ;;
    --sprint)
      SPRINT="$2"
      shift 2
      ;;
    --story)
      STORY="$2"
      shift 2
      ;;
    --pr)
      PR="$2"
      shift 2
      ;;
    -w|--workdir)
      WORKDIR="$2"
      shift 2
      ;;
    --create-git-worktree)
      CREATE_WORKTREE=true
      shift
      ;;
    --model)
      MODEL="$2"
      shift 2
      ;;
    --effort)
      EFFORT="$2"
      shift 2
      ;;
    --api-key)
      API_KEY="$2"
      shift 2
      ;;
    -h|--help)
      show_help
      ;;
    *)
      echo "Error: Unknown argument: $1" >&2
      show_help
      ;;
  esac
done

if [[ -z "${NAME}" ]]; then
  echo "Error: --name <name> is required." >&2
  exit 1
fi

if [[ -z "${PROFILE}" ]]; then
  echo "Error: --profile <profile> is required." >&2
  exit 1
fi

# Check if profile exists
PROFILE_DIR="${PROFILES_DIR}/${PROFILE}"
if [[ ! -d "${PROFILE_DIR}" ]]; then
  # Check if alias exists or normalize
  if [[ "${PROFILE}" == "qa-security-auditor" ]]; then
    PROFILE="testing-qa-engineer"
    PROFILE_DIR="${PROFILES_DIR}/${PROFILE}"
  elif [[ "${PROFILE}" == "cto" ]]; then
    PROFILE="chief-technology-officer"
    PROFILE_DIR="${PROFILES_DIR}/${PROFILE}"
  fi
fi

if [[ ! -d "${PROFILE_DIR}" ]]; then
  echo "Error: Profile '${PROFILE}' not found in ${PROFILES_DIR}." >&2
  echo "Available profiles:" >&2
  ls -1 "${PROFILES_DIR}" >&2
  exit 1
fi

# Read profile metadata if present
if [[ -z "${SENIORITY}" ]]; then
  if grep -q "seniority: junior" "${PROFILE_DIR}/profile.yaml" 2>/dev/null; then
    SENIORITY="junior"
  elif grep -q "seniority: senior" "${PROFILE_DIR}/profile.yaml" 2>/dev/null; then
    SENIORITY="senior"
  elif grep -q "seniority: lead" "${PROFILE_DIR}/profile.yaml" 2>/dev/null; then
    SENIORITY="lead"
  elif grep -q "seniority: executive" "${PROFILE_DIR}/profile.yaml" 2>/dev/null; then
    SENIORITY="executive"
  else
    SENIORITY="senior"
  fi
fi

if [[ -z "${ROLE}" ]]; then
  if grep -q "role: reviewer" "${PROFILE_DIR}/profile.yaml" 2>/dev/null; then
    ROLE="reviewer"
  elif grep -q "role: auditor" "${PROFILE_DIR}/profile.yaml" 2>/dev/null; then
    ROLE="auditor"
  elif grep -q "role: tester" "${PROFILE_DIR}/profile.yaml" 2>/dev/null; then
    ROLE="tester"
  elif grep -q "role: lead" "${PROFILE_DIR}/profile.yaml" 2>/dev/null; then
    ROLE="lead"
  elif grep -q "role: pm" "${PROFILE_DIR}/profile.yaml" 2>/dev/null; then
    ROLE="pm"
  elif grep -q "role: cto" "${PROFILE_DIR}/profile.yaml" 2>/dev/null; then
    ROLE="cto"
  else
    ROLE="builder"
  fi
fi

if [[ -z "${WORKDIR}" ]]; then
  WORKDIR="${WORKSPACES_DIR}/${SPRINT}/${NAME}"
fi

mkdir -p "${WORKDIR}"

echo "================================================================================"
echo "Generating Antigravity CLI Agent: ${NAME}"
echo "  Profile:   ${PROFILE} (${SENIORITY} / ${ROLE})"
echo "  Sprint:    ${SPRINT}"
echo "  Story:     ${STORY}"
if [[ -n "${PR}" ]]; then
  echo "  PR Slice:  PR ${PR}"
fi
echo "  Workdir:   ${WORKDIR}"
echo "================================================================================"

# 1. Generate tailored context and tasks via generate_agent.py
GEN_ARGS=(
  "--name" "${NAME}"
  "--profile" "${PROFILE}"
  "--role" "${ROLE}"
  "--seniority" "${SENIORITY}"
  "--sprint" "${SPRINT}"
  "--story" "${STORY}"
  "--workdir" "${WORKDIR}"
)

if [[ -n "${PR}" ]]; then
  GEN_ARGS+=("--pr" "${PR}")
fi

if [[ "${CREATE_WORKTREE}" == true ]]; then
  GEN_ARGS+=("--create-git-worktree")
fi

python3 "${REPO_ROOT}/scripts/agents/generate_agent.py" "${GEN_ARGS[@]}"

# 2. Setup native Antigravity CLI Agent in .agents/agents/<name>/agent.md
AGENT_DIR="${AGENTS_DIR}/${NAME}"
mkdir -p "${AGENT_DIR}"

SYSTEM_PROMPT_CONTENT=""
if [[ -f "${PROFILE_DIR}/system_prompt.md" ]]; then
  SYSTEM_PROMPT_CONTENT=$(cat "${PROFILE_DIR}/system_prompt.md")
fi

cat << EOF > "${AGENT_DIR}/agent.md"
---
name: ${NAME}
description: Antigravity CLI agent instance '${NAME}' for sprint '${SPRINT}', profile '${PROFILE}', story '${STORY}'.
tools:
  - send_message
  - view_file
  - read_url_content
  - search_web
  - multi_replace_file_content
  - replace_file_content
  - write_to_file
  - run_command
  - manage_task
---

# Agent Instance: ${NAME}

## Context & Assignment
- **Profile**: \`${PROFILE}\` (\`${SENIORITY}\` / \`${ROLE}\`)
- **Sprint**: \`${SPRINT}\`
- **Story**: \`${STORY}\`
- **Assigned PR**: \`${PR:-All PRs}\`
- **Assigned Workdir**: \`${WORKDIR}\`

## Tailored Context & Instructions
See the detailed sprint context at:
\`${WORKDIR}/context.md\`
\`${WORKDIR}/tasks.md\`

${SYSTEM_PROMPT_CONTENT}
EOF

# 3. Setup isolated agent profile home in .agent_profiles/<name>/
AGENT_HOME="${AGENT_PROFILES_DIR}/${NAME}"
mkdir -p "${AGENT_HOME}/.gemini/antigravity-cli"

cat << EOF > "${AGENT_PROFILES_DIR}/${NAME}.env"
# Environment configuration for Antigravity Agent: ${NAME}
MODEL="${MODEL}"
EFFORT="${EFFORT}"
GEMINI_API_KEY="${API_KEY}"
SPRINT="${SPRINT}"
STORY="${STORY}"
PR="${PR:-all}"
WORKDIR="${WORKDIR}"
EOF

if [[ -n "${API_KEY:-}" ]]; then
  echo '{"modelProvider": "gemini"}' > "${AGENT_HOME}/.gemini/antigravity-cli/settings.json"
else
  echo '{}' > "${AGENT_HOME}/.gemini/antigravity-cli/settings.json"
fi

# 4. Create one-click runner script in workdir: run.sh
# generate_agent.py already emitted a runner through agy_agent.sh and its quota pool.
chmod +x "${WORKDIR}/run.sh"

echo ""
echo "================================================================================"
echo "Agent '${NAME}' successfully generated and registered with Antigravity CLI!"
echo "  1. CLI Discovery:     agy agents | grep ${NAME}"
echo "  2. Workdir Artifacts: ${WORKDIR}/ (agent.yaml, context.md, tasks.md, run.sh)"
echo "  3. Profile Home:      ${AGENT_HOME}/"
echo "  4. Direct Runner:     ${WORKDIR}/run.sh"
echo "  5. Script Launcher:   ./scripts/agents/agy_agent.sh ${NAME}"
echo "================================================================================"
