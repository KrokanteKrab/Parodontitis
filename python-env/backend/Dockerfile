FROM python:3.10-slim

WORKDIR /app

COPY python-env/backend/requirements.txt .
RUN pip install -r requirements.txt

# Install nginx
RUN apt-get update && apt-get install -y nginx

# Copy nginx configuration file
COPY python-env/backend/nginx.conf /etc/nginx/nginx.conf

COPY python-env/backend/scripts/prediction_parser.py scripts/
COPY python-env/backend/scripts/patient_parser.py scripts/
COPY python-env/backend/model/model-best-v2.h5 model/
COPY python-env/backend/data/patients-v6.csv data/
COPY python-env/backend/api.py .

EXPOSE 80
EXPOSE 443

# Start nginx
CMD ["sh", "-c", "python api.py & nginx -g 'daemon off;'"]