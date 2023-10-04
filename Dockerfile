# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy the Pipfile and Pipfile.lock to the container
#COPY Pipfile Pipfile.lock /app/

# install psycopg2 dependencies
RUN apt-get update \
    && apt-get install -y libpq-dev gcc libpangocairo-1.0-0 gettext fonts-deva

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .

RUN pip install -r requirements.txt
# Copy the rest of the application code to the container
COPY . /app/

# Expose port 8000
EXPOSE 8000

# Run the Django application
CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
