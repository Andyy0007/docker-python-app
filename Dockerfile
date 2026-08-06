# Base image
FROM python:3.12-slim

# Create working directory
WORKDIR /app

# Copy dependency file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Application listens on port 5000
EXPOSE 5000

# Start the application
CMD ["python", "app.py"]