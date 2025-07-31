#!/bin/bash

# Deploy script for Formalize API Production

set -e

echo "🚀 Starting Formalize API Production Deployment"

# Check if .env.prod exists
if [ ! -f .env.prod ]; then
    echo "❌ .env.prod file not found!"
    echo "Please copy .env.prod.example to .env.prod and configure it with your production values."
    exit 1
fi

# Check if Docker and Docker Compose are installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed!"
    exit 1
fi

if ! command -v docker compose &> /dev/null; then
    echo "❌ Docker Compose is not installed!"
    exit 1
fi

echo "📋 Checking environment..."

# Create logs directory
mkdir -p logs

# Create SSL directory (for future HTTPS setup)
mkdir -p ssl

echo "🛠️  Building and starting containers..."

# Stop any running containers
docker compose -f docker-compose.prod.yml down

# Build and start containers
docker compose -f docker-compose.prod.yml --env-file .env.prod up --build -d

echo "⏳ Waiting for services to be ready..."

# Wait for database to be ready
echo "Waiting for database..."
sleep 30

# Check if services are running
if docker compose -f docker-compose.prod.yml ps | grep -q "Up"; then
    echo "✅ Services are running!"
    
    echo "🔄 Running database migrations..."
    docker compose -f docker-compose.prod.yml exec -T web python manage.py migrate
    
    echo "📁 Collecting static files..."
    docker compose -f docker-compose.prod.yml exec -T web python manage.py collectstatic --noinput
    
    echo "🎉 Deployment completed successfully!"
    echo ""
    echo "📊 Service Status:"
    docker compose -f docker-compose.prod.yml ps
    echo ""
    echo "🌐 Your API is available at:"
    echo "   - API: http://localhost:8001"
    echo ""
    echo "📝 Useful commands:"
    echo "   - View logs: docker-compose -f docker-compose.prod.yml logs -f"
    echo "   - Stop services: docker-compose -f docker-compose.prod.yml down"
    echo "   - Create superuser: docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser"
    
else
    echo "❌ Something went wrong! Check the logs:"
    docker compose -f docker-compose.prod.yml logs
    exit 1
fi
