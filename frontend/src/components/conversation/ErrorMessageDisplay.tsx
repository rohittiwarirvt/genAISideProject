import { AiFillExclamationCircle } from "react-icons/ai";

const ErrorMessageDisplay = () => {
  return (
    <div className="mt-2 flex w-80 items-center rounded border border-red-500 bg-red-100 bg-opacity-20 p-1">
      <div className="ml-2">
        <AiFillExclamationCircle className="fill-red-500" size={20} />
      </div>
      <div className="ml-4 text-red-400">
        Error: unable to load chat response
      </div>
    </div>
  );
};


export default ErrorMessageDisplay