
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import Optional

from app.spec import schema
from app.models.db import Conversation, Message


async def fetch_conversation_with_messages(db: AsyncSession, conversation_id : str) -> Optional[schema.ConversationResp]:
    """_summary_

    Args:
        db (AsyncSession): _description_
        coversation_id (str): _description_

    Returns:
        Optional[schema.Coversation]: _description_
    """
    stmt = (
        select(Conversation)
        .options(joinedload(Conversation.messages))
    ).where(Conversation.id == conversation_id)

    result = await db.execute(stmt)
    conversation = result.scalars().first()
    if conversation is not None:
        convo_dict = {**conversation.__dict__ }
        return schema.ConversationResp(**convo_dict)
    return None


async def create_conversation(db: AsyncSession ) -> schema.ConversationCreate:
    conversation = Conversation()
    db.add(conversation)
    await db.commit()
    await db.refresh(conversation)
    return await fetch_conversation_with_messages(db, conversation.id)


async def delete_conversation(db: AsyncSession, conversation_id: str ):
    stmt = delete(Conversation).where(Conversation.id==conversation_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0


async def fetch_message(
    db: AsyncSession, message_id: str
) -> Optional[schema.MessageResp]:
    """
    Fetch a message with its sub processes
    return None if the message with the given id does not exist
    """
    # Eagerly load required relationships
    stmt = (
        select(Message)
        .where(Message.id == message_id)
    )
    result = await db.execute(stmt)  # execute the statement
    message = result.scalar_one_or_none()  # get the first result
    if message is not None:
        return schema.MessageResp.from_orm(message)
    return None