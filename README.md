# PADDEL
Repository for PADDEL (*PArkinson's Disease DEtection Library*).

## Project structure
This project has the following components:

### PADDEL library
Located in the `paddel` directory, this is an installable Python package that
contains the core of the application.

### Notebooks
The `notebooks` directory contains multiple Jupyter notebooks that were used
during the research and development of the PADDEL library.

### Web application
Located in the `app` directory, it is comprized of the following Docker containers:

- **proxy**: Caddy web server based container that implements a reverse proxy to
  forward api requests to the `api` container and web requests to the `web`
  container. This container also serves as an SSL certifiate management tool to
  automate the creation and renewal of these certificates, redirect http
  requests to https and thus allow for a secure connection across the Internet.

- **web**: NodeJS-lts based container implementing the SvelteKit JavaScript
  library. It interacts with the API to fetch the data it needs.

- **api**: Python 3.9 based container with a FastAPI instance that depends on
  the PADDEL library. It's main purpose is to serve as an interface between the
  website and the library. Swagger documentation for the API can be accessed in
  the `/api/docs` path of a deployment of the containers.

This folder also containes a `sample.env` file which contains environment
variables used by the containers and some base values. It should be edited to
match the running environment both in production and development and saved as
`.env` in the same directory.

Once the `.env` file is setup launching the containers is as simple as executing
`make prod` or `make dev` accordingly while having the Docker Engine running. In
development mode the `web` and `api` containers scan the source code and reload
automatically when a change is detected, this will work most of the time, but
some changes may still require a restart of the containers.

Restarting the containers is done by re-running the `make prod` or `make dev`
command.

Stopping the containers is done by running `make down`, this will also remove
the container images, but not image cache, so build time will still be fast
after the first build.

### Documentation
The `docs` folder contains the LaTeX documentation for this project, it is
written in Spanish.
