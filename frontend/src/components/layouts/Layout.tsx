import React from "react";
import type { PropsWithChildren } from "react";
import Link from "next/link";
import { GeistSans } from "geist/font/sans";
const Layout = ({ children }: PropsWithChildren) => {
  return <>

    <header className="bg-white shadow">
      <div  className={GeistSans.className} >
        <div className=" container mx-auto px-6 py-3 flex justify-between items-center" >
          <div >
            <Link href="/" className="text-gray-800 text-xl font-bold" >AI Assistant</Link>
          </div>
          <div>
            <a className="text-gray-800 hover:text-gray-600 mx-3" href="#">Home</a>
            <a className="text-gray-800 hover:text-gray-600 mx-3" href="#features">Features</a>
            <a className="text-gray-800 hover:text-gray-600 mx-3" href="#">Pricing</a>
            <a className="text-gray-800 hover:text-gray-600 mx-3" href="#">Contact</a>
          </div>
        </div>
      </div>
    </header>
    <div className={GeistSans.className}>
      {children}
    </div>

  </>;
};
export default Layout;
