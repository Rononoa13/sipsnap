.PHONY: install test lint format docker-build docker-up docker-down

install:
	cd backend && python3 -m pip install -r requirements.txt

test:
	cd backend && python -m pytest

lint:
	cd backend && ruff check .

format:
	cd backend && ruff format .

docker-build:
	docker compose build

docker-up:
	docker compose up

docker-down:
	docker compose down