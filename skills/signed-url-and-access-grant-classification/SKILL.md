---
name: signed-url-and-access-grant-classification
description: "Classify time-limited access grants found in files, including their expiry and scope, because an expired grant is hygiene while an unexpired one is a live path to data. Use when the corpus contains signed URLs, presigned requests or expiring access grants"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [classify, signed-urls, access]
---

# Signed URL and Access Grant Classification

> Classify time-limited access grants found in files, including their expiry and scope, because an expired grant is hygiene while an unexpired one is a live path to data

**Use when:** the corpus contains signed URLs, presigned requests or expiring access grants

**Avoid when:** no signed or time-limited access artifacts exist in any readable tree

## Procedure

1. Identify the grant type: a signed object request, an expiring link or a bearer-style access parameter.
2. Decode the visible parameters locally to read expiry, scope and resource, without ever fetching the URL.
3. Record the resource the grant addresses, the expiry time and the file that contains it.
4. Compute whether the grant is still valid relative to the assessment date and record that verdict.
5. Check whether the grant appears in a tracked or published file, since a published unexpired grant is the urgent case.
6. Classify by validity and reach, and state that the URL was never requested.

## Signals

- A presigned URL with a future expiry sits in a tracked file
- The same grant appears in a document published outside the organization
- A grant addresses a resource more sensitive than the file's purpose suggests
- Expiry is far enough ahead that the grant will outlive the assessment

## Patterns

**1. Grant record**

```text
type: presigned object request | resource: export bucket path | expiry: 2026-11-01 (valid at assessment date) | file: notes.md | published: yes
```

**2. Validity verdict**

```text
valid | expired | no-expiry; each verdict recorded with the date the assessment ran, since validity is time-dependent
```

**3. Never-requested statement**

```text
the report states the URL was never fetched, and the evidence is the decoded parameters alone
```

## Pitfalls

- Fetching the URL to see what it exposes, which uses the grant you were assessing
- Reporting an expired grant as a live access path
- Recording validity without the assessment date, which makes the claim stale immediately

## Done when

- Each grant records type, resource, expiry, validity verdict and publication state
- The report states the URL was never requested

## References

- [AWS - Presigned URL security considerations](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ShareObjectPreSignedURL.html)
- [CWE-639 - Authorization bypass through user-controlled key](https://cwe.mitre.org/data/definitions/639.html)
