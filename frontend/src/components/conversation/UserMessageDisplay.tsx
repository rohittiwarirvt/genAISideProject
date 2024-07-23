
import { Message } from "@/types/conversation";
import { formatDisplayDate } from "@/lib/timezone";

interface UserMessageDisplayProps {
  message: Message;
  showLoading: boolean;
}

const UserMessageDisplay: React.FC<UserMessageDisplayProps> = ({message, showLoading}) => {
  return (
    <>
      <div className="flex border-r bg-gray-00 pb-4">
        <div className="mt-4 w-1/5 flex-grow text-right font-nunito text-gray-60">
          <div className="flex items-center justify-center">
            {formatDisplayDate(message.created_at)}
          </div>
        </div>
        <div className="mt-4 w-4/5 pr-3 font-nunito font-bold text-gray-90">
          {message.content}
        </div>
      </div>

    </>
  )
}


export default UserMessageDisplay