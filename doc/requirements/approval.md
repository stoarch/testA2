# Requirements Baseline Approval

- Baseline: Retail forex/CFD support-ticket co-pilot
- Source: [`../master-prompt.md`](../master-prompt.md), with [`../task-desc.md`](../task-desc.md) as the original product brief
- Prepared: 2026-10-23
- Decision: Accepted as WBS planning baseline
- Authority: Project requester instruction to use `master-prompt.md` and fix architecture/documentation against it
- Named operational owner: TBD before production

## Review checklist

- [x] Required classification fields are specified.
- [x] Grounded drafting, citations, abstention, and human routing are specified.
- [x] Trading-advice, complaint, KYC, and AML hard rules are preserved.
- [x] KB gaps, overlaps, and inconsistencies affect acceptance behavior.
- [x] Phase 1 timebox/UI/provider constraints are preserved.
- [x] Phase 2 volume and KB/SOP growth are covered.
- [x] BDD scenarios and verification layers are mapped.
- [x] The one-page business-case inputs, equations, and decision rule are defined.
- [x] Unknown operational values remain explicit questions rather than invented targets.
- [x] Prompt injection, invalid input, unsupported language, PII-safe logging, and deterministic pre/post gates are specified.
- [x] Offline synthetic fixtures, rules-only execution, and live-provider execution are distinguishable.
- [x] The evaluation minimum is at least 30 labeled tickets with zero critical violations targeted on that set.

This approval closes WBS-002 as a requirements-definition work package. It does not authorize autonomous customer messaging or production handling of customer data.

