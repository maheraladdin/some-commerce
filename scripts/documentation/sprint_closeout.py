#!/usr/bin/env python3
"""Render/check required sprint closeout documentation; does not execute application tests."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import argparse
import re

ROOT = Path(__file__).resolve().parents[2]
HEADING = '## End-of-Sprint Test Gate'
# Concrete targets selected from each sprint's accepted scope. Carry forward existing suites.
TARGETS = {
 'sprint-1.1': (
  'OTP verification, JWT authorization, SDUI cache/304 reads and scoped faceted search; measure cold/warm latency and cache memory.',
  'Sign-in → scoped storefront/search → profile update; verify tenant/user isolation, lost invalidation and account switching.',
  'Phone/locale inputs, JWT claims, SDUI block decoding, taxonomy paths and nested search filters.',
  'Rust cache publish/invalidate ordering, request coalescing and identity/config snapshot publication; assert no mismatched payload/version or stale privilege acceptance.'),
 'sprint-1.2': (
  'Cart sync, checkout allocation/reservation, webhook ingestion and carrier booking dispatch under retry load.',
  'Offline cart → checkout → prepaid/full-COD/deposit-COD → shipment/tracking; race late payment with expiry and reconcile side-effect counts.',
  'Cart mutations, address payloads, money/deposit boundaries, payment/carrier webhook decoders and duplicate/reordered event sequences.',
  'Rust in-process reservation/payment transition guards and duplicate-dispatch coordination; assert one local winner and safe cancellation. Prove database atomicity separately in integration tests.'),
 'sprint-2.1': (
  'Digital checksum/streaming memory, license signature verification, property/variant resolution and entitlement checks.',
  'Upload/quarantine → confirmed purchase → authorized download/license issuance → offline activation/CRL/CEK flow; check expiry and tampering.',
  'License/QR/CRL parsers, property definitions, variant combinations, multipart metadata and checksum error paths.',
  'Rust key/CRL snapshot rotation and activation cache coordination; no partial publication or stale-key acceptance beyond policy.'),
 'sprint-2.2': (
  'Rust/TypeScript SDK verification, release entitlement comparison, vault rendering and wishlist sync with representative datasets.',
  'Cross-SDK golden vectors → vault/QR → release gating → revocation update; include lost push, offline reconnect and notification preferences.',
  'Versioned certificates, release timestamps, malformed QR inputs, revocation lists and wishlist/preference mutation sequences.',
  'Rust entitlement/revocation snapshot publication and concurrent activation/revocation; consumers observe coherent versions. Non-Rust SDK behavior needs its own runtime tests.'),
 'sprint-3.1': (
  'Tier/MOQ pricing, organization-scoped facets, bounded parallel carrier quotes and customer tool execution.',
  'B2B registration/approval → scoped prices/facets → MOQ cart/checkout → cross-border quote/invoice; include customer assistant and address reuse.',
  'Tier boundaries, discount rounding, MOQ/filter expressions, customs/address fields and untrusted assistant tool arguments.',
  'Rust organization/price-list snapshot refresh, parallel quote result aggregation and cancellation; isolate tenant/org results and prevent stale response overwrite.'),
 'sprint-3.2': (
  'RFQ transitions, credit checks, LAN seat checkout/release, aggregation quotes and paginated order history.',
  'RFQ → counter-offer → PO approval → net-terms/reminders using controlled time; proxy lease/seat recovery and carrier fallback without duplicate booking.',
  'RFQ/PO revisions, invoice/lease formats, seat commands, pagination cursors and malformed copilot tool payloads.',
  'Rust final-seat checkout/release/expiry and workflow wake-up ownership; no double issue, negative seats or lost wake-up. Distributed credit/timer races remain integration tests.'),
 'sprint-4.1': (
  'Multi-vendor grouping/splitting, fee/deposit allocation, gateway secret lookup and shared MCP schema/dispatch overhead.',
  'Vendor approval → scoped catalog → grouped checkout/sub-orders; gateway rotation and web/mobile tool dispatch under tenant/vendor isolation.',
  'Vendor IDs, sub-order allocation boundaries, credential/config request schemas and MCP tool names/arguments/confirmation tokens.',
  'Rust credential rotation/cache reads, concurrent split coordination and MCP confirmation consumption; no mixed secret versions or repeated local mutation.'),
 'sprint-4.2': (
  'Balanced ledger postings, payout reservation, partial refunds, portal projections and payment reconciliation.',
  'Delivery/remittance → escrow → RMA freeze/refund or payout; race release/payout/return and crypto settlement while verifying balanced journal and no duplicate transfer.',
  'Ledger amounts/currency/rounding, return quantities, payout requests, BTCPay event decoders and bulk admin transitions.',
  'Rust payout/RMA/release coordination and ledger projection publication; no local double-spend or torn snapshot. Provider transfers and persisted journal races require integration tests.'),
 'sprint-5.1': (
  'Infrastructure synthesis, fresh deploy/upgrade/restore duration, usage aggregation and metering batch throughput/cost estimates.',
  'Fresh-account deployment → onboarding/subscription → usage → accepted metering records; test partial batch failure, entitlement change, rollback and retained-data restore.',
  'Deployment context, tenant/subscriber/dimension IDs, usage boundaries, billing batch responses and malformed subscription events.',
  'Rust metering accumulator snapshot/flush/retry coordination; no lost/double-flushed local usage. AWS/IaC and cross-process semantics require deployed or isolated integration evidence.'),
 'sprint-6.1': (
  'SDUI validation/rendering, large layout editing/publish, cache freshness and edition cutover under an approved load profile.',
  'Studio draft → preview → approved publish → runtime render → version rollback; concurrent edits, stale caches, copilot approval and failed edition cutover.',
  'SDUI AST nesting/size, unsafe URLs/props, layout versions, publish payloads and infrastructure mode requests.',
  'Rust layout/version publication, invalidation and runtime/config snapshot swapping; consumers see a consistent published version during cutover.'),
 'sprint-6.2': (
  'White-label job enqueue/status/artifact retrieval, client startup/bundle metrics and full purchase-flow performance regression.',
  'Brand config → isolated build → authorized signed artifact; replay callbacks, partial platform failure, launch/onboarding and complete auth-to-payout journey.',
  'Brand assets/metadata, build dispatch inputs, status callbacks, artifact paths and existing API/license/protocol corpus regressions.',
  'Changed Rust job-status/cache/callback coordination plus all previously introduced models; do not invent a Rust model for TypeScript or hosted build service behavior.'),
 'sprint-6.3': (
  'Full platform cold/warm capacity, search/checkout p95/p99, memory, queue age, cache hit rate and resource cost on the agreed launch workload.',
  'All accepted stories across web/iOS/Android plus backup/restore, canary rollback, dependency failure, controller restart and complete junior-to-CTO handoffs.',
  'All maintained security/protocol fuzz targets and saved regressions; extend high-risk auth/payment/license/sync inputs and stateful event-sequence targets.',
  'All maintained Rust Loom models with approved launch bounds, including cache/config, reservation, seat, payout, metering and queue coordination; reject any incomplete exploration.'),
}


def render(sprint_id):
    benchmark, integration, fuzz, loom = TARGETS[sprint_id]
    return f'''{HEADING}

**Status: Pending — required closeout evidence, not executed test results.** Run this suite at the end of {sprint_id}, on the exact integration/release candidate, before SG4 and CTO review. Earlier story checks remain mandatory. Follow the [sprint closeout policy](../SPRINT_TESTING.md) and attach the [evidence record](../validation/SPRINT_TEST_EVIDENCE_TEMPLATE.md).

- [ ] **E1 — Benchmark tests:** {benchmark}
- [ ] **E2 — Integration tests:** {integration}
- [ ] **E3 — Fuzz tests:** {fuzz}
- [ ] **E4 — Loom concurrency tests:** {loom}
- [ ] **E5 — Independent closeout review:** QA lead records actual test/target/model counts, candidate and baseline commits, tool/environment versions, performance thresholds/results, corpus/reproducers, Loom bounds/completion and independent reviewer decisions. Missing targets, crashes, regressions, unexplored bounds or unreviewed N/A block acceptance; repairing the candidate invalidates affected results.

At SG0, assign test authors and independent senior QA/security/architecture reviewers; approve workload, benchmark baseline/regression thresholds, fuzz time/memory/input budgets and Loom model bounds. Carry forward affected regression suites. E4 is mandatory for applicable changed or affected Rust shared-state synchronization; only the scope-based N/A procedure in the policy can exclude it, with architecture + QA approval and alternative concurrency evidence. A missing implementation/harness is Pending, never N/A or Pass. Keep this section last, including after sprint-plan regeneration.
'''


def append_closeout(content, sprint_id):
    # Replace the generated footer without discarding earlier authored sprint content.
    content = content.split(HEADING, 1)[0].rstrip()
    return content + '\n\n' + render(sprint_id)


def validate_sprint(content, sprint_id):
    errors = []
    if content.count(HEADING) != 1:
        return [f'{sprint_id}: expected exactly one end-of-sprint gate']
    footer = content.split(HEADING, 1)[1]
    if re.search(r'^## ', footer, re.M):
        errors.append(f'{sprint_id}: closeout gate must be the last section')
    for number, label in enumerate(('Benchmark tests', 'Integration tests', 'Fuzz tests', 'Loom concurrency tests', 'Independent closeout review'), 1):
        if not re.search(rf'^- \[[ x]\] \*\*E{number} — {label}:\*\* .+', footer, re.M):
            errors.append(f'{sprint_id}: missing E{number} {label}')
    for text in ('../SPRINT_TESTING.md', '../validation/SPRINT_TEST_EVIDENCE_TEMPLATE.md', 'At SG0', 'exact integration/release candidate'):
        if text not in footer:
            errors.append(f'{sprint_id}: missing closeout requirement {text}')
    for target in TARGETS[sprint_id]:
        if target not in footer:
            errors.append(f'{sprint_id}: missing sprint-specific test target')
    return errors


def check_all(root=ROOT):
    directory = root / 'docs/sprints'
    paths = {p.stem: p for p in directory.glob('sprint-*.md')}
    errors = []
    if set(paths) != set(TARGETS):
        errors.append('Sprint files must match the 12 closeout target specifications')
    for sprint_id in sorted(set(paths) & set(TARGETS)):
        errors.extend(validate_sprint(paths[sprint_id].read_text(), sprint_id))
    for path in ('docs/SPRINT_TESTING.md', 'docs/validation/SPRINT_TEST_EVIDENCE_TEMPLATE.md'):
        if not (root / path).is_file():
            errors.append(f'Missing closeout policy/evidence file: {path}')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='Append/refresh closeout sections only')
    args = parser.parse_args()
    if args.write:
        for sprint_id in TARGETS:
            path = ROOT / 'docs/sprints' / (sprint_id + '.md')
            path.write_text(append_closeout(path.read_text(), sprint_id))
    errors = check_all()
    if errors:
        raise SystemExit('\n'.join(errors))
    print('SPRINT CLOSEOUT DOCS PASSED: all 12 sprints contain benchmark, integration, fuzz and Loom gates; execution remains pending.')


if __name__ == '__main__':
    main()
