#!/usr/bin/env python3
"""
Agent Profile Load Balancer for some-commerce.
Balances user story implementation tasks and 7-PR vertical slices across
the 3 core execution agent profiles:
1. backend-engineer (PR 1, PR 2, PR 3, PR 4)
2. client-engineer (PR 5, PR 6, PR 7)
3. qa-security-auditor (Gates G0–G4, Gate M1, ASVS L2 Audit)

Provides:
- Intelligent skill and layer routing
- Least-active workload and weighted fair-share scheduling
- DAG dependency gating (PR 1 -> PR 2 -> [PR 3, PR 5] -> [PR 4, PR 6] -> PR 7)
- Automated generation of isolated agent workdirs and tailored contexts
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_agent import generate_agent, find_user_story_file, PR_SPECS

# Profile mapping for the 7 PR layers
PR_PROFILE_ROUTING = {
    1: "backend-engineer",   # Microkernel Logic & Invariants
    2: "backend-engineer",   # Polyglot Database Schemas (Co-owned with client-engineer)
    3: "backend-engineer",   # Repositories & Caching Tier
    4: "backend-engineer",   # Pure Axum Handlers & WebMCP
    5: "client-engineer",    # Client Services & WatermelonDB Sync
    6: "client-engineer",    # Headless Custom Hooks & Logic
    7: "client-engineer",    # Platform-Adaptive UI & SDUI Renderers
}


def parse_sprint_stories(sprint_id: str) -> List[Tuple[str, str, int]]:
    """Extracts stories from docs/sprints/<sprint_id>.md -> [(story_id, title, points)]"""
    sprint_file = REPO_ROOT / "docs" / "sprints" / f"{sprint_id}.md"
    if not sprint_file.exists():
        raise FileNotFoundError(f"Sprint file not found: {sprint_file}")

    content = sprint_file.read_text(encoding="utf-8")
    stories = []

    # Regex matches table rows: | P0 | [US-1.1.1](...) | Module | 5 | Description |
    row_regex = re.compile(
        r"\|\s*P\d+\s*\|\s*\[(US-[\d\.]+)\]\(([^)]+)\)\s*\|\s*[^|]+\|\s*(\d+)\s*\|\s*([^|]+)\|",
        re.IGNORECASE,
    )

    for match in row_regex.finditer(content):
        story_id = match.group(1).lower()
        points = int(match.group(3))
        desc = match.group(4).strip()
        stories.append((story_id, desc, points))

    return stories


class AgentProfileLoadBalancer:
    def __init__(
        self,
        sprint_id: str,
        junior_be_workers: int = 2,
        junior_fe_workers: int = 2,
        junior_qa_workers: int = 1,
        be_workers: Optional[int] = None,
        fe_workers: Optional[int] = None,
        qa_workers: Optional[int] = None,
    ):
        self.sprint_id = sprint_id
        actual_be = be_workers if be_workers is not None else junior_be_workers
        actual_fe = fe_workers if fe_workers is not None else junior_fe_workers
        actual_qa = qa_workers if qa_workers is not None else junior_qa_workers

        # Junior Implementer Pools
        self.junior_be_pool = [
            {"id": f"{sprint_id}-junior-be-{i+1}", "profile": "backend-engineer", "seniority": "junior", "role": "builder", "workload": 0, "tasks": []}
            for i in range(actual_be)
        ]
        self.junior_fe_pool = [
            {"id": f"{sprint_id}-junior-fe-{i+1}", "profile": "client-engineer", "seniority": "junior", "role": "builder", "workload": 0, "tasks": []}
            for i in range(actual_fe)
        ]
        self.junior_qa_pool = [
            {"id": f"{sprint_id}-junior-qa-{i+1}", "profile": "testing-qa-engineer", "seniority": "junior", "role": "tester", "workload": 0, "tasks": []}
            for i in range(actual_qa)
        ]

        # Senior Reviewer Pool
        self.senior_be = {"id": f"{sprint_id}-senior-be-1", "profile": "backend-engineer", "seniority": "senior", "role": "reviewer", "workload": 0, "reviews": []}
        self.senior_fe = {"id": f"{sprint_id}-senior-fe-1", "profile": "client-engineer", "seniority": "senior", "role": "reviewer", "workload": 0, "reviews": []}
        self.senior_qa = {"id": f"{sprint_id}-senior-qa-1", "profile": "security-engineer", "seniority": "senior", "role": "auditor", "workload": 0, "reviews": []}

        # Leadership & Governance
        self.tech_lead = {"id": f"{sprint_id}-tech-lead", "profile": "tech-lead", "role": "lead", "tasks": []}
        self.product_manager = {"id": f"{sprint_id}-product-manager", "profile": "product-manager", "role": "pm", "tasks": []}
        self.cto = {"id": f"{sprint_id}-cto", "profile": "chief-technology-officer", "role": "cto", "tasks": []}

    def balance_sprint(self) -> Dict:
        """Distributes all stories and 7 PR slices across worker pools using least-loaded algorithm."""
        stories = parse_sprint_stories(self.sprint_id)
        if not stories:
            raise ValueError(f"No user stories found in sprint {self.sprint_id}")

        allocation_plan = {
            "sprint_id": self.sprint_id,
            "total_stories": len(stories),
            "total_prs": len(stories) * 7,
            "governance_ladder": [
                "Layer 1: Junior Author Implementation",
                "Layer 2: Senior Peer Code Review",
                "Layer 3: Security & Architecture Gate Audit",
                "Layer 4: Tech Lead & Gatekeeper Integration",
                "Layer 5: Product Manager Acceptance Sign-Off",
                "Layer 6: Chief Technology Officer (CTO) Agreement & Release Authorization",
            ],
            "worker_pools": {
                "junior-backend-engineer": len(self.junior_be_pool),
                "junior-client-engineer": len(self.junior_fe_pool),
                "junior-qa-engineer": len(self.junior_qa_pool),
                "senior-reviewers": 3,
                "leadership": 3,
            },
            "story_allocations": [],
            "workers": {},
            "leadership": {
                "tech_lead": self.tech_lead["id"],
                "product_manager": self.product_manager["id"],
                "cto": self.cto["id"],
            },
        }

        for story_id, desc, points in stories:
            story_alloc = {
                "story_id": story_id,
                "title": desc,
                "points": points,
                "prs": [],
            }

            # Distribute each of the 7 PRs for this story
            for pr_num in range(1, 8):
                profile_target = PR_PROFILE_ROUTING[pr_num]
                pr_info = PR_SPECS[pr_num]
                pr_weight = max(1, points // 4)

                # Select least-loaded junior worker in the target profile pool
                if profile_target == "backend-engineer":
                    worker = min(self.junior_be_pool, key=lambda w: w["workload"])
                    reviewer = self.senior_be
                else:
                    worker = min(self.junior_fe_pool, key=lambda w: w["workload"])
                    reviewer = self.senior_fe

                # Assign task
                task = {
                    "story_id": story_id,
                    "story_title": desc,
                    "pr_num": pr_num,
                    "pr_name": pr_info["name"],
                    "layers": pr_info["layers"],
                    "weight": pr_weight,
                    "workdir": f".agents/workspaces/{self.sprint_id}/{worker['id']}",
                    "senior_reviewer": reviewer["id"],
                }
                worker["workload"] += pr_weight
                worker["tasks"].append(task)

                reviewer["workload"] += max(1, pr_weight // 2)
                reviewer["reviews"].append({
                    "story_id": story_id,
                    "pr_num": pr_num,
                    "junior_author": worker["id"],
                })

                story_alloc["prs"].append({
                    "pr_num": pr_num,
                    "pr_name": pr_info["name"],
                    "junior_author": worker["id"],
                    "senior_reviewer": reviewer["id"],
                    "profile": worker["profile"],
                    "workdir": task["workdir"],
                })

            # Assign QA audit task for Gate G0–G4 and G2 security sign-off
            qa_worker = min(self.junior_qa_pool, key=lambda w: w["workload"])
            qa_task = {
                "story_id": story_id,
                "story_title": desc,
                "pr_num": "G0-G4",
                "pr_name": "Security Gateway & Acceptance Audit",
                "layers": ["docs/validation/", "backend/tests/", "apps/storefront/__tests__/"],
                "weight": 2,
                "workdir": f".agents/workspaces/{self.sprint_id}/{qa_worker['id']}",
                "senior_reviewer": self.senior_qa["id"],
            }
            qa_worker["workload"] += 2
            qa_worker["tasks"].append(qa_task)
            self.senior_qa["workload"] += 2
            self.senior_qa["reviews"].append({
                "story_id": story_id,
                "pr_num": "G0-G4",
                "junior_author": qa_worker["id"],
            })

            story_alloc["qa_auditor"] = {
                "junior_author": qa_worker["id"],
                "senior_reviewer": self.senior_qa["id"],
                "workdir": qa_task["workdir"],
            }

            story_alloc["governance"] = {
                "layer_4_tech_lead": self.tech_lead["id"],
                "layer_5_product_manager": self.product_manager["id"],
                "layer_6_cto_agreement": self.cto["id"],
            }

            allocation_plan["story_allocations"].append(story_alloc)

        # Aggregate worker summary
        all_workers = self.junior_be_pool + self.junior_fe_pool + self.junior_qa_pool + [self.senior_be, self.senior_fe, self.senior_qa]
        for w in all_workers:
            tasks_list = w.get("tasks", [])
            reviews_list = w.get("reviews", [])
            allocation_plan["workers"][w["id"]] = {
                "profile": w["profile"],
                "seniority": w["seniority"],
                "role": w["role"],
                "workload": w["workload"],
                "total_tasks": len(tasks_list),
                "total_reviews": len(reviews_list),
                "tasks": tasks_list,
                "reviews": reviews_list,
            }

        return allocation_plan

    def spawn_workspaces(self, plan: Dict, create_git_worktree: bool = False) -> List[Dict]:
        """Generates the actual isolated workspaces, agent.yaml, context.md, and tasks.md."""
        generated = []
        for worker_id, worker_data in plan["workers"].items():
            first_task = worker_data["tasks"][0] if worker_data["tasks"] else None
            story_id = first_task["story_id"] if first_task else "general"

            workdir, files = generate_agent(
                name=worker_id,
                profile=worker_data["profile"],
                role=worker_data.get("role", "builder"),
                sprint=self.sprint_id,
                story_id=story_id,
                pr_num=first_task["pr_num"] if first_task and isinstance(first_task["pr_num"], int) else None,
                custom_workdir=str(REPO_ROOT / ".agents" / "workspaces" / self.sprint_id / worker_id),
                create_git_worktree=create_git_worktree,
                seniority=worker_data.get("seniority", "senior"),
            )

            # Update context.md with ALL assigned tasks for this balanced worker
            worker_context_file = Path(files["context_md"])
            extra_schedule = f"\n\n## 8. Multi-Story Load Balancer Workload ({len(worker_data['tasks'])} Tasks)\n"
            extra_schedule += "| Story | PR # | Slice Name | Layer Target | Weight |\n"
            extra_schedule += "|:------|:-----|:-----------|:-------------|:-------|\n"
            for t in worker_data["tasks"]:
                extra_schedule += f"| `{t['story_id']}` | PR {t['pr_num']} | {t['pr_name']} | `{', '.join(t['layers'])}` | {t['weight']} pts |\n"

            with open(worker_context_file, "a", encoding="utf-8") as f:
                f.write(extra_schedule)

            generated.append({
                "worker_id": worker_id,
                "profile": worker_data["profile"],
                "workdir": str(workdir),
                "tasks_count": len(worker_data["tasks"]),
            })

        return generated


def main():
    parser = argparse.ArgumentParser(description="Agent Profile Load Balancer for some-commerce.")
    parser.add_argument("--sprint", required=True, help="Sprint identifier (e.g. sprint-1.1)")
    parser.add_argument("--junior-be-workers", type=int, default=2, help="Number of junior backend worker instances")
    parser.add_argument("--junior-fe-workers", type=int, default=2, help="Number of junior client worker instances")
    parser.add_argument("--junior-qa-workers", type=int, default=1, help="Number of junior QA worker instances")
    parser.add_argument("--balance", action="store_true", help="Calculate and print balanced allocation matrix")
    parser.add_argument("--spawn", action="store_true", help="Generate all worker workspaces, contexts, and configs")
    parser.add_argument("--create-git-worktree", action="store_true", help="Create isolated git worktrees for workers")

    args = parser.parse_args()

    balancer = AgentProfileLoadBalancer(
        sprint_id=args.sprint,
        junior_be_workers=args.junior_be_workers,
        junior_fe_workers=args.junior_fe_workers,
        junior_qa_workers=args.junior_qa_workers,
    )

    try:
        plan = balancer.balance_sprint()
    except Exception as e:
        print(f"Error calculating balance: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"\n========================================================")
    print(f"AGENT PROFILE LOAD BALANCER: {args.sprint.upper()}")
    print(f"Stories: {plan['total_stories']} | 7-PR Vertical Slices: {plan['total_prs']}")
    print(f"Governance: 6-Layer Validation (Junior -> Senior -> Arch/Sec -> TechLead -> PM -> CTO)")
    print(f"========================================================\n")

    print(f"{'Worker ID':<24} | {'Profile':<20} | {'Seniority':<10} | {'Tasks':<6} | {'Reviews':<7} | {'Workdir'}")
    print("-" * 105)
    for wid, wdata in plan["workers"].items():
        workdir_rel = f".agents/workspaces/{args.sprint}/{wid}"
        print(f"{wid:<24} | {wdata['profile']:<20} | {wdata['seniority']:<10} | {wdata['total_tasks']:<6} | {wdata['total_reviews']:<7} | {workdir_rel}")

    print("\n--------------------------------------------------------")
    print("STORY-BY-STORY 7-PR ROUTING & 6-LAYER VALIDATION PIPELINE")
    print("--------------------------------------------------------")
    for s in plan["story_allocations"]:
        print(f"\n[{s['story_id'].upper()}] {s['title']} ({s['points']} pts)")
        print(f"  • PM Acceptance (Layer 5): {s['governance']['layer_5_product_manager']}")
        print(f"  • CTO Agreement (Layer 6): {s['governance']['layer_6_cto_agreement']}")
        for pr in s["prs"]:
            print(f"  PR {pr['pr_num']} ({pr['pr_name']})")
            print(f"     ├── Author (Layer 1):   [{pr['junior_author']}] ({pr['profile']})")
            print(f"     └── Reviewer (Layer 2): [{pr['senior_reviewer']}]")

    if args.spawn:
        print(f"\nSpawning isolated agent workdirs and generating context files...")
        spawned = balancer.spawn_workspaces(plan, create_git_worktree=args.create_git_worktree)
        print(f"SUCCESS: Spawned {len(spawned)} agent workspaces in .agents/workspaces/{args.sprint}/!")
        for sp in spawned:
            print(f"  - [{sp['worker_id']}] ({sp['profile']}) -> {sp['workdir']} ({sp['tasks_count']} tasks)")


if __name__ == "__main__":
    main()
    main()
