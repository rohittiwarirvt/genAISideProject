import asyncio
import time
import anyio

from anyio import ClosedResourceError
from anyio.streams.memory import MemoryObjectSendStream
from pydantic import BaseModel
from faker import Faker
from app.spec import schema


"""This function will be used for testing streaming of answer to a question by faker
"""
async def handle_chat_message(
  conversation: schema.ConversationCreate,
  user_message: schema.UserMessageCreate,
  send_chan: MemoryObjectSendStream
  )-> None:
  async with send_chan:
    fake = Faker()
    start_time = time.time()
    response_str = ""
    while time.time() - start_time < 5:
      response_str+=fake.paragraph(nb_sentences=1)
      data = schema.StreamedMessage(content=response_str)
      await send_chan.send(data)
      await anyio.sleep(1)
