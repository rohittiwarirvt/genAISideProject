import { GeistSans } from "geist/font/sans";
import { type AppType } from "next/dist/shared/lib/utils";
import Layout from "@/components/Layout";
import "@/styles/globals.css";

const MyApp: AppType = ({ Component, pageProps }) => {
  return (
    <div className={GeistSans.className }>
      <Layout>
        <Component {...pageProps} />
      </Layout>
    </div>
  );
};

export default MyApp;
