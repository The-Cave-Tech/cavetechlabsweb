# The Cave Tech Labs Website - Design Document

**Version**: 1.0  
**Last Updated**: January 16, 2026  
**Repository**: https://github.com/The-Cave-Tech/cavetechlabsweb  
**Organization**: The-Cave-Tech  

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Data Models](#data-models)
4. [Application Structure](#application-structure)
5. [Views and URL Routing](#views-and-url-routing)
6. [Templates and Frontend](#templates-and-frontend)
7. [Development Workflow](#development-workflow)
8. [Testing Strategy (TDD)](#testing-strategy-tdd)
9. [Deployment](#deployment)
10. [Technology Stack](#technology-stack)
11. [Security](#security)
12. [Common Tasks](#common-tasks)

---

## Project Overview

### Purpose

The Cave Tech Labs Website is a Django-based website for **The Cave Tech**, Oslo's premier maker space. The site showcases:
- **Members**: People who are part of The Cave Tech community
- **Projects**: Work created by members, categorized by type

### Goals

- ✅ Showcase maker space members and their projects
- ✅ Provide Django admin interface for content management
- ✅ Enable easy deployment via Docker
- ✅ Support development with debugging in VS Code
- ✅ Maintain clean separation of credentials from code
- ✅ Implement test-driven development practices
- ✅ Auto-commit passing tests to git

### Key Features

- Responsive design (works on all devices)
- Member profiles with bio and projects
- Project gallery with category filtering
- Django admin panel for management
- Hot-reload development
- Secure credential handling
- VS Code debugging support

---

## Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────┐
│         Nginx Reverse Proxy (Port 80)       │
│   (www.cavetechlabs.com → localhost:8000)   │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│        Docker Container (Port 8000)         │
│  ┌──────────────────────────────────────┐  │
│  │   Django Application                 │  │
│  │  ┌────────────────────────────────┐  │  │
│  │  │ Views (Class-Based)            │  │  │
│  │  │ - IndexView                    │  │  │
│  │  │ - PeopleListView               │  │  │
│  │  │ - PersonDetailView             │  │  │
│  │  │ - ProjectsListView             │  │  │
│  │  │ - ProjectDetailView            │  │  │
│  │  └────────────────────────────────┘  │  │
│  │  ┌────────────────────────────────┐  │  │
│  │  │ Models                         │  │  │
│  │  │ - Person                       │  │  │
│  │  │ - Project                      │  │  │
│  │  └────────────────────────────────┘  │  │
│  │  ┌────────────────────────────────┐  │  │
│  │  │ Templates                      │  │  │
│  │  │ - base.html (layout)           │  │  │
│  │  │ - index.html (homepage)        │  │  │
│  │  │ - people_list.html             │  │  │
│  │  │ - person_detail.html           │  │  │
│  │  │ - projects_list.html           │  │  │
│  │  │ - project_detail.html          │  │  │
│  │  └────────────────────────────────┘  │  │
│  └──────────────────────────────────────┘  │
│  ┌──────────────────────────────────────┐  │
│  │ SQLite Database (/tmp/db.sqlite3)    │  │
│  │ - Users (Django auth)                │  │
│  │ - People                             │  │
│  │ - Projects                           │  │
│  └──────────────────────────────────────┘  │
│  ┌──────────────────────────────────────┐  │
│  │ Debugpy (Port 5678)                  │  │
│  │ - Enables VS Code debugging          │  │
│  └──────────────────────────────────────┘  │
└──────────────────────────────────────────────┘
```

### Directory Structure

```
cavetechlabsweb/
├── .git/                          # Git repository
├── .vscode/
│   ├── launch.json                # VS Code debug configuration
│   └── tasks.json                 # VS Code tasks
├── .gitignore                     # Git ignore patterns (credentials)
├── .dockerignore                  # Docker build ignore
├── cavetechlabs/                  # Django project settings package
│   ├── __init__.py
│   ├── settings.py                # Django configuration
│   ├── urls.py                    # Root URL routing
│   ├── wsgi.py                    # WSGI application
│   └── asgi.py                    # ASGI application
├── cavetechapp/                   # Main Django application
│   ├── __init__.py
│   ├── apps.py                    # App configuration
│   ├── admin.py                   # Django admin setup
│   ├── models.py                  # Data models (Person, Project)
│   ├── views.py                   # View classes
│   ├── urls.py                    # App URL routing
│   ├── tests.py                   # Unit tests
│   └── migrations/                # Database migrations
│       ├── __init__.py
│       └── 0001_initial.py        # Initial schema migration
├── templates/                     # HTML templates
│   ├── base.html                  # Base template (layout)
│   └── cavetechapp/
│       ├── index.html             # Homepage
│       ├── people_list.html       # People directory
│       ├── person_detail.html     # Individual person profile
│       ├── projects_list.html     # Projects gallery
│       └── project_detail.html    # Individual project details
├── static/                        # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
├── scripts/                       # Utility scripts
│   └── docker-debug.sh            # Debug setup
├── tests/                         # Test suite (TDD)
│   ├── __init__.py
│   ├── test_models.py             # Model tests
│   ├── test_views.py              # View tests
│   ├── test_admin.py              # Admin tests
│   └── conftest.py                # Pytest configuration
├── Dockerfile                     # Container image definition
├── docker-compose.yml             # Docker Compose configuration
├── entrypoint.sh                  # Container entrypoint
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
├── setup.sh                       # Initial setup script
├── update_credentials.sh           # Update credentials script
├── run_tests.sh                   # Run test suite with auto-commit
├── admin_credentials.json          # Admin credentials (NOT IN GIT)
├── README.md                      # User-facing documentation
└── DESIGN.md                      # This file
```

---

## Data Models

### Person Model

Represents a member of The Cave Tech.

```python
class Person(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    image = models.ImageField(upload_to='people/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'People'
    
    def __str__(self):
        return self.name
```

**Fields**:
- `name` (required): Full name of the person
- `title` (optional): Role/position (e.g., "Founder", "Lead Instructor")
- `bio` (optional): Biography/description
- `email` (optional): Contact email
- `image` (optional): Profile photo
- `created_at` (auto): Creation timestamp
- `updated_at` (auto): Last update timestamp

**Relationships**:
- Has many `Project` objects (via ForeignKey in Project model)

**Ordering**: By name (A-Z)

---

### Project Model

Represents a project created by members.

```python
class Project(models.Model):
    CATEGORY_CHOICES = [
        ('3d_printing', '3D Printing'),
        ('woodworking', 'Woodworking'),
        ('metalworking', 'Metalworking'),
        ('electronics', 'Electronics'),
        ('software', 'Software'),
        ('art', 'Art & Design'),
        ('robotics', 'Robotics'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    creator = models.ForeignKey(Person, on_delete=models.SET_NULL, 
                                null=True, blank=True, related_name='projects')
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
```

**Fields**:
- `title` (required): Project name
- `slug` (required, unique): URL-friendly identifier (auto-generated from title)
- `description` (required): Full project description
- `category` (required): Type of project (dropdown)
- `creator` (optional): FK to Person who created it
- `image` (optional): Project photo
- `featured` (optional): If True, shows on homepage
- `created_at` (auto): Creation timestamp
- `updated_at` (auto): Last update timestamp

**Categories**:
- 3D Printing
- Woodworking
- Metalworking
- Electronics
- Software
- Art & Design
- Robotics
- Other

**Relationships**:
- Belongs to one `Person` (nullable, can exist without creator)

**Ordering**: By created_at (newest first)

**Special Behavior**:
- Slug is auto-generated from title on first save
- Category is dropdown-selectable via choices

---

## Application Structure

### Installed Apps

```python
INSTALLED_APPS = [
    'django.contrib.admin',       # Admin interface
    'django.contrib.auth',        # User authentication
    'django.contrib.contenttypes', # Content types framework
    'django.contrib.sessions',    # Session management
    'django.contrib.messages',    # Messages framework
    'django.contrib.staticfiles', # Static files
    'cavetechapp',                # Our main app
]
```

### Middleware

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

### CSRF Protection

**Trusted Origins**:
- `https://www.cavetechlabs.com`
- `http://www.cavetechlabs.com`
- `http://localhost:8000`
- `http://127.0.0.1:8000`

All POST forms require `{% csrf_token %}` in templates.

---

## Views and URL Routing

### View Classes

All views are class-based views extending `django.views.View`.

#### IndexView

**URL**: `/`  
**Template**: `cavetechapp/index.html`  
**Purpose**: Homepage with featured projects and members

**Logic**:
```python
def get(self, request):
    featured_projects = Project.objects.filter(featured=True)[:6]
    people = Person.objects.all()
    context = {
        'featured_projects': featured_projects,
        'people': people,
    }
    return render(request, 'cavetechapp/index.html', context)
```

**Context Variables**:
- `featured_projects`: List of up to 6 featured projects
- `people`: List of all people

---

#### PeopleListView

**URL**: `/people/`  
**Template**: `cavetechapp/people_list.html`  
**Purpose**: Directory of all members

**Logic**:
```python
def get(self, request):
    people = Person.objects.all()
    context = {'people': people}
    return render(request, 'cavetechapp/people_list.html', context)
```

**Context Variables**:
- `people`: List of all people (ordered by name)

---

#### PersonDetailView

**URL**: `/people/<id>/`  
**Template**: `cavetechapp/person_detail.html`  
**Purpose**: Individual member profile

**Logic**:
```python
def get(self, request, pk):
    person = get_object_or_404(Person, pk=pk)
    projects = person.projects.all()
    context = {'person': person, 'projects': projects}
    return render(request, 'cavetechapp/person_detail.html', context)
```

**Context Variables**:
- `person`: Single Person instance
- `projects`: List of projects by this person

---

#### ProjectsListView

**URL**: `/projects/`  
**Template**: `cavetechapp/projects_list.html`  
**Purpose**: Project gallery with category filtering

**Logic**:
```python
def get(self, request):
    projects = Project.objects.all()
    category = request.GET.get('category')
    if category:
        projects = projects.filter(category=category)
    categories = Project.objects.values_list('category', flat=True).distinct()
    context = {
        'projects': projects,
        'categories': categories,
        'selected_category': category,
    }
    return render(request, 'cavetechapp/projects_list.html', context)
```

**Query Parameters**:
- `category` (optional): Filter by category

**Context Variables**:
- `projects`: Filtered list of projects
- `categories`: List of all available categories
- `selected_category`: Currently selected category (for UI highlighting)

---

#### ProjectDetailView

**URL**: `/projects/<slug>/`  
**Template**: `cavetechapp/project_detail.html`  
**Purpose**: Individual project details

**Logic**:
```python
def get(self, request, slug):
    project = get_object_or_404(Project, slug=slug)
    related_projects = Project.objects.filter(
        category=project.category
    ).exclude(pk=project.pk)[:3]
    context = {
        'project': project,
        'related_projects': related_projects,
    }
    return render(request, 'cavetechapp/project_detail.html', context)
```

**Context Variables**:
- `project`: Single Project instance
- `related_projects`: Up to 3 other projects in same category

---

### URL Routing

**Root URLs** (`cavetechlabs/urls.py`):
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cavetechapp.urls')),
]
```

**App URLs** (`cavetechapp/urls.py`):
```python
app_name = 'cavetechapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('people/', PeopleListView.as_view(), name='people_list'),
    path('people/<int:pk>/', PersonDetailView.as_view(), name='person_detail'),
    path('projects/', ProjectsListView.as_view(), name='projects_list'),
    path('projects/<slug:slug>/', ProjectDetailView.as_view(), name='project_detail'),
]
```

**URL Reference Table**:

| URL | Name | View | Parameters |
|-----|------|------|-----------|
| `/` | `cavetechapp:index` | IndexView | - |
| `/people/` | `cavetechapp:people_list` | PeopleListView | - |
| `/people/<id>/` | `cavetechapp:person_detail` | PersonDetailView | pk (int) |
| `/projects/` | `cavetechapp:projects_list` | ProjectsListView | ?category=slug |
| `/projects/<slug>/` | `cavetechapp:project_detail` | ProjectDetailView | slug (string) |
| `/admin/` | - | Django Admin | - |

---

## Templates and Frontend

### Base Template (`base.html`)

Master layout template extended by all other templates.

**Structure**:
```
<head>
  - Meta tags
  - Title ({% block title %})
  - Inline CSS (no external stylesheets)
</head>
<body>
  <header>
    - Logo
    - Navigation menu
  </header>
  
  {% block content %}{% endblock %}
  
  <footer>
    - Copyright
    - Links
</footer>
```

**Styling**:
- All CSS is inline in `<style>` tag
- Color scheme:
  - Dark Blue: `#1a1a2e`, `#16213e`
  - Accent Cyan: `#00d4ff`
  - Text: `#333`, `#555`, `#666`
- Responsive grid using CSS Grid
- Mobile-first design

**Navigation**:
```
Home → People → Projects → Admin
```

---

### Template Hierarchy

```
base.html
├── index.html (homepage)
├── people_list.html (people directory)
├── person_detail.html (person profile)
├── projects_list.html (projects gallery)
└── project_detail.html (project details)
```

### Template Variables (Cheat Sheet)

**index.html**:
- `featured_projects`: List[Project]
- `people`: List[Person]

**people_list.html**:
- `people`: List[Person]

**person_detail.html**:
- `person`: Person
- `projects`: List[Project]

**projects_list.html**:
- `projects`: List[Project]
- `categories`: List[str] (category keys)
- `selected_category`: str or None

**project_detail.html**:
- `project`: Project
- `related_projects`: List[Project]

---

## Development Workflow

### 1. Test-Driven Development (TDD)

**Important**: Always follow TDD approach:

1. **Write the test first** - Define expected behavior
2. **Run the test** - It should fail (RED)
3. **Write minimal code** - Make the test pass (GREEN)
4. **Refactor** - Clean up code (REFACTOR)
5. **Commit** - Auto-commit if all tests pass

### 2. Test Structure

Tests are located in:
- `cavetechapp/tests.py` - Quick tests
- `tests/` - Comprehensive test suite

**Test categories**:

```
tests/
├── test_models.py       # Model behavior
├── test_views.py        # View logic and responses
├── test_admin.py        # Admin interface
└── conftest.py          # Pytest fixtures and configuration
```

### 3. Running Tests

```bash
# Run all tests with auto-commit on pass
bash run_tests.sh

# Run specific test file
docker-compose exec web python -m pytest tests/test_models.py -v

# Run specific test
docker-compose exec web python -m pytest tests/test_models.py::TestPerson::test_person_creation -v

# Run with coverage
docker-compose exec web python -m pytest --cov=cavetechapp tests/
```

### 4. Auto-Commit Workflow

The `run_tests.sh` script:
1. Runs all tests
2. If all pass: auto-commits with message showing test count
3. If any fail: stops and shows failures
4. On pass, auto-pushes to master

**Example**:
```bash
bash run_tests.sh
```

Automatically commits as:
```
✓ All 24 tests passing - auto-commit [24/24 tests]
```

### 5. Git Workflow

**Branching**:
- `master`: Always stable, contains passing tests
- `feature/xxx`: Feature branches (optional for large changes)

**Commits**:
- Manual: `git commit -m "message"`
- Automatic: Via `run_tests.sh` on test pass

**Pushing**:
- Manual: `git push origin master`
- Automatic: Via `run_tests.sh` after auto-commit

### 6. Development Cycle

```
1. Check out existing code
   └─ git pull origin master

2. Create/modify tests in tests/
   └─ Define expected behavior

3. Run tests (RED)
   └─ bash run_tests.sh → Fails

4. Write minimal code to pass tests
   └─ Modify models/views

5. Run tests (GREEN)
   └─ bash run_tests.sh → Passes + Auto-commits + Auto-pushes

6. Refactor if needed
   └─ Clean up code
   └─ Run tests to ensure nothing breaks
   └─ Auto-commit on pass
```

---

## Testing Strategy (TDD)

### Test Philosophy

- **Never trust untested code**
- **Write tests first** - Think through requirements
- **Test behavior, not implementation** - Flexible refactoring
- **One assertion per test** - Clear failures
- **Use descriptive names** - `test_person_with_no_name_should_fail()`

### Test Types

#### Unit Tests (Models)

Test model methods and properties:

```python
# tests/test_models.py

from django.test import TestCase
from cavetechapp.models import Person, Project

class TestPerson(TestCase):
    def setUp(self):
        self.person = Person.objects.create(
            name="John Doe",
            title="Founder",
            email="john@example.com"
        )
    
    def test_person_creation(self):
        """Test that a person can be created"""
        self.assertEqual(self.person.name, "John Doe")
    
    def test_person_string_representation(self):
        """Test that str(person) returns name"""
        self.assertEqual(str(self.person), "John Doe")
    
    def test_person_ordering(self):
        """Test that people are ordered by name"""
        person2 = Person.objects.create(name="Alice Smith")
        people = Person.objects.all()
        self.assertEqual(people[0].name, "Alice Smith")
```

#### View Tests

Test view responses and context:

```python
# tests/test_views.py

from django.test import TestCase, Client
from cavetechapp.models import Person, Project

class TestIndexView(TestCase):
    def setUp(self):
        self.client = Client()
        self.person = Person.objects.create(name="John Doe")
        self.project = Project.objects.create(
            title="Cool Project",
            description="A cool project",
            category="electronics",
            featured=True,
            creator=self.person
        )
    
    def test_index_view_returns_200(self):
        """Test that index view returns HTTP 200"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_index_view_contains_featured_projects(self):
        """Test that featured projects appear on homepage"""
        response = self.client.get('/')
        self.assertIn(self.project, response.context['featured_projects'])
    
    def test_index_view_contains_people(self):
        """Test that people appear on homepage"""
        response = self.client.get('/')
        self.assertIn(self.person, response.context['people'])
```

#### Integration Tests

Test full workflows:

```python
def test_project_detail_shows_related_projects(self):
    """Test that project detail shows related projects"""
    # Create 2 projects in same category
    project1 = Project.objects.create(
        title="Project 1",
        description="...",
        category="electronics"
    )
    project2 = Project.objects.create(
        title="Project 2",
        description="...",
        category="electronics"
    )
    
    # Access project detail
    response = self.client.get(f'/projects/{project1.slug}/')
    
    # Check related projects includes project2
    self.assertIn(project2, response.context['related_projects'])
```

### Test Coverage

Aim for **>80% coverage**:

```bash
docker-compose exec web python -m pytest --cov=cavetechapp tests/
```

### Pytest Configuration

**conftest.py**:
```python
import pytest
from django.conf import settings

@pytest.fixture
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }

@pytest.fixture
def sample_person(db):
    """Fixture: Create a sample person"""
    from cavetechapp.models import Person
    return Person.objects.create(
        name="Test Person",
        email="test@example.com"
    )

@pytest.fixture
def sample_project(db, sample_person):
    """Fixture: Create a sample project"""
    from cavetechapp.models import Project
    return Project.objects.create(
        title="Test Project",
        description="Test",
        category="electronics",
        creator=sample_person
    )
```

---

## Deployment

### Development Environment

```bash
# Start containers
docker-compose up -d

# Access site
http://localhost:8000

# Access admin
http://localhost:8000/admin/
```

### Production Checklist

- [ ] Set `DEBUG=False` in environment
- [ ] Generate new `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Switch to PostgreSQL (from SQLite)
- [ ] Use Gunicorn (from Django dev server)
- [ ] Set up Nginx reverse proxy
- [ ] Enable HTTPS
- [ ] Backup `admin_credentials.json` securely
- [ ] Set up automated backups
- [ ] Monitor error logs

### Environment Variables

```bash
DEBUG=True                        # Set to False in production
DJANGO_SETTINGS_MODULE=cavetechlabs.settings
PYTHONUNBUFFERED=1
SECRET_KEY=generate-new-key-for-production
ALLOWED_HOSTS=www.cavetechlabs.com,cavetechlabs.com
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

---

## Technology Stack

### Backend

- **Framework**: Django 4.2.8
- **Database**: SQLite (dev), PostgreSQL (production)
- **Server**: Gunicorn (production), Django dev server (dev)
- **Containerization**: Docker & Docker Compose

### Frontend

- **Templates**: Django Template Language
- **CSS**: Inline (no external framework)
- **JavaScript**: Vanilla (no frameworks)
- **Responsive**: CSS Grid & Flexbox

### Development Tools

- **Testing**: pytest, pytest-django
- **Version Control**: Git, GitHub CLI
- **Debugging**: debugpy (VS Code integration)
- **Code Quality**: (Future: black, flake8, isort)

### Python Dependencies

See `requirements.txt`:
- Django 4.2.8
- Pillow (image handling)
- debugpy (debugging)
- gunicorn (production server)
- psycopg2 (PostgreSQL adapter)

---

## Security

### Credentials

**NEVER commit**:
- `admin_credentials.json`
- `.env` files
- `settings_local.py`
- Database files
- Private keys

**Enforce via `.gitignore`**:
```
admin_credentials.json
*_credentials.json
*_secrets.json
.env
.env.*.local
```

### CSRF Protection

All POST forms require `{% csrf_token %}`:

```html
<form method="post">
    {% csrf_token %}
    <!-- form fields -->
</form>
```

**Trusted origins** (in settings.py):
```python
CSRF_TRUSTED_ORIGINS = [
    'https://www.cavetechlabs.com',
    'http://www.cavetechlabs.com',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]
```

### Password Security

- Passwords hashed via Django's password hashers
- Never store plaintext passwords
- Use strong passwords (min 8 chars, mixed case, numbers, symbols)

### SQL Injection Prevention

- **Always use ORM**: `Person.objects.filter(name=user_input)`
- **Never concatenate strings**: ❌ `f"SELECT * FROM person WHERE name = '{name}'"`
- **Use parameterized queries**: ✅ `Person.objects.filter(name=name)`

### XSS Prevention

- Django templates auto-escape by default
- Use `|safe` filter only for trusted content
- Validate all user input

---

## Common Tasks

### Adding a New Page

1. **Create view** in `cavetechapp/views.py`
2. **Create template** in `templates/cavetechapp/`
3. **Add URL** in `cavetechapp/urls.py`
4. **Write tests** in `tests/test_views.py`
5. **Run tests**: `bash run_tests.sh`

Example:
```python
# views.py
class NewPageView(View):
    def get(self, request):
        context = {...}
        return render(request, 'cavetechapp/new_page.html', context)

# urls.py
path('new-page/', NewPageView.as_view(), name='new_page'),

# tests/test_views.py
def test_new_page_view(client):
    response = client.get('/new-page/')
    assert response.status_code == 200
```

### Adding a Model

1. **Define model** in `cavetechapp/models.py`
2. **Register in admin** in `cavetechapp/admin.py`
3. **Create migration**: `docker-compose exec web python manage.py makemigrations`
4. **Apply migration**: `docker-compose exec web python manage.py migrate`
5. **Write tests** in `tests/test_models.py`
6. **Run tests**: `bash run_tests.sh`

### Updating Admin Credentials

```bash
# Edit credentials file
vi admin_credentials.json

# Apply changes
bash update_credentials.sh
```

### Running Migrations

```bash
# Create migration
docker-compose exec web python manage.py makemigrations

# Apply migration
docker-compose exec web python manage.py migrate

# Check migration status
docker-compose exec web python manage.py showmigrations
```

### Creating Database Backups

```bash
# SQLite backup
docker-compose exec web cp /tmp/db.sqlite3 /tmp/db.sqlite3.backup

# PostgreSQL backup (production)
docker-compose exec db pg_dump -U postgres dbname > backup.sql
```

### Accessing Container Shell

```bash
docker-compose exec web bash

# Inside container:
python manage.py shell
```

### Viewing Logs

```bash
# All logs
docker-compose logs -f web

# Last 50 lines
docker-compose logs --tail=50 web

# Specific service
docker-compose logs -f [service-name]
```

### Resetting Database

```bash
# Delete and recreate (development only)
docker-compose down -v
docker-compose up -d
bash setup.sh
```

---

## Important Notes for Future Development

### Context Length Considerations

This document is designed to be **context-complete**. When working with AI:

1. **Always reference this document** at the start of a session
2. **Copy relevant sections** into your prompt if needed
3. **Use file paths** as references (e.g., "See line 45 of test_models.py")
4. **Provide git history** if debugging: `git log --oneline -10`

### Onboarding New Developers / AIs

**Minimal steps to understand project**:

1. Read: Project Overview section
2. Read: Architecture section
3. Read: Data Models section
4. Clone: `git clone https://github.com/The-Cave-Tech/cavetechlabsweb.git`
5. Setup: `bash setup.sh`
6. Read: Testing Strategy section
7. Run: `bash run_tests.sh`

### Git Workflow Recap

```
git pull origin master          # Get latest
# Make changes
bash run_tests.sh               # Tests + auto-commit + auto-push
git push origin master          # (already done by run_tests.sh)
```

### Code Style Guidelines

- **Line length**: 88 characters (default)
- **Indentation**: 4 spaces
- **Imports**: Alphabetical within groups (future: use isort)
- **Comments**: Explain WHY, not WHAT
- **Functions**: Keep under 20 lines

### Useful Commands Reference

```bash
# Development
docker-compose up -d           # Start containers
docker-compose logs -f web     # View logs
bash setup.sh                  # Initial setup
bash update_credentials.sh     # Update admin credentials

# Testing & Deployment
bash run_tests.sh              # Run tests + auto-commit
docker-compose exec web pytest tests/ -v  # Run tests verbose
docker-compose exec web python manage.py migrate  # Run migrations

# Git
git pull origin master         # Get latest code
git log --oneline              # View commit history
git diff                       # View uncommitted changes
```

---

## Document Versioning

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Jan 16, 2026 | Initial design document |

**Maintainer**: Elisabeth Roynestad (elisabethroynestad)  
**Last Updated**: January 16, 2026  
**Status**: Active Development  

---

End of Design Document.
