# Security

## Secrets
- Store API keys and TLS material in Vault (`infra/vault/vault.hcl`).
- Never commit credentials.

## Governance
- OPA policies in `infra/opa/policies.rego`.
- Enforce least privilege and role-based access via authz service.
