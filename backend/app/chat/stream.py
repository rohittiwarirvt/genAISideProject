import asyncio
import time
import anyio

from anyio import ClosedResourceError
from anyio.streams.memory import MemoryObjectSendStream
from pydantic import BaseModel
from faker import Faker
from app.spec import schema

class StreamedMessage(BaseModel):
  content:str


async def handle_chat_message(
  conversation: schema.ConversationCreate,
  user_message: schema.UserMessageCreate,
  send_chan: MemoryObjectSendStream
  )-> None:
  async with send_chan:
    fake = Faker()
    start_time = time.time()
    while time.time() - start_time < 5:
      data = StreamedMessage(content=fake.paragraph(nb_sentences=1))
      await send_chan.send(data)
      await anyio.sleep(1)
