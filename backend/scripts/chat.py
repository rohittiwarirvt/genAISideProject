from os import getenv
from pathlib import Path

from llama_index.core  import SimpleDirectoryReader
from llama_index.vector_stores.opensearch import(
  OpensearchVectorClient,
  OpensearchVectorStore
)

from llama_index.core import(
  VectorStoreIndex,
  StorageContext
)

endpoint = getenv("OPENSEARCH_ENDPOINT", "http://localhost:9200")

idx = getenv("OPENSEARCH_INDEX", "gpt-index-demo-resume")

path = Path(__file__).parent / "../resumes"
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


vector_store = OpensearchVectorStore(client)
storage_context = StorageContext.from_defaults(vector_store=vector_store)


# index = VectorStoreIndex.from_documents(
#     documents=documents, storage_context=storage_context
# )


index = VectorStoreIndex.from_vector_store(vector_store)

query_engine = index.as_query_engine()
# res = query_engine.query("What is Rohits Tiwari skills compared to harshita profile?")
res = query_engine.query("How many years of experienc Urmila Manjarikar has and Top 5 Skill of Her?")
res.response
print(res.response)