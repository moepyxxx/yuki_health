## README.md

- run server

```
uv run uvicorn main:app --reload
```

- migration

```
uv run alembic revision --autogenerate -m "create family table"
uv run alembic upgrade head
```

- pgcli

```
pgcli postgresql://bird_user:bird_password@localhost:5432/bird_health_db
```
