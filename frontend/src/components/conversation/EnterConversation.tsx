'use client'
import { useRouter } from "next/navigation"
import React, { useState } from "react"
import { conversationClient } from "@/lib/restClientConversation"
import {LoadingSpinner} from '@/components/misc/Loading'
import { AiOutlineArrowRight  } from "react-icons/ai";




export const EnterConversation = () => {
  const [isLoadingConversation, setIsLoadingConversation] = useState(false)
  // map all message and generate components assistan or user
  // if last message some special
  // sample message todo to start
  // add textbox in last

  const router = useRouter();

  const handleAddConversation = async ( event: { preventDefault: () => void}) => {
    setIsLoadingConversation(true)
    event.preventDefault();
    const conversationID = await conversationClient.createConversation()
    setIsLoadingConversation(false)
    router.push(`/conversation/${conversationID}`)
  }
  return(
    <div className="box-border flex h-full flex-col justify-start">
      <div className="relative">

        <button className="bg-blue-500 text-white font-bold py-2 px-4 rounded-lg hover:bg-blue-700" onClick={handleAddConversation} disabled={isLoadingConversation}>
          <div className="flex items-center justify-st">
                    {isLoadingConversation ? (
                      <div className="flex h-[22px] w-[180px] items-center justify-center">
                        <LoadingSpinner />
                      </div>
                    ) : (
                      <>
                        Start Troubleshooting
                        <div className="ml-2">
                          <AiOutlineArrowRight />
                        </div>
                      </>
                    )}
            </div>
        </button>
      </div>
    </div>
  )
}