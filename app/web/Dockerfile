FROM node:lts-slim AS base
WORKDIR /code

COPY ./package.json ./package.json
COPY ./package-lock.json ./package-lock.json
RUN npm ci

COPY . ./
RUN npm run prepare


FROM base AS production
ENV PORT=80
CMD [ \
    "sh", "-c", \
    "npm run build && node build" \
    ]


FROM base AS development
CMD [ \
    "sh", "-c", \
    "npm run dev -- \
    --host 0.0.0.0 \
    --port 80" \
    ]
