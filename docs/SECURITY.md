# 🔒 Security & Data Protection Policy
## Grupo Aylesva — E-Commerce & Web Infrastructure

---

## 1. Security Architecture Principles

This project adheres to enterprise web security best practices, including OWASP Top 10 guidelines for web applications and Shopify Theme Security standards:

### 1.1 Credential & Secret Management
- **Zero Secrets in Source Control:** Private access tokens (`shpat_`, `shpca_`), API keys, webhooks, and private database credentials must **never** be committed to git.
- **Environment Isolation:** Local configuration files (`.env`) are strictly ignored via `.gitignore`.
- **Sanitized Examples:** Only `.env.example` with dummy values is checked into version control.

### 1.2 Cross-Site Scripting (XSS) Prevention
- All dynamic Liquid outputs rendered from user input or query strings use appropriate Liquid escaping filters:
  - `{{ text | escape }}` for general strings.
  - `{{ text | strip_html }}` for unformatted text.
  - `{{ json_data | json }}` for inline JavaScript variables.

### 1.3 Content Security & Third-Party Integrations
- Third-party forms (e.g. GoHighLevel, New Benefits, Stripe) are integrated via sandboxed `<iframe>` tags or authenticated server-to-server webhook endpoints.
- External links to social media or partner portals strictly enforce `rel="noopener noreferrer"` and `target="_blank"`.

### 1.4 Personal Identifiable Information (PII)
- No customer data, order logs, or customer addresses are stored locally in the theme repository. All transactional data is securely processed through Shopify's PCI-DSS compliant infrastructure.
