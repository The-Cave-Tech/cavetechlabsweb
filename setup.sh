#!/bin/bash
# Setup script - prompts for credentials if admin_credentials.json doesn't exist

set -e

CREDS_FILE="admin_credentials.json"
SETUP_COMPLETE_FILE=".setup_complete"

# Check if credentials file exists
if [ ! -f "$CREDS_FILE" ]; then
    echo ""
    echo "🔐 ======================================"
    echo "   ADMIN CREDENTIALS SETUP REQUIRED"
    echo "======================================"
    echo ""
    echo "The admin_credentials.json file is missing."
    echo "Please provide credentials for the Django admin panel:"
    echo ""
    
    read -p "👤 Username (default: admin): " USERNAME
    USERNAME=${USERNAME:-admin}
    
    read -p "📧 Email (default: admin@cavetechlabs.com): " EMAIL
    EMAIL=${EMAIL:-admin@cavetechlabs.com}
    
    read -sp "🔑 Password: " PASSWORD
    echo ""
    read -sp "🔑 Confirm Password: " PASSWORD_CONFIRM
    echo ""
    
    if [ "$PASSWORD" != "$PASSWORD_CONFIRM" ]; then
        echo "❌ Passwords do not match!"
        exit 1
    fi
    
    # Create the credentials file
    cat > "$CREDS_FILE" << EOF
{
  "username": "$USERNAME",
  "email": "$EMAIL",
  "password": "$PASSWORD"
}
EOF
    
    echo "✅ Credentials file created: $CREDS_FILE"
    echo ""
    echo "⚠️  IMPORTANT: This file is listed in .gitignore and will NOT be committed to git."
    echo "⚠️  Keep this file safe and never share it."
    echo ""
else
    echo "✓ Credentials file found: $CREDS_FILE"
fi

echo "🚀 Starting setup..."
echo ""

# Check if Docker Compose is running
if ! docker-compose ps | grep -q "Up"; then
    echo "🐳 Starting Docker containers..."
    docker-compose up -d
    echo "⏳ Waiting for services to be ready..."
    sleep 5
else
    echo "✓ Docker containers already running"
fi

# Run migrations
echo "📦 Running database migrations..."
docker-compose exec -T web python manage.py migrate

# Update admin credentials
echo "👤 Setting up admin user..."
bash update_credentials.sh

echo ""
echo "✅ Setup complete!"
echo ""
echo "🌐 Access your site:"
echo "   → Home:  http://localhost:8000"
echo "   → Admin: http://localhost:8000/admin/"
echo ""
