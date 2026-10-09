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
    # the later suppliers: PR #200 (physical-frame ledger) and PR #194 (source-assisted flow word)
    for key, name, saving in (('network_pr200', 'pr200', '3327/5000000'), ('network_pr194', 'pr194', '7009/10000000'), ('network_pr233', 'pr233', '7086/10000000')):
        pin = sources[key]
        children = (ROOT / 'certificates' / ('network-children-%s.json' % name)).read_bytes()
        digest = hashlib.sha256(children).hexdigest()
        assert digest == pin['derived_sha256'], '%s children file differs from SOURCES.json pin' % name
        meta = json.loads(children)
        assert meta['source']['sha256'] == pin['sha256'] and meta['source']['commit'] == pin['commit'], '%s upstream pin mismatch' % name
        moment = json.loads((ROOT / 'certificates' / ('moment-%s.json' % name)).read_text())
        assert moment['children_sha256'] == digest and moment['passed'], '%s moment certificate is stale or failed' % name
        assert moment['a'] == saving, '%s moment certificate records another saving' % name
        print('sources PASS: %s children %s, upstream %s at %s, a = %s' % (name, digest[:12], pin['sha256'][:12], pin['commit'][:7], moment['a']))


if __name__ == '__main__':
    main()
