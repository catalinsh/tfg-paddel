import { faGithub } from "@fortawesome/free-brands-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

const Footer = () => (
  <footer>
    <div className="mx-auto max-w-7xl px-6 py-12 md:flex md:items-center md:justify-between lg:px-8">
      <div className="flex justify-center space-x-6 md:order-2">
        <a
          key="GitHub"
          href="https://github.com/cataand/tfg"
          target="_blank"
          className="text-zinc-400 hover:text-zinc-500 dark:hover:text-zinc-300"
        >
          <span className="sr-only">GitHub</span>
          <FontAwesomeIcon
            icon={faGithub}
            className="h-6 w-6"
            aria-hidden="true"
          />
        </a>
      </div>
      <div className="mt-8 md:order-1 md:mt-0">
        <p className="text-center text-xs leading-5 text-zinc-500 dark:text-zinc-400">
          &copy; 2023 Catalin Andrei, Cacuci
        </p>
      </div>
    </div>
  </footer>
);

export default Footer;
