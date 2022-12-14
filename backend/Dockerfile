FROM python:3.10-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/scripts/patient_parser.py scripts/
COPY backend/model/model-best.h5 model/
COPY backend/data/patients-v5.csv data/
COPY backend/api.py .

EXPOSE 3000

CMD ["python", "api.py"]