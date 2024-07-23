

import { useRouter } from "next/router";
import React, { useEffect, useRef, useState } from "react";
import type { ChangeEvent } from "react";
import { BsArrowUpCircle } from "react-icons/bs";
import { BiArrowBack } from "react-icons/bi";

import  useMessages  from "@/hooks/useMessages"
import { RenderConversations } from "@/components/conversation/RenderConversation";

import { conversationClient } from "@/lib/restClientConversation"
import { BACKENDURL } from "@/consts/const";
import { Message, MESSAGE_STATUS } from "@/types/conversation"

export default function Conversation() {
  const router = useRouter();
  console.log( router.query.slug)
  const { id } = router.query;

  const lastElementRef = useRef<HTMLDivElement | null>(null)
  const { messages, userSendMessage, systemSendMessage, setMessages } = useMessages(id as string)
  const [userMessage, setUserMessage ] = useState("")
  const [conversationID, setConversationID ] = useState<string | null>(null)
  const [isMessagePending, setIsMessagePending] = useState(false);

  const textFocusRef = useRef<HTMLTextAreaElement | null>(null);

  useEffect(()=>{
    if (lastElementRef.current) {
      lastElementRef.current.scrollIntoView()
    }
  },[messages])


  const setSuggestedMessage = (text: string) =>{
    setUserMessage(text)
    if (textFocusRef.current){
      textFocusRef.current.focus()
    }
  }

  useEffect(()=> {
    if (textFocusRef.current) {
      textFocusRef.current.focus()
    }
  },[])

  useEffect(() => {
    if (id && typeof id == "string") {
      setConversationID(id)
    }
  })

  const handleTextChange = (event: ChangeEvent<HTMLTextAreaElement>) => {
    setUserMessage(event.target.value)
  }

  // oncomponentRendr populate conversation

  useEffect(() => {
    const fetchConversation = async (conversationID: string) => {
        const result = await conversationClient.fetchConversation(conversationID)
        if (result.messages) {
          setMessages(result.messages)
        }
      }

      try {
        if (conversationID) {
          debugger
          fetchConversation(conversationID)
        }
      } catch (error) {
        console.log(error)
      }

    }, [conversationID, setMessages])
  // submit callback

   const submit = () => {
    if (!userMessage || !conversationID) {
      return
    }

    setIsMessagePending(true)
    userSendMessage(userMessage)
    setUserMessage("")

    // const messageEndpoint  =   `/api/conversation/${conversationID}/message`
    const messageEndpoint  =   `/api/conversation/${conversationID}/mockllm-message`
    const url = BACKENDURL + messageEndpoint +`?user_message=${encodeURI(userMessage)}`
    debugger
    const events = new EventSource(url)

    events.onmessage = (event : MessageEvent) =>{
      debugger
      const parsedData: Message = JSON.parse(event.data)
      systemSendMessage(parsedData);

      if (parsedData.status == MESSAGE_STATUS.SUCCESS ||
        parsedData.status == MESSAGE_STATUS.ERROR) {
          events.close()
          setIsMessagePending(false)
        }
    }
   }

  return (
    <div className="flex h-[100vh] w-full items-center bjustify-center bg-slate-200">
      <div className="flex h-[100vh] w-full items-center justify-center">
        <div className="flex h-[100vh] w-[44vw] flex-col items-center border-r-2 bg-white">
          <div className="flex h-[44px] w-full items-center justify-between border-b-2 ">
            <div className="flex w-full items-center justify-between">
              <button
                onClick={() => {
                  router
                    .push("/conversation")
                    .catch(() => console.error("error navigating home"));
                }}
                className="ml-4 flex items-center justify-center rounded px-2 font-light text-[#9EA2B0] hover:text-gray-90"
              >
                <BiArrowBack className="mr-1" /> Back to Document Selection
              </button>

            </div>
          </div>
          <div className="flex max-h-[calc(100vh-114px)] w-[44vw] flex-grow flex-col overflow-scroll ">
            <RenderConversations
              messages={messages}
              setUserMessage={setSuggestedMessage}
            />
          </div>
          <div className="relative flex h-[70px] w-[44vw] w-full items-center border-b-2 border-t">
            <textarea
              ref={textFocusRef}
              rows={1}
              className="box-border w-full flex-grow resize-none overflow-hidden rounded px-5 py-3 pr-10 text-gray-90 placeholder-gray-60 outline-none"
              placeholder={"Start typing your question..."}
              value={userMessage}
              onChange={handleTextChange}
            />
            <button
              disabled={isMessagePending || userMessage.length === 0}
              onClick={submit}
              className="z-1 absolute right-6 top-1/2 mb-1 -translate-y-1/2 transform rounded text-gray-90 opacity-80 enabled:hover:opacity-100 disabled:opacity-30"
            >
              <BsArrowUpCircle size={24} />
            </button>
          </div>
        </div>

      </div>
    </div>
  )
}