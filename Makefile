.PHONY: install
install:
	pip install -U poetry && poetry install

.PHONY: install-pre-commit
install-pre-commit:
	poetry run pre-commit install --hook-type pre-commit

.PHONY: update
update:
	poetry update

.PHONY: lint
lint:
	poetry run pre-commit run

.PHONY: rundev
rundev:
	poetry run uvicorn backend.app.main:app --reload --port=8000 --host=0.0.0.0