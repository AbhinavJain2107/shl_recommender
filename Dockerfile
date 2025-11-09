# Base Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (Cloud Run listens on 8080)
EXPOSE 8080

# Start FastAPI app
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8080"]
