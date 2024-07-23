import sys

from os import getenv
from pathlib import Path
from datetime import datetime

from llama_index.core import (
    ServiceContext,
    VectorStoreIndex
)

from typing import List
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.llms.openai import  OpenAI
from llama_index.agent.openai import OpenAIAgent

from llama_index.embeddings.openai import (
    OpenAIEmbedding,
    OpenAIEmbeddingMode,
    OpenAIEmbeddingModelType,
)
from llama_index.core.chat_engine.types import BaseChatEngine
from llama_index.core.tools import QueryEngineTool
from llama_index.core.tools import ToolMetadata

from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.base.base_query_engine import BaseQueryEngine

from llama_index.core.callbacks.base import BaseCallbackHandler, CallbackManager
from llama_index.core import(
  VectorStoreIndex,
  StorageContext
)
from app.core.config import settings
from app.spec.schema import MessageResp, ConversationResp

from app.models.db import MessageRoleEnum, MessageStatusEnum
from app.chat.pg_vector import get_vector_store_singleton

from app.consts.const import (
  NODE_PARSER_CHUNK_OVERLAP,
  NODE_PARSER_CHUNK_SIZE,
  OPENAI_TOOL_LLM_NAME,
  OPENAI_CHAT_LLM_NAME
)
from app.chat.prompt import SYSTEM_MESSAGE

async def get_index_from_pg() -> VectorStoreIndex:
  service_context = get_tool_service_context([])
  vector_store = await get_vector_store_singleton()
  storage_context = StorageContext.from_defaults(vector_store=vector_store)

  index = VectorStoreIndex.from_vector_store(vector_store=vector_store,
    storage_context=storage_context,service_context=service_context,show_progress=True
  )
  return index


def index_to_query_engine(index: VectorStoreIndex) -> BaseQueryEngine:
  kwargs = {"similarity_top_k": 3}
  return index.as_query_engine(**kwargs)


def get_tool_service_context(
  callback_handlers: List[BaseCallbackHandler]
) -> ServiceContext:
  llm = OpenAI(
    temperature=0,
    model=OPENAI_TOOL_LLM_NAME,
    streaming=False,
    api_key=settings.OPENAI_API_KEY
  )

  callback_manager = CallbackManager(callback_handlers)
  embedding_model = OpenAIEmbedding(
    mode=OpenAIEmbeddingMode.SIMILARITY_MODE,
    model_type=OpenAIEmbeddingModelType.TEXT_EMBED_ADA_002,
    api_key=settings.OPENAI_API_KEY
  )

  node_parser = SentenceSplitter(
    chunk_size=NODE_PARSER_CHUNK_SIZE,
    chunk_overlap=NODE_PARSER_CHUNK_OVERLAP,
    callback_manager=callback_manager
  )

  service_context = ServiceContext.from_defaults(
    callback_manager=callback_manager,
    llm=llm,
    embed_model=embedding_model,
    node_parser=node_parser
  )
  return service_context



def get_chat_history(
    chat_messages: List[MessageResp],
) -> List[ChatMessage]:
    """
    Given a list of chat messages, return a list of ChatMessage instances.

    Failed chat messages are filtered out and then the remaining ones are
    sorted by created_at.
    """
    chat_messages = [
        m
        for m in chat_messages
        if m.content.strip() and m.status == MessageStatusEnum.SUCCESS
    ]

    chat_messages = sorted(chat_messages, key=lambda m: m.created_at)

    chat_history = []
    for message in chat_messages:
        role = (
            MessageRole.ASSISTANT
            if message.role == MessageRoleEnum.assistant
            else MessageRole.USER
        )
        chat_history.append(ChatMessage(content=message.content, role=role))

    return chat_history

async def get_chat_engine(
  callback_handlers: BaseCallbackHandler,
  conversation: ConversationResp
) -> BaseChatEngine:

  service_context = get_tool_service_context([callback_handlers])

  index = await get_index_from_pg();
  manual_engine = index_to_query_engine(index)
  query_engine_tools = [
    QueryEngineTool(
        query_engine=manual_engine,
        metadata=ToolMetadata(
            name="washine machine manual",
            description="Provides information about Washing machines. "
            "Use a detailed plain text question as input to the tool.",
        )
    ),
  ]
  chat_messages: List[MessageResp] = conversation.messages
  chat_history = get_chat_history(chat_messages)
  print(chat_history)
  chat_llm = OpenAI(
        temperature=0,
        model=OPENAI_CHAT_LLM_NAME,
        streaming=True,
        api_key=settings.OPENAI_API_KEY,
  )
  curr_date = datetime.utcnow().strftime("%Y-%m-%d")
  chat_engine = OpenAIAgent.from_tools(
        llm=chat_llm,
        chat_history=chat_history,
        verbose=settings.VERBOSE,
        callback_manager=service_context.callback_manager,
        max_function_calls=3,
        system_prompt=SYSTEM_MESSAGE.format(curr_date=curr_date)
  )

  return chat_engine

