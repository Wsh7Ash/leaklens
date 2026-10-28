---
name: generated-artifact-scan
description: "Scan build output, bundles and archives as first-class content, since generated files commonly carry the very values the source carefully does not. Use when a build, bundle or archive exists inside an in-scope tree and has not been confirmed clean"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [discover, artifacts, build]
---

# Generated Artifact Scan

> Scan build output, bundles and archives as first-class content, since generated files commonly carry the very values the source carefully does not

**Use when:** a build, bundle or archive exists inside an in-scope tree and has not been confirmed clean

**Avoid when:** the owner confirms generated output contains no values and a scan of it proves the claim

## Procedure

1. List the generated regions present: build directories, bundles, source maps, container layers and archives.
2. Confirm whether the tool reads them, and expand or extract the ones it does not when the boundary permits.
3. Scan source maps separately, since they reconstruct original content that may carry values removed from the built file.
4. Check embedded images, fonts and other binaries for appended data, which is rare but cheap to rule out.
5. Record which artifacts were read, extracted or skipped, with a reason for every skip.
6. Feed hits to classification with the region recorded, because an artifact finding usually implies the source once held it too.

## Signals

- Build output is excluded by an ignore rule that predates the current data flows
- Source maps exist for a build whose originals were cleaned
- An archive inside the tree was never expanded
- A value appears in built output but not in the current source

## Patterns

**1. Artifact row**

```text
artifact | type | read | finding
bundle.js | built | yes | none
bundle.js.map | source map | yes | value present, source clean
image.png | binary | skipped, reason: no appended data expected
```

**2. Implied-history rule**

```text
a value in an artifact with clean source implies the source held it once; write that as a history question, not as a separate discovery
```

**3. Skip reason**

```text
every unread artifact carries a written reason so the coverage statement stays honest
```

## Pitfalls

- Accepting an inherited ignore rule for build output without checking what it hides today
- Cleaning the source and declaring the problem solved while the artifact still carries the value
- Scanning binaries by content rules that can never match and calling the region covered

## Done when

- Every generated region has a read, extracted or skipped status with a reason
- At least one artifact region is confirmed scanned or explicitly excluded with justification

## References

- [CWE-527 - Version control and artifact exposure](https://cwe.mitre.org/data/definitions/527.html)
- [OWASP - Build and pipeline security](https://owasp.org/www-project-application-security-verification-standard/)
