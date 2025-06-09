FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY models ./models
COPY soap_service.py .
COPY run_soap.py .

CMD ["python", "run_soap.py"]