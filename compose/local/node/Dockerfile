FROM docker.io/node:23-bookworm-slim

WORKDIR /app

COPY ./package.json ./package-lock.json /app/

RUN npm install && npm cache clean --force

ENV PATH ./node_modules/.bin/:$PATH
