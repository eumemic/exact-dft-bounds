#!/usr/bin/env python3
"""Check that the committed children file matches the pin in SOURCES.json and that the
moment certificate records the same children file."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    sources = json.loads((ROOT / 'SOURCES.json').read_text())
    children = (ROOT / 'certificates' / 'network-children.json').read_bytes()
    digest = hashlib.sha256(children).hexdigest()
    assert digest == sources['network']['derived_sha256'], 'children file differs from SOURCES.json pin'
    meta = json.loads(children)
    assert meta['source']['sha256'] == sources['network']['sha256'], 'upstream pin mismatch'
    assert meta['source']['commit'] == sources['network']['commit'], 'upstream commit mismatch'
    moment = json.loads((ROOT / 'certificates' / 'moment.json').read_text())
    assert moment['children_sha256'] == digest and moment['passed'], 'moment certificate is stale or failed'
    print('sources PASS: children %s, upstream %s at %s' % (digest[:12], sources['network']['sha256'][:12],
                                                          sources['network']['commit'][:7]))


if __name__ == '__main__':
    main()
