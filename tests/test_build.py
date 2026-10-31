#!/usr/bin/env python3
"""Self-tests for the Calmer Bills build.

Run with:  python3 tests/test_build.py
Stdlib only. Builds the site into a scratch directory, never touching the
real site/ output, then verifies structure, links, determinism, the exact
LICENSE text, and absence of personal data in the docs.
"""

from __future__ import annotations

import hashlib
import re
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

import build  # noqa: E402

LICENSE_COPYRIGHT = "Copyright (c) 2026 Asdale Dynamics, LLC"
EDU_PHRASE = "never legal"


def build_to(tmp: Path) -> Path:
    out = tmp / "site"
    stats = build.build(REPO / "docs", out)
    assert stats["pages"] > 0
    return out


class BuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.site = build_to(Path(cls._tmp.name))
        cls.html_files = sorted(p for p in cls.site.rglob("*.html"))

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def test_every_sidebar_page_is_built(self):
        for doc_path, _label in [e for _, es in build.SIDEBAR for e in es]:
            out_rel = doc_path[len("docs/") :][:-3] + ".html"
            self.assertTrue(
                (self.site / out_rel).is_file(),
                f"missing built page for {doc_path}",
            )

    def test_no_unexpected_or_missing_pages(self):
        source = {p.relative_to(REPO / "docs").with_suffix(".html")
                  for p in (REPO / "docs").rglob("*.md")}
        built = {p.relative_to(self.site) for p in self.html_files}
        self.assertEqual(source, built)

    def test_build_is_deterministic(self):
        with tempfile.TemporaryDirectory() as t2:
            site2 = build_to(Path(t2))
            for f in self.html_files:
                other = site2 / f.relative_to(self.site)
                self.assertTrue(other.is_file(), f"missing {other}")

            def digest(root: Path) -> str:
                parts = []
                for f in sorted(root.rglob("*.html")):
                    parts.append(
                        f.relative_to(root).as_posix()
                        + ":"
                        + hashlib.sha256(f.read_bytes()).hexdigest()
                    )
                return hashlib.sha256("".join(parts).encode()).hexdigest()

            self.assertEqual(digest(self.site), digest(site2))

    def test_one_h1_per_page(self):
        for f in self.html_files:
            n = len(re.findall(r"<h1[ >]", f.read_text(encoding="utf-8")))
            self.assertEqual(n, 1, f"{f.name} has {n} h1 tags")

    def test_disclaimer_banner_on_every_page(self):
        for f in self.html_files:
            text = f.read_text(encoding="utf-8")
            self.assertIn("Education only", text, f.name)
            self.assertIn(EDU_PHRASE, text, f.name)

    def test_all_internal_links_resolve(self):
        for f in self.html_files:
            text = f.read_text(encoding="utf-8")
            for href in re.findall(r'href="([^"]+)"', text):
                if href.startswith(("#", "http://", "https://", "mailto:")):
                    continue
                target = (f.parent / href.split("#")[0]).resolve()
                self.assertTrue(
                    target.is_file(),
                    f"{f.relative_to(self.site)} -> broken link {href}",
                )
                self.assertFalse(
                    target.suffix == ".md",
                    f"{f.name} still links a raw .md: {href}",
                )

    def test_footer_credits_llc(self):
        for f in self.html_files:
            self.assertIn("Asdale Dynamics, LLC", f.read_text(encoding="utf-8"))

    def test_license_copyright_is_exact(self):
        license_text = (REPO / "LICENSE").read_text(encoding="utf-8")
        self.assertIn(LICENSE_COPYRIGHT, license_text)
        # Exact line, nothing else on it.
        lines = [
            line.strip()
            for line in license_text.splitlines()
            if "Copyright" in line
        ]
        self.assertEqual(lines, [LICENSE_COPYRIGHT])

    def test_readme_credits_llc(self):
        readme = (REPO / "README.md").read_text(encoding="utf-8")
        self.assertIn("Asdale Dynamics, LLC", readme)

    def test_no_personal_data_in_docs(self):
        email = re.compile(r"[A-Za-z0-9._%+-]+@(?!example\.)[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
        phone = re.compile(r"\b\d{3}-\d{3}-\d{4}\b")
        ssn = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
        for md in sorted((REPO / "docs").rglob("*.md")):
            text = md.read_text(encoding="utf-8")
            self.assertFalse(
                email.search(text), f"possible email in {md.name}"
            )
            self.assertFalse(
                phone.search(text), f"possible phone number in {md.name}"
            )
            self.assertFalse(ssn.search(text), f"possible SSN in {md.name}")

    def test_minified_html_has_nav_and_pager(self):
        index = (self.site / "index.html").read_text(encoding="utf-8")
        self.assertIn('class="toc"', index)
        self.assertIn("pager", index)
        scripts = (self.site / "scripts" / "internet.html").read_text(
            encoding="utf-8"
        )
        self.assertIn('href="../index.html"', scripts)


if __name__ == "__main__":
    unittest.main(verbosity=2)
