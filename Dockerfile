# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the work directory
WORKDIR /user_ticketing

# Install dependencies
COPY requirements.txt /user_ticketing
RUN pip install --no-cache-dir -r requirements.txt

# Install PostgreSQL client dependencies
RUN apt-get update \
    && apt-get install -y \
       libpq-dev \
       gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .
RUN mkdir -p /user_ticketing/staticfiles
# Collect static files
RUN python manage.py collectstatic --no-input

# Expose the port Django will run on
EXPOSE 8000

# Run the server with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--reload", "user_ticketing.wsgi:application"]
