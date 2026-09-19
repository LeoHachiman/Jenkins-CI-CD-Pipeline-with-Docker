# Use a minimal Python base image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy and install dependencies first (Docker caches this layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# When the container starts, run app.py
CMD ["python", "app.py"]
