# Use Python 3.12
FROM python:3.12-slim AS builder

# Install system depend
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libc6-dev libffi-dev libssl-dev cargo \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .

RUN python -m pip install --upgrade pip
RUN python -m pip install --prefix=/install --no-cache-dir -r requirements.txt

FROM python:3.12-slim

#RUN apt-get update && apt-get install -y --no-install-recommends \
#    libssl3 libffi8 libc6 \
#    && rm -rf /var/lib/apt/lists/* \

COPY --from=builder /install /usr/local
WORKDIR /app

COPY . .

ENTRYPOINT ["python", "main.py"]