
import { useState } from "react";
import { v4 as uuidv4 } from "uuid";
import { ROLE, MESSAGE_STATUS, Message } from "@/types/conversation";
import { getDateWithUTCOffset } from "@/lib/timezone";

const useMessages = (conversationID: string) => {
  const [messages, setMessages] = useState<Message[]>([]);

  const userSendMessage = (content: string) => {
    setMessages((prevMessages) => [
      ...prevMessages,

      {
        id: uuidv4(),
        conversationID,
        content,
        role: ROLE.USER,
        status: MESSAGE_STATUS.PENDING,
        created_at: getDateWithUTCOffset(),
      },
    ]);
  };

  const systemSendMessage = (message: Message) => {
    setMessages((prevMessages) => {
      const existingMessageIndex = prevMessages.findIndex(
        (msg) => msg.id === message.id
      );

      // Update the existing message
      if (existingMessageIndex > -1) {
        const updatedMessages = [...prevMessages];
        updatedMessages[existingMessageIndex] = message;
        return updatedMessages;
      }

      // Add a new message if it doesn't exist
      return [...prevMessages, message];
    });
  };

  return {
    messages,
    userSendMessage,
    setMessages,
    systemSendMessage,
  };
};

export default useMessages;
