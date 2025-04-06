FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y docker.io

RUN mkdir -p /airbyte/tmp/ && \
    chmod -R 777 /airbyte/tmp/

# Set environment variables
ENV AIRBYTE_LOCAL_ROOT=/airbyte

# Copy application files
COPY . .

RUN pip install -r requirements.txt

# Set entrypoint
CMD ["python", "airbyte_sync.py"]
