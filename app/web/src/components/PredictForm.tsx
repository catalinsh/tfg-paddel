import { VideoCameraIcon } from "@heroicons/react/20/solid";
import { useForm, SubmitHandler } from "react-hook-form";

export type PredictInputs = {
  videoHand: string;
  dominantHand: string;
  age: string;
  sex: string;
  video: FileList;
};

const PredictForm = ({
  onSubmit,
}: {
  onSubmit: SubmitHandler<PredictInputs>;
}) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<PredictInputs>();

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div className="mt-12">
        <div className="border-b border-zinc-900/10 pb-12 dark:border-white/10">
          <h2 className="text-xl font-semibold leading-7 text-zinc-900 dark:text-white">
            Predecir
          </h2>
          <p className="mt-1 text-sm leading-6 text-zinc-600 dark:text-zinc-400">
            Introduzca la siguiente información para obtener una predicción.
          </p>

          <div className="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
            <div className="sm:col-span-3">
              <span className="block text-base font-semibold leading-6 text-zinc-900 dark:text-white">
                Su mano dominante
              </span>
              <div className="mt-2 space-y-3">
                <div className="flex items-center gap-x-3">
                  <input
                    id="dominant-hand-left"
                    className="h-4 w-4 border-zinc-300 text-indigo-600 focus:ring-indigo-600 dark:border-zinc-600 dark:bg-zinc-700 dark:text-indigo-400 dark:focus:ring-indigo-400 dark:focus:ring-offset-zinc-900"
                    type="radio"
                    value={0}
                    {...register("dominantHand", {
                      required: true,
                    })}
                  />
                  <label
                    htmlFor="dominant-hand-left"
                    className="block text-sm font-medium leading-6 text-zinc-900 dark:text-white"
                  >
                    Izquierda
                  </label>
                </div>
                <div className="flex items-center gap-x-3">
                  <input
                    id="dominant-hand-right"
                    className="h-4 w-4 border-zinc-300 text-indigo-600 focus:ring-indigo-600 dark:border-zinc-600 dark:bg-zinc-700 dark:text-indigo-400 dark:focus:ring-indigo-400 dark:focus:ring-offset-zinc-900"
                    type="radio"
                    value={1}
                    {...register("dominantHand", {
                      required: true,
                    })}
                  />
                  <label
                    htmlFor="dominant-hand-right"
                    className="block text-sm font-medium leading-6 text-zinc-900 dark:text-white"
                  >
                    Derecha
                  </label>
                </div>
                {errors.dominantHand && (
                  <p className="mt-2 text-sm text-red-600" id="email-error">
                    Campo obligatorio.
                  </p>
                )}
              </div>
            </div>

            <div className="sm:col-span-3">
              <span className="block text-base font-semibold leading-6 text-zinc-900 dark:text-white">
                Mano que muestra en el vídeo
              </span>
              <div className="mt-2 space-y-3">
                <div className="flex items-center gap-x-3">
                  <input
                    id="video-hand-left"
                    className="h-4 w-4 border-zinc-300 text-indigo-600 focus:ring-indigo-600 dark:border-zinc-600 dark:bg-zinc-700 dark:text-indigo-400 dark:focus:ring-indigo-400 dark:focus:ring-offset-zinc-900"
                    type="radio"
                    value={0}
                    {...register("videoHand", {
                      required: true,
                    })}
                  />
                  <label
                    htmlFor="video-hand-left"
                    className="block text-sm font-medium leading-6 text-zinc-900 dark:text-white"
                  >
                    Izquierda
                  </label>
                </div>
                <div className="flex items-center gap-x-3">
                  <input
                    id="video-hand-right"
                    className="h-4 w-4 border-zinc-300 text-indigo-600 focus:ring-indigo-600 dark:border-zinc-600 dark:bg-zinc-700 dark:text-indigo-400 dark:focus:ring-indigo-400 dark:focus:ring-offset-zinc-900"
                    type="radio"
                    value={1}
                    {...register("videoHand", {
                      required: true,
                    })}
                  />
                  <label
                    htmlFor="video-hand-right"
                    className="block text-sm font-medium leading-6 text-zinc-900 dark:text-white"
                  >
                    Derecha
                  </label>
                </div>
                {errors.videoHand && (
                  <p className="mt-2 text-sm text-red-600" id="email-error">
                    Campo obligatorio.
                  </p>
                )}
              </div>
            </div>

            <div className="sm:col-span-3">
              <label
                htmlFor="age"
                className="block text-base font-semibold leading-6 text-zinc-900 dark:text-white"
              >
                Edad
              </label>
              <div className="mt-2 flex w-28">
                <input
                  id="age"
                  className="block w-full min-w-0 flex-1 rounded-none rounded-l-md border-0 py-1.5 text-right text-zinc-900 ring-1 ring-inset ring-zinc-300 placeholder:text-zinc-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 dark:bg-zinc-700 dark:text-white dark:ring-zinc-600 dark:focus:ring-indigo-400 sm:text-sm sm:leading-6"
                  type="number"
                  {...register("age", {
                    required: true,
                    min: 0,
                    max: 255,
                    pattern: new RegExp("^[0-9]+$"),
                  })}
                />
                <label
                  htmlFor="age"
                  className="inline-flex select-none items-center rounded-r-md border border-l-0 border-zinc-300 px-3 text-zinc-500 dark:border-zinc-600 dark:bg-zinc-700 dark:text-zinc-400 sm:text-sm"
                >
                  años
                </label>
              </div>
              {errors.age && (
                <p className="mt-2 text-sm text-red-600" id="email-error">
                  Valor inválido.
                </p>
              )}
            </div>

            <div className="sm:col-span-3">
              <span className="block text-base font-semibold leading-6 text-zinc-900 dark:text-white">
                Sexo
              </span>
              <div className="mt-2 space-y-3">
                <div className="flex items-center gap-x-3">
                  <input
                    id="sex-male"
                    className="h-4 w-4 border-zinc-300 text-indigo-600 focus:ring-indigo-600 dark:border-zinc-600 dark:bg-zinc-700 dark:text-indigo-400 dark:focus:ring-indigo-400 dark:focus:ring-offset-zinc-900"
                    type="radio"
                    value={0}
                    {...register("sex", { required: true })}
                  />
                  <label
                    htmlFor="sex-male"
                    className="block text-sm font-medium leading-6 text-zinc-900 dark:text-white"
                  >
                    Masculino
                  </label>
                </div>
                <div className="flex items-center gap-x-3">
                  <input
                    id="sex-female"
                    className="h-4 w-4 border-zinc-300 text-indigo-600 focus:ring-indigo-600 dark:border-zinc-600 dark:bg-zinc-700 dark:text-indigo-400 dark:focus:ring-indigo-400 dark:focus:ring-offset-zinc-900"
                    type="radio"
                    value={1}
                    {...register("sex", { required: true })}
                  />
                  <label
                    htmlFor="sex-female"
                    className="block text-sm font-medium leading-6 text-zinc-900 dark:text-white"
                  >
                    Femenino
                  </label>
                </div>
                {errors.sex && (
                  <p className="mt-2 text-sm text-red-600" id="email-error">
                    Campo obligatorio.
                  </p>
                )}
              </div>
            </div>

            <div className="col-span-full">
              <label
                htmlFor="cover-photo"
                className="block text-base font-semibold leading-6 text-zinc-900 dark:text-white"
              >
                Vídeo
              </label>
              <div className="mt-2 flex justify-center rounded-lg border border-dashed border-zinc-900/25 px-6 py-10 dark:border-zinc-100/25">
                <div className="text-center">
                  <VideoCameraIcon
                    className="dark:text-zinc-7500 mx-auto h-12 w-12 text-zinc-500"
                    aria-hidden="true"
                  />
                  <div className="mt-4 flex text-sm leading-6 text-zinc-600 dark:text-zinc-400">
                    <label
                      htmlFor="hand-video-upload"
                      className="relative cursor-pointer rounded-md bg-white font-semibold text-indigo-600 focus-within:outline-none focus-within:ring-2 focus-within:ring-indigo-600 focus-within:ring-offset-2 hover:text-indigo-500 dark:bg-zinc-900 dark:text-indigo-400 dark:focus-within:ring-indigo-400"
                    >
                      <span>Suba un archivo</span>
                      <input
                        id="hand-video-upload"
                        className="sr-only"
                        type="file"
                        {...register("video", {
                          required: true,
                        })}
                      />
                    </label>
                    <p className="pl-1">o arrastre y suelte</p>
                  </div>
                  <p className="text-xs leading-5 text-zinc-600 dark:text-zinc-400">
                    MP4, MOV, AVI hasta 100MB
                  </p>
                </div>
              </div>
              {errors.video && (
                <p className="mt-2 text-sm text-red-600" id="email-error">
                  Debe subir un archivo.
                </p>
              )}
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
  );
};

export default PredictForm;
