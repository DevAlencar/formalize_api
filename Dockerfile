# Use Python 3.10 official image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=formalize_api.settings

# Set work directory
WORKDIR /app

# Install system dependencies for MySQL and production
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        default-libmysqlclient-dev \
        build-essential \
        pkg-config \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Create necessary directories
RUN mkdir -p /app/staticfiles /app/mediafiles /var/log/gunicorn

# Set ownership and permissions
RUN chown -R appuser:appuser /app /var/log/gunicorn

# Collect static files
RUN python manage.py collectstatic --noinput --clear

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8001/admin/ || exit 1

# Run the application with Gunicorn
CMD ["gunicorn", "--config", "gunicorn.conf.py", "formalize_api.wsgi:application"]
