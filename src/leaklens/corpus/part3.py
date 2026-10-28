"""leaklens skills 31-50: confirm, harden and document phases."""

from __future__ import annotations

SKILLS: list[dict] = [
    {
        "slug": "format-plus-context-corroboration",
        "title": "Format Plus Context Corroboration",
        "summary": "Require a format match and a surrounding context signal before calling a candidate real, because either alone produces a report full of noise or one full of misses",
        "use_when": "candidates have been generated and each must be judged as a real value or a false positive",
        "avoid_when": "a candidate already has an independent confirmation that does not rely on its shape",
        "tags": ["confirm", "precision", "detection"],
        "steps": [
            "For each candidate record the format evidence: prefix, length and alphabet that matched.",
            "Record the context evidence: the key name it sits under, the file region and the surrounding code's use of it.",
            "Accept as a real value only when at least one format signal and one context signal agree.",
            "Log candidates rejected by this rule with the reason, so a later reader can see what was excluded and why.",
            "Sample the rejected set to check that real values are not being discarded by an over-strict context rule.",
            "Record precision for the rule as accepted over reviewed, so the rule's quality is a stated number.",
        ],
        "signals": [
            "A candidate matches format but sits under a key named example or sample",
            "A strong key name holds a value whose shape does not match any known format",
            "The rejected set was never sampled, so over-strict exclusion would go unnoticed",
            "No precision figure exists for a rule that determines what reaches the report",
        ],
        "patterns": [
            (
                "Two-signal rule",
                "accept only when format evidence and context evidence both hold; record both signals per candidate",
            ),
            (
                "Rejection log",
                "candidate #214 | format match: yes | context: key name 'example_password' | verdict: rejected | sampled later: clean",
            ),
            (
                "Precision figure",
                "accepted 18 of 61 reviewed -> precision 30%; stated with the rule version that produced it",
            ),
        ],
        "pitfalls": [
            "Accepting on format alone and filling the report with hashes and identifiers",
            "Accepting on key name alone and reporting every example value in the documentation",
            "Never sampling the rejected set, which is how a real secret gets tuned away",
        ],
        "done_when": [
            "Every accepted candidate records both format and context evidence",
            "A precision figure with the rule version is recorded and the rejected set has been sampled",
        ],
        "refs": [
            "[OWASP - Secret detection accuracy](https://owasp.org/www-project-web-security-testing-guide/)",
            "[CWE-798 - Use of hard-coded credentials](https://cwe.mitre.org/data/definitions/798.html)",
        ],
        "meta": {"phase": "confirm"},
    },
    {
        "slug": "near-miss-false-positive-taxonomy",
        "title": "Near-Miss False-Positive Taxonomy",
        "summary": "Name the categories of thing your rules mistake for secrets, because a labelled false positive can be excluded systematically while an unlabelled one keeps coming back",
        "use_when": "the same kinds of non-secret keep appearing as candidates across runs",
        "avoid_when": "the candidate set is already small enough that every rejection is judged individually",
        "tags": ["confirm", "false-positives", "precision"],
        "steps": [
            "Group rejected candidates by why they were rejected rather than reviewing them one at a time.",
            "Name each group concretely: content hashes, identifiers with readable prefixes, encoded fixtures, base64 data blobs.",
            "Write one exclusion rule per group and record which group each rule targets.",
            "Re-run against the fixture corpus to confirm each new exclusion still leaves real fixtures hitting.",
            "Track group counts over time so a growing group is visible rather than absorbed into a total.",
            "Keep one catch-all group for anything no rule explains, and review it before it grows large.",
        ],
        "signals": [
            "The same rejection reason is written out by hand many times in one run",
            "An exclusion rule was added that stopped a real fixture from hitting",
            "Group counts are never tracked, so a growing noise class is invisible",
            "Everything unexplained is discarded without a catch-all review",
        ],
        "patterns": [
            (
                "Group table",
                "group | count this run | exclusion rule | fixture still hits\ncontent hashes | 412 | length plus alphabet | yes\nreadable identifiers | 188 | prefix allow-list | yes\nbase64 blobs | 61 | entropy floor | yes",
            ),
            (
                "Rule-to-group binding",
                "every exclusion rule names the group it targets, so removing a rule later is a safe, scoped change",
            ),
            (
                "Catch-all review",
                "unexplained rejections are counted and sampled before each run; a growing catch-all means a new group is forming",
            ),
        ],
        "pitfalls": [
            "Writing one broad exclusion that silently removes a class of real findings",
            "Never re-running fixtures after adding an exclusion, which is how precision is bought with recall",
            "Letting the catch-all become a dumping ground where real values disappear",
        ],
        "done_when": [
            "Rejected candidates are grouped by reason with a named exclusion rule per group",
            "Every exclusion rule is confirmed to leave its fixtures hitting",
        ],
        "refs": [
            "[OWASP - Verification methodology](https://owasp.org/www-project-application-security-verification-standard/)",
            "[CWE-546 - Suspicious pattern evaluation](https://cwe.mitre.org/data/definitions/546.html)",
        ],
        "meta": {"phase": "confirm"},
    },
    {
        "slug": "deduplication-across-copies",
        "title": "Deduplication Across Copies",
        "summary": "Collapse one value found in many locations into a single finding with N rotation targets, so the report counts exposures rather than file lines",
        "use_when": "the same value or the same logical secret appears in more than one file or region",
        "avoid_when": "each finding is already unique by value and location",
        "tags": ["confirm", "deduplication", "reporting"],
        "steps": [
            "Group findings by a stable identity: the value hash, or the logical secret when a value was assembled differently in two places.",
            "For each group record every location, separating tracked files, artifacts, history and logs.",
            "Pick a canonical finding entry and cross-reference the other locations inside it rather than repeating the detail.",
            "Count locations as rotation targets, since each one must be handled for the rotation to be complete.",
            "Record how the copies were matched, so a reader can tell value identity from logical identity.",
            "Re-check after remediation that every location in the group has been handled, not only the canonical one.",
        ],
        "signals": [
            "One value appears in source, a log and an artifact and is reported as three unrelated findings",
            "Two locations hold the same secret assembled differently, so a literal match misses one",
            "Rotation was completed on the canonical location while another copy remained",
            "The report counts file lines rather than distinct exposures",
        ],
        "patterns": [
            (
                "Group entry",
                "identity: sha256 3f2a... | locations: 3 (src/client.py:18, log/app.log:902, build/bundle.js) | canonical: src/client.py:18 | rotation targets: 3",
            ),
            (
                "Match basis",
                "basis: value hash | logical match: same secret assembled at runtime in two files, matched by lookup name",
            ),
            (
                "Close-out rule",
                "the finding closes only when every listed location is verified handled; one outstanding location keeps it open",
            ),
        ],
        "pitfalls": [
            "Reporting duplicates as separate findings, which makes the exposure look larger and the fix incomplete",
            "Matching only on literal value and missing a copy assembled differently",
            "Closing a finding after the canonical location was fixed while other copies remain",
        ],
        "done_when": [
            "Each group has one canonical entry with all locations cross-referenced as rotation targets",
            "The match basis, value or logical, is recorded per group",
        ],
        "refs": [
            "[NIST SP 800-53 - Information consistency controls](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)",
            "[OWASP - Secrets management guidance](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "confirm"},
    },
    {
        "slug": "false-positive-rate-sampling",
        "title": "False-Positive Rate Sampling",
        "summary": "Measure what proportion of your report is noise by sampling, so precision is a number in the report rather than a feeling about the tool",
        "use_when": "a run produced a large candidate set and nobody has measured how much of it is real",
        "avoid_when": "the candidate set is small enough to review exhaustively, which removes the need to sample",
        "tags": ["confirm", "precision", "measurement"],
        "steps": [
            "Define the sample: a random selection from the accepted set, with the sample size recorded.",
            "Review each sampled entry against the two-signal rule and classify it real or false.",
            "Compute the real proportion and state it with the sample size, so a reader can judge the margin.",
            "Repeat for a second sample if the first is small enough that the result is unstable.",
            "Extrapolate to the full set only as an estimate, and label it an estimate with its sample basis.",
            "Feed the false entries found into the taxonomy so the measurement improves the rules.",
        ],
        "signals": [
            "No sample was taken and the report implies all entries are real",
            "A sample of three entries was used to claim a precision figure",
            "Extrapolation is presented as a count rather than as an estimate",
            "False entries found during sampling were not fed back into any rule",
        ],
        "patterns": [
            (
                "Sampling record",
                "sample size: 30 random from 418 accepted | real: 26 | precision: 87% +/- margin | rule version: v7",
            ),
            (
                "Extrapolation label",
                "estimate: roughly 54 real findings in 418, based on a sample of 30; stated as an estimate, never as a count",
            ),
            (
                "Feedback loop",
                "each false entry found in sampling is added to the taxonomy with a group name, then rules are re-run against fixtures",
            ),
        ],
        "pitfalls": [
            "Quoting a precision number without its sample size, which makes it meaningless",
            "Sampling only the top of the ranked list, where precision is highest by construction",
            "Finding false positives during sampling and adjusting nothing afterwards",
        ],
        "done_when": [
            "A precision figure with its sample size and rule version appears in the report",
            "False entries found during sampling are recorded in the taxonomy with a rule change",
        ],
        "refs": [
            "[OWASP - Measurement and verification guidance](https://owasp.org/www-project-application-security-verification-standard/)",
            "[NIST - Measurement discipline considerations](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)",
        ],
        "meta": {"phase": "confirm"},
    },
    {
        "slug": "value-never-used-verification",
        "title": "Value Never Used Verification",
        "summary": "Confirm a finding from local evidence alone and state in the report that the value was never presented anywhere, because using the credential to prove it exists changes the incident",
        "use_when": "a real value has been found and the temptation to test it exists",
        "avoid_when": "the owner explicitly commissions an active test and provides a controlled environment for it",
        "tags": ["confirm", "ethics", "method"],
        "steps": [
            "Confirm the finding from format, context and location evidence, all of which are local operations.",
            "Record explicitly in the evidence entry that the value was not presented to any endpoint.",
            "Where liveness matters, use only non-network evidence such as configuration, dates or companion metadata.",
            "If an active test were ever commissioned, record that commissioning separately from the finding itself.",
            "State the confirmation basis in the report so a reviewer knows exactly how the claim was established.",
            "Keep the value out of every artifact produced, since confirmation never requires writing it down.",
        ],
        "signals": [
            "Someone suggests trying the value against an endpoint to see if it works",
            "A report claims a credential is live without saying how that was established",
            "A value appears in a shell history from being typed during a test",
            "An active test was performed without a written commission",
        ],
        "patterns": [
            (
                "Confirmation basis",
                "basis: format match + key context + tracked location; network use: none; stated explicitly in the report entry",
            ),
            (
                "Liveness substitute",
                "judge from local evidence: config names the service, dates show recent use, companion metadata identifies the purpose",
            ),
            (
                "Commission record",
                "if an active test is commissioned: record who commissioned it, the environment and the date, as a separate entry",
            ),
        ],
        "pitfalls": [
            "Testing a credential against a live service to strengthen a report, which turns exposure into use",
            "Leaving the value in shell history while testing, which creates a second copy",
            "Writing that a credential is live without stating the evidence that supports it",
        ],
        "done_when": [
            "Every real-value finding records a confirmation basis and an explicit no-network-use statement",
            "Any active test is documented as separately commissioned with owner, environment and date",
        ],
        "refs": [
            "[NIST - Evidence-based assessment practice](https://csrc.nist.gov/publications/detail/sp/800-86/final)",
            "[OWASP - Ethical testing boundaries](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "confirm"},
    },
    {
        "slug": "temporal-staleness-assessment",
        "title": "Temporal Staleness Assessment",
        "summary": "Establish how old a finding is and whether it is still reachable, because an expired credential in history and a credential used this morning demand entirely different responses",
        "use_when": "a finding's age and continued validity have not been established from local evidence",
        "avoid_when": "the owner supplies current status for every credential the corpus could contain",
        "tags": ["confirm", "staleness", "triage"],
        "steps": [
            "Read file dates, commit dates and any embedded timestamps to establish when the value was written.",
            "Look for evidence of later removal, such as a rotation note, a change entry or an absent companion.",
            "Determine validity from local evidence only: expiry fields, rotation records or configuration that supersedes it.",
            "Rank stale and current findings separately, since a reader of the report triages them differently.",
            "Record the assessment date beside every staleness verdict, because validity is time-dependent.",
            "Flag findings where staleness could not be determined rather than assuming either way.",
        ],
        "signals": [
            "A finding carries no date, so a reader cannot tell whether it is current",
            "History holds a value that a later commit appears to have rotated",
            "Staleness could not be determined and the report implies it is live",
            "An expired value and a current one appear in the same priority band",
        ],
        "patterns": [
            (
                "Staleness record",
                "written: 2025-08-14 | last seen in history: 2026-02-02 | rotation evidence: none found | verdict: unknown, not assumed",
            ),
            (
                "Date basis",
                "verdict: current | stale | unknown; basis: embedded expiry, rotation note, or file and commit dates",
            ),
            (
                "Rank split",
                "current findings triage first; stale ones are batched; unknown ones go to the owner for a status answer",
            ),
        ],
        "pitfalls": [
            "Assuming an old value is dead because it is old, when nobody has checked",
            "Presenting an unknown staleness verdict as though it were current",
            "Ranking without the assessment date, which makes the claim stale the moment it is written",
        ],
        "done_when": [
            "Each finding carries a staleness verdict with its basis and the assessment date",
            "Unknown verdicts are listed for owner confirmation rather than assumed either way",
        ],
        "refs": [
            "[NIST SP 800-53 - Currency of information controls](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)",
            "[CWE-672 - Operation on a resource after expiration](https://cwe.mitre.org/data/definitions/672.html)",
        ],
        "meta": {"phase": "confirm"},
    },
    {
        "slug": "severity-ranking-by-class-and-reach",
        "title": "Severity Ranking by Class and Reach",
        "summary": "Rank findings from two axes at once, what the value is and who can already read it, because either axis alone systematically misorders the work",
        "use_when": "findings span several classes and locations and need a single priority order",
        "avoid_when": "the owner supplies a ranking policy that already covers both axes",
        "tags": ["confirm", "severity", "triage"],
        "steps": [
            "Assign each finding its class from the ladder: internal, personal or secret.",
            "Assign each finding its reach: local file, tracked repository, published repository or external destination.",
            "Rank on the pair, giving reach the deciding weight when two findings share a class.",
            "Record the two inputs beside the rank so a reader can re-derive it rather than accept it.",
            "Check the resulting order against the remediation order by copy, since a reachable secret should not sit below a stored personal record.",
            "Re-rank after any change in reach, because moving a file changes the priority without changing the value.",
        ],
        "signals": [
            "Findings are ranked by class alone, putting a stored secret above a published one",
            "A rank appears in the report with no record of its two inputs",
            "Reach changed after ranking, such as a file being published mid-assessment",
            "The ranking order and the remediation order disagree without explanation",
        ],
        "patterns": [
            (
                "Rank matrix",
                "class \\ reach | local | tracked | published\nsecret | high | critical | critical\npersonal | medium | high | critical\ninternal | low | medium | high",
            ),
            (
                "Input record",
                "finding E-004 | class: secret | reach: published repository | rank: critical | inputs recorded for re-derivation",
            ),
            (
                "Re-rank trigger",
                "a reach change during the assessment triggers an immediate re-rank, noted with the time it happened",
            ),
        ],
        "pitfalls": [
            "Ranking purely on class, which buries the published finding under stored ones",
            "Presenting a rank without its inputs, so nobody can challenge or reproduce it",
            "Never re-ranking when a file moves from local to published during the work",
        ],
        "done_when": [
            "Every finding records class, reach and the rank derived from both",
            "The ranking order is reconciled with the remediation order, or the difference is explained",
        ],
        "refs": [
            "[OWASP - Risk rating methodology](https://owasp.org/www-community/OWASP_Risk_Rating_Methodology)",
            "[CVSS - Qualitative severity mapping](https://www.first.org/cvss/)",
        ],
        "meta": {"phase": "confirm"},
    },
    {
        "slug": "independent-second-reader-review",
        "title": "Independent Second Reader Review",
        "summary": "Have a second person re-derive a sample of your classifications without seeing your reasoning, because agreement on the easy cases proves nothing about the hard ones",
        "use_when": "the finding set is large enough that a single reader's judgement drives the whole report",
        "avoid_when": "the finding set is a handful of entries reviewed jointly as they were found",
        "tags": ["confirm", "review", "precision"],
        "steps": [
            "Select a sample covering every class and both high- and low-confidence findings, with the sample size recorded.",
            "Give the second reader the evidence entries without your classification or rank.",
            "Have them classify and rank each entry independently using the same ladder.",
            "Compare and record agreement as a proportion, naming each disagreement with both readings.",
            "Resolve disagreements by referring to the ladder text rather than by preference, and amend the ladder if it was ambiguous.",
            "Feed each ambiguity found back into the ladder so the next run starts from a clearer rule.",
        ],
        "signals": [
            "Only the obvious findings were reviewed, so agreement says nothing about the hard ones",
            "The second reader saw your reasoning first, which anchors their judgement",
            "Disagreements were resolved by deferring to the original author",
            "An ambiguity found during review was never written back into the ladder",
        ],
        "patterns": [
            (
                "Review record",
                "sample: 18 of 418, spanning all classes | agreement: 14/18 (78%) | disagreements: 4, each with both readings",
            ),
            (
                "Blind rule",
                "the second reader receives evidence only, never the classification; seeing your rank first turns review into confirmation",
            ),
            (
                "Ladder feedback",
                "disagreement caused by ambiguous ladder text -> the ladder text changes in the same change that resolves the finding",
            ),
        ],
        "pitfalls": [
            "Reviewing only the easy findings and reporting a high agreement figure",
            "Settling a disagreement by deferring to the first reader rather than to the ladder",
            "Finding an ambiguity and leaving it for the next assessment to rediscover",
        ],
        "done_when": [
            "A blind sample spanning all classes has an agreement figure with each disagreement recorded",
            "Ambiguities found are written back into the ladder text",
        ],
        "refs": [
            "[NIST - Quality review considerations](https://csrc.nist.gov/publications/detail/sp/800-86/final)",
            "[OWASP - Verification methodology](https://owasp.org/www-project-application-security-verification-standard/)",
        ],
        "meta": {"phase": "confirm"},
    },
    {
        "slug": "remediation-readiness-check",
        "title": "Remediation Readiness Check",
        "summary": "Verify before reporting that every finding has an owner, a destination and a stated fix, so the report hands over work rather than observations",
        "use_when": "the finding set is complete and about to be handed to the owning team",
        "avoid_when": "findings are delivered to an audience that supplies their own owners and fixes",
        "tags": ["confirm", "handover", "remediation"],
        "steps": [
            "Attach an owner to every finding, or mark it unowned and escalate, because an unowned finding does not get fixed.",
            "State the fix for each: rotate, remove, redact, restrict reach, or accept with a reason.",
            "Confirm each fix names its target locations from the deduplicated group, not only the canonical file.",
            "Check that reach-reducing steps, such as unpublishing, are included where reach drove the rank.",
            "Record the expected verification for each fix, so closure has a defined test rather than a claim.",
            "List findings that cannot yet be fixed with the blocker, since an unfixable finding needs a decision, not a status.",
        ],
        "signals": [
            "A finding has no owner and no stated fix",
            "The fix names one location while the group holds three",
            "A reach-driven rank has no reach-reducing step attached",
            "Closure has no defined verification, only an assertion that it was done",
        ],
        "patterns": [
            (
                "Readiness row",
                "finding | owner | fix | targets | verification\nE-004 | platform | rotate + unpublish | 3 locations | new value absent from re-scan",
            ),
            (
                "Fix classes",
                "rotate (value changes) | remove (file changes) | redact (report changes) | restrict reach (location changes) | accept with reason",
            ),
            (
                "Blocked list",
                "blocked finding | blocker | who can unblock | needed decision; listed so it is escalated rather than left in a backlog",
            ),
        ],
        "pitfalls": [
            "Handing over observations and calling the assessment complete",
            "Rotating the canonical location while two group locations keep the old value",
            "Letting a blocked finding sit in the list without naming who can unblock it",
        ],
        "done_when": [
            "Every finding has an owner, a fix class, its full target list and a defined verification",
            "Blocked findings name their blocker and the person who can unblock them",
        ],
        "refs": [
            "[OWASP - Remediation guidance](https://owasp.org/www-project-web-security-testing-guide/)",
            "[NIST SP 800-40 - Patch and configuration management](https://csrc.nist.gov/pubs/sp/800/40/r4/final)",
        ],
        "meta": {"phase": "confirm"},
    },
    {
        "slug": "rotation-before-publication",
        "title": "Rotation Before Publication",
        "summary": "Rotate every live value before any report that could be read more widely than intended, because publication is irreversible while rotation is not",
        "use_when": "a report naming live values is about to move to a destination with a wider audience",
        "avoid_when": "the finding set contains only internal references and no live values",
        "tags": ["harden", "rotation", "disclosure"],
        "steps": [
            "Identify which findings carry live values rather than internal references, using the class and reach record.",
            "Sequence rotation ahead of publication, starting with the highest-ranked reachable values.",
            "Confirm each rotation through the defined verification, which for a value is usually a re-scan showing absence.",
            "Check that every group location was updated, not only the canonical file, before treating a rotation as done.",
            "Only after rotations verify does the report move to the agreed destination.",
            "Record the order performed and the verification result for each, so the sequence can be audited.",
        ],
        "signals": [
            "A report is being shared while live values it names are still valid",
            "Rotation was performed on one location while other group locations still hold the value",
            "No verification step exists, so a rotation is a claim rather than a result",
            "Publication preceded rotation because the deadline was closer than the fix",
        ],
        "patterns": [
            (
                "Sequence record",
                "1. rank reachable live values  2. rotate each  3. verify by re-scan  4. confirm all group locations  5. publish report",
            ),
            (
                "Verification",
                "for a value: re-scan shows the value absent everywhere it appeared; for a file: re-read shows redaction applied",
            ),
            (
                "Order evidence",
                "rotation timestamps precede publication timestamp; both recorded so the order is provable",
            ),
        ],
        "pitfalls": [
            "Publishing first and rotating afterwards because the report was already written",
            "Calling a rotation complete when only the canonical location was changed",
            "Recording no verification, so nobody can tell later whether the value actually died",
        ],
        "done_when": [
            "Every live finding rotates and verifies before the report reaches a wider audience",
            "Rotation and publication timestamps are recorded in the order they occurred",
        ],
        "refs": [
            "[NIST SP 800-57 - Key rotation](https://csrc.nist.gov/pubs/sp/800/57/r5/final)",
            "[OWASP - Coordinated disclosure guidance](https://owasp.org/www-project-vulnerability-disclosure/)",
        ],
        "meta": {"phase": "harden"},
    },
    {
        "slug": "history-rewrite-and-verification",
        "title": "History Rewrite and Verification",
        "summary": "Remove a value from history deliberately and then prove it is gone, because removing a file from the working tree changes nothing about what a clone still receives",
        "use_when": "a live value was found in tracked history and remains retrievable from a clone",
        "avoid_when": "the value never entered history or the repository has no shared history to rewrite",
        "tags": ["harden", "history", "git"],
        "steps": [
            "Confirm from the finding record that the value exists in history, not only in the working tree.",
            "Notify collaborators that history will be rewritten and agree a window, since clones will need re-cloning.",
            "Choose the rewrite scope: one file, one path or every occurrence, based on the deduplicated group's location list.",
            "Perform the rewrite and then re-scan history for the value hash to confirm absence rather than trusting the tool's report.",
            "Expire any cached copies: run clones, mirrors, artifact storage and any service that indexed the old history.",
            "Record the rewrite, the verification scan and the caches cleared, each with a date.",
        ],
        "signals": [
            "A value was deleted from the tree and the issue was closed without a history check",
            "A rewrite was performed but no independent re-scan confirmed the value is gone",
            "A mirror or CI cache still serves the pre-rewrite history",
            "No window was agreed, so collaborators lost work when their clones diverged",
        ],
        "patterns": [
            (
                "Verification scan",
                "re-scan history by value hash -> zero matches; the zero is the evidence, recorded with the date and the scan scope",
            ),
            (
                "Cache list",
                "caches to clear: local clones, remote mirrors, CI caches, indexed search, artifact storage; each marked done or not applicable",
            ),
            (
                "Window note",
                "rewrite window announced at <time>; collaborators re-cloned by <time>; recorded so fallout is visible",
            ),
        ],
        "pitfalls": [
            "Deleting a file and declaring the exposure resolved while history still serves it",
            "Trusting a rewrite tool's success message without an independent hash scan",
            "Leaving mirrors and caches in place, which keep serving the value after the rewrite",
        ],
        "done_when": [
            "An independent re-scan of history returns zero matches for the value hash",
            "Every cache and mirror is recorded as cleared or not applicable with a date",
        ],
        "refs": [
            "[CWE-527 - Version control information exposure](https://cwe.mitre.org/data/definitions/527.html)",
            "[OWASP - Repository hygiene guidance](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "harden"},
    },
    {
        "slug": "exclusion-and-ignore-hygiene",
        "title": "Exclusion and Ignore Hygiene",
        "summary": "Review every ignore and exclusion rule against what the tree actually contains today, since an exclusion written years ago is the most common reason a scan reports clean",
        "use_when": "a scan's coverage is in doubt or an exclusion rule predates the current data flows",
        "avoid_when": "exclusions are documented, current and each carries a written reason",
        "tags": ["harden", "configuration", "coverage"],
        "steps": [
            "List every ignore and exclusion rule in effect, with where it is defined and when it was last reviewed.",
            "For each rule, list what it currently hides by running the tree against it rather than by reading the pattern.",
            "Flag rules that hide regions now containing data, especially build output, exports and local overrides.",
            "Replace broad patterns with narrower ones, or keep the broad pattern with a written reason beside it.",
            "Re-run the scan with rules adjusted and record the delta in candidates, which shows what the rules were hiding.",
            "Add the rule list to the assessment evidence so a later reader can see what was and was not read.",
        ],
        "signals": [
            "An exclusion rule dates from before a data flow was introduced",
            "A rule hides a region that a manual spot-check shows contains values",
            "No one can say when exclusion rules were last reviewed",
            "Removing a rule produces a large candidate delta nobody expected",
        ],
        "patterns": [
            (
                "Rule review",
                "rule: build/** | defined: 2023 | hides: 412 files | now contains data: yes | action: narrow to build/**/assets",
            ),
            (
                "Delta measure",
                "candidates with rules as-is: 418 | candidates with reviewed rules: 691 | delta 273 was hidden by exclusions",
            ),
            (
                "Reason rule",
                "every kept broad rule carries a written reason recorded with the rule, not in a separate document",
            ),
        ],
        "pitfalls": [
            "Reading a pattern and assuming you know what it hides without running it against the tree",
            "Narrowing rules without measuring the delta, so the effect stays unknown",
            "Documenting reasons elsewhere where nobody reviewing a rule will find them",
        ],
        "done_when": [
            "Every exclusion rule has a current hides-list and a reason or a narrowed pattern",
            "The candidate delta from reviewing rules is recorded in the evidence",
        ],
        "refs": [
            "[OWASP - Configuration review guidance](https://owasp.org/www-project-application-security-verification-standard/)",
            "[CWE-693 - Protection mechanism failure](https://cwe.mitre.org/data/definitions/693.html)",
        ],
        "meta": {"phase": "harden"},
    },
    {
        "slug": "pre-commit-and-cicd-secret-gate",
        "title": "Pre-Commit and CICd Secret Gate",
        "summary": "Put the detection where a value is created, at commit time and in the pipeline, because an assessment finds what a gate would have blocked months earlier",
        "use_when": "values have reached history and nothing currently stops the next one",
        "avoid_when": "a gate already runs at commit and in the pipeline with fixtures proving it works",
        "tags": ["harden", "prevention", "pipeline"],
        "steps": [
            "Choose the enforcement points: commit time for the fast feedback, pipeline for the authoritative block.",
            "Encode the same rules at both points so a bypassed local hook does not also bypass the pipeline.",
            "Plant fixtures in the fixture corpus and require the gate to block each one, proving the gate works.",
            "Decide the response on a hit: block the commit, or warn with a required acknowledgement, and record which.",
            "Ensure the gate reports a path and a rule, never the value, so the gate's own output is safe to read.",
            "Record coverage: which repositories, which pipelines and which remain without a gate.",
        ],
        "signals": [
            "A local hook exists but the pipeline has no equivalent check",
            "The gate has never been tested against a planted fixture",
            "A gate hit prints the value into the console output",
            "Some repositories remain ungated with no record of that fact",
        ],
        "patterns": [
            (
                "Gate record",
                "point: pre-commit + pipeline | rules: same version | fixture tested: yes (4 of 4 blocked) | on hit: block | output: path and rule only",
            ),
            (
                "Fixture proof",
                "plant each fixture, attempt a commit, require the block; the block message is the evidence the gate works",
            ),
            (
                "Coverage list",
                "gated: 12 repositories | ungated: 3, each named; the named list is the work item",
            ),
        ],
        "pitfalls": [
            "Installing only a local hook, which any contributor can bypass or forget to install",
            "Shipping a gate that has never been proven to block anything",
            "Letting the gate print the value it just caught into a log the whole company can read",
        ],
        "done_when": [
            "Gates run at commit and in the pipeline with the same rules and fixture proof of blocking",
            "Ungated repositories are named as a list rather than omitted",
        ],
        "refs": [
            "[OWASP - CI/CD security guidance](https://owasp.org/www-project-application-security-verification-standard/)",
            "[CWE-798 - Use of hard-coded credentials](https://cwe.mitre.org/data/definitions/798.html)",
        ],
        "meta": {"phase": "harden"},
    },
    {
        "slug": "centralized-secret-storage-migration",
        "title": "Centralized Secret Storage Migration",
        "summary": "Move values out of files into a store with access control and audit, then verify none remain, because removing a value is only half the fix",
        "use_when": "values live in files and configuration because no store exists to hold them",
        "avoid_when": "a store is already in use and files reference it without embedding values",
        "tags": ["harden", "secrets-management", "migration"],
        "steps": [
            "List every value found, its locations and its owning application, from the deduplicated group list.",
            "Stand up or select the store and confirm it has access control, audit logging and per-environment separation.",
            "Move each value to the store and change the reading code to fetch it, keeping one change per value so it can be reviewed.",
            "After each move, re-run the scan against that location to confirm the value is absent from the file.",
            "Handle rotation for values that must change once they are out of the file, since the move exposed them to the file's readers.",
            "Record the migration with the re-scan result per location and the store entry each value now lives under.",
        ],
        "signals": [
            "Values are moved to a store while the file still contains the literal",
            "The store has no per-environment separation, so one key serves all environments",
            "No re-scan confirms the file no longer holds the value",
            "Files were edited in bulk, making each change hard to review or roll back",
        ],
        "patterns": [
            (
                "Migration row",
                "value group: E-004 | store entry: prod/payments/api_key | file updated: yes | re-scan: absent | rotation: required, scheduled",
            ),
            (
                "One-at-a-time rule",
                "one value per change so a failure is attributable and a rollback is small",
            ),
            (
                "Store requirements",
                "access control, audit log, per-environment separation, rotation support; each confirmed rather than assumed",
            ),
        ],
        "pitfalls": [
            "Moving a value into a store while leaving the original in place, which now has two copies",
            "Migrating in one bulk edit that nobody can review",
            "Skipping rotation on the grounds that the value is now safely stored",
        ],
        "done_when": [
            "Each migrated value records its store entry, the file update and a re-scan showing absence",
            "Rotation status is recorded per value rather than assumed complete",
        ],
        "refs": [
            "[OWASP - Secrets management cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)",
            "[NIST SP 800-57 - Key storage guidance](https://csrc.nist.gov/pubs/sp/800/57/r5/final)",
        ],
        "meta": {"phase": "harden"},
    },
    {
        "slug": "logging-redaction-at-source",
        "title": "Logging Redaction at Source",
        "summary": "Redact values where they are written rather than where they are found, because a log that has already shipped retains every copy you failed to stop",
        "use_when": "a value was found in logs, traces or telemetry and the emitting code is under your control",
        "avoid_when": "the emitting component is a third party you cannot modify and only retention can be changed",
        "tags": ["harden", "logging", "redaction"],
        "steps": [
            "Trace each logged value back to the exact statement or serializer that produced it.",
            "Redact at the emitting statement by allow-listing fields, or by masking values whose key matches a sensitive name.",
            "Prefer structural redaction over pattern replacement, since a pattern misses values it has never seen.",
            "Verify with a fixture: emit a synthetic sensitive value and confirm the log output does not contain it.",
            "Address retention for the copies already written, since fixing the source does not touch existing log files.",
            "Record the emitting statement changed, the fixture result and the retention action for existing copies.",
        ],
        "signals": [
            "A structured log serializes a whole object, capturing fields the author never named",
            "Redaction is done by pattern, so a new value format slips through",
            "The source was fixed while existing log files still hold the values",
            "No fixture proves the redaction actually removes the value",
        ],
        "patterns": [
            (
                "Emit record",
                "statement: app.log:118 serializer=whole object | fix: allow-list of fields | fixture: synthetic value absent from output: yes",
            ),
            (
                "Allow-list over deny-list",
                "log the fields you mean to log; a deny-list of sensitive keys fails on the key name you did not anticipate",
            ),
            (
                "Retention pairing",
                "source fix plus retention action on existing files, both recorded, because only the pair closes the exposure",
            ),
        ],
        "pitfalls": [
            "Fixing the source and leaving months of log files holding the values",
            "Redacting by pattern and declaring the pipeline clean when a new format will bypass it",
            "Writing a redaction test that never proves the value is absent from output",
        ],
        "done_when": [
            "Each emitting statement is changed with a fixture proving absence from output",
            "A retention action for existing copies is recorded alongside the source fix",
        ],
        "refs": [
            "[OWASP - Logging cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)",
            "[CWE-532 - Insertion of sensitive information into log file](https://cwe.mitre.org/data/definitions/532.html)",
        ],
        "meta": {"phase": "harden"},
    },
    {
        "slug": "continuous-scan-and-drift-monitoring",
        "title": "Continuous Scan and Drift Monitoring",
        "summary": "Run the same detection on a schedule against the same fixture corpus, so a regression is caught by a monitor instead of by the next assessment a year later",
        "use_when": "the assessment is closing and nothing will currently run the detection again",
        "avoid_when": "a scheduled scan already runs with a fixture corpus and an alert on regression",
        "tags": ["harden", "monitoring", "regression"],
        "steps": [
            "Schedule the scan against the tracked tree on a cadence, plus an artifact region scan where those exist.",
            "Run the fixture corpus in the same job so a rule regression is visible as a fixture miss, not as a silent pass.",
            "Define the alert: new findings, fixture misses, or a coverage region becoming unreadable.",
            "Record the baseline finding count so a later run can be compared against something.",
            "Assign the alert to an owner, since an unowned alert becomes noise within a week.",
            "Review the cadence against how fast values reach the tree, and shorten it if the interval outlives the risk.",
        ],
        "signals": [
            "No scheduled scan exists and the next assessment is the only check",
            "Fixtures are not part of the job, so a rule regression produces no signal",
            "An alert has no owner and no one reads it",
            "The scan interval is longer than the rate at which values reach the tree",
        ],
        "patterns": [
            (
                "Schedule record",
                "cadence: daily tracked scan + weekly artifact scan | fixtures: in every job | baseline: 0 findings | owner: platform",
            ),
            (
                "Fixture signal",
                "a fixture miss alerts on its own; it means the rule got weaker and the scan would otherwise look cleaner than reality",
            ),
            (
                "Baseline compare",
                "compare against the recorded baseline so a new finding stands out instead of blending into a total nobody remembers",
            ),
        ],
        "pitfalls": [
            "Scheduling a scan without fixtures, so a weakening rule looks like an improvement",
            "Owning the alert personally rather than as a team, so it dies when people move",
            "Choosing a cadence by convenience without reference to how fast values arrive",
        ],
        "done_when": [
            "A scheduled job runs the scan with the fixture corpus and has a named owner",
            "A baseline finding count is recorded for comparison on later runs",
        ],
        "refs": [
            "[NIST SP 800-53 - Continuous monitoring controls](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)",
            "[OWASP - Security regression testing](https://owasp.org/www-project-application-security-verification-standard/)",
        ],
        "meta": {"phase": "harden"},
    },
    {
        "slug": "exposure-finding-evidence-pack",
        "title": "Exposure Finding Evidence Pack",
        "summary": "Assemble a report where every exposure claim carries its location, class, reach, rank and confirmation basis without ever containing the value itself",
        "use_when": "findings are ready to be written up for the owning team or the destination agreed in scope",
        "avoid_when": "the finding has already been reported and only a closing note remains",
        "tags": ["document", "evidence", "reporting"],
        "steps": [
            "State the finding in one sentence naming location, class and reach, without adjectives.",
            "Attach the confirmation basis: format evidence, context evidence and the explicit statement that no network use occurred.",
            "Include class, reach and rank with both rank inputs, so a reader can re-derive the priority.",
            "List the group's locations as rotation targets, so remediation has its full scope.",
            "Record the staleness verdict with the assessment date it was made on.",
            "Attach the boundary and rule versions that permitted the read and produced the detection.",
        ],
        "signals": [
            "A report claims an exposure without saying where it was read from",
            "Rank appears without its class and reach inputs",
            "Confirmation basis is absent, so a reader cannot tell how the claim was established",
            "Only one location is listed for a value that appears in three",
        ],
        "patterns": [
            (
                "Claim skeleton",
                "claim: <class> value at <location>, reach <reach>, rank <rank>\nbasis: format + context, no network use\nlocations: <N rotation targets>\nstaleness: <verdict> as of <date>",
            ),
            (
                "Evidence line",
                "E-004 | src/client.py:18 | class: secret | reach: tracked | sha256: 3f2a... | rule v7 | boundary v3 | no network use",
            ),
            (
                "Value-free rule",
                "the pack contains hashes, paths and field names; a reviewer can act on every entry without ever seeing a value",
            ),
        ],
        "pitfalls": [
            "Including a value for context, which re-creates the exposure in the ticket",
            "Omitting the group locations, so remediation covers one file of three",
            "Presenting a rank without its inputs, which makes it impossible to challenge",
        ],
        "done_when": [
            "Every claim carries location, class, reach, rank inputs, confirmation basis and staleness",
            "The pack contains no value, only hashes, paths and field names",
        ],
        "refs": [
            "[NIST SP 800-61 - Incident documentation](https://csrc.nist.gov/pubs/sp/800/61/r2/final)",
            "[OWASP - Reporting security findings](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "document"},
    },
    {
        "slug": "redaction-for-shareable-reporting",
        "title": "Redaction for Shareable Reporting",
        "summary": "Prepare a version of the report that can go to a wider audience than the working copy, and test that redaction actually holds before sending it",
        "use_when": "the report will reach an audience wider than the team that produced it",
        "avoid_when": "the report stays inside the destination and audience agreed during scope",
        "tags": ["document", "redaction", "handling"],
        "steps": [
            "Produce two versions: a working copy in the agreed destination and a shareable copy for the wider audience.",
            "Apply redaction by removing values and replacing identifiers with stable labels that still allow tracking.",
            "Re-run detection over the shareable copy itself, since redaction is a change that can leave something behind.",
            "Check for values hiding in included excerpts, pasted context, screenshots and attachments.",
            "Record which version went to which audience with the date, so a later reader knows who saw what.",
            "Keep the working copy under the retention rule and confirm the shareable copy needs none of the removed detail.",
        ],
        "signals": [
            "A shareable version was produced but never re-scanned after redaction",
            "An excerpt or screenshot in the report still shows a value",
            "Both versions live in the same destination with the same access",
            "Nobody recorded which audience received which version",
        ],
        "patterns": [
            (
                "Version record",
                "working copy: internal ticket, audience security+owner | shareable: pdf, audience vendor; redaction re-scan: clean, 2026-10-28",
            ),
            (
                "Self-scan",
                "run the same detection over the shareable artifact before sending; a hit there means redaction missed something",
            ),
            (
                "Label mapping",
                "values replaced with stable labels like FINDING-004 so the shareable copy still tracks to the working copy without carrying detail",
            ),
        ],
        "pitfalls": [
            "Redacting by eye and never re-scanning the result",
            "Shipping a screenshot that shows the value the text carefully omitted",
            "Keeping both versions in one place where a wider audience can read the working copy",
        ],
        "done_when": [
            "The shareable copy has been re-scanned after redaction and the result recorded",
            "Each version has a recorded audience and the audience that received it",
        ],
        "refs": [
            "[ISO 27002 - Information sharing controls](https://www.iso.org/standard/75652.html)",
            "[OWASP - Information disclosure guidance](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "document"},
    },
    {
        "slug": "remediation-order-by-copy",
        "title": "Remediation Order by Copy",
        "summary": "Sequence the fix across every copy of a value, from the most reachable to the least, so the exposure stops widening while slower copies are still being cleaned",
        "use_when": "a value exists in several locations and the fix must be sequenced",
        "avoid_when": "each value has exactly one location, which removes the ordering question",
        "tags": ["document", "remediation", "sequencing"],
        "steps": [
            "List all copies of each value from the deduplicated group, including history, artifacts and logs.",
            "Order copies by reach: published first, then tracked, then local, then retained logs and history.",
            "Rotate or remove in that order, so the copies an external reader could reach are handled first.",
            "Re-scan each location after it is handled, and record the result rather than moving on by assumption.",
            "Handle history and caches last but schedule them explicitly, since they are the steps most often forgotten.",
            "Write the sequence into the report so the owning team sees the order and the reason for it.",
        ],
        "signals": [
            "A local file was fixed while a published copy remained reachable",
            "History and caches were never scheduled and survive after the report closes",
            "No re-scan confirms each copy was actually cleaned",
            "The order was chosen by file convenience rather than by reach",
        ],
        "patterns": [
            (
                "Sequence",
                "1 published repo  2 tracked files  3 build artifacts  4 local overrides  5 logs with retention  6 history and mirrors",
            ),
            (
                "Per-copy close",
                "each copy: handled at <time>, re-scan result <absent/present>; a present result keeps the group open",
            ),
            (
                "Reason line",
                "order follows reach so the exposure stops widening first; written into the report with the ordering rule",
            ),
        ],
        "pitfalls": [
            "Fixing the easiest file first and leaving the published copy live for days",
            "Never scheduling history and mirrors, which keep serving the old value",
            "Marking a copy handled without a re-scan showing it is actually clean",
        ],
        "done_when": [
            "Every copy appears in a reach-ordered sequence with a per-copy re-scan result",
            "History and mirrors are scheduled explicitly rather than left implicit",
        ],
        "refs": [
            "[NIST SP 800-40 - Remediation sequencing](https://csrc.nist.gov/pubs/sp/800/40/r4/final)",
            "[OWASP - Remediation guidance](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "document"},
    },
    {
        "slug": "post-closure-verification-record",
        "title": "Post-Closure Verification Record",
        "summary": "Re-scan after the fix and record the result as dated evidence, so closure is a measured outcome rather than an assertion by whoever closed the ticket",
        "use_when": "a finding has been fixed and is about to be closed",
        "avoid_when": "the fix is still in progress and closure is not yet being considered",
        "tags": ["document", "verification", "closure"],
        "steps": [
            "Re-run the same rule version against every location listed in the group after the fix lands.",
            "Record the result per location as absent or present with the date and the rule version used.",
            "Confirm the fixture corpus still passes, so an absence result is not explained by a weakened rule.",
            "Check history and caches where those were in scope, since a clean working tree proves nothing about them.",
            "Attach the verification record to the finding and close only when every location returns absent.",
            "Keep the record past closure for the retention period, since it is the only proof the exposure ended.",
        ],
        "signals": [
            "A finding was closed on the strength of a fix commit with no re-scan",
            "The rule version used for verification differs from the one that found the issue",
            "A fixture miss went unnoticed, so an absence result may just be a weaker rule",
            "History was never re-checked after the working tree was cleaned",
        ],
        "patterns": [
            (
                "Closure record",
                "group E-004 | locations: 3 | re-scan 2026-10-28 rule v7: absent everywhere | fixtures: 4 of 4 hit | history: zero matches",
            ),
            (
                "Rule parity",
                "verify with the same rule version that produced the finding, or record why a different one was used",
            ),
            (
                "Fixture guard",
                "a passing fixture run in the same job proves absence means absence rather than a rule that stopped matching",
            ),
        ],
        "pitfalls": [
            "Closing on a commit hash instead of on evidence that the value is gone",
            "Re-scanning with a modified rule that no longer matches the original pattern",
            "Skipping history, so the value remains available from a clone after closure",
        ],
        "done_when": [
            "Every location in the group returns absent on re-scan with the date and rule version recorded",
            "The fixture run passes in the same verification job, guarding the absence result",
        ],
        "refs": [
            "[NIST SP 800-53 - Assessment and monitoring records](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)",
            "[OWASP - Verification methodology](https://owasp.org/www-project-application-security-verification-standard/)",
        ],
        "meta": {"phase": "document"},
    },
]