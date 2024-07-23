
import { type AppType } from "next/dist/shared/lib/utils";
import "@/styles/globals.css";
import Layout from "@/components/layouts/Layout";
import type { ReactElement, ReactNode } from 'react'
import type { NextPage } from 'next'
import type { AppProps } from 'next/app'

export type NextPageWithLayout<P = {}, IP = P> = NextPage<P, IP> & {
  getLayout?: (page: ReactElement) => ReactNode
}

type AppPropsWithLayout = AppProps & {
  Component: NextPageWithLayout
}

// const MyApp: AppType = ({ Component, pageProps }): AppPropsWithLayout => {

//   const getLayout = Component.getLayout ?? ((page) => page)

//   return getLayout(<Component {...pageProps} />)
//   return (
//     <div className={GeistSans.className }>
//       <Layout>
//         <Component {...pageProps} />
//       </Layout>
//     </div>
//   );
// };

 function MyApp({ Component, pageProps }: AppPropsWithLayout) {
  // Use the layout defined at the page level, if available
  const getLayout = Component.getLayout ?? ((page) => page)

  return getLayout(<Component {...pageProps} />)
}

export default MyApp
