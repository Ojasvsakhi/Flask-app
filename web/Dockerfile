FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
  && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . /app

EXPOSE 5000

# Use gunicorn for production-like server
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
