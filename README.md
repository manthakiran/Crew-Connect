# CrewConnect

**Connect your workforce. Manage your people.**

CrewConnect is a web-based Human Resource Management System (HRMS) built with Django. It gives HR teams a central place to manage employees, departments and designations, review leave requests, and gives employees a self-service portal to view their profile, apply for leave and track their calendar.

![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-092E20?logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.x-4479A1?logo=mysql&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?logo=bootstrap&logoColor=white)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [URL Reference](#url-reference)
- [Data Model](#data-model)
- [Dependencies](#dependencies)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

CrewConnect separates the application into two experiences, determined at login:

| Role | Who they are | What they can do |
| --- | --- | --- |
| **HR / Admin** | Any Django user **not** linked to an `Employee` record (e.g. a superuser) | Manage employees, departments and designations; approve or reject leave requests |
| **Employee** | A Django user linked to an `Employee` record | View profile, apply for leave, track leave status, view a personal calendar |

New employees are onboarded securely: when HR creates an employee, CrewConnect creates a login for them with **no password**, then emails a one-time link so the employee can set their own password. HR never sees or handles employee passwords.

## Features

**HR / Admin portal**

- Secure login with role-based redirect (HR dashboard vs. employee dashboard)
- Employee management: add, edit, view, and activate/deactivate (soft delete)
- Automatic account creation and emailed password-setup link for each new employee
- Department management: create, edit, activate/deactivate, delete
- Designation management: create, edit, activate/deactivate, delete
- Leave approval workflow: view all requests and approve or reject them
- Referential protection: departments and designations that still have employees cannot be deleted

**Employee self-service portal**

- Personal dashboard and profile
- Apply for leave (Earned Leave or Sick Leave)
- View personal leave history and request status (Pending / Approved / Rejected)
- Interactive leave calendar showing approved leaves, attendance (present/absent) and holidays

## Tech Stack

| Layer | Technology |
| --- | --- |
| Backend | Python, Django 6.0 |
| Database | MySQL |
| Frontend | Django templates, HTML, CSS, JavaScript |
| UI libraries | Bootstrap 5.3.3, Bootstrap Icons 1.11.3, FullCalendar 6.1.19 (all loaded via CDN) |
| Email | Django SMTP backend (Gmail SMTP by default) |

## Project Structure

```
CrewConnect/                      # Project root (contains manage.py)
├── manage.py                     # Django command-line utility
├── CrewConnect/                  # Project configuration package
│   ├── settings.py               # Settings (database, email, static files, apps)
│   ├── urls.py                   # Root URL configuration
│   ├── asgi.py
│   └── wsgi.py
├── hr/                           # HR / admin app
│   ├── models.py                 # Department, Designation, Employee, Leave,
│   │                             #   LeaveBalance, Attendance, Holiday
│   ├── views.py                  # Login, dashboard, employee/department/
│   │                             #   designation CRUD, leave approval
│   ├── urls.py                   # Routes mounted at "/"
│   ├── admin.py                  # Django admin registrations
│   └── migrations/               # Database migrations (0001–0006)
├── employee/                     # Employee self-service app
│   ├── views.py                  # Password setup, dashboard, profile,
│   │                             #   apply leave, my leaves, leave calendar
│   ├── urls.py                   # Routes mounted at "/employee/"
│   └── models.py                 # (models live in the hr app)
├── templates/                    # Project-level HTML templates
│   ├── base.html                 # Shared layout (loads Bootstrap + FullCalendar)
│   ├── sidebar.html              # HR navigation
│   ├── employee_sidebar.html     # Employee navigation
│   ├── login.html
│   ├── dashboard.html            # HR dashboard
│   ├── employee_dashboard.html
│   ├── employee_list.html / employee_add_update.html
│   ├── department_list.html / department_create.html
│   ├── designations_list.html / designation_create.html
│   ├── leave_approval.html
│   ├── apply_leave.html / my_leaves.html / employee_leave_calendar.html
│   ├── profile.html
│   └── set_password.html
└── static/
    └── css/
        ├── sidebar.css           # Sidebar and layout styles
        └── style1.css            # Login page styles
```

## Installation

### Prerequisites

- **Python 3.12 or newer** (Django 6.0 requires 3.12+; the project was developed on Python 3.13)
- **MySQL 8.x** (or a compatible MariaDB) running locally
- **pip** and **venv**
- An **SMTP account** for sending password-setup emails (or use Django's console email backend during development)

### 1. Get the code

```bash
git clone https://github.com/<your-username>/CrewConnect.git
cd CrewConnect
```

Make sure you are in the directory that contains `manage.py` for all following commands.

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

The MySQL driver (`mysqlclient`) compiles against the MySQL client libraries on Linux and macOS. Install those first:

```bash
# Debian / Ubuntu
sudo apt install build-essential pkg-config python3-dev default-libmysqlclient-dev

# macOS (Homebrew)
brew install mysql pkg-config
```

Then install the Python packages:

```bash
pip install "Django>=6.0,<6.1" mysqlclient
```

> Tip: once everything works, run `pip freeze > requirements.txt` so others can install with `pip install -r requirements.txt`.

### 4. Create the database

```sql
CREATE DATABASE crewconnect CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Configure the project

Open `CrewConnect/settings.py` and set your own values for the database, email and secret key. See [Configuration](#configuration) for details.

### 6. Apply migrations

```bash
python manage.py migrate
```

### 7. Create an HR administrator

```bash
python manage.py createsuperuser
```

This account has no linked `Employee` record, so it is treated as HR/Admin when it logs in.

### 8. Run the development server

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000/** and sign in.

## Configuration

All configuration lives in `CrewConnect/settings.py`.

| Setting | Purpose | What to do |
| --- | --- | --- |
| `SECRET_KEY` | Cryptographic signing | Generate a new, private key for every environment |
| `DEBUG` | Debug mode | Keep `True` for local development; **must be `False` in production** |
| `ALLOWED_HOSTS` | Allowed hostnames | Set to your domain(s) in production |
| `DATABASES['default']` | MySQL connection | Set `NAME`, `USER`, `PASSWORD`, `HOST`, `PORT` |
| `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS` | SMTP server | Defaults target Gmail SMTP on port 587 with TLS |
| `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` | SMTP credentials | Use your own account (for Gmail, an [App Password](https://support.google.com/accounts/answer/185833)) |
| `DEFAULT_FROM_EMAIL` | Sender address | Defaults to `EMAIL_HOST_USER` |

> **Security:** never commit real secrets (secret key, database password, email password) to version control. Load them from environment variables or a `.env` file that is listed in `.gitignore`. For example:
>
> ```python
> import os
> SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
> DATABASES["default"]["PASSWORD"] = os.environ["DB_PASSWORD"]
> EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
> ```

**Developing without SMTP:** switch to the console backend so password-setup links are printed in your terminal instead of emailed:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

## Usage

### HR workflow

1. **Sign in** at `/` using your superuser credentials. You'll land on the HR dashboard (`/dashboard/`).
2. **Create departments** (e.g. IT, HR, Marketing) and **designations** (e.g. Software Developer, Trainer) from the sidebar. These must exist before you can add employees.
3. **Add an employee** via *Employees → Add Employee*. Fill in the employee ID, name, email, phone, department, designation, joining date, employment type (Permanent / Contract / Part-time / Intern), salary and address.
4. On save, CrewConnect creates the employee's login (**the employee's email is their username**) and emails them a password-setup link.
5. **Manage employees** from *Employees → View Employees*: edit details or deactivate/reactivate an employee.
6. **Review leave requests** under *Leave Approval* and choose **Approve** or **Reject**.

### Employee workflow

1. Open the password-setup link from the email and choose a password.
2. **Sign in** at `/` with your email address and the new password.
3. From the employee dashboard you can:
   - **My Profile** – view your employment details
   - **Leave Management → Apply Leave** – submit an Earned Leave or Sick Leave request
   - **Leave Management → My Leaves** – track the status of your requests
   - **Leave Management → Leave Calendar** – see approved leaves, attendance and holidays at a glance

### Adding holidays and attendance

The `Holiday` and `Attendance` models feed the employee calendar but do not have UI screens or admin registrations yet. Until they do, add records from the Django shell:

```bash
python manage.py shell
```

```python
from hr.models import Holiday, Attendance, Employee
import datetime

Holiday.objects.create(
    name="Republic Day",
    date=datetime.date(2027, 1, 26),
    holiday_type="National",
    state="Andhra Pradesh",
)

emp = Employee.objects.get(employee_id="EMP001")
Attendance.objects.create(employee=emp, date=datetime.date.today(), status="Present")
```

### Django admin

The built-in admin is available at `/admin/` and has `Department`, `Designation` and `Employee` registered.

### Running tests

```bash
python manage.py test
```

> Test modules are scaffolded in each app but no tests have been written yet. See [Contributing](#contributing).

## URL Reference

### HR / Admin (`hr` app, mounted at `/`)

| URL | View | Description |
| --- | --- | --- |
| `/` | `login_view` | Login page |
| `/logout/` | `logout_view` | Log out |
| `/dashboard/` | `dashboard` | HR dashboard |
| `/employees/` | `employee_list` | List active employees |
| `/employees_create/` | `employee_create` | Add an employee |
| `/employees/<id>/edit/` | `employee_update` | Edit an employee |
| `/employees/<id>/delete/` | `employee_delete` | Activate / deactivate an employee |
| `/leave_approval/` | `leave_approval` | View all leave requests |
| `/leave/<id>/action/` | `leave_action` | Approve or reject a request (POST) |
| `/department_list/` | `department_list` | List departments |
| `/department_create/` | `department_create` | Add a department |
| `/departments/<id>/edit/` | `department_edit` | Edit a department |
| `/departments/<id>/delete/` | `department_delete` | Delete a department |
| `/designations_list/` | `designations_list` | List designations |
| `/designations_create/` | `designations_create` | Add a designation |
| `/designation/<id>/edit/` | `designation_edit` | Edit a designation |
| `/designation/<id>/delete/` | `designation_delete` | Delete a designation |

### Employee portal (`employee` app, mounted at `/employee/`)

| URL | View | Description |
| --- | --- | --- |
| `/employee/set-password/<uidb64>/<token>/` | `set_password` | One-time password setup |
| `/employee/dashboard/` | `employee_dashboard` | Employee dashboard |
| `/employee/profile/` | `employee_profile` | Employee profile |
| `/employee/apply_leave/` | `apply_leave` | Submit a leave request |
| `/employee/my_leaves/` | `my_leaves` | Personal leave history |
| `/employee/employee_leave_calendar/` | `employee_leave_calendar` | Calendar of leaves, attendance and holidays |

## Data Model

All models are defined in `hr/models.py`.

| Model | Key fields | Notes |
| --- | --- | --- |
| `Department` | `name` (unique), `status` | Protected from deletion while employees reference it |
| `Designation` | `name` (unique), `status` | Protected from deletion while employees reference it |
| `Employee` | `user` (1:1 → Django `User`), `employee_id` (unique), `name`, `email` (unique), `phone`, `department`, `designation`, `joining_date`, `employment_type`, `salary`, `address`, `status` | Links an HR record to a login account |
| `Leave` | `employee`, `leave_type` (EL / SL), `start_date`, `end_date`, `reason`, `status`, `applied_date` | Status: Pending → Approved / Rejected |
| `LeaveBalance` | `employee` (1:1), `earned_leave` (default 12), `sick_leave` (default 8) | Per-employee leave quota |
| `Attendance` | `employee`, `date`, `status` (Present / Absent) | Unique per employee per day |
| `Holiday` | `name`, `date` (unique), `holiday_type`, `description`, `state` | Types: Festival, National, Public, Optional |

## Dependencies

### Python packages

| Package | Version | Purpose |
| --- | --- | --- |
| [Django](https://www.djangoproject.com/) | 6.0.x | Web framework |
| [mysqlclient](https://pypi.org/project/mysqlclient/) | latest | MySQL database driver for Django |

### Front-end libraries (loaded via CDN, no install needed)

| Library | Version | Purpose |
| --- | --- | --- |
| [Bootstrap](https://getbootstrap.com/) | 5.3.3 | Layout and components |
| [Bootstrap Icons](https://icons.getbootstrap.com/) | 1.11.3 | Iconography |
| [FullCalendar](https://fullcalendar.io/) | 6.1.19 | Employee leave calendar |

> The CDN-hosted libraries require an internet connection in the browser. For offline or locked-down environments, download them and serve them from `static/`.

### System requirements

- Python 3.12+
- MySQL 8.x (or compatible) and its client libraries
- An SMTP server for outgoing email

## Roadmap

Ideas the codebase is already pointing towards, and good places to start contributing:

- [ ] Add a `requirements.txt` and `.gitignore`
- [ ] Move secrets and environment-specific settings to environment variables
- [ ] Write unit and integration tests for the views and models
- [ ] Register `Leave`, `LeaveBalance`, `Attendance` and `Holiday` in the Django admin
- [ ] Build UI screens for managing holidays and marking attendance
- [ ] Deduct approved leave from `LeaveBalance` automatically
- [ ] Payroll and payslips
- [ ] Reports and analytics
- [ ] Add a custom "invalid link" page for expired password-setup tokens

## Contributing

Contributions are welcome — whether it's a bug fix, a new feature, tests or documentation.

### Getting started

1. **Fork** the repository and clone your fork.
2. Follow the [Installation](#installation) steps to get a working local environment.
3. Create a feature branch from `main`:
   ```bash
   git checkout -b feature/short-description
   ```
   Use prefixes such as `feature/`, `fix/`, `docs/` or `refactor/`.

### Development guidelines

- **Code style:** follow [PEP 8](https://peps.python.org/pep-0008/) and Django's [coding style](https://docs.djangoproject.com/en/stable/internals/contributing/writing-code/coding-style/). Use clear, descriptive names for views, models and templates.
- **Migrations:** if you change a model, generate and commit the migration (`python manage.py makemigrations`). Never edit or delete migrations that have already been applied elsewhere.
- **Templates:** extend `base.html` and reuse the existing sidebar and Bootstrap components for a consistent look.
- **Access control:** protect new views with `@login_required` and, where relevant, make sure employees cannot reach HR-only actions.
- **Tests:** add tests for new behaviour and make sure `python manage.py test` passes before you open a pull request.
- **Secrets:** never commit credentials, API keys, `.env` files or database dumps.
- **Scope:** keep each pull request focused on a single change.

### Commit messages

Use short, imperative messages, ideally following [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add holiday management screen
fix: prevent employees from approving their own leave
docs: clarify email configuration steps
```

### Submitting a pull request

1. Push your branch to your fork.
2. Open a pull request against `main` with:
   - a clear title and description of **what** changed and **why**
   - screenshots for any UI changes
   - steps to test the change
   - a link to the related issue, if there is one
3. Respond to review feedback; a maintainer will merge once everything is approved.

### Reporting bugs and requesting features

Open a GitHub issue and include:

- what you expected to happen and what actually happened
- steps to reproduce (for bugs)
- your Python, Django and MySQL versions and operating system
- relevant error messages or screenshots

Please be respectful and constructive in all interactions.

## License

No license has been specified for this project yet. Add a `LICENSE` file (for example MIT or Apache-2.0) to let others know how they may use and contribute to the code, then update this section.

---

<p align="center">Built with Django · Maintained by the CrewConnect contributors</p>
