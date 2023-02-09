FROM nginx:alpine-slim AS base


FROM base AS production

COPY production.conf /etc/nginx/conf.d/default.conf


FROM base AS development

COPY development.conf /etc/nginx/conf.d/default.conf