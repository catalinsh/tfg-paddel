import { ScriptProps } from "next/script";

const ButtonSecondary = ({ children }: ScriptProps) => (
  <button
    type="button"
    className="inline-flex items-center gap-x-2 rounded-md bg-white px-3.5 py-2.5 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 dark:bg-white/10 dark:text-white dark:ring-0 dark:hover:bg-white/20"
  >
    {children}
  </button>
);

export default ButtonSecondary;
