
import asyncio
import time
import logging
import anyio

from anyio import ClosedResourceError
from anyio.streams.memory import MemoryObjectSendStream
from pydantic import BaseModel
from typing import Optional,Dict,Any, List
from app.spec import schema
from app.chat.llm_engine import get_chat_engine
from llama_index.core.chat_engine.types import StreamingAgentChatResponse
from llama_index.core.callbacks.base import BaseCallbackHandler
from llama_index.core.callbacks.schema import CBEventType
logger = logging.getLogger(__name__)




class ChatCallbackHandler(BaseCallbackHandler):
    def __init__(
        self,
        send_chan: MemoryObjectSendStream,
    ):
        """Initialize the base callback handler."""
        ignored_events = [CBEventType.CHUNKING, CBEventType.NODE_PARSING]
        super().__init__(ignored_events, ignored_events)
        self._send_chan = send_chan

    def on_event_start(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> str:
        """Create the MessageSubProcess row for the event that started."""
        asyncio.create_task(
            self.async_on_event(
                event_type, payload, is_start_event=True, **kwargs
            )
        )

    def on_event_end(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Create the MessageSubProcess row for the event that completed."""
        asyncio.create_task(
            self.async_on_event(
                event_type, payload,  is_start_event=False, **kwargs
            )
        )

    async def async_on_event(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        is_start_event: bool = False,
        **kwargs: Any,
    ) -> None:

        if self._send_chan._closed:
            logger.debug("Received event after send channel closed. Ignoring.")
            return

    def start_trace(self, trace_id: Optional[str] = None) -> None:
        """No-op."""

    def end_trace(
        self,
        trace_id: Optional[str] = None,
        trace_map: Optional[Dict[str, List[str]]] = None,
    ) -> None:
        """No-op."""


async def openai_handle_chat_message(
    conversation: schema.ConversationCreate,
    user_message: schema.UserMessageCreate,
    send_chan: MemoryObjectSendStream,
) -> None:
    async with send_chan:
        chat_engine = await get_chat_engine(
            ChatCallbackHandler(send_chan), conversation
        )

        logger.debug("Engine received")
        templated_message = f"""
Remember - if I have asked a relevant product service question, please answer correctly.

{user_message.content}
        """.strip()
        streaming_chat_response: StreamingAgentChatResponse = (
            await chat_engine.astream_chat(templated_message)
        )
        response_str = ""
        async for text in streaming_chat_response.async_response_gen():
            ## just to simulate streaming
            await anyio.sleep(.1)
            response_str += text
            if send_chan._closed:
                logger.debug(
                    "Received streamed token after send channel closed. Ignoring."
                )
                return
            await send_chan.send(schema.StreamedMessage(content=response_str))

        if response_str.strip() == "":
            await send_chan.send(
                StreamedMessage(
                    content="Sorry, I either wasn't able to understand your question or I don't have an answer for it."
                )
            )
