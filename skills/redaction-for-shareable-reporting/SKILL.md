---
name: redaction-for-shareable-reporting
description: "Prepare a version of the report that can go to a wider audience than the working copy, and test that redaction actually holds before sending it. Use when the report will reach an audience wider than the team that produced it"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [document, redaction, handling]
---

# Redaction for Shareable Reporting

> Prepare a version of the report that can go to a wider audience than the working copy, and test that redaction actually holds before sending it

**Use when:** the report will reach an audience wider than the team that produced it

**Avoid when:** the report stays inside the destination and audience agreed during scope

## Procedure

1. Produce two versions: a working copy in the agreed destination and a shareable copy for the wider audience.
2. Apply redaction by removing values and replacing identifiers with stable labels that still allow tracking.
3. Re-run detection over the shareable copy itself, since redaction is a change that can leave something behind.
4. Check for values hiding in included excerpts, pasted context, screenshots and attachments.
5. Record which version went to which audience with the date, so a later reader knows who saw what.
6. Keep the working copy under the retention rule and confirm the shareable copy needs none of the removed detail.

## Signals

- A shareable version was produced but never re-scanned after redaction
- An excerpt or screenshot in the report still shows a value
- Both versions live in the same destination with the same access
- Nobody recorded which audience received which version

## Patterns

**1. Version record**

```text
working copy: internal ticket, audience security+owner | shareable: pdf, audience vendor; redaction re-scan: clean, 2026-10-28
```

**2. Self-scan**

```text
run the same detection over the shareable artifact before sending; a hit there means redaction missed something
```

**3. Label mapping**

```text
values replaced with stable labels like FINDING-004 so the shareable copy still tracks to the working copy without carrying detail
```

## Pitfalls

- Redacting by eye and never re-scanning the result
- Shipping a screenshot that shows the value the text carefully omitted
- Keeping both versions in one place where a wider audience can read the working copy

## Done when

- The shareable copy has been re-scanned after redaction and the result recorded
- Each version has a recorded audience and the audience that received it

## References

- [ISO 27002 - Information sharing controls](https://www.iso.org/standard/75652.html)
- [OWASP - Information disclosure guidance](https://owasp.org/www-project-web-security-testing-guide/)
