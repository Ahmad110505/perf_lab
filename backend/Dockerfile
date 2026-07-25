FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (e.g. for building MySQL client)
RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential pkg-config && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
