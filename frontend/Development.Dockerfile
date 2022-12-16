FROM node:16.7.0 as build-stage

WORKDIR /app
COPY package.json ./

RUN npm install
ENV REACT_APP_API_URL http://localhost

COPY . .
RUN npm run build

FROM nginx
# Copy nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf

COPY --from=build-stage /app/build /usr/share/nginx/html

EXPOSE 80
EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]