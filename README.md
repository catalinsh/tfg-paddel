# PADDEL
Repository for PADDEL (*PArkinson's Disease DEtection Library*).

## Project structure
This project has the following components:

### PADDEL library
Located in the `paddel` directory, this is an installable Python package that
contains the core of the application.

### Docker containers
The web application is built around Docker to facilitate development and
deployment. It consists of the following containers:

- **api**: Python 3.9 based container with a FastAPI instance that depends on
  the PADDEL library. It's main purpose is to serve as an interface between the
  website and the library.
- **web**: NodeJS-lts based container implementing the SvelteKit JavaScript
  library. It interacts with the API to fetch the data it needs.
- **proxy**: Nginx container deploying a reverse proxy, all connections going to
  the API or to the web have to go through this container first. All requests
  going to the */api* path are routed to the api container, the rest goes to the
  web container.

`docker-compose.yml` defines the main deployment configuration for all three
containers. It can be used with the `make docker-up` command.

`docker-compose.dev.yml` defines the values to be overwritten in the main
configuration in order to start the containers for development, meaning they
will watch the code for modifications and change accordingly. It can be used
with the `make docker-up-dev` command.

### Documentation
The `docs` folder contains the LaTeX documentation for this project, it is
written in Spanish.
