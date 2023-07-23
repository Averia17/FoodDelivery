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
**Import model to app/config/db/\__init\__.py** \
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
