FROM python:3.12-slim-bookworm

WORKDIR /app

COPY requirements.txt ./

RUN apt-get update && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


RUN pip install --no-cache-dir -r requirements.txt

COPY . .
