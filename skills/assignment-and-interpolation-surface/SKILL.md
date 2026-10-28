---
name: assignment-and-interpolation-surface
description: "Find the structural places where a value is bound to a name, because that is where a credential lives even when its format is unfamiliar. Use when scanning source and configuration where the credential format is unknown or self-generated"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [discover, detection, structure]
---

# Assignment and Interpolation Surface

> Find the structural places where a value is bound to a name, because that is where a credential lives even when its format is unfamiliar

**Use when:** scanning source and configuration where the credential format is unknown or self-generated

**Avoid when:** format rules already cover every credential class the corpus can contain

## Procedure

1. List the assignment shapes that bind secrets: direct assignment, environment lookup, connection string, header construction and template interpolation.
2. Search for those shapes by structure and by key name rather than by value shape.
3. Rank by key name, since a variable called password or token is a stronger signal than an arbitrary identifier.
4. Handle indirection, where the value is fetched from a store at runtime and the file only names the key.
5. Record which shapes were searched and which the corpus contains, so coverage is stated rather than implied.
6. Pass survivors to classification alongside the format and entropy candidates.

## Signals

- A value is fetched from a store at runtime and only the name appears in the file
- A connection string assembles credentials from parts rather than storing one literal
- Key-name searching missed a credential because the name is an abbreviation
- Template interpolation hides a value inside a larger string

## Patterns

**1. Shape list**

```text
key = literal | getenv("KEY") | url with user:pass | header with bearer | string template embedding a variable
```

**2. Key-name ranking**

```text
strong names: password, secret, token, api_key, private, credential; weak names: value, data, config, id
```

**3. Indirection note**

```text
when a file only names a store key, record that as a reference finding rather than a value finding, since the value lives elsewhere
```

## Pitfalls

- Reporting a store-key reference as though it were the credential itself
- Missing indirection entirely and concluding the corpus holds no credentials
- Treating every assignment to a weakly named variable as a candidate and burying the real ones

## Done when

- Each assignment shape searched is listed with whether the corpus contains it
- Indirection findings are labelled as references, separate from value findings

## References

- [OWASP - Code quality and secret handling](https://owasp.org/www-project-application-security-verification-standard/)
- [CWE-798 - Hard-coded credentials](https://cwe.mitre.org/data/definitions/798.html)
