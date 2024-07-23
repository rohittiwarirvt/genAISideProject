# Learn Gen AI backend build on FastAPI


## Small Walkthrough
<img alt="screengrab.gif" src="https://github.com/rohittiwarirvt/genAISideProject/blob/master/backend/manuals/screengrab.gif?raw=true" data-hpc="true" >

### Components/Workflow
<img alt="chat-draw.png" src="https://github.com/rohittiwarirvt/genAISideProject/blob/master/backend/manuals/chat-draw.png?raw=true" data-hpc="true" >

Note:
    - UI supports openllm can set `NEXT_PUBLIC_IS_MOCKEDLLM=false // or default is true` to switch openai llm calls or use mockllm streaming  faker to stream every 1/3 of second


## Components

1. Frontend
   1. Used [NextJs](https://nextjs.org/docs) which supports React+SSR for seo purpose
   2. Used Page router for demo but should use app routing leveraging the Performance Gains via streaming
   3. Used T3-One for starterkit and tailwind.css for styles(Still needs a lot of work)
   4. Used docker to build and run the container
2. Backend
   1. [Fast API](https://fastapi.tiangolo.com/), pydantic, sse-starlette, asyncio, alembic and sqlalchemy for ORM by postgres.(triend Opensearch but interface is problematic)
3. Framework/dependecies
    Lamaindex for llm indexing, querying and building chat engine.
    Used OpenAI for simple llm interaction
4. Deployment
   1. Use Docker compose to build container , can be use with aws serverless, ecr to do deploy
5. Observability + Fine Tuning + Evalution

@Todo
- next-auth to do authentication using jwt
- test cases
- ui cleanup/chat history show side bar
- Error handling
- edge cases
-
## Setup Backend Workspace

1. Install [pyenv](https://github.com/pyenv/pyenv#automatic-installer) and then use it to install the Python version in `.python-version`. Good article to getteing started [here](https://douwevandermeij.medium.com/proper-python-setup-with-pyenv-poetry-4d8baea329a8)

2. install pyenv with `curl https://pyenv.run | bash`

3. [Install docker](https://docs.docker.com/engine/install/)

4. Please follow to install pyenv python and finally poetry then use `poetry shell`
   1. ```
      pyenv versions

      sudo apt update; sudo apt install build-essential libssl-dev zlib1g-dev \
      libbz2-dev libreadline-dev libsqlite3-dev curl \
      libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

      pyenv install 3.11
      pyenv versions

      pyenv global 3.11.7
      which python

      pyenv global system
      pyenv versions
      pyenv local 3.12


      pip install poetry
      poetry shell
      python -v
      poetry install
        ```

2. Create the `.env` file and source it. The `.env.backend` file is a good template.

4. `cp .env.backend .env`

5. `set -a`

6. `source .env`

7. cd backend/ && docker compose up -d

8. Run the database migrations with `make init_db`
9. Lastly, we will  want to populate your local database with some sample manuals index provided in manuals directory for starting out
    - I have a script for this! But first, open your `.env` file and replace the placeholder value for the `OPENAI_API_KEY` with your own OpenAI API key
    - You can Get an OPENAI_API_KEY from [here](https://platform.openai.com/api-keys)
    - Source the file again with `set -a` then `source .env`
    - Run `make index_knowledgebase`
        - If this step fails, you may find it helpful to run `make refresh_db` to wipe your local database and re-start with emptied tables.
10. Rune for seeding the database with vectorembedding if not done already `make index_knowledgebase`
11. Run `make run` to start the server locally

    - Done 🏁! You can run `make run` again and you should see some backend running and  loaded at http://localhost:8000

 -- create coversation `curl --location --request POST 'http://localhost:8000/api/conversation'`

 -- Chat with llms  `curl --location --request GET 'http://localhost:8000/api/conversation/c8db9594-235e-42c3-8c3b-5369a98d0b8f/message?user_message="What is manual about?"'"`

 -- Chat with fakerLLm GET `curl --location --request GET 'http://localhost:8000/api/conversation/c8db9594-235e-42c3-8c3b-5369a98d0b8f/mockllm-message?user_message="What is manual about?"'`

## Setup Frontend Workspace

### Docker Way only needs docker
1. [Install docker](https://docs.docker.com/engine/install/)

2. Create the `.env` file and source it. The `.env.frontend` file is a good template.

3. `cp .env.frontend .env`

4. `set -a`

5. `source .env`

6. `docker compose up -d`.

- Done 🏁! You can run `make run` again and you should see some frontend running and  loaded at http://localhost:3000 or `http://[dockerip:3000]

### Local Run
1. next part is not needed if node > Node.js 18.17 or later

2. Install nvm to as next js needs node greater then 18 or install by running in bash `curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash`


3. start dev locally `npm run dev`


- I have provide vscode launch file as well to make it work [here](https://github.com/rohittiwarirvt/genAISideProject/blob/master/.vscode/launch.json)




