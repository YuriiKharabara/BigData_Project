FROM python:3.9-slim

COPY requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt


COPY src/ src/


CMD uvicorn --host 0.0.0.0 --port 8080 src.main:app --reload