# FastAPI Authentication Service

  

Asynchronous authentication service developed using Clean Architecture Principles.

  

## Getting Started

  

Docker:

```bash

cd docker/

docker-compose up --build -d

```

  

Apply alembic migrations:

```bash

docker-compose exec -e ALEMBIC_CONFIG=/home/app/web/src/alembic.ini fastapi alembic upgrade head

```



Create new migration:

```bash

docker-compose exec -e ALEMBIC_CONFIG=/home/app/web/src/alembic.ini fastapi alembic revision --autogenerate -m "Migration name"

```
