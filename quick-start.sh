#!/bin/bash

# Music from Drawings Pro - Quick Start Script
# This script sets up the entire application stack

set -e

echo "🎨 → 🎵 Music from Drawings Pro - Quick Start"
echo "=============================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env_example.txt .env
    echo "⚠️  Please edit .env file with your API keys before continuing."
    echo "   Required: GEMINI_API_KEY, SUNO_API_KEY, BEATOVEN_API_KEY"
    read -p "Press Enter to continue after editing .env file..."
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p backend/uploads
mkdir -p frontend/build
mkdir -p nginx/ssl
mkdir -p monitoring/grafana/dashboards
mkdir -p monitoring/grafana/datasources

# Build and start services
echo "🐳 Building and starting Docker containers..."
docker-compose up -d --build

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Check if services are running
echo "🔍 Checking service health..."

# Check MongoDB
if docker-compose exec -T mongodb mongosh --eval "db.runCommand('ping')" > /dev/null 2>&1; then
    echo "✅ MongoDB is running"
else
    echo "❌ MongoDB is not responding"
fi

# Check Redis
if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis is running"
else
    echo "❌ Redis is not responding"
fi

# Check Backend
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend API is running"
else
    echo "❌ Backend API is not responding"
fi

# Check Frontend
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend is running"
else
    echo "❌ Frontend is not responding"
fi

echo ""
echo "🎉 Setup complete! Your application is ready:"
echo ""
echo "🌐 Frontend:     http://localhost:3000"
echo "🔧 Backend API:  http://localhost:8000"
echo "📚 API Docs:     http://localhost:8000/docs"
echo "📊 Grafana:      http://localhost:3001 (admin/admin123)"
echo "📈 Prometheus:   http://localhost:9090"
echo ""
echo "🚀 To start drawing and generating music:"
echo "   1. Open http://localhost:3000 in your browser"
echo "   2. Draw something amazing on the canvas"
echo "   3. Click 'Generate Music' to create your song!"
echo ""
echo "🛠️  To stop the application:"
echo "   docker-compose down"
echo ""
echo "📝 To view logs:"
echo "   docker-compose logs -f"
echo ""
echo "Happy creating! 🎨🎵"
