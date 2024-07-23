
import React, { useEffect, useRef } from "react";
import { Message, ROLE } from '@/types/conversation'

import AssistantMessageDisplay  from "@/components/conversation/AssistantMessageDisplay"
import UserMessageDisplay  from "@/components/conversation/UserMessageDisplay"


interface IRenderConversation {
  messages: Message[];
  setUserMessage: (str: string) => void;
}

export const RenderConversations: React.FC<IRenderConversation> = ({
  messages,
  setUserMessage
}) => {
  const lastElementRef = useRef<HTMLDivElement | null>(null)
  useEffect(() =>{
  if (lastElementRef.current) {
    lastElementRef.current.scrollIntoView()
  }
  },[messages])

  const showLoading = messages[messages.length -1]?.role === ROLE.USER;
  return (
    <div className="box-border flex h-full flex-col justify-start font-nunito text-sm text-[#2B3175]">
      {messages.map( (message, index) => {
        let display
        if (message.role == ROLE.ASSISTANT) {
          display = (
            <AssistantMessageDisplay
              message={message}
              key={`${message.id}-answer-${index}`}
              showLoading={showLoading}
            />
          );
        } else if  (message.role == ROLE.USER) {
          display = (
            <UserMessageDisplay
              message={message}
              key={`${message.id}-question-${index}-user`}
              showLoading={index === messages.length - 1 ? showLoading : false}
            />
          );
        } else {
          display = <div>Sorry, there is a problem.</div>;
        }
        if (index === messages.length - 1) {
          return (
            <div className="mb-4 flex flex-col" key={`message-${message.id}`}>
              {display}
            </div>
          );
        } else {
          return (
            <div className="flex flex-col" key={`${message.id}-${index}`}>
              {display}
            </div>
          );
        }
      })
    }
      <div ref={lastElementRef}></div>
    </div>
  )
}