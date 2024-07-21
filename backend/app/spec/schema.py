
from datetime import datetime

from  alembic.config import Config
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID


from app.models.db import MessageRoleEnum, MessageStatusEnum


class Base(BaseModel):
  id: Optional[UUID] = Field(None, description="Unique identifier")
  created_at: Optional[datetime] = Field(None, description="Creation datetime")
  updated_at: Optional[datetime] = Field(None, description="Update datetime")

  class Config:
    from_attributes = True
    arbitrary_types_allowed =  True


class UserMessageCreate(BaseModel):
  content: str

class ConversationCreate(BaseModel):
  pass

class MessageResp(Base):
  conversation_id: UUID
  content: str
  role: MessageRoleEnum
  status: MessageStatusEnum

class ConversationResp(Base):
  messages: List[MessageResp]
