PYTHON ?= python3
TECTONIC ?= tectonic

.PHONY: verify note

verify:
	$(PYTHON) scripts/verify_moment.py
	$(PYTHON) scripts/verify_moment.py --children certificates/network-children-pr200.json --a 3327/5000000
	$(PYTHON) scripts/verify_moment.py --children certificates/network-children-pr194.json --a 7009/10000000
	$(PYTHON) scripts/verify_moment.py --children certificates/network-children-pr233.json --a 7086/10000000
	$(PYTHON) scripts/check_sources.py

note:
	$(TECTONIC) -X compile notes/batched-dft-note.tex --outdir artifacts
