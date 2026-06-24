#!/usr/bin/env python3
"""
Agora Reference Authenticity Check

Scans changed Markdown files for DOIs and URLs, verifies they resolve,
and outputs a Markdown report for a GitHub PR comment.

A PASS here means links are live — not that references are sound.
Content accuracy requires human review (see REVIEW_CHECKLIST.md).
"""

import re
import sys
import time
import requests

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "Agora-Reference-Check/1.0 (github.com/agora)"})

# Matches bare DOIs, doi: prefixed, and doi.org URLs
DOI_RE = re.compile(
    r"(?:"
    r"https?://(?:dx\.)?doi\.org/(10\.[^\s\)\]>,;]+)"
    r"|doi[:\s]+(10\.[^\s\)\]>,;]+)"
    r"|(10\.\d{4,9}/[^\s\)\]>,;]+)"
    r")",
    re.IGNORECASE,
)
URL_RE = re.compile(r"https?://[^\s\)\]>,;]+", re.IGNORECASE)


def refs_section(text):
    m = re.search(r"\n##\s+References\s*\n(.*?)(?=\n##\s|\Z)", text, re.DOTALL | re.IGNORECASE)
    return m.group(1) if m else text  # fall back to whole file if no section found


def find_dois(text):
    dois = set()
    for m in DOI_RE.finditer(text):
        doi = (m.group(1) or m.group(2) or m.group(3) or "").rstrip(".,;)")
        if doi:
            dois.add(doi)
    return dois


def find_urls(text):
    urls = set()
    for m in URL_RE.finditer(text):
        url = m.group(0).rstrip(".,;)")
        if "doi.org" not in url.lower():
            urls.add(url)
    return urls


def check_doi(doi):
    try:
        r = SESSION.get(f"https://api.crossref.org/works/{doi}", timeout=15)
        if r.status_code == 200:
            title = r.json().get("message", {}).get("title", [""])[0]
            return True, (title[:80] if title else "(title unavailable)")
        return False, f"HTTP {r.status_code}"
    except Exception as e:
        return False, str(e)[:80]


def check_url(url):
    try:
        r = SESSION.head(url, timeout=10, allow_redirects=True)
        return r.status_code < 400, f"HTTP {r.status_code}"
    except Exception:
        # Some servers reject HEAD; fall back to GET
        try:
            r = SESSION.get(url, timeout=10, allow_redirects=True, stream=True)
            r.close()
            return r.status_code < 400, f"HTTP {r.status_code}"
        except Exception as e:
            return False, str(e)[:80]


def check_file(path):
    with open(path) as f:
        text = f.read()
    target = refs_section(text)
    dois = find_dois(target)
    urls = find_urls(target)

    doi_results = []
    for doi in sorted(dois):
        time.sleep(0.3)  # stay within Crossref's polite rate limit
        ok, detail = check_doi(doi)
        doi_results.append((doi, ok, detail))

    url_results = []
    for url in sorted(urls):
        ok, detail = check_url(url)
        url_results.append((url, ok, detail))

    return doi_results, url_results


def render_report(file_results):
    lines = [
        "## Agora Reference Authenticity Check\n",
        "> **A green result means links are live — not that references are sound.**  ",
        "> Whether a source says what the contributor claims requires human judgment.  ",
        "> See [REVIEW_CHECKLIST.md](./REVIEW_CHECKLIST.md) — reference authenticity is item 1.\n",
    ]

    any_findings = False
    for path, (dois, urls) in file_results:
        if not dois and not urls:
            continue
        any_findings = True
        lines.append(f"\n### `{path}`\n")

        if dois:
            lines.append("**DOIs — checked via Crossref**\n")
            for doi, ok, detail in dois:
                icon = "✅" if ok else "❌"
                lines.append(f"- {icon} `{doi}` — {detail}")
            lines.append("")

        if urls:
            lines.append("**URLs**\n")
            for url, ok, detail in urls:
                icon = "✅" if ok else "❌"
                lines.append(f"- {icon} {url} — {detail}")
            lines.append("")

    if not any_findings:
        lines.append("\n_No DOIs or URLs found in the changed files — nothing to verify._")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: check_references.py <changed_files.txt>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1]) as f:
        files = [line.strip() for line in f if line.strip().endswith(".md")]

    if not files:
        print("_No Markdown files changed in this PR._")
        return

    file_results = []
    for path in files:
        try:
            results = check_file(path)
        except FileNotFoundError:
            results = ([], [])
        file_results.append((path, results))

    print(render_report(file_results))


if __name__ == "__main__":
    main()
