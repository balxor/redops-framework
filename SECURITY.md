# Security Policy

## Purpose

RedOps Framework is intended for authorized security assessment, red team planning, pentest workflow management, purple team activity, detection validation, and security documentation.

The project must be used only within approved scope, approved targets, and approved rules of engagement.

---

## Authorized Use

Accepted use cases:

* Internal security assessment
* Client-approved pentest engagement
* Client-approved red team engagement
* Purple team exercise
* Detection engineering
* Security control validation
* Lab-based validation
* Security documentation and reporting
* ATT&CK-based campaign planning
* Evidence and finding management

---

## Prohibited Use

The project must not be used for:

* Unauthorized access
* Unauthorized scanning
* Unauthorized exploitation
* Credential theft
* Malware deployment
* Payload delivery
* Evasion tooling
* Destructive operations
* Persistence deployment on systems outside approved scope
* Activity against systems without written authorization
* Activity that violates law, policy, contract, or rules of engagement

---

## Security Design Principles

The framework follows these principles:

* Scope-bound operation
* Approval-based workflow
* Target allowlist
* Audit logging
* Evidence integrity
* Role-based access control
* Reversible validation workflow
* Lab-first validation
* Telemetry-based review
* Human approval for sensitive actions

---

## Scope and Approval

A project must define scope before any campaign or validation workflow is planned.

Minimum scope requirements:

* Allowed targets
* Forbidden targets
* Test window
* Rules of engagement
* Emergency contact
* Approval requirement
* Restricted action list

Actions outside approved scope must be rejected.

Actions with elevated risk must require explicit approval.

---

## Restricted Content

The repository should not contain:

* Working exploit chains
* Credential dumping procedures
* EDR or AV bypass procedures
* Malware code
* Persistence payloads for unauthorized use
* Phishing delivery content
* Destructive test procedures
* Instructions for unauthorized access
* Instructions for bypassing monitoring or enforcement controls

Safe examples may be accepted when they are clearly scoped for documentation, lab validation, detection engineering, or controlled workflow design.

---

## LLM-Assisted Workflow

LLM assistance may be used for:

* Scope summary
* ATT&CK mapping suggestion
* Campaign plan draft
* Evidence summary
* Finding draft
* Remediation draft
* Report draft
* Telemetry gap analysis
* Cleanup checklist

LLM output must be reviewed before use.

LLM-generated plans must pass:

* Schema validation
* ATT&CK registry validation
* Scope validation
* Policy validation
* Human approval

LLM output must not be treated as authorization.

---

## Reporting Security Issues

Report security issues privately.

Contact:

```text
Kenshin Himura
roxlab.org@gmail.com
```

Include the following information when possible:

* Affected file or component
* Description of the issue
* Impact
* Reproduction steps, if safe to share
* Suggested fix, if available

Do not include public exploit details in GitHub issues or pull requests.

---

## Public Issue Handling

Do not open public issues containing:

* Exploit instructions
* Sensitive target data
* Credentials
* API keys
* Private logs
* Client data
* Internal network data
* Payload code
* Evasion details

Use private contact for sensitive reports.

---

## Supported Versions

| Version | Status          |
| ------- | --------------- |
| v0.1    | Community draft |

Security review applies to the current draft and future documentation updates.

---

## Disclosure Process

Security reports will be reviewed using the following process:

1. Receive report.
2. Validate the issue.
3. Assess impact.
4. Prepare a fix or documentation update.
5. Credit the reporter when appropriate.
6. Publish the update.

No fixed response time is guaranteed for the community draft phase.

---

## Data Handling

Contributors must not include real client data in this repository.

Do not commit:

* Credentials
* Tokens
* Private keys
* Internal IP lists
* Client reports
* Private screenshots
* Production logs
* SIEM exports containing sensitive data
* EDR exports containing sensitive data
* Cloud account identifiers from real environments

Use sanitized examples only.

---

## Contribution Review

Security-related contributions must be reviewed before merge.

Review focus:

* Authorized use
* Scope boundary
* Safety control
* Data sensitivity
* Abuse potential
* Documentation clarity
* Removal of unnecessary operational detail

Contributions that increase misuse risk may be rejected or moved to a safer abstraction.

---

## License

This security policy applies to RedOps Framework under the project license.
