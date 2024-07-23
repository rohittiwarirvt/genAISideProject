import React, {useState} from "react";
import type { PropsWithChildren } from "react";
import Link from "next/link";


const ConversationLayout = ({ children }: PropsWithChildren) => {
  const [messages, setMessages] = useState([
    { id: 1, text: 'Hello! How can I help you today?' },
    { id: 2, text: 'What is the status of my order?' },
  ]);

  return (
    <div className="flex gap-8">
      <aside className="flex-[2]">
        <div className="bg-white shadow-lg p-6 flex flex-col">
          <h2 className="text-2xl font-bold mb-6">Chat History</h2>
          <ul className="flex-grow overflow-y-auto">
          <p>:Todo work on conversation fetch and put here</p>
            {messages.map((message) => (
              <li key={message.id} className="mb-4">
                <div className="bg-blue-100 p-3 rounded-lg">{message.text}</div>
              </li>
            ))}
          </ul>
          <div className="mt-6">
            <button
              className="bg-blue-500 text-white py-2 px-4 rounded-lg"
              onClick={() => setMessages([])}
            >
              Clear History
            </button>
          </div>
        </div>
      </aside>
      <div className="bg-gray-100 flex-[8] p-4 rounded min-h-[300px]">
        {children}

      </div>
    </div>
    );
};
export default ConversationLayout;
