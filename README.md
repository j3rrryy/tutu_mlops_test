# Тестовое задание MLOps

## Что нужно для запуска

- Docker (обязательно)
- Python 3.12, uv, Make (опционально — для локальной разработки)

## Начало работы

Создайте в корне проекта файл `.env` на основе `.env.example`. (Либо для быстрого запуска можно просто переименовать `.env.example` в `.env`)

## Запуск и загрузка признаков

```shell
make docker-up
```

Если Make не установлен:

```shell
docker compose up -d --build
```

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
- `make test` - запуск тестов
- `make docker-up` - запуск контейнеров
- `make docker-down` - остановка контейнеров
- `make makemigrations m="<название_миграции>"` - создание новой миграции
- `make migrate` - накатывание миграции
- `make downgrade` - откат миграции
- `make load-features` - загрузка признаков в БД
