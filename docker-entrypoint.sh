#!/bin/bash
# Docker entrypoint script for FreshMart Backend

set -e

echo "🚀 Starting FreshMart Backend..."
echo "================================"

# Check required environment variables
if [ -z "$DATABASE_URL" ]; then
    echo "❌ ERROR: DATABASE_URL is not set!"
    echo ""
    echo "Please set environment variables:"
    echo "  DATABASE_URL=postgresql://user:password@host:5432/dbname"
    echo "  SECRET_KEY=your-secret-key"
    echo ""
    echo "Example:"
    echo "  docker run -e DATABASE_URL=... -e SECRET_KEY=... backend"
    exit 1
fi

if [ -z "$SECRET_KEY" ]; then
    echo "❌ ERROR: SECRET_KEY is not set!"
    echo ""
    echo "Please set SECRET_KEY environment variable"
    echo "Generate one with: openssl rand -hex 32"
    exit 1
fi

echo "✅ Environment variables loaded"
echo "✅ DATABASE_URL: ${DATABASE_URL%%@*}@***"  # Hide password
echo "✅ SECRET_KEY: ${SECRET_KEY:0:10}***"      # Hide key
echo ""

# Wait for database to be ready (if using postgres host)
if [[ $DATABASE_URL == *"postgres"* ]] || [[ $DATABASE_URL == *"postgresql"* ]]; then
    echo "⏳ Waiting for database to be ready..."
    
    # Extract host and port from DATABASE_URL
    DB_HOST=$(echo $DATABASE_URL | sed -n 's/.*@\([^:]*\):.*/\1/p')
    DB_PORT=$(echo $DATABASE_URL | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')
    
    if [ -n "$DB_HOST" ]; then
        echo "   Checking $DB_HOST:${DB_PORT:-5432}..."
        
        # Wait up to 30 seconds for database
        for i in {1..30}; do
            if nc -z "$DB_HOST" "${DB_PORT:-5432}" 2>/dev/null; then
                echo "✅ Database is ready!"
                break
            fi
            
            if [ $i -eq 30 ]; then
                echo "⚠️  Warning: Database not responding after 30s, continuing anyway..."
            else
                echo "   Attempt $i/30..."
                sleep 1
            fi
        done
    fi
fi

echo ""
echo "🎯 Starting Uvicorn server..."
echo "================================"
echo ""

# Execute the main command
exec "$@"
