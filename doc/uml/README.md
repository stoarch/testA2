# UML Models

The UML-style views are Markdown files containing Mermaid diagrams. They intentionally use placeholders until `task-desc.md` defines the system actors, responsibilities, integrations, and deployment constraints.

## Views

| Diagram | Purpose | Update when |
|---|---|---|
| [System context](system-context.md) | External actors, system boundary, and integrations | A user type, external dependency, or system responsibility changes |
| [Component overview](component-overview.md) | Major runtime components and dependencies | Component ownership or interfaces change |
| [Primary flow](primary-flow.md) | End-to-end behavior for the main use case | Request order, error behavior, or integration calls change |
| [Deployment](deployment.md) | Runtime nodes and deployment relationships | Hosting, data, network, or operational topology changes |

## Conventions

- Use conservative Mermaid syntax supported by common Markdown renderers.
- Keep element names consistent across views.
- Explain important assumptions outside the diagram instead of hiding them in node labels.
- Add related `REQ-###`, `ADR-####`, and `WBS-###` IDs where useful.

