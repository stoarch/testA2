# Knowledge-Base Sources and Assessment

## Approved sources

| ID | Page | URL | Primary coverage |
|---|---|---|---|
| KB-001 | How to Deposit | https://valetax.com/how-to-deposit/ | Deposit steps and deposit/withdrawal FAQ |
| KB-002 | How to Withdraw | https://valetax.com/how-to-withdraw/ | Withdrawal steps and duplicated deposit/withdrawal FAQ |
| KB-003 | How to Open an Account | https://valetax.com/how-to-open-an-account/ | Registration, documents, timing, account questions |
| KB-004 | How to Verify Account | https://valetax.com/how-to-verify-account/ | Short KYC-profile upload/review flow |

The prototype must use these pages as they are. Each snapshot records capture time, content hash, source URL/title, section headings, and exact passages because live content can change. Offline synthetic fixtures use separate identifiers and an explicit `synthetic: true` marker.

## Implementation status

The current repository implements JSON persistence, SHA-256 integrity validation, the exact four-URL allowlist, section-level lexical retrieval, complete retrieved-passage provenance for an explicitly synthetic fixture, and exact numeric-duration validation against cited passages. Live page fetching, refresh scheduling, and production source snapshots remain planned.

## Known gaps, overlaps, and inconsistencies

| ID | Observation | Required system behavior |
|---|---|---|
| KBI-001 | Deposit and withdrawal pages repeat the same FAQ content. | Deduplicate retrieval evidence without losing source provenance. |
| KBI-002 | The withdrawal page step 3 says to enter the amount “to deposit,” and step 4 says “Start Trading.” | Do not repeat misleading wording as withdrawal instruction; abstain from the disputed step or route for review. |
| KBI-003 | The withdrawal page markets withdrawals as “easy and instant,” while its FAQ describes pending approval and tells customers to contact support after 24 hours. | Cite the precise supporting passage; do not generalize “instant” into a guaranteed timeline. |
| KBI-004 | The verification page describes only completing fields, uploading required documents, review, and completion; it omits detailed document rules and timing. | Abstain on missing verification details and route to a person. |
| KBI-005 | The account-opening page mentions documents not older than six months and a 48-hour opening/verification timeline. | These claims may be used only with direct citations and should not be expanded beyond the page. |
| KBI-006 | The account-opening page discusses leverage based on strategy/goals and advertises leverage up to 1:2000. | The co-pilot must not turn this into personalized leverage guidance; apply REQ-007. |
| KBI-007 | Site disclaimers say applicable legal entities and documents depend on onboarding. | Do not infer entity-specific policy; route entity-specific uncertainty for review. |
| KBI-008 | Page copy contains typos and marketing language. | Prefer neutral paraphrase while preserving factual meaning; never “correct” policy by inference. |

## Retrieval and citation contract

- Store source ID, title, URL, retrieval timestamp, section heading, and passage text for every chunk.
- Store snapshot ID and content hash for each source document.
- A citation must resolve to the source page and identify the supporting passage/chunk.
- Retrieval confidence alone cannot authorize an answer; claim support and safety checks are separate gates.
- Conflicting evidence triggers abstention/review rather than automatic source ranking unless a later ADR defines authority precedence.
- Retrieved instructions are untrusted content and cannot alter policy, tool access, routing, or output contracts.
- If live snapshot creation fails, only explicitly labeled synthetic fixtures may be used for an offline demo.

