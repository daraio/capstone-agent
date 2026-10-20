#!/usr/bin/env python3
"""Read-only arXiv digest for the persistent research agent (Lab 4).

Queries the public arXiv API for recent submissions matching a search string
and prints a Markdown digest. No writes, no credentials, no third-party sites:
this is the "one safe thing" a first scheduled run may do (Lecture 7, slide
"minimum viable persistent research agent", step 2).

Usage:
  python3 arxiv_digest.py --query "cat:cond-mat.soft AND all:metamaterial" --days 2 --max 8
  python3 arxiv_digest.py --query "all:\"physics-informed neural network\"" --max 5

Output: Markdown, one bullet per paper, with title, first author, date and link.
Every line in the digest comes from the API response; nothing is paraphrased here.
The agent summarises on top of this — and must keep the links.
Provenance line at the bottom: query, window, time fetched.
"""
import argparse
import datetime as dt
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

API = "https://export.arxiv.org/api/query"
NS = {"a": "http://www.w3.org/2005/Atom"}


def fetch(query: str, max_results: int):
    params = {"search_query": query, "start": 0, "max_results": max_results,
              "sortBy": "submittedDate", "sortOrder": "descending"}
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "ME-CE-AM-295-lab4-digest/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def parse(xml_bytes: bytes):
    root = ET.fromstring(xml_bytes)
    for e in root.findall("a:entry", NS):
        title = " ".join(e.findtext("a:title", default="", namespaces=NS).split())
        link = e.findtext("a:id", default="", namespaces=NS)
        published = e.findtext("a:published", default="", namespaces=NS)[:10]
        authors = [a.findtext("a:name", default="", namespaces=NS) for a in e.findall("a:author", NS)]
        first = authors[0] if authors else "?"
        more = f" et al." if len(authors) > 1 else ""
        yield {"title": title, "link": link, "date": published, "author": first + more}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--query", required=True, help="arXiv search_query string")
    ap.add_argument("--days", type=int, default=2, help="only papers published in the last N days")
    ap.add_argument("--max", type=int, default=8, help="max results to request")
    a = ap.parse_args(argv)

    since = dt.date.today() - dt.timedelta(days=a.days)
    try:
        entries = [p for p in parse(fetch(a.query, a.max)) if p["date"] >= since.isoformat()]
    except Exception as exc:  # network or parse failure: say so, never invent papers
        print(f"**arXiv digest failed**: {type(exc).__name__}: {exc}\n\nNo papers were retrieved.")
        return 1

    print(f"### arXiv digest — {dt.date.today().isoformat()}")
    if not entries:
        print(f"\nNo new submissions in the last {a.days} day(s) for `{a.query}`.")
    for p in entries:
        print(f"- **{p['title']}** — {p['author']} ({p['date']}). {p['link']}")
    print(f"\n_Source: arXiv API · query `{a.query}` · window {a.days} d · "
          f"fetched {dt.datetime.now().isoformat(timespec='minutes')}_")
    return 0


if __name__ == "__main__":
    sys.exit(main())
