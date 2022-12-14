FROM node:16.7.0-alpine as build-stage

WORKDIR /app
COPY package.json ./

RUN npm install
ARG REACT_APP_API_URL
ENV REACT_APP_API_URL $REACT_APP_API_URL

COPY . .
RUN npm run build

FROM nginx:1.19.0-alpine
COPY --from=build-stage /app/build /usr/share/nginx/html

EXPOSE 80
EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]