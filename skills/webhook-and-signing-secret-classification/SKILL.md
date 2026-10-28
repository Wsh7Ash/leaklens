---
name: webhook-and-signing-secret-classification
description: "Classify signing secrets by consumer and algorithm, and note that rotating one breaks every partner that has not been told, so the rotation target is wider than the file. Use when a candidate resembles a webhook signing secret or a symmetric verification key"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [classify, webhooks, secrets]
---

# Webhook and Signing Secret Classification

> Classify signing secrets by consumer and algorithm, and note that rotating one breaks every partner that has not been told, so the rotation target is wider than the file

**Use when:** a candidate resembles a webhook signing secret or a symmetric verification key

**Avoid when:** the corpus contains no signing secrets and no webhook configuration

## Procedure

1. Identify the consumer from configuration nearby: which provider or partner signs with this value.
2. Note the algorithm and expected length, since a mismatch usually means the value is something else.
3. Check whether both a live and a test secret appear and whether they are distinguishable by marker.
4. Record the file, whether it is tracked, and any history containing the same value.
5. List the rotation target: every partner that must be notified and every environment holding the value.
6. Classify as secret and attach a rotation cost note, because the partner notification is usually the slow part.

## Signals

- A signing secret sits in tracked configuration with no environment separation
- A live and a test secret appear with no marker distinguishing them
- History holds the same value after it was moved to a store
- No partner notification record exists for a value that partners verify against

## Patterns

**1. Secret record**

```text
consumer: payments provider | algorithm: HMAC-SHA256 | expected length: 32 | live and test distinguished: no | tracked: yes
```

**2. Rotation target list**

```text
targets: partner A, partner B, env prod, env staging, history; each listed because each must be handled separately
```

**3. Cost note**

```text
record that partner notification is the long pole, so the plan schedules it before the technical rotation
```

## Pitfalls

- Rotating the value and breaking partners who were never notified
- Assuming a test secret is harmless because it lives in a test directory
- Missing that history still holds the value after the file was cleaned

## Done when

- Each signing secret records consumer, algorithm, environment separation and history presence
- A rotation target list including partner notification is attached to the finding

## References

- [Stripe - Rotating webhook secrets](https://docs.stripe.com/webhooks#rotate-endpoint-secret)
- [NIST SP 800-57 - Key rotation guidance](https://csrc.nist.gov/pubs/sp/800/57/r5/final)
