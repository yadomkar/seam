# Polling Service Documentation

This document outlines the implementation of a polling service designed to fetch data from a third-party API at specified intervals and store the response data. The service is built using Django for the backend, Celery for task scheduling and execution, Redis for task queuing and locking, and PostgreSQL for data storage.

## Overview

The service is capable of handling polling jobs for specific users, creating polling jobs with configurable intervals, and ensuring the persistence and uniqueness of data.

### Key Features

- **User-Specific Polling**: Polls third-party APIs based on user-specific configurations.
- **Configurable Polling Jobs**: Accepts requests to create polling jobs with specified API endpoints and intervals.
- **Persistent Storage**: Utilizes PostgreSQL to store response data, ensuring data persistence across service restarts.
- **Duplicate Data Handling**: Implements logic to prevent the storage of duplicate data.
- **Scalability**: Designed for horizontal scaling by adding more Celery workers.

## Setup and Configuration

### Technologies Used

- **Backend**: Django
- **Task Scheduling**: Celery
- **Task Queuing and Locking**: Redis
- **Data Storage**: PostgreSQL

### API Endpoint for Polling

```
https://dummyapi.online/api/users
```

### Creating a Polling Job

To create a new polling job, make a POST request to the service:

**POST Request URL**:
```
http://127.0.0.1:8000/polling-jobs
```

**Sample Request Body**:
```json
{
  "userId": "7",
  "apiEndpoint": "https://dummyapi.online/api/users",
  "pollingInterval": 70000
}
```

## Implementation Details

### Polling and Storage

- The service polls the specified API endpoint at the interval defined in the request. 
- The polling interval and API endpoint are dynamically configurable through the request body.
- PostgreSQL is chosen for storage due to its reliability and support for complex queries, which is beneficial for handling and querying large volumes of data.

### Handling Duplicates and Job Persistence

- Duplicate data is identified and handled to ensure that only unique data entries are stored, maintaining data integrity.
- Polling jobs are made persistent by storing their configurations in PostgreSQL. This allows polling jobs to resume from where they left off in case of a service crash or restart, ensuring no loss of scheduled tasks.

### Logging and Scalability

- Logs can be monitored through Docker, providing insights into the application's behavior and facilitating debugging.
- The service is designed for horizontal scalability. By adding more Celery workers, the service can handle increased load. Future enhancements may include support for Gunicorn for handling HTTP requests and database sharding for scaling data storage.

## Running the Service

1. **Build Containers**: Navigate to the project root (where `docker-compose.yml` is located) and run:
   ```bash
   docker-compose build
   ```
   
2. **Start Containers**: Launch your containers in detached mode:
   ```bash
   docker-compose up -d
   ```
   
3. **Apply Django Migrations**:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

4. **Restart Docker**:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

5. **Create Django Superuser to Access Admin Dashboard**:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```
   Follow the prompts to complete the setup.

6. **Accessing the Service**: The service can be accessed at the following URLs:
   - Admin Dashboard: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)
   - Polling Jobs: [http://127.0.0.1:8000/polling-jobs](http://127.0.0.1:8000/polling-jobs)

## Screenshots

### Periodic Tasks Persisted
![Periodic Tasks](/screenshots/tasks.png?raw=true "Periodic Tasks Persisted")

### User Data Persisted by Periodic Tasks
![Users](/screenshots/users.png?raw=true "User Data Persisted by Periodic Tasks")

## Conclusion

This polling service offers a robust solution for fetching and storing data from third-party APIs at configurable intervals. Its architecture ensures data persistence, uniqueness, and scalability, making it well-suited for applications requiring reliable data polling mechanisms.

