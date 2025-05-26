FROM python:3.10-slim

WORKDIR /app

COPY app.py .
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 27014

ENTRYPOINT ["python", "app.py"]

HEALTHCHECK --interval=5m --timeout=3s CMD curl -f http://localhost:27014/ping || exit 1
