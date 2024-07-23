init_db:
	docker compose create db
	docker compose start db
	docker compose create opensearch
	docker compose start opensearch
	make init_appschema


init_appschema:
	poetry run python -m alembic upgrade head
	poetry run python -m alembic revision --autogenerate -m "Added initial setup"
	poetry run python -m alembic upgrade head
	poetry run python -m scripts.build_vector_tables

refresh_db:
	docker compose stop db
	docker compose rm db
	docker volume rm backend_postgres_data_genai
	docker compose create db
	docker compose start db
	rm -rf migrations/versions/*
	make init_appschema

run:
	poetry run start
