#!/bin/bash
# Entrypoint script for Django container

set -e

echo "🚀 Starting Django application..."

# Run migrations
echo "📦 Running migrations..."
python manage.py migrate --noinput

# Create superuser if it doesn't exist
echo "👤 Ensuring admin user exists..."
python manage.py shell << 'END'
import json
from django.contrib.auth.models import User

# Load credentials from JSON file
with open('/app/admin_credentials.json', 'r') as f:
    creds = json.load(f)

username = creds.get('username', 'admin')
email = creds.get('email', 'admin@cavetechlabs.com')
password = creds.get('password', 'admin123')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"✓ Admin user created (username: {username})")
else:
    print(f"✓ Admin user '{username}' already exists")
END

# Start the application with debugpy
echo "🔧 Starting with debugpy debugger..."
exec python -m debugpy --listen 0.0.0.0:5678 manage.py runserver 0.0.0.0:8000
