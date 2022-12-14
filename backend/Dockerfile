FROM python:3.10-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

# Install nginx
RUN apt-get update && apt-get install -y nginx

# Copy nginx configuration file
COPY backend/nginx.conf /etc/nginx/nginx.conf

COPY backend/scripts/patient_parser.py scripts/
COPY backend/model/model-best.h5 model/
COPY backend/data/patients-v5.csv data/
COPY backend/api.py .

EXPOSE 80
EXPOSE 443

# Start nginx
CMD ["nginx", "-g", "daemon off;"]