PYTHON ?= python3
TECTONIC ?= tectonic

.PHONY: verify note

verify:
	$(PYTHON) scripts/verify_moment.py
	$(PYTHON) scripts/verify_moment.py --children certificates/network-children-pr200.json --a 3327/5000000
	$(PYTHON) scripts/verify_moment.py --children certificates/network-children-pr194.json --a 7009/10000000
	$(PYTHON) scripts/verify_moment.py --children certificates/network-children-pr233.json --a 7099/10000000
	$(PYTHON) scripts/five_stage_children.py certificates/network-children-pr194.json /tmp/five-pr194.json && cmp /tmp/five-pr194.json certificates/network-children-pr194-five.json
	$(PYTHON) scripts/five_stage_children.py certificates/network-children-pr233.json /tmp/five-pr233.json && cmp /tmp/five-pr233.json certificates/network-children-pr233-five.json
	$(PYTHON) scripts/verify_moment.py --children certificates/network-children-pr194-five.json --a 7474/10000000
	$(PYTHON) scripts/verify_moment.py --children certificates/network-children-pr233-five.json --a 7547/10000000
	$(PYTHON) scripts/check_sources.py

note:
	$(TECTONIC) -X compile notes/batched-dft-note.tex --outdir artifacts
