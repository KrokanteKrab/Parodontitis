FROM node:16.7.0-alpine as build-stage

WORKDIR /app
COPY frontend/package.json ./

RUN npm install
ENV REACT_APP_API_URL https://parodontitis-api.azurewebsites.net

COPY frontend/. .
RUN npm run build

FROM nginx:1.19.0-alpine
COPY --from=build-stage /app/build /usr/share/nginx/html

EXPOSE 80
EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]