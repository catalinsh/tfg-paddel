import Link from "next/link";
import {
  UserIcon,
  ArrowTopRightOnSquareIcon,
  VideoCameraIcon,
} from "@heroicons/react/20/solid";

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

      <form
        action={`${process.env.NEXT_PUBLIC_API_LOCATION}/predict`}
        method="post"
        encType="multipart/form-data"
      >
        <div className="mt-12">
          <div className="border-b border-stone-900/10 pb-12 dark:border-white/10">
            <h2 className="text-xl font-semibold leading-7 text-stone-900 dark:text-white">
              Predecir
            </h2>
            <p className="mt-1 text-sm leading-6 text-stone-600 dark:text-stone-400">
              Introduzca la siguiente información para obtener una predicción.
            </p>

            <div className="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
              <div className="sm:col-span-3">
                <div className="text-base font-semibold leading-6 text-stone-900 dark:text-white">
                  Su mano dominante
                </div>
                <div className="mt-2 space-y-3">
                  <div className="flex items-center gap-x-3">
                    <input
                      id="dominant-hand-left"
                      name="dominant_hand"
                      type="radio"
                      value={0}
                      required
                      className="h-4 w-4 border-stone-300 text-indigo-600 focus:ring-indigo-600 dark:border-stone-600 dark:bg-stone-700 dark:text-indigo-400 dark:ring-offset-stone-900 dark:focus:ring-indigo-400"
                    />
                    <label
                      htmlFor="dominant-hand-left"
                      className="block text-sm font-medium leading-6 text-stone-900 dark:text-white"
                    >
                      Izquierda
                    </label>
                  </div>
                  <div className="flex items-center gap-x-3">
                    <input
                      id="dominant-hand-right"
                      name="dominant_hand"
                      type="radio"
                      value={1}
                      required
                      className="h-4 w-4 border-stone-300 text-indigo-600 focus:ring-indigo-600 dark:border-stone-600 dark:bg-stone-700 dark:text-indigo-400 dark:ring-offset-stone-900 dark:focus:ring-indigo-400"
                    />
                    <label
                      htmlFor="dominant-hand-right"
                      className="block text-sm font-medium leading-6 text-stone-900 dark:text-white"
                    >
                      Derecha
                    </label>
                  </div>
                </div>
              </div>

              <div className="sm:col-span-3">
                <div className="text-base font-semibold leading-6 text-stone-900 dark:text-white">
                  Mano que muestra en el vídeo
                </div>
                <div className="mt-2 space-y-3">
                  <div className="flex items-center gap-x-3">
                    <input
                      id="video-hand-left"
                      name="video_hand"
                      type="radio"
                      value={0}
                      required
                      className="h-4 w-4 border-stone-300 text-indigo-600 focus:ring-indigo-600 dark:border-stone-600 dark:bg-stone-700 dark:text-indigo-400 dark:ring-offset-stone-900 dark:focus:ring-indigo-400"
                    />
                    <label
                      htmlFor="video-hand-left"
                      className="block text-sm font-medium leading-6 text-stone-900 dark:text-white"
                    >
                      Izquierda
                    </label>
                  </div>
                  <div className="flex items-center gap-x-3">
                    <input
                      id="video-hand-right"
                      name="video_hand"
                      type="radio"
                      value={1}
                      required
                      className="h-4 w-4 border-stone-300 text-indigo-600 focus:ring-indigo-600 dark:border-stone-600 dark:bg-stone-700 dark:text-indigo-400 dark:ring-offset-stone-900 dark:focus:ring-indigo-400"
                    />
                    <label
                      htmlFor="video-hand-right"
                      className="block text-sm font-medium leading-6 text-stone-900 dark:text-white"
                    >
                      Derecha
                    </label>
                  </div>
                </div>
              </div>

              <div className="sm:col-span-6">
                <div className="text-base font-semibold leading-6 text-stone-900 dark:text-white">
                  Sexo
                </div>
                <div className="mt-2 space-y-3">
                  <div className="flex items-center gap-x-3">
                    <input
                      id="sex-male"
                      name="sex"
                      type="radio"
                      value={0}
                      required
                      className="h-4 w-4 border-stone-300 text-indigo-600 focus:ring-indigo-600 dark:border-stone-600 dark:bg-stone-700 dark:text-indigo-400 dark:ring-offset-stone-900 dark:focus:ring-indigo-400"
                    />
                    <label
                      htmlFor="sex-male"
                      className="block text-sm font-medium leading-6 text-stone-900 dark:text-white"
                    >
                      Masculino
                    </label>
                  </div>
                  <div className="flex items-center gap-x-3">
                    <input
                      id="sex-female"
                      name="sex"
                      type="radio"
                      value={1}
                      required
                      className="h-4 w-4 border-stone-300 text-indigo-600 focus:ring-indigo-600 dark:border-stone-600 dark:bg-stone-700 dark:text-indigo-400 dark:ring-offset-stone-900 dark:focus:ring-indigo-400"
                    />
                    <label
                      htmlFor="sex-female"
                      className="block text-sm font-medium leading-6 text-stone-900 dark:text-white"
                    >
                      Femenino
                    </label>
                  </div>
                </div>
              </div>

              <div className="col-span-full">
                <label
                  htmlFor="cover-photo"
                  className="block text-base font-semibold leading-6 text-stone-900 dark:text-white"
                >
                  Vídeo
                </label>
                <div className="mt-2 flex justify-center rounded-lg border border-dashed border-stone-900/25 px-6 py-10 dark:border-stone-100/25">
                  <div className="text-center">
                    <VideoCameraIcon
                      className="dark:text-stone-7500 mx-auto h-12 w-12 text-stone-500"
                      aria-hidden="true"
                    />
                    <div className="mt-4 flex text-sm leading-6 text-stone-600 dark:text-stone-400">
                      <label
                        htmlFor="hand-video-upload"
                        className="relative cursor-pointer rounded-md bg-white font-semibold text-indigo-600 focus-within:outline-none focus-within:ring-2 focus-within:ring-indigo-600 focus-within:ring-offset-2 hover:text-indigo-500 dark:bg-stone-900 dark:text-indigo-400 dark:focus-within:ring-indigo-400"
                      >
                        <span>Suba un archivo</span>
                        <input
                          id="hand-video-upload"
                          name="video"
                          type="file"
                          className="sr-only"
                          required
                        />
                      </label>
                      <p className="pl-1">o arrastre y suelte</p>
                    </div>
                    <p className="text-xs leading-5 text-stone-600 dark:text-stone-400">
                      MP4, MOV, AVI hasta 100MB
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-6 flex items-center justify-end gap-x-6">
          <button
            type="submit"
            className="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 dark:bg-indigo-500 dark:hover:bg-indigo-400"
          >
            Obtener predicción
          </button>
        </div>
      </form>

      <footer>
        <div className="mx-auto max-w-7xl px-6 py-12 md:flex md:items-center md:justify-between lg:px-8">
          <div className="flex justify-center space-x-6 md:order-2">
            <a
              key="GitHub"
              href="https://github.com/cataand/tfg"
              target="_blank"
              className="text-stone-400 hover:text-stone-500 dark:hover:text-stone-300"
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
            <p className="text-center text-xs leading-5 text-stone-500 dark:text-stone-400">
              &copy; 2023 Catalin Andrei, Cacuci
            </p>
          </div>
        </div>
      </footer>
    </div>
  </>
);

export default Home;
