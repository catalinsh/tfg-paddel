FROM node:lts-slim AS base

WORKDIR /web

COPY package.json package-lock.json ./

RUN npm ci

COPY . ./


FROM base AS production

RUN npm run build

ENV PORT=80
CMD ["node", "build"]


FROM base AS development

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "80"]