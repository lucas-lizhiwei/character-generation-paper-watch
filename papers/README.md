# Formal PDF Library

Canonical PDFs are stored only after a paper passes the venue, acceptance, relevance, and deduplication gates.

Each paper has exactly one primary category and at most one stored PDF. Secondary categories are metadata only and never create copies. The filename contract is:

`P{priority}_{year}_{venue}_{ShortName}- {Canonical Formal Title}.pdf`

A record may remain formal when its PDF cannot be downloaded. In that case its `pdf_status` records the failure and its path, SHA-256, and download date remain empty. PDF presence never proves acceptance.

The repository validator checks stored-file existence, PDF signature, canonical filename and category placement, SHA-256, duplicate path/content, and orphan PDFs.

