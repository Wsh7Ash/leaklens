"""leaklens skills 1-15: scope and discover phases."""

from __future__ import annotations

SKILLS: list[dict] = [
    {
        "slug": "authorized-corpus-boundary",
        "title": "Authorized Corpus Boundary",
        "summary": "Write down exactly which repositories, paths, artifacts and data classes the exposure assessment may read, before the first file is opened",
        "use_when": "a data-exposure assessment is about to start and no written list states which trees, artifacts or datasets are in scope",
        "avoid_when": "the owner already publishes a machine-readable list of readable trees with an explicit exclusion list",
        "tags": ["scope", "authorization", "rules-of-engagement"],
        "steps": [
            "Collect the written authorization, the ownership statement and any path list into one place and note the versions you used.",
            "List every in-scope tree, repository, artifact location and environment exactly as written, without normalizing or guessing wildcards.",
            "Record explicit exclusions too, since a subtree excluded by name is the most common way an assessment reads something it may not.",
            "State the data classes you expect to encounter and which of them you are cleared to read versus only to detect the presence of.",
            "Write the boundary as a short pre-flight checklist you re-read before the first read of every session, not as a note recalled from memory.",
            "Save the boundary text beside the evidence so a reviewer can prove every recorded path fell inside the permitted set.",
        ],
        "signals": [
            "Authorization names a repository but is silent on generated output and build directories",
            "A subtree is excluded in prose while a glob in the same document includes it",
            "No one can say whether reading a backup artifact is permitted",
            "A previous session recorded paths you cannot find in any current document",
        ],
        "patterns": [
            (
                "Boundary record",
                "scope:\n  trees: [src/**, config/**, docs/**]\n  excluded: [vendor/**, third_party/**]\n  artifacts: [build output read allowed]\n  classes: [detect only: personal, secret]\n  network: forbidden",
            ),
            (
                "Pre-flight echo",
                "Before session start, restate: readable trees, exclusions, classes detect-only, and the network ban. Any element you cannot quote from the document is a gap to resolve, not a permission to assume.",
            ),
            (
                "Evidence binding",
                "Store boundary.md beside evidence/ so each recorded finding carries a document version it can be checked against during review.",
            ),
        ],
        "pitfalls": [
            "Reading a wildcard as permission for every subtree when the document lists specific paths only",
            "Scanning build output that the owner never opened up for assessment",
            "Treating an old approval as current after the repository changed hands or gained new data",
        ],
        "done_when": [
            "A written boundary table names readable trees, exclusions, data classes and the network ban",
            "Every later evidence entry carries the document version that justified reading it",
        ],
        "refs": [
            "[OWASP - Sensitive data exposure guidance](https://owasp.org/www-project-top-ten/)",
            "[NIST SP 800-53 - PII and information handling](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)",
        ],
        "meta": {"phase": "scope"},
    },
    {
        "slug": "dataset-inventory-and-provenance",
        "title": "Dataset Inventory and Provenance",
        "summary": "Build a list of where data actually comes from and where it is copied, because an exposure is only actionable once every copy of the record is known",
        "use_when": "the assessment covers a system whose data reaches more than one store, artifact or third party",
        "avoid_when": "one authoritative store exists and the owner can account for every derived copy",
        "tags": ["scope", "inventory", "lineage"],
        "steps": [
            "Enumerate the sources that produce records: application database, object storage, logs, exports, third-party syncs and build artifacts.",
            "For each source record what it holds, roughly how many records, and whether it contains personal or secret classes.",
            "Trace where each source is copied to: warehouses, backups, analytics pipelines, support tooling and developer workstations.",
            "Mark each copy as authoritative, derived or incidental, since each class implies a different remediation path.",
            "Note any copy whose owner is unknown and carry it into the discover phase as an open question.",
            "Write the inventory as a table with source, contents, class, copies and owner, and mark unconfirmed cells as unknown.",
        ],
        "signals": [
            "A warehouse table mirrors production data with no recorded owner",
            "A support export leaves the system and nobody can say where the file went",
            "Backups exist for one store but no one has considered the log pipeline",
            "A third-party sync was configured by a former team member",
        ],
        "patterns": [
            (
                "Lineage row",
                "source | contents | class | copies | owner\nprimary db | accounts | personal | warehouse, backup | data-team\napp logs | request traces | internal | log store | platform\nexports | reports | personal | drive folder | unknown",
            ),
            (
                "Copy class",
                "authoritative (the record lives here) | derived (computed from it) | incidental (a by-product); each class changes who fixes a leak",
            ),
            (
                "Unknown rule",
                "any cell you could not confirm is written as unknown and carried forward rather than dropped from the inventory",
            ),
        ],
        "pitfalls": [
            "Inventorying only the primary store while the log pipeline holds the same records",
            "Assuming a derived copy is harmless because it was computed rather than copied",
            "Omitting third-party syncs, which are usually where the data class widens",
        ],
        "done_when": [
            "Every source has a row with contents, class, copies and owner, and unknown cells are listed",
            "At least one derived or incidental copy is traced to its destination with an owner named",
        ],
        "refs": [
            "[OWASP - Data-centric security guidance](https://owasp.org/www-project-top-ten/)",
            "[NIST SP 800-53 - System boundary documentation](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)",
        ],
        "meta": {"phase": "scope"},
    },
    {
        "slug": "data-class-ladder-definition",
        "title": "Data Class Ladder Definition",
        "summary": "Agree the ladder of data classes and what each one permits, so a detection is judged against a stated rule instead of against whoever reads the report",
        "use_when": "findings will be ranked and no agreed ladder defines what separates public from personal from secret",
        "avoid_when": "the organization already publishes a classification policy with handling rules per class",
        "tags": ["scope", "classification", "policy"],
        "steps": [
            "Adopt or write a short ladder: public, internal, personal, secret, and state what each class means in one sentence.",
            "Define the handling rule for each class, particularly whether detection alone is permitted or whether reading a value is allowed.",
            "Record which classes are detect-only for this engagement, since that single decision shapes every later confirmation step.",
            "Agree how a value straddling two classes is ranked, because most real findings sit between them.",
            "Note the retention rule for evidence per class, so a captured value has a defined lifetime from the moment it is written.",
            "Store the ladder beside the boundary document and reference it from every finding you record.",
        ],
        "signals": [
            "Two readers rank the same finding differently with no policy to settle it",
            "A class is defined but no handling rule says what you may do with it",
            "Evidence retention differs per finding only because individuals decided differently",
            "A straddling value has no defined ranking and gets argued each time",
        ],
        "patterns": [
            (
                "Ladder definition",
                "public: fine to publish\ninternal: harms nobody outside if exposed, still not published\npersonal: identifies or contacts a person\nsecret: grants access if used; detect-only in this engagement",
            ),
            (
                "Handling column",
                "class | read value | record value | retain\ndetect-only: detect yes, record no, retain no\npersonal: detect yes, record hash only, retain until report",
            ),
            (
                "Straddle rule",
                "a token inside a personal record ranks as the higher of the two classes and inherits the stricter handling rule",
            ),
        ],
        "pitfalls": [
            "Publishing a secret value in a report that a ticket system will retain forever",
            "Defining classes with no handling column, so every reader improvises",
            "Ranking a straddling value by the lower class because that keeps the report short",
        ],
        "done_when": [
            "A ladder with a handling column and a retention rule is written and referenced by findings",
            "The straddle rule is stated, and at least one finding cites it",
        ],
        "refs": [
            "[NIST SP 800-60 - Information categorization](https://csrc.nist.gov/pubs/sp/800/60/v1r1/final)",
            "[OWASP - Sensitive data discovery](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "scope"},
    },
    {
        "slug": "local-only-toolchain-preparation",
        "title": "Local-Only Toolchain Preparation",
        "summary": "Prepare a scanning chain that never uploads content anywhere, because a tool that phones home with your repository has already caused the incident you are assessing",
        "use_when": "any tool, model or service will read in-scope content and its network behaviour has not been confirmed",
        "avoid_when": "the owner already supplies an air-gapped toolchain with a documented network policy",
        "tags": ["scope", "tooling", "data-handling"],
        "steps": [
            "List every tool that will read in-scope content and record whether it transmits anything, including telemetry and crash reporting.",
            "Disable telemetry and auto-update on each tool where an option exists, and record which options you set.",
            "Confirm that no tool sends content to a hosted model or service; local execution is the requirement, not a preference.",
            "Verify the exclusion and ignore files so caches and previous output do not get re-read as new findings.",
            "Run a dry pass over a harmless file and inspect the tool's own logs or network counters for any outbound attempt.",
            "Record the prepared toolchain with versions and settings beside the evidence, so the run can be reproduced exactly.",
        ],
        "signals": [
            "A tool has default telemetry enabled and no documented way to disable it",
            "A model-backed helper would send file contents to a hosted endpoint",
            "No one has checked whether the runner has outbound network access at all",
            "Cache directories from a previous run are about to be re-read as fresh findings",
        ],
        "patterns": [
            (
                "Toolchain record",
                "tool | version | network | telemetry | settings applied\nscanner-x | 2.3 | disabled at OS level | off | --no-telemetry\nhelper-y | 1.1 | blocked by firewall rule | off | local model only",
            ),
            (
                "Dry pass",
                "run against one known-harmless file, then inspect egress counters; any outbound attempt stops the session and is reported as a toolchain defect",
            ),
            (
                "Exclusion list",
                "exclude caches, previous results and vendored dependencies before the first pass so re-reads never masquerade as new findings",
            ),
        ],
        "pitfalls": [
            "Letting an AI helper summarize repository content through a hosted API the owner never approved",
            "Re-running against a cache from a previous session and reporting duplicates as new",
            "Assuming a tool is offline because it has no obvious upload button",
        ],
        "done_when": [
            "Every tool reading in-scope content has a recorded network posture and the settings applied",
            "A dry pass shows no outbound attempt, and exclusions are set before the first real run",
        ],
        "refs": [
            "[OWASP - Secure development toolchain guidance](https://owasp.org/www-project-application-security-verification-standard/)",
            "[NIST SP 800-53 - Monitoring and boundary protection](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)",
        ],
        "meta": {"phase": "scope"},
    },
    {
        "slug": "synthetic-first-confirmation-rule",
        "title": "Synthetic First Confirmation Rule",
        "summary": "Confirm every detection technique against a planted synthetic value first, so the technique is proven before it ever touches a real record",
        "use_when": "a detection rule is being introduced or changed and its false-positive behaviour is unmeasured",
        "avoid_when": "a golden corpus of synthetic fixtures already covers each class and the rule passes against it",
        "tags": ["scope", "validation", "method"],
        "steps": [
            "Create synthetic fixtures for each class: a fake cloud key, a fake token, a fake personal record, each clearly marked.",
            "Plant them in a temporary tree you own, never in the repository under assessment.",
            "Run the rule against the fixtures and require a hit on every one before the rule is used for real content.",
            "Introduce near-miss fixtures, such as an identifier that resembles a token, and require the rule to stay quiet.",
            "Record the fixture set with the rule version so a later rule change can be measured against the same corpus.",
            "Only after both hit and quiet behave as expected, run the rule against in-scope content.",
        ],
        "signals": [
            "A rule was written and applied directly to production content without a fixture test",
            "Near-miss fixtures produce hits, which means every real finding will need manual clearing",
            "The fixture set exists in someone's shell history rather than in a file",
            "A rule change shipped with no re-run against the corpus",
        ],
        "patterns": [
            (
                "Fixture row",
                "class | fixture | expected | observed\ncloud-key | AKIA...fixture | hit | hit\ntoken | ghp_fixture | hit | hit\nnear-miss | order_reference_123 | quiet | hit  <- rule too broad",
            ),
            (
                "Two-sided test",
                "every rule needs both a hit requirement and a quiet requirement; only the hit side leaves precision unmeasured",
            ),
            (
                "Version binding",
                "store the fixture set with a rule version so a later change is measured against the identical corpus",
            ),
        ],
        "pitfalls": [
            "Tuning a rule against real content until it stops firing, which is how a real secret gets tuned out",
            "Testing only the positive case and accepting a rule that flags half the repository",
            "Keeping fixtures in an ad-hoc location so they are unavailable when the rule changes",
        ],
        "done_when": [
            "A fixture set with hit and quiet expectations exists per class and passes before real content is scanned",
            "The fixture set is stored with the rule version that last passed against it",
        ],
        "refs": [
            "[OWASP - Verification and testing guidance](https://owasp.org/www-project-application-security-verification-standard/)",
            "[CWE-546 - Suspicious comment and pattern checking](https://cwe.mitre.org/data/definitions/546.html)",
        ],
        "meta": {"phase": "scope"},
    },
    {
        "slug": "read-only-evidence-capture",
        "title": "Read-Only Evidence Capture",
        "summary": "Capture enough of a detection to prove it later while never copying the sensitive value itself, so the assessment cannot become the second copy of a leak",
        "use_when": "a detection must be recorded in a report, a ticket or a shared document",
        "avoid_when": "the finding is a path with no value attached, such as a file missing an exclusion rule",
        "tags": ["scope", "evidence", "redaction"],
        "steps": [
            "Record the path, the line or offset, the class assigned by the rule and a hash or prefix of the value, never the value itself.",
            "For personal records, record presence and a hash of a non-identifying region rather than any identifying field.",
            "Keep the raw capture in a file excluded from version control with a defined deletion date from the retention rule.",
            "Number each evidence entry and link it to the boundary version and the rule version that produced it.",
            "Verify before sharing that the evidence file contains no value that would grant access or identify a person.",
            "Delete transient captures once the report is filed, keeping only what the disclosure record requires.",
        ],
        "signals": [
            "A report or ticket contains a complete credential because it was pasted for context",
            "A raw scan output file sits in a tracked directory",
            "Evidence has no deletion date and will outlive its purpose",
            "An evidence entry cannot be tied to the rule version that produced it",
        ],
        "patterns": [
            (
                "Evidence line",
                "E-014 | path: config/settings.py | line: 42 | class: cloud-key | sha256: 3f2a... | rule v7 | boundary v3",
            ),
            (
                "Value substitute",
                "prefix 4 chars plus a hash proves sameness and allows later rotation checks without ever storing the secret",
            ),
            (
                "Retention note",
                "raw capture deleted on <date>; report entry retained; both dates recorded when the entry is written",
            ),
        ],
        "pitfalls": [
            "Pasting a value into a ticket that a vendor portal will retain permanently",
            "Keeping raw outputs in the repository, which recreates the exposure being assessed",
            "Omitting the rule version, so a later reader cannot tell which rule produced the line",
        ],
        "done_when": [
            "No archived evidence contains a usable credential or an identifying personal field",
            "Every evidence entry carries a number, a rule version and a boundary version",
        ],
        "refs": [
            "[NIST SP 800-53 - Audit record content](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)",
            "[OWASP - Sensitive data in logs](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)",
        ],
        "meta": {"phase": "scope"},
    },
    {
        "slug": "report-destination-safety",
        "title": "Report Destination Safety",
        "summary": "Decide where findings may be written before writing any, because the destination determines whether your report becomes a second copy of every secret it names",
        "use_when": "findings will be shared and the destination, its retention and its audience have not been agreed",
        "avoid_when": "the owner supplies a private channel with stated retention and an audience you have confirmed",
        "tags": ["scope", "reporting", "handling"],
        "steps": [
            "Name the destination for findings: private repository, internal ticket, encrypted channel or in-person, with its retention rule.",
            "Confirm who can read that destination, since an internal audience and a vendor audience change what you may include.",
            "Check whether the destination indexes content for search, which turns a redacted report into a discoverable one if redaction slips.",
            "Agree what happens after closure: deletion, archival or retention, with a date attached to each.",
            "Record the destination and its rules beside the boundary document so every later finding inherits them.",
            "Before first write, send one synthetic entry to the destination and inspect exactly what was stored and where.",
        ],
        "signals": [
            "Findings are headed for a public repository by default",
            "A ticket system retains deleted attachments",
            "A shared document is indexed by an enterprise search nobody remembered",
            "No one can say what happens to findings after closure",
        ],
        "patterns": [
            (
                "Destination record",
                "channel: internal ticket | audience: security + owning team | retention: 90 days post-closure | indexed: yes | search: redacted only",
            ),
            (
                "Test write",
                "send one synthetic finding first, then inspect what was stored, indexed and retained; that observation is the basis for the decision",
            ),
            (
                "Closure rule",
                "on closure: raw captures deleted at date X, report retained to date Y, both recorded when the finding is opened",
            ),
        ],
        "pitfalls": [
            "Defaulting to a public issue tracker because it is the most convenient place to write",
            "Assuming a deletion in a ticket system also removes attachments and search copies",
            "Letting an enterprise search index a report containing partially redacted values",
        ],
        "done_when": [
            "A destination record names audience, retention, indexing behaviour and closure handling",
            "A synthetic test write has been inspected before any real finding is recorded",
        ],
        "refs": [
            "[OWASP - Information disclosure guidance](https://owasp.org/www-project-web-security-testing-guide/)",
            "[ISO 27002 - Information handling controls](https://www.iso.org/standard/75652.html)",
        ],
        "meta": {"phase": "scope"},
    },
    {
        "slug": "repository-surface-enumeration",
        "title": "Repository Surface Enumeration",
        "summary": "Map every place in a repository that can carry a value: source, configuration, fixtures, generated output and history, so a scan does not quietly skip the class most likely to hold one",
        "use_when": "a repository is in scope and no one has listed which of its regions are readable and which contain data",
        "avoid_when": "the owner supplies a manifest stating each region's contents and data class",
        "tags": ["discover", "inventory", "repository"],
        "steps": [
            "List the regions that exist: tracked source, untracked local files, generated output, vendored dependencies, archives and history.",
            "Classify each region by likelihood of holding values: configuration and fixtures high, vendored code low but large.",
            "Check whether generated output is scanned at all, since build directories are frequently excluded by an old ignore rule.",
            "Note archives and bundles, because a compressed copy will never match a pattern that reads plain text.",
            "Include commit history in the plan, since a removed value usually still exists there.",
            "Write the surface as a table of region, class, scanned or not and the reason for any skip.",
        ],
        "signals": [
            "An ignore rule excludes build output from an era when it contained no data",
            "Archives are present but the tool reads only plain text",
            "History is not part of the scan plan even though values were removed last quarter",
            "Untracked local files exist that no plan step covers",
        ],
        "patterns": [
            (
                "Surface row",
                "region | class | scanned | reason\ntracked source | internal | yes | -\nbuild output | internal | no | ignore rule from 2023\narchives | unknown | no | tool reads plain text only\nhistory | internal | planned | remediation check",
            ),
            (
                "Skip discipline",
                "every unscanned region carries a written reason; an unscanned region with no reason is a gap, not a decision",
            ),
            (
                "Archive note",
                "list archive formats present and state whether they were expanded or deliberately skipped",
            ),
        ],
        "pitfalls": [
            "Accepting an inherited ignore rule without checking what it excludes today",
            "Reporting coverage over tracked files while archives and history went unread",
            "Scanning vendored dependencies so noisily that real findings are buried",
        ],
        "done_when": [
            "A surface table covers every region with class, scanned status and reason for any skip",
            "Archives and history each have an explicit decision recorded",
        ],
        "refs": [
            "[OWASP - Source code analysis guidance](https://owasp.org/www-project-web-security-testing-guide/)",
            "[CWE-527 - Version control information exposure](https://cwe.mitre.org/data/definitions/527.html)",
        ],
        "meta": {"phase": "discover"},
    },
    {
        "slug": "high-entropy-string-detection",
        "title": "High-Entropy String Detection",
        "summary": "Use entropy as a candidate generator rather than as a verdict, because an entropy threshold alone will fill the report with hashes and identifiers nobody can act on",
        "use_when": "scanning content where the value format is unknown and a broad first pass is needed",
        "avoid_when": "every class in scope has a known format, which makes format matching both tighter and cheaper",
        "tags": ["discover", "entropy", "detection"],
        "steps": [
            "Choose a minimum length and an alphabet for the candidate pass, and record both with the entropy measure you used.",
            "Exclude strings that are obviously not secrets: hashes of known length, identifiers with a readable prefix, checksums.",
            "Rank candidates by entropy and length so the review order puts the most likely values first.",
            "Sample the top, middle and bottom of the ranked list to estimate how much of it is noise before reviewing in full.",
            "Record the candidate count and the sample hit rate so the rule's precision is stated rather than assumed.",
            "Feed the survivors into classification rather than reporting an entropy hit as a finding on its own.",
        ],
        "signals": [
            "The candidate list is dominated by hashes, uuids and identifiers",
            "No sample was taken, so nobody knows the precision of the pass",
            "The threshold was chosen after looking at the data that it then validated",
            "Entropy hits are being reported directly as findings without classification",
        ],
        "patterns": [
            (
                "Pass record",
                "min length: 24 | alphabet: base64/hex | measure: Shannon bits per char >= 4.0 | candidates: 812 | sampled hit rate: 6%",
            ),
            (
                "Noise exclusions",
                "drop: sha256-length hex, uuid-shaped, well-known identifier prefixes; record each exclusion with its rule",
            ),
            (
                "Ranking order",
                "sort by entropy then length so review starts where a real value is most likely and stops when the sample says the tail is empty",
            ),
        ],
        "pitfalls": [
            "Reporting raw entropy hits as findings, which trains readers to ignore the report",
            "Tuning the threshold against the same content it will be judged on",
            "Ignoring sample hit rate and reviewing thousands of candidates by hand",
        ],
        "done_when": [
            "Thresholds, alphabet, exclusions and the measured sample hit rate are recorded",
            "No entropy hit appears in the report without a classification step after it",
        ],
        "refs": [
            "[OWASP - Secret detection patterns](https://owasp.org/www-project-web-security-testing-guide/)",
            "[CWE-331 - Insufficient entropy](https://cwe.mitre.org/data/definitions/331.html)",
        ],
        "meta": {"phase": "discover"},
    },
    {
        "slug": "known-format-token-identification",
        "title": "Known-Format Token Identification",
        "summary": "Match the documented prefixes and lengths of well-known credentials first, because a format match is cheap, precise and far easier to rank than an entropy hit",
        "use_when": "scanning content for credentials issued by platforms that publish a recognisable format",
        "avoid_when": "the secrets in scope are self-generated values with no published format at all",
        "tags": ["discover", "detection", "tokens"],
        "steps": [
            "List the platforms whose credentials could appear in this corpus and look up each documented prefix and length.",
            "Encode those formats as rules with the fixture set from the synthetic-first step, and require every fixture to hit.",
            "Run the format pass before the entropy pass so precise candidates are reviewed first.",
            "Handle prefixes that overlap with ordinary words by requiring an exact prefix match plus a length bound.",
            "Record a hit with its platform, the path and line, and the rule version, never the value.",
            "Note formats you looked for and did not find, so absence is a recorded result rather than an omission.",
        ],
        "signals": [
            "A format rule fires on ordinary prose because the prefix check has no length bound",
            "Credentials from a platform in use across the company are absent from the rule list",
            "A rule passes without ever having been tested against a planted fixture",
            "Overlapping prefixes produce a large false-positive group in comments and docs",
        ],
        "patterns": [
            (
                "Format rule",
                "platform: version-control token | prefix: ghp_ | length: 36..44 | fixture: ghp_fixture0000000000000000000000 | expected: hit",
            ),
            (
                "Review order",
                "format hits first, then entropy survivors, then structural matches; the order is chosen by precision, not by ease of writing the rule",
            ),
            (
                "Absence record",
                "formats checked and not found: <list>; recorded so a later reader knows they were searched for",
            ),
        ],
        "pitfalls": [
            "Writing format rules from memory and getting a length or prefix subtly wrong",
            "Reporting a prefix hit in prose where a length bound would have excluded it",
            "Never recording which formats were searched, so absence is indistinguishable from not looking",
        ],
        "done_when": [
            "Every platform rule has a fixture that hits and a length bound that keeps prose quiet",
            "Formats searched but not found are listed as a recorded result",
        ],
        "refs": [
            "[OWASP - Secrets in source code](https://owasp.org/www-project-web-security-testing-guide/)",
            "[CWE-798 - Use of hard-coded credentials](https://cwe.mitre.org/data/definitions/798.html)",
        ],
        "meta": {"phase": "discover"},
    },
    {
        "slug": "assignment-and-interpolation-surface",
        "title": "Assignment and Interpolation Surface",
        "summary": "Find the structural places where a value is bound to a name, because that is where a credential lives even when its format is unfamiliar",
        "use_when": "scanning source and configuration where the credential format is unknown or self-generated",
        "avoid_when": "format rules already cover every credential class the corpus can contain",
        "tags": ["discover", "detection", "structure"],
        "steps": [
            "List the assignment shapes that bind secrets: direct assignment, environment lookup, connection string, header construction and template interpolation.",
            "Search for those shapes by structure and by key name rather than by value shape.",
            "Rank by key name, since a variable called password or token is a stronger signal than an arbitrary identifier.",
            "Handle indirection, where the value is fetched from a store at runtime and the file only names the key.",
            "Record which shapes were searched and which the corpus contains, so coverage is stated rather than implied.",
            "Pass survivors to classification alongside the format and entropy candidates.",
        ],
        "signals": [
            "A value is fetched from a store at runtime and only the name appears in the file",
            "A connection string assembles credentials from parts rather than storing one literal",
            "Key-name searching missed a credential because the name is an abbreviation",
            "Template interpolation hides a value inside a larger string",
        ],
        "patterns": [
            (
                "Shape list",
                "key = literal | getenv(\"KEY\") | url with user:pass | header with bearer | string template embedding a variable",
            ),
            (
                "Key-name ranking",
                "strong names: password, secret, token, api_key, private, credential; weak names: value, data, config, id",
            ),
            (
                "Indirection note",
                "when a file only names a store key, record that as a reference finding rather than a value finding, since the value lives elsewhere",
            ),
        ],
        "pitfalls": [
            "Reporting a store-key reference as though it were the credential itself",
            "Missing indirection entirely and concluding the corpus holds no credentials",
            "Treating every assignment to a weakly named variable as a candidate and burying the real ones",
        ],
        "done_when": [
            "Each assignment shape searched is listed with whether the corpus contains it",
            "Indirection findings are labelled as references, separate from value findings",
        ],
        "refs": [
            "[OWASP - Code quality and secret handling](https://owasp.org/www-project-application-security-verification-standard/)",
            "[CWE-798 - Hard-coded credentials](https://cwe.mitre.org/data/definitions/798.html)",
        ],
        "meta": {"phase": "discover"},
    },
    {
        "slug": "url-embedded-credential-detection",
        "title": "URL-Embedded Credential Detection",
        "summary": "Find credentials carried inside connection strings, callbacks and repository URLs, a form that survives every value-shape rule because it is hidden inside a structure nobody greps for",
        "use_when": "the corpus contains URLs, connection strings or remote endpoints of any kind",
        "avoid_when": "the corpus is confirmed free of URLs and remote endpoints entirely",
        "tags": ["discover", "urls", "credentials"],
        "steps": [
            "Extract every URL-shaped token from the corpus, including those inside quotes, connection strings and command lines.",
            "Parse each into components and look for user info before the host, which is where embedded credentials live.",
            "Record the scheme, the presence of a password component and the target host, never the credential itself.",
            "Check whether the URL appears in a tracked file, since that determines whether history removal is also needed.",
            "Note URLs that carry a token in a query parameter instead of user info, which is the other common placement.",
            "Pass each hit to classification with its placement recorded as userinfo or query.",
        ],
        "signals": [
            "A connection string embeds a user and password before the host",
            "A repository remote URL carries a token in place of a password",
            "A callback URL carries an access token as a query parameter",
            "An image or webhook URL embeds credentials to authenticate a fetch",
        ],
        "patterns": [
            (
                "Extraction pattern",
                "scheme://user:password@host -> record scheme, presence of userinfo, host; never store the credential component",
            ),
            (
                "Query variant",
                "?access_token=... or ?key=... -> record parameter name and the file that contains it",
            ),
            (
                "Placement field",
                "placement: userinfo | query | fragment; each implies a different rotation target and a different log to check",
            ),
        ],
        "pitfalls": [
            "Grep-ing for a colon-slash-slash and missing URLs assembled at runtime from parts",
            "Recording the full URL in the report, which re-publishes the credential it contains",
            "Fixing the value without noticing that history still holds the original",
        ],
        "done_when": [
            "Every URL-shaped token parsed yields a placement verdict with host recorded and credential omitted",
            "Whether the URL appears in tracked history is recorded per hit",
        ],
        "refs": [
            "[RFC 3986 - URI userinfo component](https://www.rfc-editor.org/rfc/rfc3986)",
            "[OWASP - Credential exposure guidance](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "discover"},
    },
    {
        "slug": "configuration-and-dotfile-surface",
        "title": "Configuration and Dotfile Surface",
        "summary": "Sweep the configuration and dotfile region deliberately, because these files are small, high-value and routinely left out of a scan by a default include rule",
        "use_when": "a repository or workstation tree is in scope and configuration files have not been explicitly included",
        "avoid_when": "the plan already lists configuration files by path and confirms the tool reads them",
        "tags": ["discover", "configuration", "files"],
        "steps": [
            "Enumerate configuration files by name and by extension, including hidden dotfiles that a default include may skip.",
            "Check whether the tool's default file selection actually opens them, and add them explicitly when it does not.",
            "Look for environment files and their templates, since the template sometimes carries the real value instead of a placeholder.",
            "Inspect local override files that are untracked but present, since those often hold developer credentials.",
            "Record which configuration paths were read and which were skipped with the reason.",
            "Pass content from these files to classification with the file region recorded, because region changes the remediation path.",
        ],
        "signals": [
            "An environment template carries a real value where a placeholder belongs",
            "Hidden files are not opened by the tool's default selection",
            "An untracked local override holds a credential that the tracked template does not",
            "A configuration path was skipped by a default rule nobody chose deliberately",
        ],
        "patterns": [
            (
                "Region row",
                "path | tracked | read | finding class\n.env | no | yes | secret\n.env.example | yes | yes | placeholder ok\ndotfile.local | no | yes | secret, developer machine only",
            ),
            (
                "Template check",
                "compare each template against its real counterpart: a value where a placeholder belongs is a finding even in a tracked file",
            ),
            (
                "Skip reason",
                "any configuration path not read carries a written reason; absence of a reason means the plan has a hole",
            ),
        ],
        "pitfalls": [
            "Scanning only tracked files and missing the untracked local override that holds the real value",
            "Assuming a template is safe because the file name says example or sample",
            "Letting default file selection decide which configuration is read",
        ],
        "done_when": [
            "Configuration paths are listed with tracked, read and finding class per row",
            "Every unread path carries a written reason rather than no reason at all",
        ],
        "refs": [
            "[OWASP - Configuration and secrets management](https://owasp.org/www-project-web-security-testing-guide/)",
            "[CWE-312 - Cleartext storage of sensitive information](https://cwe.mitre.org/data/definitions/312.html)",
        ],
        "meta": {"phase": "discover"},
    },
    {
        "slug": "generated-artifact-scan",
        "title": "Generated Artifact Scan",
        "summary": "Scan build output, bundles and archives as first-class content, since generated files commonly carry the very values the source carefully does not",
        "use_when": "a build, bundle or archive exists inside an in-scope tree and has not been confirmed clean",
        "avoid_when": "the owner confirms generated output contains no values and a scan of it proves the claim",
        "tags": ["discover", "artifacts", "build"],
        "steps": [
            "List the generated regions present: build directories, bundles, source maps, container layers and archives.",
            "Confirm whether the tool reads them, and expand or extract the ones it does not when the boundary permits.",
            "Scan source maps separately, since they reconstruct original content that may carry values removed from the built file.",
            "Check embedded images, fonts and other binaries for appended data, which is rare but cheap to rule out.",
            "Record which artifacts were read, extracted or skipped, with a reason for every skip.",
            "Feed hits to classification with the region recorded, because an artifact finding usually implies the source once held it too.",
        ],
        "signals": [
            "Build output is excluded by an ignore rule that predates the current data flows",
            "Source maps exist for a build whose originals were cleaned",
            "An archive inside the tree was never expanded",
            "A value appears in built output but not in the current source",
        ],
        "patterns": [
            (
                "Artifact row",
                "artifact | type | read | finding\nbundle.js | built | yes | none\nbundle.js.map | source map | yes | value present, source clean\nimage.png | binary | skipped, reason: no appended data expected",
            ),
            (
                "Implied-history rule",
                "a value in an artifact with clean source implies the source held it once; write that as a history question, not as a separate discovery",
            ),
            (
                "Skip reason",
                "every unread artifact carries a written reason so the coverage statement stays honest",
            ),
        ],
        "pitfalls": [
            "Accepting an inherited ignore rule for build output without checking what it hides today",
            "Cleaning the source and declaring the problem solved while the artifact still carries the value",
            "Scanning binaries by content rules that can never match and calling the region covered",
        ],
        "done_when": [
            "Every generated region has a read, extracted or skipped status with a reason",
            "At least one artifact region is confirmed scanned or explicitly excluded with justification",
        ],
        "refs": [
            "[CWE-527 - Version control and artifact exposure](https://cwe.mitre.org/data/definitions/527.html)",
            "[OWASP - Build and pipeline security](https://owasp.org/www-project-application-security-verification-standard/)",
        ],
        "meta": {"phase": "discover"},
    },
    {
        "slug": "log-and-telemetry-surface-scan",
        "title": "Log and Telemetry Surface Scan",
        "summary": "Sweep logs, traces and telemetry as their own region, because this is where a value appears even when every source file was written carefully",
        "use_when": "log files, traces or telemetry exports are inside the readable boundary",
        "avoid_when": "log content is excluded from the assessment in writing and no log data is readable",
        "tags": ["discover", "logs", "telemetry"],
        "steps": [
            "List the telemetry sources in scope: application logs, access logs, traces, crash dumps and analytics events.",
            "Sample across time rather than reading only the newest file, since the interesting line usually predates the current policy.",
            "Look for full request and response bodies, authorization headers and query strings recorded verbatim.",
            "Check whether structured logging serializes objects wholesale, which captures fields nobody intended to log.",
            "Record the sources read with the sample window, so coverage over time is stated.",
            "Pass hits to classification with the source recorded, because log remediation differs from code remediation.",
        ],
        "signals": [
            "A structured log line serializes an entire object including its credential field",
            "Authorization headers appear verbatim in an access log",
            "Only the newest log file was read while the interesting events are older",
            "A crash dump contains request state including a token",
        ],
        "patterns": [
            (
                "Source row",
                "source | window read | finding class\napp.log | 2026-10-01..28 | token in structured field\naccess.log | 2026-10-20..28 | authorization header verbatim\ncrash.dmp | not read, reason: binary dump out of boundary",
            ),
            (
                "Structural check",
                "look for whole-object serialization and interpolation of request context; both capture fields the author never meant to log",
            ),
            (
                "Time coverage",
                "record the sample window explicitly; a scan of only recent files cannot support a claim about older exposure",
            ),
        ],
        "pitfalls": [
            "Reading only the newest file and concluding the pipeline is clean",
            "Reporting a value in logs without tracing where it was logged from",
            "Treating a log finding as a code finding and fixing the wrong layer",
        ],
        "done_when": [
            "Telemetry sources are listed with the sample window read and any skip reason",
            "At least one structured or header finding is traced to the code that emitted it",
        ],
        "refs": [
            "[OWASP - Logging cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)",
            "[CWE-532 - Insertion of sensitive information into log file](https://cwe.mitre.org/data/definitions/532.html)",
        ],
        "meta": {"phase": "discover"},
    },
]