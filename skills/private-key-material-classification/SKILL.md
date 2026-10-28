---
name: private-key-material-classification
description: "Recognise private key blocks and their variants, and separate a live key from an expired or test one, since key material in a file is a different class from any token. Use when a candidate resembles a private key block, a key header, or an encoded key blob"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [classify, keys, cryptography]
---

# Private Key Material Classification

> Recognise private key blocks and their variants, and separate a live key from an expired or test one, since key material in a file is a different class from any token

**Use when:** a candidate resembles a private key block, a key header, or an encoded key blob

**Avoid when:** the corpus contains no key material and no key-like blocks

## Procedure

1. Identify the key type from its header or encoding: signing key, transport key, or an encrypted variant.
2. Record the file, the block boundaries and whether the material is passphrase protected.
3. Look for companion material nearby: certificates, fingerprints or configuration naming the key's purpose.
4. Determine from local evidence whether the key is a test fixture, an expired one, or appears current, without contacting any service.
5. Note whether the block appears in tracked history as well as in the working tree.
6. Classify as secret and record the intended rotation target, which for a key also includes every certificate that trusts it.

## Signals

- A key block sits in a tracked file with no passphrase protection
- A companion certificate in the same tree names the key's purpose
- The key appears in a fixtures directory but lacks a synthetic marker
- History holds the key after it was deleted from the working tree

## Patterns

**1. Key record**

```text
type: private key block | protected: no | purpose hint: tls client auth (from companion cert) | tracked: yes | history: yes
```

**2. Rotation target**

```text
for a key, the target is not one file: it is every trust anchor, certificate and configuration that references it, listed next to the finding
```

**3. Local-only check**

```text
fixture, expired or current is judged from local files and dates only; no service is contacted to confirm
```

## Pitfalls

- Publishing the key block in a report or ticket, which re-creates the exposure permanently
- Rotating the key while leaving the certificates that trust it untouched
- Assuming a key in a fixtures directory is synthetic because of where it lives

## Done when

- Each key finding records type, protection, purpose hint, tracked status and history presence
- The rotation target list names every trust anchor alongside the key itself

## References

- [NIST SP 800-57 - Key management](https://csrc.nist.gov/pubs/sp/800/57/r5/final)
- [CWE-321 - Use of hard-coded cryptographic key](https://cwe.mitre.org/data/definitions/321.html)
