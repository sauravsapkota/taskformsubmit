# taskformsubmit
taskformsubmit: A Django web app for effortless user registration and streamlined form submissions, ensuring efficiency and precision in managing user data.

This is the README file for taskformsubmit project. It provides documentation and instructions for setting up and using this project.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Running Locally](#running-locally)
  - [Admin Interface](#admin-interface)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This web application allows users to register with their personal information, and administrators can manage user records through the admin interface.

## Features

- User registration form with validation.
- Customizable date picker for Date of Birth.
- Admin interface for managing user records (update, delete, undelete).
- Dockerized for easy deployment.

## Project Structure

The project is structured as follows:

- `formsubmission/`: Django app responsible for user management, including models, forms, and views.
- `taskformsubmit/`: The Django project settings and configuration.
- `static/`: Static files (e.g., CSS, JavaScript).
- `templates/`: HTML templates.
- `Dockerfile`: Docker configuration for the application.
- `docker-compose.yml`: Docker Compose configuration.
- `requirements.txt`: Python dependencies for running this project.
- `README.md`: This documentation file.

## Getting Started

### Prerequisites

Before running the application, make sure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/sauravsapkota/taskformsubmit
   cd taskformsubmit
   git checkout main
   ```

-   For development environment
    - Install docker and docker-compose

    - Keep the environment file .env in project root directory

    - run these commands in order:
    ```
    docker compose up -d --build
    docker compose exec web python manage.py migrate --noinput
    ```

    - use this command to create superuser
    ```
    docker compose run web python manage.py createsuperuser
    ```

    - Setup .env as following:
    ```
    ENVIRONMENT_TYPE=development

    SECRET_KEY=foo
    
    DEBUG=False
    ALLOWED_HOSTS=['*']
    
    DB_ENGINE=django.db.backends.postgresql_psycopg2
    DB_NAME=tfs_database
    DB_USER=postgres
    DB_PASSWORD=postgres
    DB_HOST=db
    DB_PORT=5432
    DATABASE=postgres
    ```
# Installation

- <b>Not required if docker is being used</b>

`virtualenv env`

# Database

- Not required if docker is being used

`CREATE DATABASE tfs_database;`

- Create a Virtual Environment (Optional)

It's a good practice to create a virtual environment to isolate project dependencies. Navigate to the project directory and run:

- Activate the virtual environment:
# For Mac/ Linux

`source env/bin/activate`

# For Window

`env\scripts\activate`

`pip install -r requirements.txt`

`python manage.py makemigrations`

`python manage.py migrate`

`python manage.py runserver`

`python manage.py createsuperuser`



