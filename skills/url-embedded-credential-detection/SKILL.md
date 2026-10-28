---
name: url-embedded-credential-detection
description: "Find credentials carried inside connection strings, callbacks and repository URLs, a form that survives every value-shape rule because it is hidden inside a structure nobody greps for. Use when the corpus contains URLs, connection strings or remote endpoints of any kind"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [discover, urls, credentials]
---

# URL-Embedded Credential Detection

> Find credentials carried inside connection strings, callbacks and repository URLs, a form that survives every value-shape rule because it is hidden inside a structure nobody greps for

**Use when:** the corpus contains URLs, connection strings or remote endpoints of any kind

**Avoid when:** the corpus is confirmed free of URLs and remote endpoints entirely

## Procedure

1. Extract every URL-shaped token from the corpus, including those inside quotes, connection strings and command lines.
2. Parse each into components and look for user info before the host, which is where embedded credentials live.
3. Record the scheme, the presence of a password component and the target host, never the credential itself.
4. Check whether the URL appears in a tracked file, since that determines whether history removal is also needed.
5. Note URLs that carry a token in a query parameter instead of user info, which is the other common placement.
6. Pass each hit to classification with its placement recorded as userinfo or query.

## Signals

- A connection string embeds a user and password before the host
- A repository remote URL carries a token in place of a password
- A callback URL carries an access token as a query parameter
- An image or webhook URL embeds credentials to authenticate a fetch

## Patterns

**1. Extraction pattern**

```text
scheme://user:password@host -> record scheme, presence of userinfo, host; never store the credential component
```

**2. Query variant**

```text
?access_token=... or ?key=... -> record parameter name and the file that contains it
```

**3. Placement field**

```text
placement: userinfo | query | fragment; each implies a different rotation target and a different log to check
```

## Pitfalls

- Grep-ing for a colon-slash-slash and missing URLs assembled at runtime from parts
- Recording the full URL in the report, which re-publishes the credential it contains
- Fixing the value without noticing that history still holds the original

## Done when

- Every URL-shaped token parsed yields a placement verdict with host recorded and credential omitted
- Whether the URL appears in tracked history is recorded per hit

## References

- [RFC 3986 - URI userinfo component](https://www.rfc-editor.org/rfc/rfc3986)
- [OWASP - Credential exposure guidance](https://owasp.org/www-project-web-security-testing-guide/)
