# The Cave Tech Labs - Website

🏭 A beautiful, modern Django website for **The Cave Tech** - Oslo's premier maker space and community workshop.

**Repository**: [The-Cave-Tech/cavetechlabsweb](https://github.com/The-Cave-Tech/cavetechlabsweb)

## Features

- 📱 **Responsive Design** - Works on all devices
- 👥 **Member Directory** - Display members with profiles and bios
- 🎨 **Project Showcase** - Featured and categorized projects
- 📊 **Django Admin** - Easy content management
- 🐳 **Docker & Docker Compose** - Simple containerized deployment
- 🐛 **VS Code Debugging** - Debug directly in VS Code with Docker
- 🔄 **Hot Reload** - Automatic reload on code changes
- 🔐 **Secure Credentials** - Credentials never committed to git

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/The-Cave-Tech/cavetechlabsweb.git
cd cavetechlabsweb
```

### 2. Run Setup Script

```bash
bash setup.sh
```

The setup script will:
- Prompt you for admin credentials (if missing)
- Start Docker containers
- Run database migrations
- Create the admin user

### 3. Access the Site

- **Website**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin/

### 4. Debug in VS Code

Press **F5** to start debugging. The debugger will attach to the running Django application on port 5678.

## Project Structure

```
cavetechlabsweb/
├── cavetechlabs/              # Django project settings
│   ├── settings.py            # Project configuration
│   ├── urls.py                # URL routing
│   ├── wsgi.py                # WSGI application
│   └── asgi.py                # ASGI application
├── cavetechapp/               # Main Django application
│   ├── models.py              # Person and Project models
│   ├── views.py               # View classes
│   ├── urls.py                # App URL routing
│   ├── admin.py               # Django admin configuration
│   └── migrations/            # Database migrations
├── templates/                 # HTML templates
├── static/                    # Static files
├── scripts/                   # Utility scripts
├── docker-compose.yml         # Docker Compose configuration
├── Dockerfile                 # Container image definition
├── requirements.txt           # Python dependencies
├── setup.sh                   # Initial setup script
├── update_credentials.sh       # Update admin credentials
└── manage.py                  # Django management script
```

## Credentials Management

### Security First ⚠️

Credentials are **NEVER** committed to git:
- `admin_credentials.json` is in `.gitignore`
- All credential files are automatically excluded

### Setting Up Credentials

**First time setup:**
```bash
bash setup.sh
```
You'll be prompted to enter admin username, email, and password.

**Update existing credentials:**
```bash
# Edit admin_credentials.json
vi admin_credentials.json

# Apply changes
bash update_credentials.sh
```

## Docker Commands

```bash
# Start containers
docker-compose up -d

# Stop containers
docker-compose down

# View logs
docker-compose logs -f web

# Access container shell
docker-compose exec web bash

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

## Models

### Person

Members of The Cave Tech:
- `name` - Full name
- `title` - Position/role (e.g., "Founder", "Instructor")
- `bio` - Biography
- `email` - Contact email
- `image` - Profile image

### Project

Projects created by members:
- `title` - Project name
- `slug` - URL-friendly identifier (auto-generated)
- `description` - Full description
- `category` - 3D Printing, Woodworking, Metalworking, Electronics, Software, Art & Design, Robotics, Other
- `creator` - FK to Person
- `image` - Project image
- `featured` - Show on homepage

## URLs

| URL | View | Description |
|-----|------|-------------|
| `/` | IndexView | Homepage with featured projects and members |
| `/people/` | PeopleListView | List all members |
| `/people/<id>/` | PersonDetailView | Individual member profile |
| `/projects/` | ProjectsListView | List all projects with filtering |
| `/projects/<slug>/` | ProjectDetailView | Individual project details |
| `/admin/` | Django Admin | Content management interface |

## Development

### Adding Content

1. Go to http://localhost:8000/admin/
2. Login with your admin credentials
3. Click "People" to add members
4. Click "Projects" to add projects
5. Mark projects as "Featured" to show on homepage

### Running Migrations

When you make changes to models:

```bash
# Create migration
docker-compose exec web python manage.py makemigrations

# Apply migration
docker-compose exec web python manage.py migrate
```

### Debugging

1. Set breakpoints in your code
2. Press F5 in VS Code
3. Refresh the browser to trigger code execution
4. Use the debugger toolbar to step through code

## Production Deployment

For production deployment:

1. Set `DEBUG=False` in environment
2. Change `SECRET_KEY` in settings.py
3. Configure proper database (PostgreSQL recommended)
4. Set up static file serving with Nginx
5. Use Gunicorn instead of Django dev server
6. Keep `admin_credentials.json` secure and not in version control

## Contributing

To contribute to this project:

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Commit: `git commit -m "Add your feature"`
4. Push: `git push origin feature/your-feature`
5. Create a Pull Request on GitHub

## Support

For questions or issues, please open an issue on GitHub or contact The Cave Tech team.

## License

© 2026 The Cave Tech Labs. All rights reserved.

---

**Location**: Oslo, Norway 🇳🇴  
**Website**: www.cavetechlabs.com  
**GitHub**: https://github.com/The-Cave-Tech/cavetechlabsweb  
**Made with ❤️ for the maker community**
