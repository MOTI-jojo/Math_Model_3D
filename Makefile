.PHONY: install run test lint clean docker-build docker-run

VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

install:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	$(VENV)/bin/streamlit run app.py

test:
	$(PYTHON) -m pytest tests/

lint:
	$(VENV)/bin/ruff check .

clean:
	rm -rf __pycache__ .pytest_cache .ruff_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf $(VENV)

docker-build:
	docker build -t math-model-3d .

docker-run: docker-build
	docker run -p 8501:8501 math-model-3d
