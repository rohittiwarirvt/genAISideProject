init_db:
	docker compose create genaipg
	docker compose start genaipg
	make init_appschema

init_appschema:
	poetry run python -m alembic upgrade head
	poetry run python -m alembic revision --autogenerate -m "Added initial setup"
	poetry run python -m alembic upgrade head
	poetry run python -m scripts.vector_schema_init

index_knowledgebase:
	poetry run python -m scripts.seed_vectorindex

refresh_db:
	docker compose stop genaipg
	docker compose rm genaipg
	docker volume rm backend_postgres_data_genai
	docker compose create genaipg
	docker compose start genaipg
	rm -rf migrations/versions/*
	make init_appschema

run:
	poetry run start
