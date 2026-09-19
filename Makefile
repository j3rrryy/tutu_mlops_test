.PHONY: sync lint format test docker-up docker-down makemigrations migrate downgrade load-features

sync:
	uv sync --dev

lint:
	uv run --group lint ruff check --fix
	uv run --group lint mypy ./src

format:
	uv run --group lint ruff format

test:
	uv run --group test pytest -m "not e2e" ./src/tests --cov=./src --cov-config=./src/tests/.coveragerc --cov-fail-under=75

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
