import copy
import importlib.util
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
