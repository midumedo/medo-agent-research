"""Verify arXiv ids/dates against the official arXiv API.

Usage: python check_arxiv.py <id1> <id2> ...
Prints: id | published | updated | title
Unknown or failed ids are printed as ERROR so nothing is silently assumed.
"""

import sys
import time
import urllib.request
import xml.etree.ElementTree as ET

ATOM = "{http://www.w3.org/2005/Atom}"
BATCH = 20


def fetch(ids):
    url = "http://export.arxiv.org/api/query?id_list=" + ",".join(ids) + "&max_results=%d" % len(ids)
    req = urllib.request.Request(url, headers={"User-Agent": "memory-research-check/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return ET.fromstring(resp.read())


def main(argv):
    ids = [a.strip() for a in argv if a.strip()]
    out = []
    for i in range(0, len(ids), BATCH):
        chunk = ids[i:i + BATCH]
        found = {}
        try:
            root = fetch(chunk)
        except Exception as exc:  # network / parse failure must not become a guess
            for cid in chunk:
                out.append("%s | ERROR | %s" % (cid, exc))
            continue
        for entry in root.findall(ATOM + "entry"):
            raw = entry.findtext(ATOM + "id", "").rsplit("/", 1)[-1]
            base = raw.split("v")[0]
            found[base] = (
                entry.findtext(ATOM + "published", "")[:10],
                entry.findtext(ATOM + "updated", "")[:10],
                " ".join(entry.findtext(ATOM + "title", "").split()),
                " ".join(entry.findtext("{http://arxiv.org/schemas/atom}comment", "").split())[:90],
                " ".join(entry.findtext("{http://arxiv.org/schemas/atom}journal_ref", "").split())[:90],
            )
        for cid in chunk:
            if cid in found:
                pub, upd, title, comment, journal = found[cid]
                out.append("%s | %s | %s | %s || comment=%s || journal=%s" % (cid, pub, upd, title, comment or "-", journal or "-"))
            else:
                out.append("%s | NOT-FOUND | not in arXiv response" % cid)
        time.sleep(3)
    print("\n".join(out))


if __name__ == "__main__":
    main(sys.argv[1:])
