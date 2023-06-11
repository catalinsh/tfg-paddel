FROM node:18-slim AS base
WORKDIR /code

COPY ./package.json ./package.json
COPY ./package-lock.json ./package-lock.json
RUN npm ci

COPY . ./

ARG PUBLIC_API_LOCATION

RUN npm run check


FROM base AS production
RUN npm run build
CMD [ \
    "sh", "-c", \
    "PORT=80 node build" \
    ]


FROM base AS development
CMD [ \
    "sh", "-c", \
    "npm run dev" \
    ]
