
import logging
import sys
from fire import Fire
import asyncio
from pathlib import Path

from llama_index.core import(
  StorageContext,
  VectorStoreIndex,
  SimpleDirectoryReader
)

from app.chat.llm_engine import (
    get_tool_service_context
)
from app.chat.pg_vector import get_vector_store_singleton

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


async def async_main_seed_storage_context():
    service_context = get_tool_service_context([])
    vector_store = await get_vector_store_singleton()
    path = Path(__file__).parent / "../manuals"

    documents = SimpleDirectoryReader(input_dir=path).load_data()
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_documents(
      documents=documents, storage_context=storage_context,service_context=service_context,show_progress=True
    )



def main_seed_storage_context():
    asyncio.run(async_main_seed_storage_context())


if __name__ == "__main__":
    Fire(main_seed_storage_context)