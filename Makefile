# FeigenbaumIA — Makefile
# Uso: make test | make demo1 | make demo2 | make demo3 | make all

PYTHON := python
PYTEST := pytest

.PHONY: all test demo1 demo2 demo3 lint clean status-report

all: test demo1

test:
	$(PYTEST) tests/ -v

test-fast:
	$(PYTEST) tests/ -q

demo1:
	PYTHONPATH=. $(PYTHON) experiments/phase1_demo.py

demo2:
	PYTHONPATH=. $(PYTHON) experiments/phase2_demo.py

demo3:
	PYTHONPATH=. $(PYTHON) experiments/phase3_demo.py

lint:
	python -m py_compile src/*.py experiments/*.py tests/*.py && echo "Syntax OK"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null; \
	find . -name "*.pyc" -delete; \
	rm -rf melissa_output/ experiments/*.png

status:
	@echo "=== FeigenbaumIA Status ==="
	@python -c "from src.constants import FEIGENBAUM_DELTA; print(f'δ = {FEIGENBAUM_DELTA}')"
	@echo "Tests:"; $(PYTEST) tests/ -q --no-header 2>&1 | tail -1


status-report:
	@echo "Relatório atual: docs/PROJECT_STATUS.md"
	@sed -n "1,40p" docs/PROJECT_STATUS.md
