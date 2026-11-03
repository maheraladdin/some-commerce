# Canonical user story records

Create **one file per story**, named `US-<id>.md` (for example `US-1.1.1.md`), from the [story record template](../STORY_RECORD_TEMPLATE.md) when that story enters planning. This directory is the review location for each story's complete operational history and current handoff snapshot. No execution history has been initialized here yet; do not infer completed actions from specifications.

Every company role reads and acknowledges the same record, records each action intent/result and decision through the controller, links artifacts, and updates the snapshot before transfer. Include the master-plan/parent node, candidate revision, failures/findings/fixes, blockers, next action and next-role acknowledgment. Preserve history with linked correction events. Attach story/sprint evidence to this record instead of creating competing authoritative role logs.

The trusted controller must serialize authenticated, idempotent events and reconcile gaps or unknown outcomes before promotion/retry. An editable Markdown file alone does not enforce append-only storage. The production collector and event-backed projection remain runtime implementation requirements; this directory and template define the required location and format.
