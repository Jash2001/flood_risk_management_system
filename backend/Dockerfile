# Use Python 3.9 slim
FROM python:3.9-slim

# Set work directory
WORKDIR /code

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
        build-essential \
        libpq-dev \
        gdal-bin \
        libgdal-dev \
        binutils \
        curl \
        git \
        && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt /code/

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project code
COPY . /code/

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Default command
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
