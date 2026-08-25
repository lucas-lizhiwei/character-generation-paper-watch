"""Validate the formal generative-image paper corpus deterministically."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import urlparse

from jsonschema import Draft202012Validator, FormatChecker


ALLOWED_VENUES = frozenset(
    {"CVPR", "ICCV", "ECCV", "NeurIPS", "ICML", "ICLR", "SIGGRAPH", "SIGGRAPH Asia", "3DV"}
)
IDENTIFIER_NAMES = ("doi", "openreview", "venue", "arxiv")
AUTHORITATIVE_HOSTS = (
    "thecvf.com",
    "openreview.net",
    "neurips.cc",
    "proceedings.mlr.press",
    "icml.cc",
    "iclr.cc",
    "acm.org",
    "siggraph.org",
    "3dv.org",
    "3dvconf.org",
    "3dvconf.github.io",
    "ieee.org",
    "eurographics.org",
    "eg.org",
)


def _path_text(path: object) -> str:
    return ".".join(str(part) for part in path) or "<root>"


def _normalized_text(value: object) -> str:
    """Normalize paper identity text for stable title and alias comparison."""
    normalized = unicodedata.normalize("NFKC", str(value)).lower()
    return " ".join(re.findall(r"[^\W_]+", normalized, flags=re.UNICODE))


def _is_authoritative_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    hostname = (parsed.hostname or "").lower().rstrip(".")
    if parsed.scheme not in {"http", "https"} or not hostname:
        return False
    return any(hostname == host or hostname.endswith(f".{host}") for host in AUTHORITATIVE_HOSTS)


def _is_openreview_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    hostname = (urlparse(value).hostname or "").lower().rstrip(".")
    return hostname == "openreview.net" or hostname.endswith(".openreview.net")


def _load_json(path: Path, label: str, errors: list[str]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"{label}: file not found")
    except json.JSONDecodeError as exc:
        errors.append(f"{label}: invalid JSON at line {exc.lineno}, column {exc.colno}")
    return None


def _schema_errors(schema: object, document: object) -> list[str]:
    if not isinstance(schema, dict):
        return ["schema/papers.schema.json: schema must be a JSON object"]
    try:
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
    except Exception as exc:  # Invalid external schema must not crash the CLI.
        return [f"schema/papers.schema.json: invalid schema: {exc.message if hasattr(exc, 'message') else exc}"]
    return [
        f"schema: {_path_text(error.absolute_path)}: {error.message}"
        for error in sorted(validator.iter_errors(document), key=lambda error: (list(error.absolute_path), error.message))
    ]


def _cross_record_errors(repo_root: Path, document: object) -> list[str]:
    if not isinstance(document, dict) or not isinstance(document.get("papers"), list):
        return []

    errors: list[str] = []
    ids: dict[str, int] = {}
    names: dict[str, tuple[int, str]] = {}
    identifiers: dict[str, dict[str, int]] = {name: {} for name in IDENTIFIER_NAMES}

    for position, paper in enumerate(document["papers"]):
        if not isinstance(paper, dict):
            continue
        prefix = f"papers[{position}]"

        paper_id = paper.get("id")
        if isinstance(paper_id, str) and paper_id:
            if paper_id in ids:
                errors.append(f"{prefix}.id: duplicate id '{paper_id}' (also papers[{ids[paper_id]}])")
            else:
                ids[paper_id] = position

        venue = paper.get("venue")
        if isinstance(venue, str) and venue not in ALLOWED_VENUES:
            errors.append(f"{prefix}.venue: forbidden venue '{venue}'")

        track = paper.get("track")
        if track != "main":
            errors.append(f"{prefix}.track: required main-conference track 'main'")

        for kind, candidates in (
            ("title", [paper.get("title")]),
            ("alias", paper.get("aliases", [])),
        ):
            for candidate in candidates:
                if not isinstance(candidate, str) or not candidate.strip():
                    continue
                normalized = _normalized_text(candidate)
                if not normalized:
                    continue
                if normalized in names:
                    earlier_position, earlier_kind = names[normalized]
                    errors.append(
                        f"{prefix}.{kind}: duplicate normalized title/alias '{normalized}' "
                        f"(also papers[{earlier_position}].{earlier_kind})"
                    )
                else:
                    names[normalized] = (position, kind)

        record_identifiers = paper.get("identifiers")
        if isinstance(record_identifiers, dict):
            for name in IDENTIFIER_NAMES:
                identifier = record_identifiers.get(name)
                if not isinstance(identifier, str) or not identifier.strip():
                    continue
                normalized_identifier = identifier.strip().casefold()
                seen = identifiers[name]
                if normalized_identifier in seen:
                    errors.append(
                        f"{prefix}.identifiers.{name}: duplicate {name} '{identifier.strip()}' "
                        f"(also papers[{seen[normalized_identifier]}])"
                    )
                else:
                    seen[normalized_identifier] = position

        evidence = paper.get("acceptance_evidence")
        evidence_type = evidence.get("type") if isinstance(evidence, dict) else None
        evidence_url = evidence.get("url") if isinstance(evidence, dict) else None
        evidence_host = (urlparse(evidence_url).hostname or "").lower() if isinstance(evidence_url, str) else ""
        if evidence_type == "arxiv" or evidence_host == "arxiv.org" or evidence_host.endswith(".arxiv.org"):
            errors.append(f"{prefix}.acceptance_evidence: arXiv-only acceptance evidence is not eligible")
        elif not _is_authoritative_url(evidence_url):
            errors.append(f"{prefix}.acceptance_evidence.url: non-authoritative acceptance evidence")
        elif evidence_type == "openreview_accepted" and not _is_openreview_url(evidence_url):
            errors.append(
                f"{prefix}.acceptance_evidence: openreview_accepted evidence must use openreview.net"
            )
        elif evidence_type in {"official_proceedings", "official_program"} and _is_openreview_url(evidence_url):
            errors.append(
                f"{prefix}.acceptance_evidence: {evidence_type} evidence must use a conference or proceedings host"
            )

        report_path = paper.get("report_path")
        if not isinstance(report_path, str) or not report_path.strip():
            errors.append(f"{prefix}.report_path: missing referenced report")
        else:
            candidate_path = (repo_root / report_path).resolve()
            try:
                candidate_path.relative_to(repo_root.resolve())
            except ValueError:
                errors.append(f"{prefix}.report_path: must remain inside the repository")
            else:
                if not candidate_path.is_file():
                    errors.append(f"{prefix}.report_path: missing referenced report '{report_path}'")

    return errors


def validate_repository(repo_root: Path) -> list[str]:
    """Return all schema and corpus-invariant violations in stable order."""
    root = Path(repo_root)
    errors: list[str] = []
    schema = _load_json(root / "schema" / "papers.schema.json", "schema/papers.schema.json", errors)
    document = _load_json(root / "index" / "papers.json", "index/papers.json", errors)
    if schema is not None and document is not None:
        errors.extend(_schema_errors(schema, document))
        errors.extend(_cross_record_errors(root, document))
    return sorted(errors)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True, help="repository root to validate")
    arguments = parser.parse_args()
    errors = validate_repository(arguments.repo)
    if errors:
        print("\n".join(errors))
        return 1

    document = json.loads((arguments.repo / "index" / "papers.json").read_text(encoding="utf-8"))
    count = len(document["papers"])
    print(f"validated {count} paper{'s' if count != 1 else ''}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
