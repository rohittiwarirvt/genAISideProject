import { type Config } from "tailwindcss";
import { fontFamily } from "tailwindcss/defaultTheme";

export default {
  content: ["./src/**/*.tsx"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["var(--font-geist-sans)", ...fontFamily.sans],
        lora: ["Lora", "serif"], // The second font is a fallback.
        nunito: ["Nunito Sans", "sans-serif"], // The second font is a fallback.
      },
    },
  },
  plugins: [],
} satisfies Config;
