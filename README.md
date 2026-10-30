# TaskFlow – Project & Task Management Application

TaskFlow is a Django-based project and task management application that helps users organize projects, manage tasks, track progress, and stay on top of their work.

The application supports user authentication, project management, task management, task filtering, and search functionality, with PostgreSQL as its database.

## Features

### User Authentication
- User registration and login.
- Secure logout functionality.
- User-specific project and task access.
- Authentication required for dashboard access.

### Project Management
- Create new projects.
- View all personal projects.
- Edit project details.
- Delete projects.
- Automatically delete associated tasks when a project is deleted.

### Task Management
- Create tasks under projects.
- Edit and delete tasks.
- Assign task priorities:
  - Low
  - Medium
  - High
- Track task status:
  - To Do
  - In Progress
  - Done
- Set task due dates.

### Dashboard
- View total tasks, completed tasks, and projects.
- Search tasks by title.
- Filter tasks by status.
- Filter tasks by priority.
- Filter tasks by project.
- Display appropriate empty states when no matching tasks are available.

### Additional Features
- Form validation and custom error messages.
- User ownership validation.
- Responsive interface for desktop and mobile devices.
- Automated tests for models, forms, and views.

## Technology Stack

| Category | Technologies |
|---|---|
| Backend | Python, Django |
| Database | PostgreSQL |
| Frontend | HTML, CSS |
| Authentication | Django Authentication |
| Testing | Django Test Framework |
| Development Tools | VS Code, Git, GitHub |

## Project Structure

```text
TaskFlow/
│
├── accounts/
│   ├── templates/
│   │   └── registration/
│   │       ├── login.html
│   │       └── register.html
│   └── ...
│
├── tasks/
│   ├── taskflow_tests/
│   │   ├── test_models.py
│   │   ├── test_forms.py
│   │   └── test_views.py
│   ├── templates/
│   │   └── tasks/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   └── urls.py
│
├── config/
│   └── urls.py
│
├── static/
│   └── tasks/
│       └── style.css
│
├── manage.py
└── README.md
```

*Note: This is a representative structure. Adjust it if your local project contains additional files or directories.*

## Getting Started

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd TaskFlow
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install django psycopg[binary]
```

If you maintain a `requirements.txt`, you can instead run:

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Create a PostgreSQL database:

```sql
CREATE DATABASE taskflow_db;
```

Configure your database connection in Django's `settings.py` using your local PostgreSQL credentials.

Example:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "taskflow_db",
        "USER": "your_postgres_username",
        "PASSWORD": "your_postgres_password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

Replace the credentials with your local PostgreSQL configuration.

### 5. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

Open the application:

http://127.0.0.1:8000/

## Running Tests

TaskFlow includes automated tests covering models, forms, and application views.

Run the complete test suite:

```bash
python manage.py test tasks.taskflow_tests
```

The current test suite contains **41 passing tests**.

## Application Modules

| Module | Responsibility |
|---|---|
| Accounts | User registration and authentication |
| Projects | Project creation and management |
| Tasks | Task creation, editing, deletion, and tracking |
| Dashboard | Task overview, search, and filtering |
| Database | PostgreSQL data persistence |

## Future Enhancements

Potential improvements for future versions:

- Task deadlines and overdue notifications.
- Task sorting and pagination.
- Dashboard analytics and progress charts.
- REST API integration.
- Deployment to a cloud platform.

## Author

**Mrudula V.**

Developed as a hands-on project to strengthen skills in Python, Django, PostgreSQL, backend development, and automated testing.

---

*TaskFlow – Organize your projects. Track your progress. Get things done.*
