import logging
import sys

from os import getenv
from pathlib import Path


from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter

from llama_index.vector_stores.opensearch import(
  OpensearchVectorClient,
  OpensearchVectorStore
)

from llama_index.llms.openai import  OpenAI

from llama_index.core import(
  VectorStoreIndex,
  StorageContext,
  ServiceContext
)
from llama_index.embeddings.openai import (
    OpenAIEmbedding,
    OpenAIEmbeddingMode,
    OpenAIEmbeddingModelType,
)

OPENAI_TOOL_LLM_NAME = "gpt-3.5-turbo"
OPENAI_CHAT_LLM_NAME = "gpt-3.5-turbo"

NODE_PARSER_CHUNK_SIZE = 512
NODE_PARSER_CHUNK_OVERLAP = 10

def get_tool_service_context(
) -> ServiceContext:
  llm = OpenAI(
    temperature=0,
    model=OPENAI_TOOL_LLM_NAME,
    api_key=OPENAI_API_KEY
  )

  # callback_manager = CallbackManager(callback_handlers)
  embedding_model = OpenAIEmbedding(
    mode=OpenAIEmbeddingMode.SIMILARITY_MODE,
    model_type=OpenAIEmbeddingModelType.TEXT_EMBED_ADA_002,
    api_key=OPENAI_API_KEY
  )

  node_parser = SentenceSplitter.from_defaults(
    chunk_size=NODE_PARSER_CHUNK_SIZE,
    chunk_overlap=NODE_PARSER_CHUNK_OVERLAP,
    # callback_manager=callback_manager
  )

  service_context = ServiceContext.from_defaults(
    # callback_manager=callback_manager,
    llm=llm,
    embed_model=embedding_model,
    node_parser=node_parser
  )
  return service_context





logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


endpoint = getenv("OPENSEARCH_ENDPOINT", "http://localhost:9200")

idx = getenv("OPENSEARCH_INDEX", "gpt-index-manuals-genai")

OPENAI_API_KEY = getenv("OPENAI_API_KEY")

path = Path(__file__).parent / "../manuals"
# print(path)

# documents = SimpleDirectoryReader(input_dir=path).load_data()
documents = SimpleDirectoryReader(input_dir=path).load_data()
text_field = "content"
# OpensearchVectorClient stores embeddings in this field by default
embedding_field = "embedding"
# OpensearchVectorClient encapsulates logic for a
# single opensearch index with vector search enabled
client = OpensearchVectorClient(
    endpoint, idx, 1536, embedding_field=embedding_field, text_field=text_field
)

service_context = get_tool_service_context()

vector_store = OpensearchVectorStore(client)
storage_context = StorageContext.from_defaults(vector_store=vector_store)


index = VectorStoreIndex.from_documents(
    documents=documents, storage_context=storage_context,service_context=service_context,show_progress=True
)


# index = VectorStoreIndex.from_vector_store(vector_store, show_progress=True, service_context=service_context)


chat_engine = index.as_chat_engine(
    chat_mode="context", streaming=True
)
# chat_engine.chat_history

response_stream = chat_engine.stream_chat("What are the product about?")
response_stream.print_response_stream()

response_stream = chat_engine.stream_chat("How I can clean machine?")

response_stream.print_response_stream()

response_stream = chat_engine.stream_chat("Can you summarize in 5 words the maintainace steps?")
response_stream.print_response_stream()