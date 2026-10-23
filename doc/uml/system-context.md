# System Context

- Authoritative source: [system-context.puml](system-context.puml)
- Related requirements: `REQ-001`-`REQ-021`, `REQ-109`, `REQ-112`

The co-pilot is an agent-assist system. Customers communicate with support agents, not directly with the co-pilot. Approved public pages and an optional live provider sit outside the trusted local boundary. Only minimized provider requests and redacted measurements may cross their respective boundaries.

The system does not execute transactions, transmit replies automatically, provide trading advice, or decide complaint, KYC, or AML outcomes.
