# Translation Service - User Documentation
## Introduction
This document provides an overview of how to set up and use the Translation Service. The service offers RESTful APIs and a GraphQL endpoint for translating and managing words in different languages.

## Environment Setup
Before running the application, create an environment file based on the provided example:

```bash
cp .env.example .env
```
Edit .env to suit your environment.

## Running the Application with Docker
To start the application, use Docker Compose:

```bash
docker-compose -f docker-compose.dev.yml up -d
```
This command runs the application in detached mode.

## Accessing the Service
- REST API: The REST API endpoints are documented in Swagger. Access the Swagger UI at http://127.0.0.1:8000/api/v1/.
- GraphQL: For GraphQL API usage access the Strawberry UI at http://127.0.0.1:8000/api/v1/graphql. 
- GraphQL python example: Refer to the examples in app/tests/examples/graphql.py.

## Database Host Configuration
- When accessing the database from a different network, use host.docker.internal as DEFAULT_DATABASE_HOSTNAME.
- To run docker-compose within a single network, use localhost.

## Development Documentation
For more details about the development setup, refer to the documentation in docs/TEMPLATE.README.md.

## Running Tests
Run tests using pytest. Note that tests use a separate database defined in docker-compose.yml, not the default one:

```bash
pytest
```

## Test Results
Expect the following output from the test suite:

```arduino
app/tests/test_auth.py::test_auth_access_token PASSED
app/tests/test_auth.py::test_auth_access_token_fail_no_user PASSED
app/tests/test_auth.py::test_auth_refresh_token PASSED
app/tests/test_users.py::test_read_current_user PASSED
app/tests/test_users.py::test_delete_current_user PASSED
app/tests/test_users.py::test_reset_current_user_password PASSED
app/tests/test_users.py::test_register_new_user PASSED
app/tests/repo/pg/test_word.py::test_get_word PASSED
app/tests/repo/pg/test_word.py::test_get_id_success PASSED
app/tests/repo/pg/test_word.py::test_get_id_not_found PASSED
app/tests/repo/pg/test_word.py::test_get_id_multiple_results PASSED
```

## Roadmap
For more details about the future improvement, refer to the documentation in docs/ROADMAP.md.

