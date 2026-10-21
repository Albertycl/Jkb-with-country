FROM node:20-alpine AS build
WORKDIR /app
RUN yarn global add @quasar/cli
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile --non-interactive --ignore-engines
COPY . .
RUN quasar build

FROM nginx:1.27-alpine
COPY default.conf.template /etc/nginx/templates/default.conf.template
ENV API_UPSTREAM=http://backend:5065
COPY --from=build /app/dist/spa /usr/share/nginx/html
EXPOSE 80
HEALTHCHECK --interval=15s --timeout=5s --retries=5 CMD wget -qO /dev/null http://127.0.0.1/ || exit 1
