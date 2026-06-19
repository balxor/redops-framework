# Contributing

Thank you for your interest in contributing to RedOps Framework.

This project is a community draft for an ATT&CK-based framework that supports authorized pentest and red team operations.

Contributions should improve documentation, structure, safety, workflow clarity, data model, schema design, examples, or implementation planning.

---

## Contribution Scope

Accepted contribution areas:

* Documentation improvement
* Product scope clarification
* Safety model improvement
* LLM-assisted workflow design
* ATT&CK registry design
* Data model proposal
* JSON schema proposal
* Example project files
* Report templates
* Finding templates
* Campaign plan templates
* API proposal
* Telemetry model
* Roadmap improvement
* Terminology and glossary improvement

---

## Restricted Contributions

Do not submit content that includes:

* Unauthorized exploitation instructions
* Credential theft procedures
* Malware code
* Payload delivery logic
* EDR or AV bypass procedures
* Phishing delivery workflow
* Destructive test instructions
* Persistence payloads for unauthorized systems
* Real client data
* Private logs
* Credentials, tokens, or private keys
* Internal network data from real environments

Contributions with high misuse risk may be rejected, edited, or moved to a safer abstraction.

---

## Writing Style

Use clear technical English.

Preferred style:

* Direct
* Professional
* Specific
* Practical
* Easy to review
* Easy to maintain

Avoid:

* Marketing language
* Overstatement
* Rhetorical phrasing
* Metaphors
* Gimmicks
* Unsupported claims
* Vague security promises
* Unnecessary offensive detail

Use technical terms as-is when they are standard in security work, such as:

* scope
* engagement
* finding
* evidence
* campaign
* telemetry
* ATT&CK
* red team
* pentest
* detection
* policy gate
* validation workflow

---

## Documentation Rules

Documentation should explain:

1. What the component is.
2. What it does.
3. How it works.
4. Why it is needed, when relevant.
5. What assumptions apply.
6. What limitations exist.

Keep paragraphs short.

Use tables for mappings, statuses, and comparisons.

Use code blocks for structure, schema, command examples, and API examples.

Do not include unnecessary implementation detail when a safer abstraction is enough.

---

## Safety Requirements

All contributions must follow the project safety model.

Required principles:

* Authorized use only
* Scope-bound workflow
* Approval-based sensitive actions
* Target allowlist
* Audit logging
* Evidence integrity
* Lab-first validation
* Human review for LLM-generated plans
* No autonomous offensive execution

Examples should be safe, controlled, and clearly scoped.

---

## LLM-Related Contributions

LLM-related contributions should focus on:

* Planning assistance
* Scope review
* ATT&CK mapping suggestion
* Evidence summary
* Finding draft
* Remediation draft
* Report draft
* Telemetry gap analysis
* Cleanup checklist

LLM contributions must not give the model direct authority to:

* Execute actions without approval
* Expand scope
* Generate unauthorized attack steps
* Generate payloads
* Perform credential theft
* Perform evasion
* Perform destructive actions

LLM output should be validated by:

* Schema validation
* ATT&CK registry validation
* Scope validation
* Policy validation
* Human approval

---

## Issue Guidelines

Before opening an issue:

1. Check existing issues.
2. Use the correct issue template.
3. Keep the issue focused.
4. Include enough detail for review.
5. Avoid sensitive or private data.

Good issue topics:

* Documentation gap
* Unclear wording
* Missing safety control
* Data model improvement
* Schema improvement
* Roadmap suggestion
* Incorrect terminology
* Broken link
* Example improvement

Do not open public issues containing:

* Credentials
* Client data
* Private logs
* Internal IP addresses
* Exploit details
* Payload code
* Evasion details

Use the security contact in `SECURITY.md` for sensitive reports.

---

## Pull Request Guidelines

A pull request should include:

* Clear title
* Short summary
* Reason for the change
* Files changed
* Safety impact, when relevant
* Related issue, when available

Before submitting a pull request:

1. Review the changed files.
2. Remove private or sensitive data.
3. Check Markdown formatting.
4. Keep the change focused.
5. Avoid unrelated edits.
6. Confirm that examples are safe and authorized-use oriented.

---

## Commit Message Style

Use short and clear commit messages.

Examples:

```text
Add safety model draft
Update LLM assistance workflow
Improve ATT&CK registry notes
Add campaign schema draft
Fix roadmap wording
Add finding template
```

Avoid vague messages:

```text
Update files
Fix stuff
Changes
More docs
```

---

## Branch Naming

Suggested branch names:

```text
docs/safety-model
docs/llm-assistance
docs/roadmap-update
schema/campaign
schema/evidence
template/finding
fix/readme-links
```

---

## Review Criteria

Contributions are reviewed based on:

* Technical clarity
* Safety alignment
* Authorized-use boundary
* Documentation quality
* Maintainability
* Consistency with project scope
* Risk of misuse
* Fit with roadmap

A contribution may be rejected if it introduces unnecessary risk or shifts the project away from authorized operations.

---

## Repository Structure

Use the existing structure:

```text
docs/       Detailed documentation
schemas/    JSON schema drafts
examples/   Safe example files
templates/  Reusable document templates
diagrams/   Mermaid diagrams and architecture visuals
.github/    Issue and pull request templates
```

Place content in the most specific folder.

Do not put long technical specifications directly in `README.md` when they belong in `docs/`.

---

## License

By contributing to this project, you agree that your contribution will be licensed under the project license.

See `LICENSE` for details.

---

## Contact

Kenshin Himura
[roxlab.org@gmail.com](mailto:roxlab.org@gmail.com)
