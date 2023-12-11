FROM python:3.7-slim-buster

# Set working directory
WORKDIR /build

RUN apt-get update && \
    apt-get install -y gcc python3-dev && \
    apt-get clean

# Copy requirements and install dependencies
COPY build/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app/worker
# Command to run the worker
CMD ["python", "worker.py"]