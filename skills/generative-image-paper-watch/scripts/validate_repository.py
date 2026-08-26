"""Validate the formal generative-image paper corpus deterministically."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import parse_qs, urlparse

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
    "ecva.net",
    "eurographics.org",
    "eg.org",
)
EVIDENCE_URL_RULES = {
    ("CVPR", "official_proceedings"): (
        (r"openaccess\.thecvf\.com", r"/content/CVPR\d{4}/html/.+_CVPR_\d{4}_paper\.html"),
    ),
    ("CVPR", "official_program"): (
        (r"cvpr\.thecvf\.com", r"/virtual/\d{4}/poster/\d+/?"),
    ),
    ("ICCV", "official_proceedings"): (
        (r"openaccess\.thecvf\.com", r"/content/ICCV\d{4}/html/.+_ICCV_\d{4}_paper\.html"),
    ),
    ("ICCV", "official_program"): (
        (r"iccv\.thecvf\.com", r"/virtual/\d{4}/poster/\d+/?"),
    ),
    ("ECCV", "official_proceedings"): (
        (r"eccv\.ecva\.net", r"/virtual/\d{4}/poster/\d+/?"),
        (r"(?:www\.)?ecva\.net", r"/papers/eccv_\d{4}/.+\.(?:html|pdf)"),
    ),
    ("ECCV", "official_program"): (
        (r"eccv\.ecva\.net", r"/virtual/\d{4}/poster/\d+/?"),
    ),
    ("NeurIPS", "official_proceedings"): (
        (
            r"proceedings\.neurips\.cc",
            r"/(?:paper/\d{4}|paper_files/paper/\d{4})/hash/[^/]+-Abstract(?:-Conference)?\.html",
        ),
    ),
    ("NeurIPS", "official_program"): (
        (r"neurips\.cc", r"/virtual/\d{4}/poster/\d+/?"),
    ),
    ("ICML", "official_proceedings"): (
        (r"proceedings\.mlr\.press", r"/v\d+/[^/]+\.html"),
    ),
    ("ICML", "official_program"): (
        (r"icml\.cc", r"/virtual/\d{4}/poster/\d+/?"),
    ),
    ("ICLR", "official_proceedings"): (
        (
            r"proceedings\.iclr\.cc",
            r"/paper_files/paper/\d{4}/hash/[^/]+-Abstract-Conference\.html",
        ),
    ),
    ("ICLR", "official_program"): (
        (r"iclr\.cc", r"/virtual/\d{4}/poster/\d+/?"),
    ),
    ("SIGGRAPH", "official_proceedings"): (
        (r"dl\.acm\.org", r"/doi/10\.1145/\d+(?:\.\d+)?"),
    ),
    ("SIGGRAPH", "official_program"): (
        (r"s\d{4}\.siggraph\.org", r"/.+technical-papers-accepted\.pdf"),
    ),
    ("SIGGRAPH Asia", "official_proceedings"): (
        (r"dl\.acm\.org", r"/doi/10\.1145/\d+(?:\.\d+)?"),
    ),
    ("SIGGRAPH Asia", "official_program"): (
        (r"asia\.siggraph\.org", r"/\d{4}/program/technical-papers(?:/.*)?"),
    ),
    ("3DV", "official_proceedings"): (
        (r"openaccess\.thecvf\.com", r"/content/3DV\d{4}/html/.+_3DV_\d{4}_paper\.html"),
        (r"ieeexplore\.ieee\.org", r"/document/\d+/?"),
    ),
    ("3DV", "official_program"): (
        (r"3dvconf\.github\.io", r"/\d{4}/program/(?:papers|technical-papers)(?:\.html|/.*)"),
    ),
}
OPENREVIEW_VENUES = frozenset({"ICLR"})
PDF_CATEGORIES = frozenset(
    {
        "00_Survey_Benchmark_Dataset",
        "01_Geometry_and_Physical_Cue_Estimation",
        "02_Object_Subject_Insertion_and_Compositing",
        "03_Relighting_and_Illumination_Control",
        "04_Shadow_Generation_and_Contact_Consistency",
        "05_Layered_Representation_and_Editable_Compositing",
        "06_Reference_Conditioned_Character_Identity",
        "07_End_to_End_CG_Guided_Anime_Character_Compositing",
        "08_Foundation_Models_and_Conditioning_Architectures",
    }
)
PDF_ROOT = "papers"


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


def _is_openreview_forum_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return (
        parsed.scheme in {"http", "https"}
        and (parsed.hostname or "").lower().rstrip(".") == "openreview.net"
        and parsed.path.rstrip("/") == "/forum"
        and bool(parse_qs(parsed.query).get("id", [""])[0])
    )


def _matches_venue_evidence_url(venue: object, evidence_type: object, value: object) -> bool:
    if not all(isinstance(item, str) for item in (venue, evidence_type, value)):
        return False
    parsed = urlparse(value)
    hostname = (parsed.hostname or "").lower().rstrip(".")
    rules = EVIDENCE_URL_RULES.get((venue, evidence_type), ())
    return any(
        re.fullmatch(host_pattern, hostname, flags=re.IGNORECASE)
        and re.fullmatch(path_pattern, parsed.path, flags=re.IGNORECASE)
        for host_pattern, path_pattern in rules
    )


def _safe_pdf_title(value: object) -> str:
    cleaned = re.sub(r'[/\\:*?"<>|]', "", str(value))
    return " ".join(cleaned.split())


def _pdf_errors(repo_root: Path, papers: list[object]) -> list[str]:
    errors: list[str] = []
    indexed_paths: dict[str, int] = {}
    indexed_hashes: dict[str, int] = {}

    for position, paper in enumerate(papers):
        if not isinstance(paper, dict):
            continue
        prefix = f"papers[{position}]"
        status = paper.get("pdf_status")
        pdf_path = paper.get("pdf_path")
        pdf_sha256 = paper.get("pdf_sha256")
        downloaded_date = paper.get("pdf_downloaded_date")
        primary_category = paper.get("primary_category")
        secondary_categories = paper.get("secondary_categories")

        if isinstance(secondary_categories, list) and primary_category in secondary_categories:
            errors.append(f"{prefix}.secondary_categories: must not repeat primary_category")

        if status != "stored":
            if pdf_path:
                errors.append(f"{prefix}.pdf_path: must be empty unless pdf_status is stored")
            if pdf_sha256:
                errors.append(f"{prefix}.pdf_sha256: must be empty unless pdf_status is stored")
            if downloaded_date:
                errors.append(
                    f"{prefix}.pdf_downloaded_date: must be empty unless pdf_status is stored"
                )
            continue

        if not isinstance(pdf_path, str) or not pdf_path:
            errors.append(f"{prefix}.pdf_path: stored PDF requires a repository path")
            continue
        if not isinstance(pdf_sha256, str) or not re.fullmatch(r"[0-9a-f]{64}", pdf_sha256):
            errors.append(f"{prefix}.pdf_sha256: stored PDF requires a lowercase SHA-256")
        if not downloaded_date:
            errors.append(f"{prefix}.pdf_downloaded_date: stored PDF requires a date")

        candidate_path = (repo_root / pdf_path).resolve()
        try:
            relative_path = candidate_path.relative_to(repo_root.resolve()).as_posix()
        except ValueError:
            errors.append(f"{prefix}.pdf_path: must remain inside the repository")
            continue

        expected_parent = f"{PDF_ROOT}/{primary_category}"
        if Path(relative_path).parent.as_posix() != expected_parent:
            errors.append(f"{prefix}.pdf_path: directory must match primary_category")

        venue_token = str(paper.get("venue", "")).replace(" ", "_")
        expected_prefix = (
            f"{paper.get('priority', '')}_{paper.get('year', '')}_{venue_token}_"
        )
        expected_suffix = f"- {_safe_pdf_title(paper.get('title', ''))}.pdf"
        filename = candidate_path.name
        short_name = filename[len(expected_prefix) : -len(expected_suffix)] if (
            filename.startswith(expected_prefix) and filename.endswith(expected_suffix)
        ) else ""
        if not short_name or re.search(r'[/\\:*?"<>|]', short_name):
            errors.append(
                f"{prefix}.pdf_path: filename must match priority/year/venue/title contract"
            )

        if relative_path in indexed_paths:
            errors.append(
                f"{prefix}.pdf_path: duplicate PDF path (also papers[{indexed_paths[relative_path]}])"
            )
        else:
            indexed_paths[relative_path] = position

        if not candidate_path.is_file():
            errors.append(f"{prefix}.pdf_path: stored PDF does not exist '{pdf_path}'")
            continue
        payload = candidate_path.read_bytes()
        if not payload.startswith(b"%PDF-") or len(payload) <= 8:
            errors.append(f"{prefix}.pdf_path: file is not a valid non-empty PDF")
            continue
        actual_hash = hashlib.sha256(payload).hexdigest()
        if actual_hash != pdf_sha256:
            errors.append(f"{prefix}.pdf_sha256: does not match stored PDF")
        if actual_hash in indexed_hashes:
            errors.append(
                f"{prefix}.pdf_sha256: duplicate PDF content "
                f"(also papers[{indexed_hashes[actual_hash]}])"
            )
        else:
            indexed_hashes[actual_hash] = position

    papers_root = repo_root / PDF_ROOT
    if papers_root.is_dir():
        for pdf_file in sorted(papers_root.rglob("*.pdf")):
            relative_path = pdf_file.relative_to(repo_root).as_posix()
            if relative_path not in indexed_paths:
                errors.append(f"papers: orphan PDF '{relative_path}'")

    return errors


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
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        validation_errors = list(validator.iter_errors(document))
    except Exception as exc:  # Invalid external schema must not crash the CLI.
        detail = " ".join(str(getattr(exc, "message", exc)).split())
        return [f"schema/papers.schema.json: invalid schema: {detail}"]
    return [
        f"schema: {_path_text(error.absolute_path)}: {error.message}"
        for error in sorted(
            validation_errors,
            key=lambda error: (list(error.absolute_path), error.message),
        )
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
        elif evidence_type == "openreview_accepted":
            if not _is_openreview_url(evidence_url):
                errors.append(
                    f"{prefix}.acceptance_evidence: openreview_accepted evidence must use openreview.net"
                )
            elif venue not in OPENREVIEW_VENUES:
                errors.append(
                    f"{prefix}.acceptance_evidence: openreview_accepted evidence is not supported for {venue}"
                )
            elif not _is_openreview_forum_url(evidence_url):
                errors.append(
                    f"{prefix}.acceptance_evidence: openreview_accepted evidence must use an openreview.net/forum?id=... record"
                )
        elif evidence_type in {"official_proceedings", "official_program"} and _is_openreview_url(evidence_url):
            errors.append(
                f"{prefix}.acceptance_evidence: {evidence_type} evidence must use a conference or proceedings host"
            )
        elif not _matches_venue_evidence_url(venue, evidence_type, evidence_url):
            errors.append(
                f"{prefix}.acceptance_evidence: {evidence_type} URL does not match the {venue} venue evidence contract"
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

    errors.extend(_pdf_errors(repo_root, document["papers"]))
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
