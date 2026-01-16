#!/bin/bash
# Update admin credentials without restarting the container

set -e

CREDS_FILE="/home/elisabeth/projects/cavetechlabs/admin_credentials.json"

if [ ! -f "$CREDS_FILE" ]; then
    echo "❌ Error: admin_credentials.json not found at $CREDS_FILE"
    exit 1
fi

echo "🔑 Updating admin credentials..."

# Use docker-compose to run the update
cd /home/elisabeth/projects/cavetechlabs

sudo docker-compose exec -T web python manage.py shell << 'PYTHON_END'
import json
from django.contrib.auth.models import User

# Load credentials from JSON file
with open('/app/admin_credentials.json', 'r') as f:
    creds = json.load(f)

username = creds.get('username', 'admin')
email = creds.get('email', 'admin@cavetechlabs.com')
password = creds.get('password', 'admin123')

try:
    user = User.objects.get(username=username)
    user.email = email
    user.set_password(password)
    user.save()
    print(f"✓ Updated existing admin user: {username}")
except User.DoesNotExist:
    User.objects.create_superuser(username, email, password)
    print(f"✓ Created new admin user: {username}")

print(f"✓ Email: {email}")
print(f"✓ Password: {password}")
print("\n✅ Admin credentials updated successfully!")
PYTHON_END
