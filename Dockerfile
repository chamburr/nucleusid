FROM node:16-alpine3.17 AS node-builder

RUN apk add --no-cache python3 make g++

RUN npm install --global --force yarn

WORKDIR /build
COPY package.json yarn.lock ./

RUN yarn --frozen-lockfile

COPY nuxt.config.js ./
COPY client/ ./client/

ARG BASE_URI
ARG SENTRY_DSN
ARG GOOGLE_ANALYTICS

ENV ENVIRONMENT production
ENV BASE_URI $BASE_URI
ENV SENTRY_DSN $SENTRY_DSN
ENV GOOGLE_ANALYTICS $GOOGLE_ANALYTICS

RUN yarn generate

FROM rust:1.75-slim-buster AS rust-builder

RUN apt-get update \
    && apt-get -y install musl-dev libpq-dev

RUN cargo install diesel_cli --no-default-features --features "postgres"

WORKDIR /build
RUN cp /usr/local/cargo/bin/diesel ./

FROM python:3.9-slim-buster

ENV PATH "/app/bin:$PATH"

EXPOSE 5001

RUN apt-get update \
    && apt-get -y install dumb-init gcc libpq-dev

RUN pip install poetry

WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY . .
COPY --from=node-builder /build/dist/ /build/
COPY --from=rust-builder /build/ ./bin/

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["docker-entrypoint"]
