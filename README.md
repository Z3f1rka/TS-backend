# TS-backend.
```bash
python -m venv .venv
```

```bash
source .venv/Scripts/activate
```

```bash
pip install -r requirements/dev.txt
```

```bash
mkdir alembic/versions
```

```bash
alembic revision --autogenerate
```

```bash
alembic upgrade head
```

проблема с импортами:
```bash
export PYTHONPATH=$(pwd)
```
отладка:
```bash
cd app
```

```bash
python -c "import sys; print(sys.path)"
```