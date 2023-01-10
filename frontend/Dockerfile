FROM node:16.10.0-alpine as build-stage

# Enviroment variables
ARG BACKEND_URL
ENV REACT_APP_BACKEND_URL=$BACKEND_URL

WORKDIR /app
COPY . .

RUN npm install
RUN npm run build

FROM nginx:1.19.0-alpine
COPY _docker/nginx.conf /etc/nginx/nginx.conf
COPY --from=build-stage /app/build /usr/share/nginx/html

EXPOSE 80
EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]