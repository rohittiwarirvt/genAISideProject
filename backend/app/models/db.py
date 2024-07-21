
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Enum, ForeignKey
from app.models.base import Base
from enum import Enum


# define this
class MessageRoleEnum(str, Enum):
  user = "user"
  assistant = "assistant"

class MessageStatusEnum(str, Enum):
  PENDING = "PENDING"
  SUCCESS = "SUCCESS"
  ERROR = "ERROR"


# to_pg_enum()
def to_pg_enum(enum_class)-> ENUM:
  return ENUM(enum_class, name=enum_class.__name__)

class Conversation(Base):
  """_summary_

  Args:
      Base (_type_): _description_
  """
  # conversation_document= relationship("ConversationDocument", back_populates="conversation")
  messages = relationship("Message", back_populates="conversation")

class Message(Base):
  """_summary_

  Args:
      Base (_type_): _description_
  """
  conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversation.id"), index=True)
  content = Column(String)
  role = Column(to_pg_enum(MessageRoleEnum))
  status = Column(to_pg_enum(MessageStatusEnum), default=MessageStatusEnum.PENDING)
  conversation = relationship("Conversation", back_populates="messages")


class Document(Base):
  """_summary_
  """
  url = Column(String, nullable=False, unique=True)
  # conversations = relationship("ConversationDocument", back_populates="document")


# class ConversationDocument(Base):
#   """_summary_

#   Args:
#       Base (_type_): _description_
#   """
#   conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversation.id"), index=True)
#   document_id = Column(UUID(as_uuid=True), ForeignKey("document.id"), index=True)
#   conversation = relationship("Conversation", back_populates="conversation_documents")
#   document = relationship("Document", back_populates="conversations")




