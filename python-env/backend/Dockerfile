FROM python:3.10-slim

WORKDIR /app
COPY _shared _shared
COPY backend backend

# Install the dependencies
WORKDIR /app/backend
RUN pip install -r requirements.txt

## Install nginx
RUN apt-get update && apt-get install -y nginx

## Copy nginx configuration file
COPY backend/_docker/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
EXPOSE 443

# Start nginx
CMD ["sh", "-c", "python api.py & nginx -g 'daemon off;'"]