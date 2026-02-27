# LMS System (Learning Management System)

LMS System is a backend web application for online learning, built with Django and Django REST Framework.
The project provides a REST API for managing courses, lessons, users, payments, and background tasks using Celery.
The application is designed to run as a multi-container system using Docker Compose.

## Content
[Features](#features)  
[Tech Stack](#tech-stack)  
[Project Architecture](#project-architecture)  
[Environment Variables](#environment-variables)   
[Installation and Running the Project (from scratch)](#installation-and-running-the-project-(from-scratch))  
[Running Services Verification](#running-services-verification)  
[Local Development (Without Docker)](#local-development-(without-docker))  
[API Overview](#api-overview)  
[API Documentation](#api-documentation)    
[Authentication (JWT)](#authentication-(jwt))  
[Users](#users)  
[Payments](#payments)  
[Courses](#courses)  
[Lessons](#lessons)  
[Subscriptions](#subscriptions)  
[Payment Result Pages](#payment-result-pages) 
[Admin Panel](#admin-panel) 
[Background Tasks](#background-tasks)  
[Summary](#summary)  
[CI/CD (GitHub Actions)](#CI/CD-(GitHub Actions))  
[CI Pipeline](#CI Pipeline)  
[Automatic Deployment (CD)](#Automatic Deployment-(CD))  
[Server Requirements](#Server Requirements)  
[Environment Configuration on Server](#Environment Configuration on Server)  
[Production URL](#Production URL) 
[One-Command Local Launch](#One-Command Local Launch) 
[Project Status](#project-status)  
[Author](#author)

## Features
- Course and lesson management (full CRUD)
- User registration and authentication 
- Role-based access control (users, moderators, admins)
- Payments tracking 
- JWT authentication 
- Filtering and search 
- Asynchronous background tasks 
- Periodic tasks scheduling


## Tech Stack
- Python 3.13+
- **Backend:** Django, Django REST Framework 
- **Database:** PostgreSQL 
- **Cache / Broker:** Redis 
- **Background Tasks:** Celery, Celery Beat 
- **Authentication:** JWT (Simple JWT)
- **Containerization:** Docker, Docker Compose

## Project Architecture
The project consists of the following services:
-	**web** — Django application (REST API)
-	**db** — PostgreSQL database
-	**redis** — message broker for Celery
-	**celery** — background task worker
-	**beat** — scheduler for periodic Celery tasks
All services are started together using **Docker Compose**.

## Environment Variables
All sensitive configuration is stored in environment variables.
1.	Copy the example file:
```bash
  cp .env.sample .env
```
2.	Fill in the required values in .env


## Installation and Running the Project (from scratch)
1. Clone the repository
```bash
   git clone https://github.com/olgapythonwq/LMS.git
   cd lms
```
2. Build and start all services
```bash
  docker compose up -d --build
```
   This command:
-	builds Docker images
-	starts Django, PostgreSQL, Redis, Celery worker, and Celery Beat
-	applies database migrations automatically
   
## Running Services Verification
**Check container status**
```bash
  docker compose ps
```
All services should be in **Up** state, and the database should be **healthy**.

**Web (Django)**
-	Open in browser:
-	http://localhost:8000/admin/
-	Django admin page should be accessible
-	Create a superuser if needed:
```bash
  docker compose exec web python manage.py createsuperuser
```

**Database (PostgreSQL)**
Check database container logs:
```bash
  docker compose logs db
```
You should see:
```bash
  database system is ready to accept connections
```

**Redis**
Verify Redis is running:
```bash
  docker compose exec redis redis-cli ping
```
Expected output:
```bash
  PONG
```

**Celery Worker**
Check Celery logs:
```bash
  docker compose logs celery
```
You should see:
```bash
  ready
```
This means the worker is connected to Redis and ready to process tasks.

**Celery Beat**
Check Beat logs:
```bash
  docker compose logs beat
```
You should see scheduled tasks being sent to the broker.

## Local Development (Without Docker)
1.	Create a virtual environment:
```bash
  python -m venv venv
```
2.	Activate it:
-	Windows:
```bash
  venv\Scripts\activate
```
-	Linux/macOS:
```bash
  source venv/bin/activate
```
3.	Install dependencies:
```bash
  pip install -r requirements.txt
```
4.	Apply migrations:
```bash
  python manage.py migrate
```
5.	Run the development server:
```bash
  python manage.py runserver
```


## API Overview
The LMS System exposes a RESTful API built with Django REST Framework.
All endpoints are grouped by application modules and are available under the base URL:
http://localhost:8000/
Interactive API documentation is available via Swagger.

## API Documentation
-	OpenAPI schema:
```md
  GET /api/schema/
```
-	Swagger UI:
```md
  GET /api/docs/
```

## Authentication (JWT)
JWT authentication is used for securing API endpoints.

| Method | Endpoint|  Description| 
| ----------- |  ----------- | ----------- | 
| POST    | /users/login/ | Obtain access and refresh tokens  |
| POST  | /users/token/refresh/  | Refresh access token  |
| POST   | /users/register/| Register a new user  |

Obtain JWT Token
```bash
  POST /users/login/
```
Request body:
```bash
  {
  "email": "user@example.com",
  "password": "password123"
}
```
Response:
```bash
  {
  "refresh": "xxx.yyy.zzz",
  "access": "aaa.bbb.ccc"
}
```
Use the access token in requests:
```bash
  Authorization: Bearer <access_token>
```

## Users
User management is implemented via a UserViewSet.

| Method | Endpoint|  Description| 
| ----------- |  ----------- | ----------- | 
| GET    | /users/ | List users  |
| GET  | /users/{id}/  | Retrieve user details  |
| PUT   | /users/{id}/| Update user  |
| PATCH   | /users/{id}/| Partial update  |
| DELETE   | /users/{id}/| Delete user  |


## Payments

| Method | Endpoint|  Description| 
| ----------- |  ----------- | ----------- | 
| GET    | /users/payments/ | List payments  |
| POST  | /users/payments/create/  | Create a payment  |
| GET   | /users/payments/{payment_id}/status/| Get payment status  |


## Courses
Courses are managed via a CourseViewSet.

| Method | Endpoint|  Description| 
| ----------- |  ----------- | ----------- | 
| GET    | /materials/courses/ | List all courses  |
| POST  | /materials/courses/  | Create a course  |
| GET  | /materials/courses/{id}/ | Retrieve course details  |
| PUT   | /materials/courses/{id}/| Update course  |
| PATCH   | /materials/courses/{id}/| Partial update  |
| DELETE   | /materials/courses/{id}/| Delete course  |


## Lessons
Lessons are handled via dedicated API views.

| Method | Endpoint| Description     | 
| ----------- |  ----------- |-----------------| 
| GET    | /materials/lessons/ | List lessons    |
| GET  | /materials/lessons/{id}/  | Retrieve lesson |
| POST  | /materials/lessons/create/ | Create lesson   |
| PUT   | /materials/lessons/{id}/update/| Update lesson   |
| DELETE   | /materials/lessons/{id}/delete/| Delete lesson   |


## Subscriptions

| Method | Endpoint|  Description| 
| ----------- |  ----------- | ----------- | 
| POST  | /materials/subscriptions/  | Create or update subscription  |
| GET   | /materials/subscriptions/list/| List subscriptions  |


## Payment Result Pages

| Method | Endpoint|  Description| 
| ----------- |  ----------- | ----------- | 
| GET  | /materials/success/	 | Payment success page  |
| GET   | /materials/cancel/| Payment cancellation page  |


## Admin Panel
-	Django Admin:
http://localhost:8000/admin/

## Background Tasks
- **Celery Worker** processes asynchronous tasks
- **Celery Beat** schedules periodic tasks
- Tasks and schedules can be managed via Django Admin panel

## Summary
To run the entire LMS system:
```bash
  docker compose up -d --build
```
After startup:
- Django API is available at http://localhost:8000
- PostgreSQL, Redis, Celery, and Beat are automatically connected
- All services can be monitored via docker compose ps and docker compose logs

## CI/CD (GitHub Actions)
Continuous Integration and Continuous Deployment are implemented using GitHub Actions.

### CI Pipeline
The CI workflow automatically runs on every:
- push to the develop branch
- pull request targeting develop
The pipeline performs the following steps:
1.	Sets up Python 3.13
2.	Installs project dependencies
3.	Runs code linting:
        - flake8
        - isort --check-only
4.	Runs automated tests using pytest
5.	Verifies Docker image build (docker build)
If any step fails, the pipeline stops and deployment is not triggered.

### Automatic Deployment (CD)
After a successful CI run on the develop branch, the project is automatically deployed to a remote Ubuntu server.
Deployment is performed via SSH using GitHub Actions and includes:
1.	Connecting to the remote server via SSH
2.	Fetching latest changes from develop
3.	Rebuilding Docker images
4.	Restarting containers with Docker Compose
Deployment script executed on the server:
```bash
  git fetch origin
  git checkout develop
  git pull origin develop
  docker compose down
  docker compose up -d --build
```
This ensures:
- The latest version of the application is deployed
- Containers are rebuilt with updated code
- Services are restarted cleanly

### Remote Server Setup
The application is deployed on a virtual machine running Ubuntu.
Server Requirements
- Ubuntu 22.04+
- Docker installed
- Docker Compose installed
- Git installed
- SSH access enabled
Initial Server Setup Steps
1.	Install Docker and Docker Compose
2.	Install Git
3.	Clone the repository
4.	Create a .env file with production variables
5.	Run:
```bash
  docker compose up -d --build
```
After this initial setup, all further deployments are fully automated via GitHub Actions.

### Environment Configuration on Server
The .env file is stored only on the server and is not committed to the repository.
Example production variables:
```bash
  POSTGRES_DB=prod_db
  POSTGRES_USER=prod_user
  POSTGRES_PASSWORD=password
  POSTGRES_HOST=db
  POSTGRES_PORT=5432

  SECRET_KEY=your_secret_key
  DJANGO_ENV=prod
  ALLOWED_HOSTS=<SERVER_IP>
```

### Production URL
The deployed application is available at:
```bash
  http://<SERVER_IP>
```
(Replace <SERVER_IP> with the actual server address.)

### One-Command Local Launch
The entire system can be started locally using a single command:
```bash
  docker compose up -d --build
```
This launches:
- Django
- PostgreSQL
- Redis
- Celery Worker
- Celery Beat

All services are connected automatically.


## Project Status
- [x] Completed
- [x] All acceptance criteria met
- [x] Ready for review

## Author
Olga