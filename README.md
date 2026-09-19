# Тестовое задание MLOps

Сервис предсказания расходов за отказ от покупки конкретного товара.
FastAPI + PostgreSQL + sklearn-модель (`artifacts/model.joblib`).

> [!NOTE]
> Приложение доступно на `http://localhost`
>
> Swagger UI: `http://localhost/docs`

## Что нужно для запуска

- Docker (обязательно)
- Python 3.12, uv, Make (опционально — для локальной разработки)

## Начало работы

Создайте в корне проекта файл `.env` на основе `.env.example`. (Либо для быстрого запуска можно просто переименовать `.env.example` в `.env`)

## Запуск

```shell
make docker-up
```

Если Make не установлен:

```shell
docker compose up -d --build
```

Поднимается PostgreSQL ⮕ прогоняются миграции ⮕ загружаются признаки товаров `artifacts/item_features.csv` ⮕ стартует основное приложение.

## Остановка

```shell
make docker-down
```

Если Make не установлен:

```shell
docker compose down
```

## Команды Make

- `make sync` - установка отсутствующих зависимостей
- `make lint` - запуск линтеров (ruff, mypy)
- `make format` - запуск форматировщика (ruff)
- `make test` - запуск unit-тестов
- `make test-all` - запуск всех тестов (unit + e2e, используется Docker)
- `make docker-up` - запуск контейнеров
- `make docker-down` - остановка контейнеров
- `make makemigrations m="<название_миграции>"` - создание новой миграции
- `make migrate` - накатывание миграции
- `make downgrade` - откат миграции
- `make load-features` - загрузка признаков в БД
