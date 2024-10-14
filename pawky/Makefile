PYTHON=python3
VENV=.venv

.PHONY: setup format test clean

setup: clean
	$(PYTHON) -m venv $(VENV)
	./$(VENV)/bin/python -m pip install --upgrade pip
	./$(VENV)/bin/python -m pip install -r requirements.txt

install:
	$(PYTHON) -m pip install -e .

format:
	yapf -ir .

test:
	./$(VENV)/bin/python test.py

clean:
	rm -rf $(VENV)
	rm -f awk/parser.out awk/parsetab.py
	rm -rf awk/__pycache__ parsetab.py __pycache__
