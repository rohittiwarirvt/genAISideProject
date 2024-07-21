# Gen AI backend build on FastAPI
WIP

- pyenv
- phoeny
- nextjs probably
- use chat template for reference
- prompts
- langfuse


Using Makefile
--
structure of app

--


db
localstack
opensearch
sqlalchemy
alembic

--

--

- create migrate script to get the db schmea in place



python script
- provide list of companies to download the documents
- go get document upload in loaclstack s3 and create corresponding embeeding


step to run docker ar
- docker compose create db
- docker compose start db

--
pyenv install

pyenv local

poetry init

poetry shell

poetry run alembic init migrate
https://www.youtube.com/watch?v=nt5sSr1A_qw&t=37s

poetry run python -m alembic revision --autogenerate -m "Added initial setup"

start server

for direct running using uvicorn
uvicorn app.restserver:app --host 0.0.0.0 --port 8080 --reload

for running through poetry
poetry install
poetry run start

sudo lsof -t -i tcp:8000 | xargs kill -9
