# Food Delivery

## General info
This project is a ecommerce web application for online ordering food.

## Setup
To run this project use:
```
docker-compose build
```
```
docker-compose up
```
To run unittests:
1. Create database **_test_db_** if not exists
2. Run command
```
docker-compose exec backend pytest
```

## Backend Development
Before commit changes you must install requirements
```
python -m venv venv
```
```
venv/Scripts/activate
```
```
pip install -r requirements.txt
```
Than you must install pre-commit
```
pre-commit install
```

### If you change something in database use migrations:
**Import model to app/alembic/env.py** \
Than create migration
```
docker-compose exec backend alembic revision --autogenerate
```
After apply the migration:
```
docker-compose exec backend alembic upgrade head
```

## Creators
- Frontend by [Ekaterina Motolyanets](https://github.com/katyamotolyanets)
- Backend by [Artyom Tabolich](https://github.com/Averia17) and [Andrey Motolyanets](https://github.com/motolyanets)
