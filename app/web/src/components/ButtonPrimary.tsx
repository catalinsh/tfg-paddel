import { ScriptProps } from "next/script";

const ButtonPrimary = ({ children }: ScriptProps) => (
  <button
    type="button"
    className="inline-flex items-center gap-x-2 rounded-md bg-indigo-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 dark:bg-indigo-500 dark:hover:bg-indigo-400 dark:focus-visible:outline-indigo-500"
  >
    {children}
  </button>
);

export default ButtonPrimary;
