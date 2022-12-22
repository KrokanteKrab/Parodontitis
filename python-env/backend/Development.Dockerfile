FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# Install nginx
RUN apt-get update && apt-get install -y nginx

# Copy nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf

COPY scripts/prediction_parser.py scripts/
COPY scripts/patient_parser.py scripts/
COPY model/model-best-v2.h5 model/
COPY data/patients-v6.csv data/
COPY api.py .

EXPOSE 80
EXPOSE 443

# Start nginx
CMD ["sh", "-c", "python api.py & nginx -g 'daemon off;'"]