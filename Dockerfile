FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    tzdata curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

ENV TZ=Asia/Kolkata
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app:/app/scripts:${PYTHONPATH}

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN mkdir -p /app/logs /app/data

CMD ["python", "main.py"]
