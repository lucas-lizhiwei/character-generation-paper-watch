import json
from pathlib import Path

import pytest


@pytest.fixture
def repository_factory(tmp_path):
    """Create a minimal formal corpus repository and return its mutable seed paper."""

    schema = json.loads(
        (Path(__file__).resolve().parents[1] / "schema" / "papers.schema.json").read_text(
            encoding="utf-8"
        )
    )
    paper = {
        "id": "cvpr-2025-layered-light-control",
        "title": "Layered Light Control for Image Editing",
        "aliases": ["Layered Light Control"],
        "authors": ["Ada Researcher", "Ben Scientist"],
        "year": 2025,
        "venue": "CVPR",
        "track": "main",
        "identifiers": {
            "doi": "10.1109/CVPR.2025.01234",
            "openreview": "cvpr-2025-layered-light-control",
            "venue": "CVPR.2025.1234",
            "arxiv": "2501.01234",
        },
        "acceptance_evidence": {
            "type": "official_proceedings",
            "url": "https://openaccess.thecvf.com/content/CVPR2025/html/Researcher_Layered_Light_Control_for_Image_Editing_CVPR_2025_paper.html",
        },
        "urls": {
            "paper": "https://openaccess.thecvf.com/content/CVPR2025/html/Researcher_Layered_Light_Control_for_Image_Editing_CVPR_2025_paper.html",
            "arxiv": "https://arxiv.org/abs/2501.01234",
            "project": "",
            "code": "",
            "demo": "",
            "model": "",
            "dataset": "",
        },
        "topics": ["image editing", "relighting"],
        "tasks": ["image editing"],
        "architectures": ["DiT"],
        "base_models": ["Stable Diffusion"],
        "training_methods": ["diffusion"],
        "conditioning_methods": ["lighting condition"],
        "relevance_score": 4,
        "relevance_rationale": "A transferable controllable image-editing method.",
        "code_status": "official_full",
        "implementation_coverage": "training and inference",
        "first_seen_date": "2025-01-10",
        "last_verified_date": "2025-01-12",
        "dedupe_keys": ["layered-light-control", "cvpr.2025.1234"],
        "report_path": "reports/2025-01-12.md",
        "notes": "Acceptance was verified from CVPR proceedings.",
    }

    def write_repository(papers=None):
        root = Path(tmp_path)
        (root / "schema").mkdir(exist_ok=True)
        (root / "index").mkdir(exist_ok=True)
        (root / "reports").mkdir(exist_ok=True)
        (root / "schema" / "papers.schema.json").write_text(
            json.dumps(schema), encoding="utf-8"
        )
        (root / "index" / "papers.json").write_text(
            json.dumps(
                {
                    "schema_version": "1.0.0",
                    "generated_at": "2025-01-12",
                    "papers": papers if papers is not None else [paper],
                }
            ),
            encoding="utf-8",
        )
        (root / "reports" / "2025-01-12.md").write_text(
            "# Formal paper report\n", encoding="utf-8"
        )

    write_repository()
    return Path(tmp_path), paper, write_repository
