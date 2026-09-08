PYTHON ?= python

.PHONY: verify figures
verify:
	$(PYTHON) scripts/verify_repository.py

figures:
	$(PYTHON) scripts/build_figures.py --input-root $(INPUT_ROOT) --output-dir figures
