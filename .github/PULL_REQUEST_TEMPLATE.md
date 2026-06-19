# Pull Request

## Summary

Describe the purpose of this pull request.

```text
Replace this line with a short summary.
```

---

## Change Type

Select the relevant type.

* [ ] Documentation
* [ ] Schema
* [ ] Example
* [ ] Template
* [ ] Diagram
* [ ] Safety model
* [ ] LLM assistance model
* [ ] ATT&CK registry model
* [ ] Telemetry model
* [ ] API proposal
* [ ] Maintenance
* [ ] Other

---

## Files Changed

List the main files changed.

```text
- path/to/file.md
- path/to/schema.json
```

---

## Reason for Change

Explain why this change is needed.

```text
Replace this line with the reason for the change.
```

---

## Safety Review

Confirm the following items before submitting.

* [ ] This pull request is aligned with authorized security work.
* [ ] This pull request does not include unauthorized exploitation instructions.
* [ ] This pull request does not include credential theft procedures.
* [ ] This pull request does not include malware code.
* [ ] This pull request does not include payload delivery workflow.
* [ ] This pull request does not include evasion or bypass instructions.
* [ ] This pull request does not include destructive test instructions.
* [ ] This pull request does not include real client data.
* [ ] This pull request does not include credentials, tokens, private keys, or secrets.
* [ ] Examples use safe placeholder values such as `example.com`, `project-001`, or `asset-001`.

---

## Documentation Review

* [ ] Markdown renders correctly.
* [ ] Headings are clear.
* [ ] Tables are readable.
* [ ] Code blocks are formatted correctly.
* [ ] Links are valid.
* [ ] Terminology matches `docs/glossary.md`.
* [ ] Related documents are updated when needed.

---

## Schema Review

Complete this section if the pull request changes files in `schemas/`.

* [ ] Required fields are defined.
* [ ] Enum values are documented.
* [ ] Example data is valid.
* [ ] Sensitive fields are identified.
* [ ] Schema names match the data model.
* [ ] Related examples are updated.

---

## LLM Assistance Review

Complete this section if the pull request changes LLM-related workflow.

* [ ] LLM-supported tasks are clearly defined.
* [ ] LLM-restricted tasks are clearly defined.
* [ ] LLM output requires review before acceptance.
* [ ] LLM output does not bypass scope, approval, or policy.
* [ ] Prompt examples do not request unsafe output.
* [ ] Sensitive data handling is documented.

---

## ATT&CK Mapping Review

Complete this section if the pull request changes ATT&CK-related content.

* [ ] ATT&CK IDs are valid.
* [ ] Domain is stated when relevant.
* [ ] Deprecated or revoked handling is considered.
* [ ] Content version handling is considered.
* [ ] Campaign, finding, or telemetry mapping is reviewable.

---

## Telemetry Review

Complete this section if the pull request changes telemetry-related content.

* [ ] Expected telemetry is defined.
* [ ] Observed telemetry is documented.
* [ ] Detection status values are consistent.
* [ ] Evidence relationship is considered.
* [ ] Detection gap language is clear.

---

## Related Issue

Link the related issue if available.

```text
Closes #
```

---

## Reviewer Notes

Add anything reviewers should pay attention to.

```text
Replace this line with reviewer notes, or write "None".
```
