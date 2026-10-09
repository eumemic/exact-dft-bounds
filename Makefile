PYTHON ?= python3
TECTONIC ?= tectonic

.PHONY: verify note

verify:
	$(PYTHON) scripts/verify_moment.py
	$(PYTHON) scripts/check_sources.py

note:
	$(TECTONIC) -X compile notes/batched-dft-note.tex --outdir artifacts
