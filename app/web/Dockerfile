FROM node:lts-slim AS base
WORKDIR /code

COPY ./package.json ./package.json
COPY ./package-lock.json ./package-lock.json
RUN npm ci

COPY . ./


FROM base AS production
CMD [ \
    "sh", "-c", \
    "npm run build && npm run start -- -p 80" \
    ]


FROM base AS development
CMD [ \
    "sh", "-c", \
    "npm run dev -- -p 80" \
    ]
