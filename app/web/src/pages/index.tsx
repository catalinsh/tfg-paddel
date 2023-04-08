import Link from "next/link";
import { UserIcon, ArrowTopRightOnSquareIcon } from "@heroicons/react/20/solid";

import Logo from "@/components/Logo";
import ButtonSecondary from "@/components/ButtonSecondary";
import ButtonPrimary from "@/components/ButtonPrimary";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faGithub } from "@fortawesome/free-brands-svg-icons";
import Head from "next/head";

const Home = () => (
  <>
    <Head>
      <title>PaDDeL</title>
    </Head>

    <div className="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8">
      <nav className="flex justify-between py-2">
        <Link href={"/"} className="group inline-flex items-center gap-2 p-2">
          <Logo></Logo>
          <span className="hidden font-bold group-hover:underline sm:inline">
            PaDDeL
          </span>
        </Link>
        <div className="flex items-center gap-2">
          <a
            href={`${process.env.NEXT_PUBLIC_API_LOCATION}/docs`}
            target="_blank"
          >
            <ButtonSecondary>
              API Docs
              <ArrowTopRightOnSquareIcon
                className="-ml-0.5 h-5 w-5"
                aria-hidden="true"
              />
            </ButtonSecondary>
          </a>
          <Link href={"/admin"}>
            <ButtonPrimary>
              Admin
              <UserIcon
                className="-ml-0.5 h-5 w-5"
                aria-hidden="true"
              ></UserIcon>
            </ButtonPrimary>
          </Link>
        </div>
      </nav>

      <footer>
        <div className="mx-auto max-w-7xl px-6 py-12 md:flex md:items-center md:justify-between lg:px-8">
          <div className="flex justify-center space-x-6 md:order-2">
            <a
              key="GitHub"
              href="https://github.com/cataand/tfg"
              target="_blank"
              className="text-gray-400 hover:text-gray-500 dark:hover:text-gray-300"
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
            <p className="text-center text-xs leading-5 text-gray-500 dark:text-gray-400">
              &copy; 2023 Catalin Andrei, Cacuci
            </p>
          </div>
        </div>
      </footer>
    </div>
  </>
);

export default Home;
