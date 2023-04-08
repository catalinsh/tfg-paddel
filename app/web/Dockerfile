FROM node:18-slim AS base
WORKDIR /code

COPY ./package.json ./package.json
COPY ./package-lock.json ./package-lock.json
RUN npm ci

COPY . ./


FROM base AS production
CMD [ \
    "sh", "-c", \
    "npm run build && npm run start -- --port 80" \
    ]


FROM base AS development
CMD [ \
    "sh", "-c", \
    "npm run dev -- --port 80" \
    ]
