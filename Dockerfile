# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /code
# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*
    
# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy Django project files
COPY . .
RUN python manage.py collectstatic --noinput
# Create logs directory and set permissions
RUN mkdir -p /code/logs && chmod -R 777 /code/logs

# Set permissions for the database directory
RUN mkdir -p /code/db && chmod -R 777 /code/db

# Expose port 8000 for Django
EXPOSE 8000

# Run migrations and start the server
CMD ["bash", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]