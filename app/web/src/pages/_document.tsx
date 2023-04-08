import { Html, Head, Main, NextScript } from "next/document";

export default function Document() {
  return (
    <Html lang="en">
      <Head />
      <body className="bg-white text-stone-900 dark:bg-stone-900 dark:text-white">
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}
