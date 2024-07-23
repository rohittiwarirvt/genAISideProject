import Link from "next/link";
import Layout from "@/components/layouts/Layout";
import { ReactElement } from "react";
export default function Home() {
  return (
    <>
      <div className="bg-gray-100 text-gray-800">
        {/* Header */}


        {/* Hero Section */}
        <section className="bg-blue-500 text-white py-20">
          <div className="container mx-auto px-6 text-center">
            <h1 className="text-4xl font-bold mb-2">Product Support AI Assistant</h1>
            <p className="text-xl mb-8">Quick and easy troubleshooting with our AI Chatbot.</p>
            <Link href="/conversation" className="bg-white text-blue-500 py-3 px-6 rounded-full text-lg">Start Troubleshooting</Link>
          </div>
        </section>

        {/* Features Section */}
        {/* <section id="features" className="py-20">
          <div className="container mx-auto px-6">
            <h2 className="text-3xl font-bold text-center mb-12">Features</h2>
            <div className="flex flex-wrap -mx-6">
              <div className="w-full md:w-1/3 px-6 mb-12 md:mb-0">
                <div className="bg-white rounded-lg shadow p-6">
                  <div className="text-3xl text-blue-500 mb-4">
                    <i className="fas fa-brain"></i>
                  </div>
                  <h3 className="text-xl font-bold mb-2">Smart Assistance</h3>
                  <p className="text-gray-600">Get instant answers and solutions to your queries with our intelligent AI.</p>
                </div>
              </div>
              <div className="w-full md:w-1/3 px-6 mb-12 md:mb-0">
                <div className="bg-white rounded-lg shadow p-6">
                  <div className="text-3xl text-blue-500 mb-4">
                    <i className="fas fa-cogs"></i>
                  </div>
                  <h3 className="text-xl font-bold mb-2">Seamless Integration</h3>
                  <p className="text-gray-600">Integrate seamlessly with your existing tools and workflows.</p>
                </div>
              </div>
              <div className="w-full md:w-1/3 px-6 mb-12 md:mb-0">
                <div className="bg-white rounded-lg shadow p-6">
                  <div className="text-3xl text-blue-500 mb-4">
                    <i className="fas fa-user-friends"></i>
                  </div>
                  <h3 className="text-xl font-bold mb-2">User-Friendly</h3>
                  <p className="text-gray-600">Enjoy an intuitive and easy-to-use interface designed for everyone.</p>
                </div>
              </div>
            </div>
          </div>
        </section> */}

        {/* Testimonials Section */}
        {/* <section className="bg-gray-200 py-20">
          <div className="container mx-auto px-6">
            <h2 className="text-3xl font-bold text-center mb-12">What Our Users Say</h2>
            <div className="flex flex-wrap -mx-6">
              <div className="w-full md:w-1/2 lg:w-1/3 px-6 mb-12 lg:mb-0">
                <div className="bg-white rounded-lg shadow p-6">
                  <p className="text-gray-600 mb-4">"This AI assistant has transformed the way I work. It's incredibly efficient and easy to use."</p>
                  <div className="text-gray-800 font-bold">- John Doe</div>
                </div>
              </div>
              <div className="w-full md:w-1/2 lg:w-1/3 px-6 mb-12 lg:mb-0">
                <div className="bg-white rounded-lg shadow p-6">
                  <p className="text-gray-600 mb-4">"I can't imagine going back to my old workflow. The AI assistant is a game changer."</p>
                  <div className="text-gray-800 font-bold">- Jane Smith</div>
                </div>
              </div>
              <div className="w-full md:w-1/2 lg:w-1/3 px-6">
                <div className="bg-white rounded-lg shadow p-6">
                  <p className="text-gray-600 mb-4">"Excellent tool! It integrates perfectly with all my other applications."</p>
                  <div className="text-gray-800 font-bold">- Michael Brown</div>
                </div>
              </div>
            </div>
          </div>
        </section> */}

        {/* Footer */}

      </div>
    );
    </>
  );
}

Home.getLayout = function getLayout(page:ReactElement)  {
  return (
    <div >
      <Layout>
        {page}
      </Layout>
    </div>
  )
}