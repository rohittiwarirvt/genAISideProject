from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID, uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from sse_starlette.sse import EventSourceResponse
import asyncio
import anyio
from app.spec.schema import (
  ConversationResp,
  ConversationCreate,
  MessageResp,
  StreamedMessage
)


from app.chat.stream import handle_chat_message as fake_handle_chat_message
from app.chat.chat import openai_handle_chat_message

from app.models.db import Message, MessageRoleEnum, MessageStatusEnum

from app.api.init.deps import get_db
from app.api.dl.conversation import (
  create_conversation as dl_create_conversation,
  fetch_conversation_with_messages,
  delete_conversation as dl_delete_conversation,
  fetch_message
)

router = APIRouter()

@router.post("/")
async def create_conversation( db: AsyncSession = Depends(get_db) ) -> ConversationResp:
  return await dl_create_conversation(db)

@router.get("/{conversation_id}")
async def get_conversation(
  conversation_id: UUID, db : AsyncSession = Depends(get_db)
  ) -> ConversationResp:
  conversation = await fetch_conversation_with_messages(db, str(conversation_id))
  if conversation is None:
    raise HTTPException(status_code=404, detail="Conversation not found")
  return conversation

@router.delete(
  "/{conversation_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT
  )
async def delete_conversation(conversation_id: UUID, db: AsyncSession = Depends(get_db)):
  did_delete = await dl_delete_conversation(db, str(conversation_id))
  if not did_delete:
    raise HTTPException(status_code=404, detail="Conversation not found")
  return




@router.get("/{conversation_id}/message")
async def message_conversation(
  conversation_id: UUID, user_message: str,
  db: AsyncSession = Depends(get_db)
) -> EventSourceResponse:
  # ferch all msg with conv
  conversation = await fetch_conversation_with_messages(db, str(conversation_id))

  if not conversation:
    raise HTTPException(status_code=404, detail="Conversation not found")
  #create message object
  user_message = Message(
    created_at=datetime.utcnow(),
    update_at=datetime.utcnow(),
    content=user_message,
    conversation_id=conversation_id,
    status=MessageStatusEnum.SUCCESS,
    role=MessageRoleEnum.user
  )

  #create channel for community across methods

  send_chan, recv_chan = anyio.create_memory_object_stream(100)

  # open send chan and pass to chatbot for it to strea respose to id
  async def event_publisher():
    async with send_chan:
      task = asyncio.create_task(
        openai_handle_chat_message(conversation, user_message, send_chan)
      )

      message_id = str(uuid4())
      # create Message
      message = Message(
        created_at=datetime.utcnow(),
        update_at=datetime.utcnow(),
        content="",
        id=message_id,
        conversation_id=conversation_id,
        status=MessageStatusEnum.PENDING,
        role=MessageRoleEnum.assistant
      )
      try:
        async for message_obj in recv_chan:
          if (isinstance(message_obj, StreamedMessage)):
            message.content = message_obj.content
          else:
            print("invalid response")
            continue
          yield MessageResp.from_orm(message).json()
        await task
        if task.exception():
          raise ValueError("hanlder chat message task failed") from task.exception()
        final_status = MessageStatusEnum.SUCCESS
      except RuntimeError as error:
        print(error)
        print("errror in exception")
        final_status = MessageStatusEnum.ERROR
      message.status = final_status
      db.add(user_message)
      db.add(message)
      await db.commit()
      #await db.refresh(message)
      final_message = await fetch_message(db, message_id)
      yield final_message.json()
  return EventSourceResponse(event_publisher())


@router.get("/{conversation_id}/mockllm-message")
async def message_conversation(
  conversation_id: UUID, user_message: str,
  db: AsyncSession = Depends(get_db)
) -> EventSourceResponse:
  # ferch all msg with conv
  conversation = await fetch_conversation_with_messages(db, str(conversation_id))

  if not conversation:
    raise HTTPException(status_code=404, detail="Conversation not found")
  #create message object
  user_message = Message(
    created_at=datetime.utcnow(),
    update_at=datetime.utcnow(),
    content=user_message,
    conversation_id=conversation_id,
    status=MessageStatusEnum.SUCCESS,
    role=MessageRoleEnum.user
  )

  #create channel for community across methods

  send_chan, recv_chan = anyio.create_memory_object_stream(100)

  # open send chan and pass to chatbot for it to strea respose to id
  async def event_publisher():
    async with send_chan:
      task = asyncio.create_task(
        fake_handle_chat_message(conversation, user_message, send_chan)
      )

      message_id = str(uuid4())
      # create Message
      message = Message(
        created_at=datetime.utcnow(),
        update_at=datetime.utcnow(),
        content="",
        id=message_id,
        conversation_id=conversation_id,
        status=MessageStatusEnum.PENDING,
        role=MessageRoleEnum.assistant
      )
      try:
        async for message_obj in recv_chan:
          if (isinstance(message_obj, StreamedMessage)):
            message.content = message_obj.content
          else:
            print("invalid response")
            continue
          yield MessageResp.from_orm(message).json()
        await task
        if task.exception():
          raise ValueError("hanlder chat message task failed") from task.exception()
        final_status = MessageStatusEnum.SUCCESS
      except RuntimeError as error:
        print(error)
        print("errror in exception")
        final_status = MessageStatusEnum.ERROR
      message.status = final_status
      db.add(user_message)
      db.add(message)
      await db.commit()
      #await db.refresh(message)
      final_message = await fetch_message(db, message_id)
      yield final_message.json()
  return EventSourceResponse(event_publisher())