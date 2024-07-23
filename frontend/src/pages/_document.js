import { Html, Head, Main, NextScript } from "next/document";
import { GeistSans } from "geist/font/sans";

export default function Document() {
  return (
    <Html>
      <Head>
        <title>Product Support AI Assistant</title>
        <link rel="icon" href="/favicon.ico" />
        <link
          href="https://fonts.googleapis.com/css2?family=Lora:wght@400;700&display=swap"
          rel="stylesheet"
        />
        <link
          href="https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;700&display=swap"
          rel="stylesheet"
        />
    </Head>
      <body >
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}
