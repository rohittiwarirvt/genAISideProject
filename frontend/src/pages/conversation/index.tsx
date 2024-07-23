
import { EnterConversation } from "@/components/conversation/EnterConversation"
import Layout from "@/components/layouts/Layout"
import ConversationLayout from "@/components/layouts/ConversationLayout"
import { ReactElement } from "react"
import { NextPageWithLayout } from "./_app"
import { GeistSans } from "geist/font/sans";


 const LandingConversation: NextPageWithLayout = () => {

  return (
      <div className="min-h-screen flex items-center h-full justify-center justify-items-center bg-gray-100">
        <div className="bg-white p-3 rounded-lg shadow self-center">
          <EnterConversation/>
        </div>
      </div>
  )
}

LandingConversation.getLayout = function getLayout(page:ReactElement)  {
  return (
    <Layout >
      <ConversationLayout>{page}</ConversationLayout>
    </Layout>
  )
}

export default LandingConversation