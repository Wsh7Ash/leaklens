---
name: pre-commit-and-cicd-secret-gate
description: "Put the detection where a value is created, at commit time and in the pipeline, because an assessment finds what a gate would have blocked months earlier. Use when values have reached history and nothing currently stops the next one"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [harden, prevention, pipeline]
---

# Pre-Commit and CICd Secret Gate

> Put the detection where a value is created, at commit time and in the pipeline, because an assessment finds what a gate would have blocked months earlier

**Use when:** values have reached history and nothing currently stops the next one

**Avoid when:** a gate already runs at commit and in the pipeline with fixtures proving it works

## Procedure

1. Choose the enforcement points: commit time for the fast feedback, pipeline for the authoritative block.
2. Encode the same rules at both points so a bypassed local hook does not also bypass the pipeline.
3. Plant fixtures in the fixture corpus and require the gate to block each one, proving the gate works.
4. Decide the response on a hit: block the commit, or warn with a required acknowledgement, and record which.
5. Ensure the gate reports a path and a rule, never the value, so the gate's own output is safe to read.
6. Record coverage: which repositories, which pipelines and which remain without a gate.

## Signals

- A local hook exists but the pipeline has no equivalent check
- The gate has never been tested against a planted fixture
- A gate hit prints the value into the console output
- Some repositories remain ungated with no record of that fact

## Patterns

**1. Gate record**

```text
point: pre-commit + pipeline | rules: same version | fixture tested: yes (4 of 4 blocked) | on hit: block | output: path and rule only
```

**2. Fixture proof**

```text
plant each fixture, attempt a commit, require the block; the block message is the evidence the gate works
```

**3. Coverage list**

```text
gated: 12 repositories | ungated: 3, each named; the named list is the work item
```

## Pitfalls

- Installing only a local hook, which any contributor can bypass or forget to install
- Shipping a gate that has never been proven to block anything
- Letting the gate print the value it just caught into a log the whole company can read

## Done when

- Gates run at commit and in the pipeline with the same rules and fixture proof of blocking
- Ungated repositories are named as a list rather than omitted

## References

- [OWASP - CI/CD security guidance](https://owasp.org/www-project-application-security-verification-standard/)
- [CWE-798 - Use of hard-coded credentials](https://cwe.mitre.org/data/definitions/798.html)
