.PHONY: sync lint format test test-all docker-up docker-down makemigrations migrate downgrade load-features

sync:
	uv sync --dev

lint:
	uv run --group lint ruff check --fix
	uv run --group lint mypy ./src

format:
	uv run --group lint ruff format

test:
	uv run --group test pytest -m "not e2e" ./src/tests --cov=./src --cov-config=./src/tests/.coveragerc --cov-fail-under=75

test-all:
	docker build -t mlops_app:test .
	docker compose -f ./docker-compose.test.yml up --abort-on-container-exit --exit-code-from mlops_app mlops_app
	docker compose -f ./docker-compose.test.yml down -v

docker-up:
	docker compose up -d --build

docker-down:
	docker compose down

makemigrations:
	docker compose run --rm migrate uv run alembic revision --autogenerate -m "$(m)"

migrate:
	docker compose run --rm migrate uv run alembic upgrade head

downgrade:
	docker compose run --rm migrate uv run alembic downgrade -1

load-features:
	docker compose run --rm item_features_loader
