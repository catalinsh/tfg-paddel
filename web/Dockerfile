FROM node:lts-slim

WORKDIR /web

COPY ./package.json ./
COPY ./package-lock.json ./
RUN npm install

COPY . ./

CMD npm run build; export PORT=80; node build