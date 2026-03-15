# FeigenbaumIA — Makefile
PYTHON  := python
PYTEST  := pytest
PYTHONPATH_PREFIX := PYTHONPATH=.

.PHONY: all test test-fast demo1 demo2 demo3 lint clean status

all: test demo1

test:
	$(PYTEST) tests/ -v

test-fast:
	$(PYTEST) tests/ -q

demo1:
	$(PYTHONPATH_PREFIX) $(PYTHON) experiments/phase1_demo.py

demo2:
	$(PYTHONPATH_PREFIX) $(PYTHON) experiments/phase2_demo.py

demo3:
	$(PYTHONPATH_PREFIX) $(PYTHON) experiments/phase3_demo.py

lint:
	$(PYTHON) -m py_compile src/*.py experiments/*.py tests/*.py && echo "Syntax OK"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	rm -rf melissa_output/ experiments/*.png

status:
	@echo "=== FeigenbaumIA Status ==="
	@$(PYTHON) -c "from src.constants import FEIGENBAUM_DELTA; print(f'delta = {FEIGENBAUM_DELTA:.10f}')"
	@$(PYTEST) tests/ -q --no-header 2>&1 | tail -1
