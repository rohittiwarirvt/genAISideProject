
import { Message, MESSAGE_STATUS } from "@/types/conversation";
import ErrorMessageDisplay from "@/components/conversation/ErrorMessageDisplay";

interface AssistantMessageDisplayProps {
  message: Message;
  showLoading: boolean;
}

const AssistantMessageDisplay: React.FC<AssistantMessageDisplayProps> = ({message, showLoading}) => {

  // const isMessageSuccessful = message.status === MESSAGE_STATUS.SUCCESS
  const isMessageError = message.status === MESSAGE_STATUS.ERROR

  return (
    <>
      <div className="border-b pb-4">
        <div className="flex">
          <div className="w-1/5"></div>
          <div className="w-4/5">
            {isMessageError && <ErrorMessageDisplay />}
          </div>
        </div>
        {!isMessageError && (
          <>
            <div className="flex items-center justify-center">
              <div className="my-3 w-11/12 border-[.5px]"></div>
            </div>
            <div className="flex ">
              <div className="w-1/5"></div>
              <div className="w-4/5">
                <p className="relative mb-2 mt-2 pr-3  whitespace-pre-wrap font-bold text-gray-90">
                  {message.content}
                </p>
              </div>
            </div>
          </>
        )}
      </div>
    </>
  )
}


export default AssistantMessageDisplay