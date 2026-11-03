#!/usr/bin/env python3
"""
Splits all monolithic user-stories module README.md files into:
1. Individual user story files: docs/user-stories/<module>/us-<id>-<slug>.md
2. Clean catalog README.md files for each module.
"""

import os
import re

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

BASE_DIR = 'docs/user-stories'

MODULE_SPRINT_MAP = {
    '01-auth-and-onboarding': 'Sprint 1.1',
    '02-storefront-and-catalog': 'Sprint 1.1',
    '03-cart-and-checkout': 'Sprint 1.2',
    '04-payments-and-cod': 'Sprint 1.2 / 4.2',
    '05-fulfillment-and-shipping': 'Sprint 1.2 / 3.1 / 4.1',
    '06-orders-and-returns': 'Sprint 1.2 / 4.2',
    '07-customer-account': 'Sprint 1.1',
    '08-webmcp-and-ai': 'Sprint 1.1',
    '09-digital-products-and-licensing': 'Sprint 2.1 / 2.2',
    '10-b2b-wholesale': 'Sprint 3.1 / 3.2',
    '11-multi-vendor-marketplace': 'Sprint 4.1 / 4.2',
    '12-admin-and-sdui-studio': 'Sprint 5.1 / 6.1 / 6.2',
    '13-deployment-and-aws-marketplace': 'Sprint 5.1',
}

modules = sorted([d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d))])

total_stories_created = 0

for m in modules:
    readme_path = os.path.join(BASE_DIR, m, 'README.md')
    if not os.path.exists(readme_path):
        continue
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parts = re.split(r'\n(?=## US-[\d\.]+)', content)
    header = parts[0].strip()
    # Strip trailing divider if present
    if header.endswith('---'):
        header = header[:-3].strip()
    
    stories_raw = parts[1:]
    catalog_entries = []
    
    # Extract Module title from header
    mod_title_match = re.search(r'^#\s+([^\n]+)', header, re.MULTILINE)
    mod_title = mod_title_match.group(1) if mod_title_match else m
    default_sprint = MODULE_SPRINT_MAP.get(m, 'Sprint 1.1')
    
    for s in stories_raw:
        lines = s.strip().split('\n')
        title_line = lines[0]
        
        # Parse ## US-X.Y.Z: Title
        m_id = re.search(r'##\s+(US-[\d\.]+):?\s*(.*)', title_line)
        if not m_id:
            continue
        
        story_id = m_id.group(1)
        story_title = m_id.group(2).strip()
        slug = f"{story_id.lower()}-{slugify(story_title)}.md"
        
        # Extract narrative (As a ... I want to ... So that ...)
        story_body = '\n'.join(lines[1:]).strip()
        
        # Extract persona
        persona_match = re.search(r'\*\*As an?\*\*\s+([^,\n]+)', story_body)
        persona = persona_match.group(1).strip() if persona_match else 'User / Shopper'
        
        # Extract summary sentence from "I want to ..."
        want_match = re.search(r'\*\*I want to\*\*\s+([^,\n]+)', story_body)
        want_summary = want_match.group(1).strip() if want_match else story_title
        
        catalog_entries.append({
            'id': story_id,
            'title': story_title,
            'persona': persona,
            'summary': want_summary,
            'filename': slug,
            'sprint': default_sprint
        })
        
        # Build individual story markdown content
        # Clean up any trailing '---' from story_body
        clean_story_body = story_body
        if clean_story_body.endswith('---'):
            clean_story_body = clean_story_body[:-3].strip()
        
        # Ensure section headers inside story use ## instead of ### if they were top-level within story
        # Specifically: ### Acceptance Criteria -> ## Acceptance Criteria
        # ### Test Cases -> ## Test Cases
        # ### Activity Diagram -> ## Activity Diagram
        formatted_body = re.sub(r'^###\s+(Acceptance Criteria|Test Cases|Activity Diagram)', r'## \1', clean_story_body, flags=re.MULTILINE)
        
        story_content = f"""# {story_id}: {story_title}

> **Module**: [{mod_title}](README.md)  
> **Master User Stories Index**: [User Stories Master Catalog](../README.md)  
> **Execution Sprint**: {default_sprint}  
> **Slicing Standard**: [7-PR Vertical Slicing Framework](../../sprints/README.md#the-7-pr-vertical-slicing-standard)

---

## User Story Narrative

{formatted_body}

---

## Sliced Implementation Blueprint (7 PRs)

Every user story in `some-commerce` is implemented across 7 sequential pull requests by autonomous AI agents:

1. **PR 1: Microkernel Logic (`crates/kernel-core`)** — Domain contracts, trait interfaces, error enums, and pure business logic with zero external AWS/database dependencies.
2. **PR 2: Database Schema (`crates/db-schema`)** — DynamoDB single-table entity definitions (`PK`, `SK`, `GSI1`–`GSI5`), serde attributes, and validation rules.
3. **PR 3: Repository Handlers & Multi-Tier Caching (`crates/db-dynamo`, `crates/cache-tier`)** — Data access methods, L1 Moka in-memory cache, L2 ElastiCache Redis distributed cache, and BLAKE3 ETag computation.
4. **PR 4: Axum API Handlers & HTTP Middleware (`bins/...`)** — REST endpoints, JWT validation, request/response validation schemas, and OpenAPI/WebMCP route registration.
5. **PR 5: Client Services & Local-First Database (`packages/api-client`, `packages/db-client`)** — Axios client endpoints, WatermelonDB SQLite schema, models, and sync synchronization handlers.
6. **PR 6: Headless Domain Hooks & Native Modules (`packages/domain-hooks`, `modules/...`)** — Headless React hooks (`use...`), state management, TanStack Query cache integration, and native platform bridges.
7. **PR 7: Platform-Adaptive UI (`apps/storefront-mobile`, `apps/storefront-web`)** — Native `@expo/ui` on iOS/Android, Semantic HTML5 + Tailwind CSS v4 on Web, with bidirectional RTL/LTR mirroring.

---

[← Back to {mod_title} Catalog (README.md)](README.md) | [Master User Stories Index](../README.md)
"""
        story_file_path = os.path.join(BASE_DIR, m, slug)
        with open(story_file_path, 'w', encoding='utf-8') as sf:
            sf.write(story_content)
        total_stories_created += 1
    
    # Now generate catalog README.md for the module
    catalog_table_rows = []
    for entry in catalog_entries:
        catalog_table_rows.append(
            f"| **[{entry['id']}]({entry['filename']})** | {entry['title']} | {entry['persona']} | {entry['sprint']} | [View Specification →]({entry['filename']}) |"
        )
    catalog_table = "\n".join(catalog_table_rows)
    
    summaries_list = []
    for entry in catalog_entries:
        summaries_list.append(
            f"#### [{entry['id']}: {entry['title']}]({entry['filename']})\n"
            f"- **Target Persona**: {entry['persona']}\n"
            f"- **Summary**: {entry['summary']}\n"
            f"- **Specification**: [`{entry['filename']}`]({entry['filename']})\n"
        )
    summaries_md = "\n".join(summaries_list)
    
    catalog_readme = f"""{header}

---

## User Stories Catalog

This module contains **{len(catalog_entries)} detailed user stories**. Each user story has its own dedicated specification document containing Gherkin acceptance criteria (`Given/When/Then`), comprehensive test matrices (happy path, edge cases, error handling, security, and concurrency), Mermaid activity diagrams, and the 7-PR implementation slice plan.

| Story ID | Title | Target Persona | Sprint | Specification Document |
| :--- | :--- | :--- | :--- | :--- |
{catalog_table}

---

## Story Summaries

{summaries_md}

---

## Autonomous Agent Implementation Standard

Every user story in this module is executed by an autonomous AI agent across the standardized **7-PR vertical slice framework**:

```
[PR 1: Kernel Core] ──> [PR 2: DB Schema] ──> [PR 3: Repo & Cache] ──> [PR 4: Axum API]
                                                                            │
[PR 7: Platform UI] <── [PR 6: Headless Hooks] <── [PR 5: Client Service & DB] <┘
```

1. **PR 1: Microkernel Logic** (`crates/kernel-core`)
2. **PR 2: Database Schema** (`crates/db-schema`)
3. **PR 3: Repository Handlers & Caching** (`crates/db-dynamo`, `crates/cache-tier`)
4. **PR 4: Axum Handlers & Middleware** (`bins/...`)
5. **PR 5: Client Services & Local Database** (`packages/api-client`, `packages/db-client`)
6. **PR 6: Headless Domain Hooks & Native Modules** (`packages/domain-hooks`, `modules/...`)
7. **PR 7: Platform-Adaptive UI** (`apps/storefront-mobile` with `@expo/ui`, `apps/storefront-web` with Tailwind CSS v4)

---

## Navigation & Cross-References

- [← Back to Master User Stories Index](../README.md)
- [Sprint Schedule & 3-Agent Parallel Framework](../../sprints/README.md)
- [System Architecture & Multi-Tier Caching](../../SYSTEM_ARCHITECTURE.md)
- [Deployment & AWS Marketplace Guide](../../DEPLOYMENT_AND_AWS_MARKETPLACE.md)
"""

    with open(readme_path, 'w', encoding='utf-8') as rf:
        rf.write(catalog_readme)
    
    print(f"Processed {m}: created {len(catalog_entries)} stories, updated README.md")

print(f"\nAll done! Total stories created: {total_stories_created}")
