# Fabrique test assigment

## Description
Simple application intended for receiving and storing customers phone numbers to use it further in selective mailings.

## Environment variables setup
Run `cat .env.example > .env` command and change variable inside of created `.env` file. Then make following changes:
* MAILING_TOKEN - JWT token for access to mailing service
* MAILING_API_URL - url of mailing service
* POSTGRES_DB - PostgreSQL database name
* POSTGRES_USER - PostgreSQL database user
* POSTGRES_PASSWORD - PostgreSQL database password
* SECRET_KEY - Django secret key
* DEBUG - Defines if debug mode is enabled or not. Should accept TRUE or FALSE
* DATABASE_URL - database url. Should be consrtucted like following example `postgres://<POSTGRES_USER>:<POSTGRES_PASSWORD>@<docker compose service name>:<POSTGRES_PORT>/<POSTGRES_DB>`. [More on that](https://jdbc.postgresql.org/documentation/head/connect.html)
* ALLOWED_HOSTS - list of allowed hosts divided by commas

## Usage
To launch the project [Docker compose](https://docs.docker.com/compose/install/) should be installed. To launch project enter
`docker compose up -d --build`

Project OpenAPI schema should be accessible on `http://127.0.0.1:8080/docs/` page.

## Additional completed tasks
The only additional tasks that were completed are task 3(Create docker compose manifest) and task 5(Implement swagger UI)
