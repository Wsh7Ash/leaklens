"""leaklens skills 16-30: classify phase."""

from __future__ import annotations

SKILLS: list[dict] = [
    {
        "slug": "cloud-access-key-classification",
        "title": "Cloud Access Key Classification",
        "summary": "Separate a cloud access key identifier from the secret half of the pair, because only one half is unusable on its own and the two demand different responses",
        "use_when": "a candidate matches a cloud provider key format or an assignment named like an access key",
        "avoid_when": "the corpus contains no cloud provider credentials of any kind",
        "tags": ["classify", "cloud", "credentials"],
        "steps": [
            "Identify which half you have: the public identifier that pairs with a secret, or the secret value itself.",
            "Record the provider, the identifier prefix, the path and line, and the region the file belongs to.",
            "Check whether the paired secret appears anywhere in the corpus, since an identifier alone still narrows an attack surface.",
            "Determine whether the key is active, disabled or merely a placeholder, using only non-network means such as configuration or documentation.",
            "Note whether the key appears in tracked history, which decides whether a rewrite is needed after rotation.",
            "Classify severity by half: identifier as internal, secret as secret, and state which one you found.",
        ],
        "signals": [
            "A key identifier appears without its secret half anywhere in the corpus",
            "Both halves appear together in the same file",
            "The key looks like a legacy format that predates the current rotation policy",
            "The identifier appears in tracked history after being removed from the working tree",
        ],
        "patterns": [
            (
                "Half record",
                "half: identifier | provider: cloud | prefix: AKIA | path: config/settings.py:42 | paired secret found: no",
            ),
            (
                "Severity by half",
                "identifier alone -> internal, useful for attribution; secret alone or both -> secret, rotation required before publication",
            ),
            (
                "History flag",
                "identifier removed from tree but present in history -> rewrite flagged as a separate remediation item",
            ),
        ],
        "pitfalls": [
            "Reporting an identifier as a full credential and inflating the severity",
            "Rotating only the half you found while the pair remains valid elsewhere",
            "Leaving history untouched after removing a secret from the working tree",
        ],
        "done_when": [
            "Each key finding states which half was found, the provider and whether a paired secret exists",
            "History presence is recorded per finding as a separate remediation item",
        ],
        "refs": [
            "[OWASP - Cloud security misconfiguration guidance](https://owasp.org/www-project-cloud-security/)",
            "[CWE-798 - Use of hard-coded credentials](https://cwe.mitre.org/data/definitions/798.html)",
        ],
        "meta": {"phase": "classify"},
    },
    {
        "slug": "api-token-and-bearer-classification",
        "title": "API Token and Bearer Classification",
        "summary": "Classify bearer-style tokens by issuer, scope and expiry, so the report can say what a reader of the file could actually do with the value",
        "use_when": "a candidate matches a published token format or sits inside an authorization header construction",
        "avoid_when": "the corpus holds no token-format values and no header construction of any kind",
        "tags": ["classify", "tokens", "authorization"],
        "steps": [
            "Identify the issuer from the prefix and record it, since scope conventions differ by platform.",
            "Record where it sits: source file, configuration, log, fixture or history, because location changes the fix.",
            "Look for scope or permission indicators nearby in code or configuration to estimate what the token could do.",
            "Note any expiry metadata associated with the token, and whether a value with no expiry path is in use.",
            "Check whether the same value appears in more than one location, since each copy is a separate rotation target.",
            "Classify by estimated capability, not by length, and state the estimate as an estimate.",
        ],
        "signals": [
            "A token sits in a tracked file with no expiry handling anywhere in the code",
            "The same value appears in a source file and in a log",
            "Scope indicators suggest a permission set wider than the component needs",
            "A fixture directory contains what looks like a live token rather than a marked test value",
        ],
        "patterns": [
            (
                "Token record",
                "issuer: code-hosting | prefix: ghp_ | location: src/client.py:18 + log/app.log:902 | scope hint: repo write | expiry: none found",
            ),
            (
                "Capability note",
                "state what the file's own code does with the token; that is the floor of what a reader of the file could do",
            ),
            (
                "Copy count",
                "one value, N locations -> N rotation targets, each listed separately so none is missed during rotation",
            ),
        ],
        "pitfalls": [
            "Reporting a token without tracing what the code does with it, which leaves severity unarguable",
            "Missing a second copy in a log and rotating only the source location",
            "Treating a fixture token as live without checking the surrounding markers",
        ],
        "done_when": [
            "Each token finding records issuer, location list, scope hint and expiry status",
            "Rotation targets are enumerated as one entry per location",
        ],
        "refs": [
            "[OWASP - Broken access control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)",
            "[CWE-798 - Use of hard-coded credentials](https://cwe.mitre.org/data/definitions/798.html)",
        ],
        "meta": {"phase": "classify"},
    },
    {
        "slug": "private-key-material-classification",
        "title": "Private Key Material Classification",
        "summary": "Recognise private key blocks and their variants, and separate a live key from an expired or test one, since key material in a file is a different class from any token",
        "use_when": "a candidate resembles a private key block, a key header, or an encoded key blob",
        "avoid_when": "the corpus contains no key material and no key-like blocks",
        "tags": ["classify", "keys", "cryptography"],
        "steps": [
            "Identify the key type from its header or encoding: signing key, transport key, or an encrypted variant.",
            "Record the file, the block boundaries and whether the material is passphrase protected.",
            "Look for companion material nearby: certificates, fingerprints or configuration naming the key's purpose.",
            "Determine from local evidence whether the key is a test fixture, an expired one, or appears current, without contacting any service.",
            "Note whether the block appears in tracked history as well as in the working tree.",
            "Classify as secret and record the intended rotation target, which for a key also includes every certificate that trusts it.",
        ],
        "signals": [
            "A key block sits in a tracked file with no passphrase protection",
            "A companion certificate in the same tree names the key's purpose",
            "The key appears in a fixtures directory but lacks a synthetic marker",
            "History holds the key after it was deleted from the working tree",
        ],
        "patterns": [
            (
                "Key record",
                "type: private key block | protected: no | purpose hint: tls client auth (from companion cert) | tracked: yes | history: yes",
            ),
            (
                "Rotation target",
                "for a key, the target is not one file: it is every trust anchor, certificate and configuration that references it, listed next to the finding",
            ),
            (
                "Local-only check",
                "fixture, expired or current is judged from local files and dates only; no service is contacted to confirm",
            ),
        ],
        "pitfalls": [
            "Publishing the key block in a report or ticket, which re-creates the exposure permanently",
            "Rotating the key while leaving the certificates that trust it untouched",
            "Assuming a key in a fixtures directory is synthetic because of where it lives",
        ],
        "done_when": [
            "Each key finding records type, protection, purpose hint, tracked status and history presence",
            "The rotation target list names every trust anchor alongside the key itself",
        ],
        "refs": [
            "[NIST SP 800-57 - Key management](https://csrc.nist.gov/pubs/sp/800/57/r5/final)",
            "[CWE-321 - Use of hard-coded cryptographic key](https://cwe.mitre.org/data/definitions/321.html)",
        ],
        "meta": {"phase": "classify"},
    },
    {
        "slug": "password-and-passphrase-classification",
        "title": "Password and Passphrase Classification",
        "summary": "Distinguish a real credential from a placeholder, an example or a test value, and rank the real ones by what the file says they protect",
        "use_when": "an assignment named like a password or passphrase holds a non-empty literal",
        "avoid_when": "every such assignment holds a documented placeholder or an environment lookup",
        "tags": ["classify", "credentials", "passwords"],
        "steps": [
            "Read the value's context: the key name, the neighbouring configuration and whether the file is tracked or local.",
            "Check for placeholder markers in the value itself and in the surrounding file before treating it as live.",
            "Look for a companion username or endpoint so you can state what the value protects without repeating the value.",
            "Note whether the value looks reused across files, since reuse widens the blast radius of one rotation.",
            "Distinguish a real credential from a test value by the environment markers in the file, not by the directory name alone.",
            "Classify by what it protects, and record a hash rather than the value in the evidence entry.",
        ],
        "signals": [
            "A password assignment holds a literal in a tracked configuration file",
            "The same literal appears under two different key names",
            "A value marked as an example carries no substitution marker in it at all",
            "A test directory contains a value with no environment marker anywhere nearby",
        ],
        "patterns": [
            (
                "Classification record",
                "key: db_password | protects: primary datastore (from companion host field) | tracked: yes | reused at: 1 other path | placeholder markers: none",
            ),
            (
                "Placeholder set",
                "placeholder markers: change-me, example, xxxx, <...>, changeme, password; any of these makes the value a finding about hygiene, not exposure",
            ),
            (
                "Hash substitute",
                "record sha256 prefix plus length so reuse can be proven across paths without storing any value",
            ),
        ],
        "pitfalls": [
            "Treating a documented example value as a live credential and inflating the report",
            "Recording the value itself in evidence, which recreates the exposure in the ticket",
            "Missing reuse because each file was read in isolation",
        ],
        "done_when": [
            "Each password finding states what it protects, whether it is tracked, and any reuse found",
            "Evidence records a hash prefix rather than the value itself",
        ],
        "refs": [
            "[OWASP - Password storage guidance](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)",
            "[CWE-259 - Use of hard-coded password](https://cwe.mitre.org/data/definitions/259.html)",
        ],
        "meta": {"phase": "classify"},
    },
    {
        "slug": "connection-string-classification",
        "title": "Connection String Classification",
        "summary": "Parse connection strings into their parts, because one string usually carries a host, a user, a credential and a database name, and each part is a separate fact to report",
        "use_when": "the corpus contains connection strings for databases, caches, queues or services",
        "avoid_when": "no connection-string shaped values exist anywhere in the readable tree",
        "tags": ["classify", "connection-strings", "databases"],
        "steps": [
            "Identify every connection-string shape present: URL form, key-value form and driver-specific forms.",
            "Parse each into components and record the host, database name, user and whether a credential component is present.",
            "Classify the credential component separately from the host, since a host is usually internal while the credential is secret.",
            "Check whether the string is assembled from parts at runtime, in which case record the parts rather than a literal.",
            "Note whether the host points at an internal or production endpoint, which determines who must be told.",
            "Record the string with its credential component redacted and a hash of it so reuse across files can still be detected.",
        ],
        "signals": [
            "A connection string embeds user and password before the host",
            "A string points at a production datastore from a development configuration file",
            "The string is assembled at runtime from environment lookups, so no literal exists",
            "The same credential appears in two strings for the same datastore",
        ],
        "patterns": [
            (
                "Parsed record",
                "scheme: postgres | host: internal-db.internal | db: app | user: app_rw | credential present: yes | sha256: 9c1d...",
            ),
            (
                "Component split",
                "host -> infrastructure reference (internal class); credential -> secret; user -> internal; each reported separately",
            ),
            (
                "Assembly case",
                "runtime-assembled string -> record the lookup names and the file, and mark the value as living in the store rather than in the file",
            ),
        ],
        "pitfalls": [
            "Reporting a whole connection string as one finding, which both over- and under-states it",
            "Redacting inconsistently so the same credential cannot be matched across two findings",
            "Missing that an internal host in a public file is its own information disclosure",
        ],
        "done_when": [
            "Each connection string yields separate entries for host, user and credential with a hash for reuse checks",
            "Runtime-assembled strings are labelled as references with the lookup source recorded",
        ],
        "refs": [
            "[CWE-312 - Cleartext storage of sensitive information](https://cwe.mitre.org/data/definitions/312.html)",
            "[OWASP - Database security guidance](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "classify"},
    },
    {
        "slug": "jwt-and-session-token-classification",
        "title": "JWT and Session Token Classification",
        "summary": "Decode the readable parts of a structured token without verifying it, so the report can state subject, scope and expiry while never treating the value as yours to use",
        "use_when": "a candidate is a structured three-part token or an opaque session identifier",
        "avoid_when": "the corpus contains no token-shaped values at all",
        "tags": ["classify", "jwt", "sessions"],
        "steps": [
            "Split the structure into its parts and decode the header and payload without verifying any signature.",
            "Record the algorithm declared in the header, the subject or audience claims, the issued-at and expiry times.",
            "Never present the token to any endpoint; decoding is local and the value is never used.",
            "Note whether the payload contains personal fields, which raises the class of the finding above internal.",
            "Check whether the token sits alongside its signing secret in the same file, which is a materially worse combination.",
            "Classify by expiry and scope: an expired token is a hygiene finding, an unexpired one with wide scope is a live risk.",
        ],
        "signals": [
            "A token decodes to an unexpired claim set with a broad scope",
            "The signing secret appears in the same file as the token",
            "The header declares a weak or unusual algorithm",
            "A payload carries personal fields alongside a scope claim",
        ],
        "patterns": [
            (
                "Decoded record",
                "alg: HS256 | sub: service account | scope: write | exp: 2026-11-02 (still valid) | personal fields: none | co-located secret: no",
            ),
            (
                "Local-only rule",
                "decode and read claims locally; never send the token anywhere, and state in the report that it was never used",
            ),
            (
                "Combination flag",
                "token plus signing secret in one file is recorded as one finding with a higher rank than either alone",
            ),
        ],
        "pitfalls": [
            "Presenting the token to an endpoint to see what it does, which is using the credential",
            "Reporting an expired token with the same rank as a live one",
            "Missing that the secret sits three lines below the token in the same file",
        ],
        "done_when": [
            "Each token finding records algorithm, subject, scope, expiry and any co-located secret",
            "The report states explicitly that no token was presented to any endpoint",
        ],
        "refs": [
            "[RFC 7519 - JSON Web Token](https://www.rfc-editor.org/rfc/rfc7519)",
            "[OWASP - JWT attack surface guidance](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "classify"},
    },
    {
        "slug": "personal-identifier-classification",
        "title": "Personal Identifier Classification",
        "summary": "Detect and classify values that identify a person, recording presence and structure rather than the identifier itself",
        "use_when": "the corpus may contain personal data and the ladder marks that class detect-only",
        "avoid_when": "the ladder explicitly permits reading personal values and the owner has confirmed it in writing",
        "tags": ["classify", "personal-data", "privacy"],
        "steps": [
            "Confirm from the ladder that this class is detect-only before running any detection at all.",
            "Detect by structure rather than by content: field names, formats and surrounding labels.",
            "Record the path, the field name, the structure detected and a hash of the value, never the value.",
            "Count occurrences per file rather than listing each one, so the report states volume without reproducing records.",
            "Note whether the file is tracked, published or exported, since location decides the urgency.",
            "Classify severity by publication state, not by the sensitivity of the field alone.",
        ],
        "signals": [
            "A tracked file contains a column of personal identifiers in plain text",
            "A fixtures directory holds what look like real records rather than synthetic ones",
            "A document or export includes personal fields with no publication restriction",
            "A detection ran against values the ladder marked detect-only",
        ],
        "patterns": [
            (
                "Presence record",
                "path: data/seed.csv | field: national_id | structure matches: yes | occurrences: 412 | tracked: yes | hash of first: 7be1...",
            ),
            (
                "Count-not-copy rule",
                "report counts and structure; the value never appears in evidence, a ticket or a chat message",
            ),
            (
                "Publication rank",
                "published or exported outranks merely stored; rank the finding by where the copy lives",
            ),
        ],
        "pitfalls": [
            "Pasting an example record into the report so a reader can see what was found",
            "Listing every occurrence individually, which turns the report into a second copy of the dataset",
            "Ranking by field sensitivity while ignoring that the file is already public",
        ],
        "done_when": [
            "Each personal-data finding records structure, count, path and publication state with no value",
            "The report cites the ladder's detect-only rule as the reason values are absent",
        ],
        "refs": [
            "[OWASP - Sensitive data exposure](https://owasp.org/www-project-top-ten/)",
            "[NIST SP 800-53 - PII processing and transparency](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)",
        ],
        "meta": {"phase": "classify"},
    },
    {
        "slug": "payment-and-financial-record-classification",
        "title": "Payment and Financial Record Classification",
        "summary": "Detect financial record fragments by structure and field name, and rank them by how far the copy has travelled from the system of record",
        "use_when": "the corpus may contain transaction, card, bank or invoice data",
        "avoid_when": "the owner confirms in writing that no financial data exists in any readable tree",
        "tags": ["classify", "financial", "personal-data"],
        "steps": [
            "Detect by structure and field naming rather than reading values, consistent with the ladder's handling rule.",
            "Record the path, the field names detected and a count per file, with a hash rather than any value.",
            "Distinguish full records from truncated or masked ones, since a masked fragment ranks far lower.",
            "Note whether the copy is a production export, a fixture or a test artifact, using local markers only.",
            "Trace whether the copy has a documented owner and retention, since an unowned export is the urgent case.",
            "Classify by completeness and location together: masked and internal is low, full and published is critical.",
        ],
        "signals": [
            "A tracked export contains unmasked financial fields",
            "A fixture directory contains records whose structure matches production exactly",
            "A copy exists with no owner and no retention date",
            "Only a masked fragment is present but it was reported as a full record",
        ],
        "patterns": [
            (
                "Completeness record",
                "path: exports/q3.csv | fields: card_number, expiry | masked: no | occurrences: 1580 | owner: unknown | retention: none",
            ),
            (
                "Masking check",
                "record whether values are fully present, partially masked or tokenized; this single field often decides the rank",
            ),
            (
                "Owner rule",
                "an export with no owner and no retention is ranked above a full record whose owner and retention are documented",
            ),
        ],
        "pitfalls": [
            "Recording an unmasked value so the reader understands the finding",
            "Ranking a masked fragment as a full record because the field name looks alarming",
            "Reporting a production export as a fixture because it lives beside test data",
        ],
        "done_when": [
            "Each financial finding records completeness, count, location, owner and retention with no values",
            "The rank is justified from completeness and publication state together",
        ],
        "refs": [
            "[PCI DSS - Requirements for stored cardholder data](https://www.pcisecuritystandards.org/)",
            "[NIST SP 800-53 - Information retention controls](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)",
        ],
        "meta": {"phase": "classify"},
    },
    {
        "slug": "email-address-corpus-classification",
        "title": "Email Address Corpus Classification",
        "summary": "Detect email addresses at volume and classify them by whether they are synthetic, role-based, employee or customer addresses, since only one of those is a privacy finding",
        "use_when": "the corpus may contain email addresses in source, fixtures, logs or exports",
        "avoid_when": "the owner confirms all addresses present are synthetic test data",
        "tags": ["classify", "personal-data", "contacts"],
        "steps": [
            "Detect addresses by structure and record counts per file rather than listing each address.",
            "Separate known synthetic domains and fixtures from addresses on real domains using local markers and domain lists.",
            "Classify remaining addresses as role-based, employee-like or customer-like based on the surrounding field and file.",
            "Check whether the addresses appear in a tracked and possibly published file, since location drives the rank.",
            "Note whether addresses co-occur with other personal fields, which raises the class from contact detail to a record.",
            "Record counts and classification per file with a hash sample, never an address.",
        ],
        "signals": [
            "A tracked file contains addresses on a real domain with no synthetic markers",
            "Addresses co-occur with other personal fields in the same row",
            "A fixture directory contains addresses that match production structure exactly",
            "A log records full addresses where a hash or truncation would do",
        ],
        "patterns": [
            (
                "Count record",
                "path: docs/examples.md | addresses: 23 | synthetic domain: 21 | real domain: 2 | co-located personal fields: no",
            ),
            (
                "Domain split",
                "synthetic domains and marked fixtures are excluded with the rule that excluded them; real-domain hits are kept and counted",
            ),
            (
                "Co-occurrence flag",
                "addresses plus another personal field in one row -> rank as a record, not as a contact detail",
            ),
        ],
        "pitfalls": [
            "Listing every address in the report, which reproduces the list you were asked to detect",
            "Treating a synthetic domain as real and inflating the count",
            "Missing co-occurring fields, which is what separates a contact detail from a record",
        ],
        "done_when": [
            "Each file yields a count split by synthetic and real with the exclusion rule recorded",
            "Co-occurrence with other personal fields is flagged per file",
        ],
        "refs": [
            "[NIST SP 800-53 - Personally identifiable information handling](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)",
            "[OWASP - Information disclosure guidance](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "classify"},
    },
    {
        "slug": "internal-infrastructure-reference-classification",
        "title": "Internal Infrastructure Reference Classification",
        "summary": "Classify internal hostnames, addresses and service names found in public or shared files, because infrastructure detail is its own disclosure even with no credential attached",
        "use_when": "the corpus contains hostnames, IP literals, service names or internal URLs",
        "avoid_when": "the tree is internal-only and its readership already includes everyone who could use the detail",
        "tags": ["classify", "infrastructure", "disclosure"],
        "steps": [
            "Extract hostnames, address literals, port numbers and service names into a counted list per file.",
            "Split them into categories: public-facing, internal naming scheme, and placeholder such as localhost or example.",
            "Record which files are tracked, published or mirrored outside the organization, since that decides exposure.",
            "Note whether the reference includes an environment label such as staging or a region, which adds detail.",
            "Check for an accompanying credential, because infrastructure detail plus a credential is one combined finding.",
            "Classify by reader reach: public file outranks internal documentation, even for the same hostname.",
        ],
        "signals": [
            "A public documentation file names an internal hostname and its port",
            "An address literal appears with an environment label beside it",
            "An internal service name appears in an example that was copied into a public repository",
            "A credential and a host appear in the same file",
        ],
        "patterns": [
            (
                "Reference record",
                "host: db-replica-2.internal | port: 5432 | env label: prod | file: README.md | tracked: yes | published: yes",
            ),
            (
                "Reader-reach rank",
                "published outside the org > public repo > internal doc > local file; rank by who can actually read the file",
            ),
            (
                "Combined flag",
                "host plus credential in one file -> one combined finding ranked above either alone, with both components described",
            ),
        ],
        "pitfalls": [
            "Reporting internal hostnames as critical when only internal readers can see them",
            "Splitting a host and credential into two findings, which understates the combination",
            "Ignoring that a public README was copied into other repositories years ago",
        ],
        "done_when": [
            "Each reference finding records host, category, environment label and reader reach",
            "Any co-located credential is recorded as a combined finding rather than a separate one",
        ],
        "refs": [
            "[CWE-200 - Exposure of sensitive information](https://cwe.mitre.org/data/definitions/200.html)",
            "[OWASP - Information disclosure guidance](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "classify"},
    },
    {
        "slug": "signed-url-and-access-grant-classification",
        "title": "Signed URL and Access Grant Classification",
        "summary": "Classify time-limited access grants found in files, including their expiry and scope, because an expired grant is hygiene while an unexpired one is a live path to data",
        "use_when": "the corpus contains signed URLs, presigned requests or expiring access grants",
        "avoid_when": "no signed or time-limited access artifacts exist in any readable tree",
        "tags": ["classify", "signed-urls", "access"],
        "steps": [
            "Identify the grant type: a signed object request, an expiring link or a bearer-style access parameter.",
            "Decode the visible parameters locally to read expiry, scope and resource, without ever fetching the URL.",
            "Record the resource the grant addresses, the expiry time and the file that contains it.",
            "Compute whether the grant is still valid relative to the assessment date and record that verdict.",
            "Check whether the grant appears in a tracked or published file, since a published unexpired grant is the urgent case.",
            "Classify by validity and reach, and state that the URL was never requested.",
        ],
        "signals": [
            "A presigned URL with a future expiry sits in a tracked file",
            "The same grant appears in a document published outside the organization",
            "A grant addresses a resource more sensitive than the file's purpose suggests",
            "Expiry is far enough ahead that the grant will outlive the assessment",
        ],
        "patterns": [
            (
                "Grant record",
                "type: presigned object request | resource: export bucket path | expiry: 2026-11-01 (valid at assessment date) | file: notes.md | published: yes",
            ),
            (
                "Validity verdict",
                "valid | expired | no-expiry; each verdict recorded with the date the assessment ran, since validity is time-dependent",
            ),
            (
                "Never-requested statement",
                "the report states the URL was never fetched, and the evidence is the decoded parameters alone",
            ),
        ],
        "pitfalls": [
            "Fetching the URL to see what it exposes, which uses the grant you were assessing",
            "Reporting an expired grant as a live access path",
            "Recording validity without the assessment date, which makes the claim stale immediately",
        ],
        "done_when": [
            "Each grant records type, resource, expiry, validity verdict and publication state",
            "The report states the URL was never requested",
        ],
        "refs": [
            "[AWS - Presigned URL security considerations](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ShareObjectPreSignedURL.html)",
            "[CWE-639 - Authorization bypass through user-controlled key](https://cwe.mitre.org/data/definitions/639.html)",
        ],
        "meta": {"phase": "classify"},
    },
    {
        "slug": "webhook-and-signing-secret-classification",
        "title": "Webhook and Signing Secret Classification",
        "summary": "Classify signing secrets by consumer and algorithm, and note that rotating one breaks every partner that has not been told, so the rotation target is wider than the file",
        "use_when": "a candidate resembles a webhook signing secret or a symmetric verification key",
        "avoid_when": "the corpus contains no signing secrets and no webhook configuration",
        "tags": ["classify", "webhooks", "secrets"],
        "steps": [
            "Identify the consumer from configuration nearby: which provider or partner signs with this value.",
            "Note the algorithm and expected length, since a mismatch usually means the value is something else.",
            "Check whether both a live and a test secret appear and whether they are distinguishable by marker.",
            "Record the file, whether it is tracked, and any history containing the same value.",
            "List the rotation target: every partner that must be notified and every environment holding the value.",
            "Classify as secret and attach a rotation cost note, because the partner notification is usually the slow part.",
        ],
        "signals": [
            "A signing secret sits in tracked configuration with no environment separation",
            "A live and a test secret appear with no marker distinguishing them",
            "History holds the same value after it was moved to a store",
            "No partner notification record exists for a value that partners verify against",
        ],
        "patterns": [
            (
                "Secret record",
                "consumer: payments provider | algorithm: HMAC-SHA256 | expected length: 32 | live and test distinguished: no | tracked: yes",
            ),
            (
                "Rotation target list",
                "targets: partner A, partner B, env prod, env staging, history; each listed because each must be handled separately",
            ),
            (
                "Cost note",
                "record that partner notification is the long pole, so the plan schedules it before the technical rotation",
            ),
        ],
        "pitfalls": [
            "Rotating the value and breaking partners who were never notified",
            "Assuming a test secret is harmless because it lives in a test directory",
            "Missing that history still holds the value after the file was cleaned",
        ],
        "done_when": [
            "Each signing secret records consumer, algorithm, environment separation and history presence",
            "A rotation target list including partner notification is attached to the finding",
        ],
        "refs": [
            "[Stripe - Rotating webhook secrets](https://docs.stripe.com/webhooks#rotate-endpoint-secret)",
            "[NIST SP 800-57 - Key rotation guidance](https://csrc.nist.gov/pubs/sp/800/57/r5/final)",
        ],
        "meta": {"phase": "classify"},
    },
    {
        "slug": "oauth-client-credential-classification",
        "title": "OAuth Client Credential Classification",
        "summary": "Classify application credentials separately from user tokens, since a client secret acts as the application itself and its rotation path runs through every grant it holds",
        "use_when": "a candidate resembles an application client identifier or its secret",
        "avoid_when": "the corpus contains no application credentials of any kind",
        "tags": ["classify", "oauth", "credentials"],
        "steps": [
            "Separate the client identifier, which is often public, from the client secret, which never is.",
            "Record which identity provider is in use and which flow the credential belongs to, from configuration context.",
            "Check for redirect URIs configured alongside, since a permissive redirect list compounds the finding.",
            "Note whether the credential appears in a tracked file, an artifact or history.",
            "List the rotation path: provider console, application configuration, every environment and any stored grant.",
            "Classify the secret as secret and the identifier as internal, and report them as two related entries.",
        ],
        "signals": [
            "A client secret sits in a tracked configuration file",
            "A redirect URI list includes a wildcard or a broad pattern",
            "The client identifier is reported with the same rank as the secret",
            "Rotation requires a provider console step nobody has access to",
        ],
        "patterns": [
            (
                "Pair record",
                "idp: major provider | flow: authorization code | client id: public, tracked (expected) | client secret: present, tracked (finding) | redirect list: 1 exact URI",
            ),
            (
                "Two entries",
                "identifier -> internal entry; secret -> secret entry; both cross-referenced so a reader sees them together",
            ),
            (
                "Rotation path",
                "steps: provider console, app config, environments, stored grants; each step has an owner or is marked blocked",
            ),
        ],
        "pitfalls": [
            "Reporting the client identifier as a credential, which is wrong and wastes reviewer time",
            "Fixing the file while the provider-side secret remains unchanged",
            "Overlooking a permissive redirect URI that makes the credential easier to exercise",
        ],
        "done_when": [
            "Client identifier and secret are reported as separate cross-referenced entries",
            "The rotation path is listed with an owner or an explicit blocker per step",
        ],
        "refs": [
            "[RFC 6749 - OAuth 2.0 client credentials](https://www.rfc-editor.org/rfc/rfc6749)",
            "[OWASP - OAuth security guidance](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "classify"},
    },
    {
        "slug": "archive-and-backup-content-classification",
        "title": "Archive and Backup Content Classification",
        "summary": "Decide which compressed or backup artifacts get opened and which are skipped, because an unread archive is a coverage claim nobody has actually tested",
        "use_when": "archives, database dumps or backup files exist inside the readable boundary",
        "avoid_when": "the boundary excludes archives in writing and no compressed artifact is readable",
        "tags": ["classify", "archives", "coverage"],
        "steps": [
            "List every archive and backup artifact with its type, size and whether it is tracked.",
            "Decide per artifact whether to open it, using the boundary and the size as the constraint, and record the decision.",
            "For opened artifacts, extract to a temporary directory outside the tree and scan the contents as a nested surface.",
            "Record which members of an archive produced findings and at what depth, since a value two levels deep is still in scope.",
            "Delete temporary extractions when finished and record that the deletion happened.",
            "Classify artifacts that were not opened as uncovered, with the reason, rather than as clean.",
        ],
        "signals": [
            "An archive exists and no plan step decides whether to open it",
            "A backup dump sits in the tree and was counted as scanned because its container was listed",
            "Temporary extraction directories were left behind after a session",
            "An artifact was reported clean without ever being opened",
        ],
        "patterns": [
            (
                "Artifact decision",
                "artifact: data-backup.tgz | type: tarball | decision: open | members scanned: 142 | findings at depth: 2 | temp deleted: yes",
            ),
            (
                "Unopened label",
                "unopened artifact -> label uncovered with reason (size, boundary, tool limit); never label it clean",
            ),
            (
                "Depth record",
                "record the deepest member scanned so coverage is stated as a measured depth rather than a yes",
            ),
        ],
        "pitfalls": [
            "Calling an unopened archive clean because its filename looked harmless",
            "Leaving extracted copies of sensitive content in a temporary directory",
            "Reporting coverage over an archive when only its member list was read",
        ],
        "done_when": [
            "Every archive has an open or uncovered decision with a reason and, if opened, a scanned depth",
            "Temporary extraction is confirmed deleted and recorded",
        ],
        "refs": [
            "[CWE-311 - Missing encryption of sensitive data](https://cwe.mitre.org/data/definitions/311.html)",
            "[OWASP - Data-at-rest handling guidance](https://owasp.org/www-project-top-ten/)",
        ],
        "meta": {"phase": "classify"},
    },
    {
        "slug": "dataset-export-classification",
        "title": "Dataset Export Classification",
        "summary": "Classify exported datasets by contents, ownership and destination, because an export is the copy most likely to leave the organization entirely",
        "use_when": "export files, data dumps or report extracts exist inside the readable boundary",
        "avoid_when": "no export artifact exists or the boundary excludes them in writing",
        "tags": ["classify", "exports", "lineage"],
        "steps": [
            "List every export artifact with its format, row count and the date it appears to have been produced.",
            "Read the header row only to classify the fields present, without reading data rows.",
            "Assign each field a class from the ladder and record the class summary, not the values.",
            "Trace where the export came from using naming, dates and any manifest alongside it.",
            "Determine, from local evidence only, whether the destination of that copy is inside or outside the organization.",
            "Classify by field classes and destination together, with retention and ownership where they are known.",
        ],
        "signals": [
            "An export contains personal-class fields with no manifest and no owner",
            "A file's date suggests it predates a retention change and was never refreshed",
            "The destination of the copy cannot be determined from anything in the tree",
            "A header row alone was enough to classify but the file was read in full anyway",
        ],
        "patterns": [
            (
                "Export record",
                "artifact: report-q3.csv | rows: 1580 | fields: id, email, plan | classes: personal | owner: unknown | destination: unknown | retention: none",
            ),
            (
                "Header-only rule",
                "read the header row to classify fields and stop; data rows are never opened when the ladder marks the class detect-only",
            ),
            (
                "Destination rank",
                "destination outside the organization outranks internal storage for the same fields; rank on destination first",
            ),
        ],
        "pitfalls": [
            "Reading data rows to be thorough when the header alone answers the classification question",
            "Reporting an export without saying where its copy went",
            "Assuming a recent file date means the content was reviewed",
        ],
        "done_when": [
            "Each export records format, row count, field classes, owner, destination and retention",
            "Classification comes from the header row, with data rows left unopened",
        ],
        "refs": [
            "[NIST SP 800-53 - Information export controls](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)",
            "[OWASP - Sensitive data discovery](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "classify"},
    },
]