PYTHON=python3
VENV=.venv

.PHONY: run setup format test clean

run:
	./$(VENV)/bin/streamlit run streamlit_app.py

setup: clean
	$(PYTHON) -m venv $(VENV)
	./$(VENV)/bin/python -m pip install --upgrade pip
	./$(VENV)/bin/python -m pip install -r requirements.txt

test:
	./$(VENV)/bin/python pawky/test.py
	./$(VENV)/bin/python pregexy/test.py

format:
	yapf -ir .

clean:
	rm -rf $(VENV)
