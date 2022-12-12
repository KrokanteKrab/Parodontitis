FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY scripts/patient_parser.py scripts/
COPY model/model-best.h5 model/
COPY ../python/data/patients-v5.csv ../python/data/
COPY api.py .

EXPOSE 5000

CMD ["python", "api.py"]