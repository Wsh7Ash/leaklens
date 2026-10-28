"""leaklens corpus: pack metadata plus 50 authored data-exposure skills.

Skills are authored as plain dicts in ``part1``..``part3`` and loaded once
into the validated :class:`~leaklens.model.Skill` shape.
"""

from __future__ import annotations

from typing import Any

from ..model import skill_from_dict
from .part1 import SKILLS as PART1
from .part2 import SKILLS as PART2
from .part3 import SKILLS as PART3

PACK: dict[str, Any] = {
    "name": "leaklens",
    "version": "1.0.0",
    "category": "data-tool",
    "license": "MIT",
    "runtime": "Claude Code, opencode, or any agent runtime that loads SKILL.md files",
    "description": (
        "50 validated data-exposure hunting skills: authorized scope, discovery "
        "over files and repositories, classification by secret and data class, "
        "false-positive reduction, reporting and rotation, with a "
        "findings-summary-to-handling-plan CLI."
    ),
    "expected_skills": 50,
    "meta_keys": ("phase",),
    "requires_verification": False,
}

PHASE_ORDER = (
    "scope",
    "discover",
    "classify",
    "confirm",
    "harden",
    "document",
)

SKILLS: list[Any] = [skill_from_dict(raw) for raw in (*PART1, *PART2, *PART3)]