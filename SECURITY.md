# Security policy

## Reporting a vulnerability

Open a [private security advisory](https://github.com/earbona23/detection-coverage/security/advisories/new)
on this repository. Please do not open a public issue for a vulnerability.

You will get an acknowledgement within 72 hours and an assessment within seven days. There
is no bounty programme — this is a single-maintainer project — but every report is credited
in the advisory unless you ask me not to.

## What counts as a vulnerability here

`detection-coverage` maps detection rules against MITRE ATT&CK and reports coverage,
gaps, and phantom coverage.

This tool exists to stop a specific self-deception: believing you are covered when you are
not. Its vulnerabilities are the ones that restore that deception.

| Class | Why it matters |
|---|---|
| **Phantom coverage counted as coverage** | A rule citing a revoked or non-existent technique covers nothing. If it is ever counted, the tool is producing exactly the false assurance it was built to expose, and with more authority than a spreadsheet. |
| **A gap reported as covered** | Any defect that turns an uncovered technique green. Someone decides not to write a detection because of that cell. |
| **Catalogue substitution** | The ATT&CK catalogue ships with provenance and a hash. Anything that lets an unverified catalogue be loaded silently undermines every result computed against it. |
| **Rule parsing that executes anything** | Detection rules are input. Parsing YAML or JSON must never evaluate it. |
| **Rule content leaving the machine** | Your detection rules describe what you can and cannot see. That is sensitive to an attacker who obtains it. |

## Out of scope

- Disagreement about whether a given rule *really* covers a technique. That is a mapping
  judgement; open a normal issue.
- Coverage of ATT&CK versions or rule formats not yet supported — a feature request.
