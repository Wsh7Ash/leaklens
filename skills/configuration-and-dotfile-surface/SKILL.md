---
name: configuration-and-dotfile-surface
description: "Sweep the configuration and dotfile region deliberately, because these files are small, high-value and routinely left out of a scan by a default include rule. Use when a repository or workstation tree is in scope and configuration files have not been explicitly included"
pack: leaklens
version: 1.0.0
category: data-tool
tags: [discover, configuration, files]
---

# Configuration and Dotfile Surface

> Sweep the configuration and dotfile region deliberately, because these files are small, high-value and routinely left out of a scan by a default include rule

**Use when:** a repository or workstation tree is in scope and configuration files have not been explicitly included

**Avoid when:** the plan already lists configuration files by path and confirms the tool reads them

## Procedure

1. Enumerate configuration files by name and by extension, including hidden dotfiles that a default include may skip.
2. Check whether the tool's default file selection actually opens them, and add them explicitly when it does not.
3. Look for environment files and their templates, since the template sometimes carries the real value instead of a placeholder.
4. Inspect local override files that are untracked but present, since those often hold developer credentials.
5. Record which configuration paths were read and which were skipped with the reason.
6. Pass content from these files to classification with the file region recorded, because region changes the remediation path.

## Signals

- An environment template carries a real value where a placeholder belongs
- Hidden files are not opened by the tool's default selection
- An untracked local override holds a credential that the tracked template does not
- A configuration path was skipped by a default rule nobody chose deliberately

## Patterns

**1. Region row**

```text
path | tracked | read | finding class
.env | no | yes | secret
.env.example | yes | yes | placeholder ok
dotfile.local | no | yes | secret, developer machine only
```

**2. Template check**

```text
compare each template against its real counterpart: a value where a placeholder belongs is a finding even in a tracked file
```

**3. Skip reason**

```text
any configuration path not read carries a written reason; absence of a reason means the plan has a hole
```

## Pitfalls

- Scanning only tracked files and missing the untracked local override that holds the real value
- Assuming a template is safe because the file name says example or sample
- Letting default file selection decide which configuration is read

## Done when

- Configuration paths are listed with tracked, read and finding class per row
- Every unread path carries a written reason rather than no reason at all

## References

- [OWASP - Configuration and secrets management](https://owasp.org/www-project-web-security-testing-guide/)
- [CWE-312 - Cleartext storage of sensitive information](https://cwe.mitre.org/data/definitions/312.html)
