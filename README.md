# Тестовое задани

---

## Стек

- Python 3.13
- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- Docker / Docker Compose

---

## Структура проекта

- `/alembic` — миграции alembic
- `/src` — исходный код приложения
- `/tests` — тесты

---

## Запуск

1. Склонировать репозиторий:

```bash
git clone <repo-url>
cd <repo>
```

2. Скопировать файл с переменными окружения:
```bash
cp .env.example .env
```

3. Запустить Docker Compose
```bash
docker-compose up -d
```

4. Документация будет доступна по адресу:
[http://localhost:8080/docs](http://localhost:8080/docs)

--- 
## Fixture
Для удобной проверки автоматически создается кошелек при развертывании приложения со следующим UUID:
```
1abac292-f635-4b74-9c5c-a93b63bcd965
```

--- 
## Tests
Роуты покрыты тестами, запуск производится из корня через команду
```
uv run pytest
```