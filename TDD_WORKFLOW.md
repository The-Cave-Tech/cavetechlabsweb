# Quick Start: TDD Development Workflow

This guide shows how to use the test-driven development setup for The Cave Tech Labs website.

## Prerequisites

```bash
# Clone the repository
git clone https://github.com/The-Cave-Tech/cavetechlabsweb.git
cd cavetechlabsweb

# Run setup script (creates credentials if needed)
bash setup.sh

# Containers are now running with auto-migrations
```

## Running Tests

```bash
# Run the full test suite with auto-commit/auto-push
bash run_tests.sh

# Expected output:
# ✅ ALL TESTS PASSED (50/50)
# 📝 Auto-committing...
# 🚀 Auto-pushing to master...
```

## Adding a New Feature (TDD Cycle)

### Step 1: Write a Failing Test (RED)

```bash
# Edit a test file
vim tests/test_models.py

# Add your test at the end of the appropriate class
def test_project_has_difficulty_level(self, db):
    """Test that projects can have a difficulty level"""
    project = Project.objects.create(
        title="Advanced Project",
        description="Hard project",
        category="robotics",
        difficulty="advanced"
    )
    assert project.difficulty == "advanced"
```

```bash
# Run tests (WILL FAIL because Project model doesn't have difficulty field)
bash run_tests.sh
# 49 passed, 1 failed ❌
# (Auto-commit is skipped because tests failed)
```

### Step 2: Write Minimal Code (GREEN)

```bash
# Edit the model
vim cavetechapp/models.py

# Add the difficulty field
class Project(models.Model):
    # ... existing fields ...
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default='beginner'
    )
```

```bash
# Create and apply migrations
docker-compose exec -T web python manage.py makemigrations
docker-compose exec -T web python manage.py migrate --noinput
```

```bash
# Run tests again
bash run_tests.sh
# 50 passed ✅
# Auto-commits: "✓ All 50 tests passing - auto-commit [50/50 tests]"
# Auto-pushes to master! 🚀
```

### Step 3: Refactor (REFACTOR)

```bash
# If needed, improve the code
# Tests must still pass after refactoring

# Run tests to ensure nothing broke
bash run_tests.sh
# If still 50 tests → Auto-commits and pushes ✅
```

## Example: Adding a Method to Person

### 1. Write the Test

```python
# tests/test_models.py
def test_person_full_name_with_title(self, db):
    """Test that person can display full name with title"""
    person = Person.objects.create(
        name="Alice Smith",
        title="Instructor"
    )
    assert person.full_display() == "Alice Smith (Instructor)"
```

### 2. Run Test (RED)
```bash
bash run_tests.sh
# AttributeError: Person object has no attribute 'full_display'
```

### 3. Add Method (GREEN)
```python
# cavetechapp/models.py
class Person(models.Model):
    # ... fields ...
    
    def full_display(self):
        """Return full display name with title"""
        if self.title:
            return f"{self.name} ({self.title})"
        return self.name
```

### 4. Run Tests
```bash
bash run_tests.sh
# ✅ All tests pass
# Auto-commits and pushes!
```

## Example: Adding a View

### 1. Write the Test

```python
# tests/test_views.py
def test_project_search_returns_results(self, db, client):
    """Test that project search finds matching projects"""
    Project.objects.create(
        title="LED Matrix",
        description="An LED display",
        category="electronics"
    )
    response = client.get('/projects/search/?q=LED')
    assert response.status_code == 200
    assert "LED Matrix" in str(response.content)
```

### 2. Run Test (RED)
```bash
bash run_tests.sh
# 404: /projects/search/ not found
```

### 3. Add URL and View (GREEN)
```python
# cavetechapp/urls.py
urlpatterns = [
    # ... existing ...
    path('projects/search/', views.ProjectSearchView.as_view(), name='project_search'),
]

# cavetechapp/views.py
class ProjectSearchView(View):
    def get(self, request):
        query = request.GET.get('q', '')
        projects = Project.objects.filter(title__icontains=query)
        return render(request, 'cavetechapp/search_results.html', {'projects': projects})
```

### 4. Create Template
```html
<!-- templates/cavetechapp/search_results.html -->
{% extends "cavetechapp/base.html" %}
{% block content %}
<h1>Search Results</h1>
{% for project in projects %}
    <h2>{{ project.title }}</h2>
{% endfor %}
{% endblock %}
```

### 5. Run Tests
```bash
bash run_tests.sh
# ✅ All tests pass
# Auto-commits and pushes!
```

## Important Rules

1. **Never commit without tests passing**
   - The auto-commit script prevents failed tests from being committed

2. **Always write the test first**
   - RED → GREEN → REFACTOR
   - This ensures you're solving real problems

3. **Keep tests focused**
   - One assertion per test concept
   - Test behavior, not implementation

4. **Run tests often**
   - After every change
   - `bash run_tests.sh` takes ~1 second

## Useful Commands

```bash
# Run specific test file
docker-compose exec -T web python -m pytest tests/test_models.py -v

# Run specific test class
docker-compose exec -T web python -m pytest tests/test_models.py::TestProjectModel -v

# Run specific test
docker-compose exec -T web python -m pytest tests/test_models.py::TestProjectModel::test_project_creation -v

# Run with verbose output
docker-compose exec -T web python -m pytest tests/ -vv

# Run with detailed failure info
docker-compose exec -T web python -m pytest tests/ -vv --tb=long

# Run and stop on first failure
docker-compose exec -T web python -m pytest tests/ -x

# Run only failed tests from last run
docker-compose exec -T web python -m pytest tests/ --lf
```

## Debugging a Test

```bash
# Add print statements in your test
def test_something(self, db):
    person = Person.objects.create(name="Test")
    print(f"Created person: {person.name}")  # Debug output
    assert person.name == "Test"

# Run with capture disabled to see print statements
docker-compose exec -T web python -m pytest tests/test_models.py::TestPersonModel::test_something -s
```

## Understanding Test Files

### conftest.py
Shared pytest configuration and fixtures available to all tests:
- `sample_person` - A test Person object
- `sample_project` - A test Project object
- `featured_project` - A test featured Project object

### test_models.py
Tests for Django models (Person, Project):
- Model field validation
- Model methods
- Database relationships
- Cascade delete behavior

### test_views.py
Tests for Django views (HTTP responses):
- View returns correct HTTP status
- View renders correct template
- View provides correct context data
- View handles filtering and pagination

### test_admin.py
Tests for Django admin configuration:
- Admin displays correct fields
- Admin has correct filters
- Admin has search functionality
- Admin prepopulated fields work

## Git Integration

The `run_tests.sh` script automatically:

1. **Runs all tests** using pytest
2. **Counts results** (PASSED/FAILED)
3. **On success:** Auto-commits with message showing test count
4. **On success:** Auto-pushes to master branch
5. **On failure:** Shows which tests failed, does NOT commit

## Understanding Auto-Commit Messages

```
✓ All 50 tests passing - auto-commit [50/50 tests]
```

This means:
- ✓ = All tests passed
- 50 tests = Total test count
- 50/50 = All tests in format passed/total

If you add a test, the message will update:
```
✓ All 51 tests passing - auto-commit [51/51 tests]
```

## FAQ

**Q: What if I only want to run specific tests?**
A: Use pytest directly with the specific test path instead of run_tests.sh

**Q: Can I manually commit without running tests?**
A: Yes, but you lose the safety of the auto-commit system. Use `git commit` normally, but always run tests first!

**Q: What if tests pass but I don't want to push?**
A: The script auto-pushes. To prevent this, manually undo the push: `git push --force-with-lease origin HEAD~1:master`

**Q: How do I see which tests changed?**
A: Check git history: `git log --oneline` shows each test count

**Q: Can multiple people develop at the same time?**
A: Yes! Each developer's tests auto-commit/push. Pull before starting: `git pull origin master`

## Next Steps

1. Read [DESIGN.md](DESIGN.md) - Full architecture reference
2. Read [TEST_SETUP.md](TEST_SETUP.md) - TDD setup details
3. Check [README.md](README.md) - User-facing documentation
4. Start writing tests for your feature!

---

**Remember:** Test → Code → Refactor → Run Tests → Auto-Commit! ✅
