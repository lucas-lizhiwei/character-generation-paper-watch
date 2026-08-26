import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_SCRIPT = REPOSITORY_ROOT / "skills/generative-image-paper-watch/scripts/validate_repository.py"
VALIDATOR_SPEC = importlib.util.spec_from_file_location(
    "validate_repository", VALIDATOR_SCRIPT
)
assert VALIDATOR_SPEC and VALIDATOR_SPEC.loader
VALIDATOR_MODULE = importlib.util.module_from_spec(VALIDATOR_SPEC)
VALIDATOR_SPEC.loader.exec_module(VALIDATOR_MODULE)
validate_repository = VALIDATOR_MODULE.validate_repository


def test_accepts_an_eligible_main_conference_paper(repository_factory):
    root, _paper, _write_repository = repository_factory

    assert validate_repository(root) == []


def test_rejects_arxiv_only_acceptance_evidence(repository_factory):
    root, paper, write_repository = repository_factory
    paper["acceptance_evidence"] = {
        "type": "arxiv",
        "url": "https://arxiv.org/abs/2501.01234",
    }
    write_repository()

    assert any("arXiv-only acceptance evidence" in error for error in validate_repository(root))


def test_rejects_forbidden_venue(repository_factory):
    root, paper, write_repository = repository_factory
    paper["venue"] = "AAAI"
    write_repository()

    assert any("forbidden venue" in error for error in validate_repository(root))


def test_rejects_an_allowed_venue_when_its_track_is_not_main(repository_factory):
    root, paper, write_repository = repository_factory
    paper["track"] = "workshop"
    write_repository()

    assert any(
        "track" in error and "main" in error for error in validate_repository(root)
    )


def test_rejects_relevance_score_below_three(repository_factory):
    root, paper, write_repository = repository_factory
    paper["relevance_score"] = 2
    write_repository()

    assert any("relevance_score" in error for error in validate_repository(root))


def test_rejects_duplicate_paper_ids(repository_factory):
    root, paper, write_repository = repository_factory
    duplicate = copy.deepcopy(paper)
    duplicate["title"] = "A Different Eligible Image Method"
    duplicate["aliases"] = ["Different Image Method"]
    duplicate["identifiers"] = {
        "doi": "10.1109/CVPR.2025.05678",
        "openreview": "",
        "venue": "CVPR.2025.5678",
        "arxiv": "2502.05678",
    }
    write_repository([paper, duplicate])

    assert any("duplicate id" in error for error in validate_repository(root))


def test_rejects_titles_that_collide_after_normalization(repository_factory):
    root, paper, write_repository = repository_factory
    duplicate = copy.deepcopy(paper)
    duplicate["id"] = "cvpr-2025-layered-light-control-revision"
    duplicate["title"] = "Layered—Light Control: for IMAGE editing!"
    duplicate["aliases"] = ["A distinct alias"]
    duplicate["identifiers"] = {
        "doi": "10.1109/CVPR.2025.05678",
        "openreview": "",
        "venue": "CVPR.2025.5678",
        "arxiv": "2502.05678",
    }
    write_repository([paper, duplicate])

    assert any("normalized title" in error for error in validate_repository(root))


@pytest.mark.parametrize("identifier", ["doi", "openreview", "arxiv"])
def test_rejects_duplicate_external_identifiers(repository_factory, identifier):
    root, paper, write_repository = repository_factory
    duplicate = copy.deepcopy(paper)
    duplicate["id"] = f"cvpr-2025-duplicate-{identifier}"
    duplicate["title"] = f"A Different Paper Sharing a {identifier}"
    duplicate["aliases"] = [f"Different {identifier} paper"]
    duplicate["identifiers"] = {
        "doi": "10.1109/CVPR.2025.05678",
        "openreview": "different-openreview-id",
        "venue": "CVPR.2025.5678",
        "arxiv": "2502.05678",
    }
    duplicate["identifiers"][identifier] = paper["identifiers"][identifier]
    write_repository([paper, duplicate])

    assert any(f"duplicate {identifier}" in error for error in validate_repository(root))


def test_rejects_non_authoritative_acceptance_evidence(repository_factory):
    root, paper, write_repository = repository_factory
    paper["acceptance_evidence"] = {
        "type": "official_proceedings",
        "url": "https://example.org/papers/layered-light-control",
    }
    write_repository()

    assert any("non-authoritative acceptance evidence" in error for error in validate_repository(root))


@pytest.mark.parametrize(
    ("venue", "url"),
    [
        (
            "NeurIPS",
            "https://openaccess.thecvf.com/content/CVPR2025/html/Researcher_Layered_Light_Control_CVPR_2025_paper.html",
        ),
        (
            "CVPR",
            "https://proceedings.neurips.cc/paper_files/paper/2025/hash/abc-Abstract-Conference.html",
        ),
    ],
)
def test_rejects_cross_venue_official_evidence(repository_factory, venue, url):
    root, paper, write_repository = repository_factory
    paper["venue"] = venue
    paper["acceptance_evidence"] = {"type": "official_proceedings", "url": url}
    write_repository()

    assert any(
        "acceptance_evidence" in error and "venue" in error
        for error in validate_repository(root)
    )


def test_rejects_openreview_evidence_for_an_unsupported_venue(repository_factory):
    root, paper, write_repository = repository_factory
    paper["acceptance_evidence"] = {
        "type": "openreview_accepted",
        "url": "https://openreview.net/forum?id=layered-light-control",
    }
    write_repository()

    assert any(
        "openreview_accepted" in error and "CVPR" in error
        for error in validate_repository(root)
    )


def test_accepts_a_supported_openreview_forum_record(repository_factory):
    root, paper, write_repository = repository_factory
    paper["venue"] = "ICLR"
    paper["acceptance_evidence"] = {
        "type": "openreview_accepted",
        "url": "https://openreview.net/forum?id=layered-light-control",
    }
    write_repository()

    assert validate_repository(root) == []


def test_rejects_an_unrecognizable_openreview_path(repository_factory):
    root, paper, write_repository = repository_factory
    paper["venue"] = "ICLR"
    paper["acceptance_evidence"] = {
        "type": "openreview_accepted",
        "url": "https://openreview.net/group?id=ICLR.cc/Conference/2025",
    }
    write_repository()

    assert any(
        "openreview_accepted" in error and "forum" in error
        for error in validate_repository(root)
    )


@pytest.mark.parametrize(
    ("venue", "evidence_type", "url"),
    [
        (
            "NeurIPS",
            "official_proceedings",
            "https://proceedings.neurips.cc/paper/2020/hash/abc-Abstract.html",
        ),
        ("ICLR", "official_program", "https://iclr.cc/virtual/2024/poster/18250"),
        (
            "ICLR",
            "official_proceedings",
            "https://proceedings.iclr.cc/paper_files/paper/2025/hash/abc-Abstract-Conference.html",
        ),
        ("ICML", "official_proceedings", "https://proceedings.mlr.press/v235/esser24a.html"),
        (
            "CVPR",
            "official_proceedings",
            "https://openaccess.thecvf.com/content/CVPR2025/html/Researcher_Layered_Light_Control_CVPR_2025_paper.html",
        ),
        (
            "ICCV",
            "official_proceedings",
            "https://openaccess.thecvf.com/content/ICCV2025/html/Researcher_Layered_Light_Control_ICCV_2025_paper.html",
        ),
        ("ECCV", "official_proceedings", "https://eccv.ecva.net/virtual/2024/poster/1434"),
        (
            "SIGGRAPH",
            "official_program",
            "https://s2022.siggraph.org/wp-content/uploads/2022/05/SIGGRAPH-2022-TECHNICAL-PAPERS-ACCEPTED.pdf",
        ),
        ("SIGGRAPH", "official_proceedings", "https://dl.acm.org/doi/10.1145/3658150"),
    ],
)
def test_accepts_current_corpus_evidence_classes(
    repository_factory, venue, evidence_type, url
):
    root, paper, write_repository = repository_factory
    paper["venue"] = venue
    paper["acceptance_evidence"] = {"type": evidence_type, "url": url}
    write_repository()

    assert validate_repository(root) == []


def test_accepts_official_ecva_eccv_proceedings_and_rejects_lookalikes(repository_factory):
    root, paper, write_repository = repository_factory
    paper["venue"] = "ECCV"
    paper["acceptance_evidence"] = {"type": "official_proceedings", "url": ""}

    for url in (
        "https://eccv.ecva.net/virtual/2024/poster/1434",
        "https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/03014.pdf",
    ):
        paper["acceptance_evidence"]["url"] = url
        write_repository()

        assert validate_repository(root) == []

    for url in (
        "https://ecva.net.example.org/virtual/2024/poster/1434",
        "https://example.org/virtual/2024/poster/1434",
    ):
        paper["acceptance_evidence"]["url"] = url
        write_repository()

        assert any("non-authoritative acceptance evidence" in error for error in validate_repository(root))


def test_rejects_openreview_evidence_claimed_on_a_proceedings_host(repository_factory):
    root, paper, write_repository = repository_factory
    paper["acceptance_evidence"] = {
        "type": "openreview_accepted",
        "url": "https://openaccess.thecvf.com/content/CVPR2025/html/paper.html",
    }
    write_repository()

    assert any(
        "openreview_accepted" in error and "openreview.net" in error
        for error in validate_repository(root)
    )


def test_rejects_a_missing_referenced_report(repository_factory):
    root, paper, write_repository = repository_factory
    paper["report_path"] = "reports/missing.md"
    write_repository()

    assert any("report_path" in error for error in validate_repository(root))


def test_accepts_a_verified_stored_pdf(repository_factory):
    root, paper, write_repository = repository_factory
    payload = b"%PDF-1.4\n%%EOF\n"
    filename = (
        "P1_2025_CVPR_LayeredLight- "
        "Layered Light Control for Image Editing.pdf"
    )
    relative_path = (
        "papers/03_Relighting_and_Illumination_Control/" + filename
    )
    pdf_path = root / relative_path
    pdf_path.parent.mkdir(parents=True)
    pdf_path.write_bytes(payload)
    paper.update(
        {
            "pdf_status": "stored",
            "pdf_path": relative_path,
            "pdf_source_type": "official_proceedings",
            "pdf_source_url": "https://openaccess.thecvf.com/paper.pdf",
            "pdf_sha256": hashlib.sha256(payload).hexdigest(),
            "pdf_downloaded_date": "2025-01-12",
        }
    )
    write_repository()

    assert validate_repository(root) == []


def test_rejects_stored_pdf_with_missing_file(repository_factory):
    root, paper, write_repository = repository_factory
    paper.update(
        {
            "pdf_status": "stored",
            "pdf_path": (
                "papers/03_Relighting_and_Illumination_Control/"
                "P1_2025_CVPR_LayeredLight- Layered Light Control for Image Editing.pdf"
            ),
            "pdf_source_type": "official_proceedings",
            "pdf_sha256": "0" * 64,
            "pdf_downloaded_date": "2025-01-12",
        }
    )
    write_repository()

    assert any("does not exist" in error for error in validate_repository(root))


def test_rejects_pdf_metadata_on_failed_download(repository_factory):
    root, paper, write_repository = repository_factory
    paper["pdf_path"] = "papers/unexpected.pdf"
    paper["pdf_sha256"] = "0" * 64
    paper["pdf_downloaded_date"] = "2025-01-12"
    write_repository()

    errors = validate_repository(root)
    assert any("pdf_path" in error and "unless" in error for error in errors)
    assert any("pdf_sha256" in error and "unless" in error for error in errors)


def test_rejects_pdf_in_wrong_category_and_with_bad_hash(repository_factory):
    root, paper, write_repository = repository_factory
    payload = b"%PDF-1.4\n%%EOF\n"
    relative_path = (
        "papers/08_Foundation_Models_and_Conditioning_Architectures/"
        "P1_2025_CVPR_LayeredLight- Layered Light Control for Image Editing.pdf"
    )
    pdf_path = root / relative_path
    pdf_path.parent.mkdir(parents=True)
    pdf_path.write_bytes(payload)
    paper.update(
        {
            "pdf_status": "stored",
            "pdf_path": relative_path,
            "pdf_source_type": "official_proceedings",
            "pdf_sha256": "0" * 64,
            "pdf_downloaded_date": "2025-01-12",
        }
    )
    write_repository()

    errors = validate_repository(root)
    assert any("primary_category" in error for error in errors)
    assert any("does not match stored PDF" in error for error in errors)


def test_rejects_orphan_pdf(repository_factory):
    root, _paper, _write_repository = repository_factory
    orphan = root / "papers/08_Foundation_Models_and_Conditioning_Architectures/orphan.pdf"
    orphan.parent.mkdir(parents=True)
    orphan.write_bytes(b"%PDF-1.4\n%%EOF\n")

    assert any("orphan PDF" in error for error in validate_repository(root))


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("paper", "file:///tmp/paper.pdf"),
        ("project", "javascript:alert('paper')"),
        ("code", "ftp://example.org/paper-code"),
    ],
)
def test_rejects_non_web_schemes_in_required_and_optional_links(
    repository_factory, field, value
):
    root, paper, write_repository = repository_factory
    paper["urls"][field] = value
    write_repository()

    assert any(f"urls.{field}" in error for error in validate_repository(root))


@pytest.mark.parametrize(
    ("malformed_schema", "expected_detail"),
    [
        ({"type": 7}, "7 is not valid"),
        ({"$ref": "#/$defs/missing"}, "/$defs/missing"),
    ],
    ids=["schema-checking", "error-iteration"],
)
def test_malformed_schema_returns_actionable_api_and_cli_errors(
    repository_factory, malformed_schema, expected_detail
):
    root, _paper, _write_repository = repository_factory
    (root / "schema" / "papers.schema.json").write_text(
        json.dumps(malformed_schema), encoding="utf-8"
    )

    errors = validate_repository(root)
    assert len(errors) == 1
    assert errors[0].startswith("schema/papers.schema.json: invalid schema:")
    assert expected_detail in errors[0]

    failure = subprocess.run(
        [sys.executable, str(VALIDATOR_SCRIPT), "--repo", str(root)],
        capture_output=True,
        text=True,
        check=False,
    )
    output = failure.stdout + failure.stderr
    assert failure.returncode == 1
    assert "schema/papers.schema.json: invalid schema:" in output
    assert expected_detail in output
    assert "Traceback" not in output


def test_cli_reports_success_and_actionable_validation_failures(repository_factory):
    root, paper, write_repository = repository_factory

    success = subprocess.run(
        [sys.executable, str(VALIDATOR_SCRIPT), "--repo", str(root)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert success.returncode == 0
    assert "validated 1 paper" in success.stdout

    paper["report_path"] = "reports/missing.md"
    write_repository()
    failure = subprocess.run(
        [sys.executable, str(VALIDATOR_SCRIPT), "--repo", str(root)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert failure.returncode != 0
    assert "report_path" in failure.stdout + failure.stderr
