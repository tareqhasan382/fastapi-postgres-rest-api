# fastapi-postgres-crud

A RESTful CRUD API built with FastAPI, SQLAlchemy, and PostgreSQL, containerized with Docker.

## Tech Stack

- **FastAPI** — modern, fast web framework for building APIs
- **SQLAlchemy** — ORM for database interaction
- **PostgreSQL** — relational database
- **Docker** — containerization
- **Alembic** — database migrations
- **Pydantic** — data validation

## Project Structure

```
crud-api/
├── app/
│   ├── __init__.py
│   ├── main.py          # app entrypoint
│   ├── database.py      # SQLAlchemy engine & session
│   ├── models.py        # ORM table definitions
│   ├── schemas.py       # Pydantic request/response models
│   ├── crud.py          # database query functions
│   └── routers/
│       └── items.py     # /items CRUD routes
├── .env                 # environment variables (not committed)
├── .env.example         # example env file
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .gitignore
```

## Getting Started

### Prerequisites

- Python 3.11+
- Docker & Docker Compose

### 1. Clone the repository

```bash
git clone https://github.com/your-username/fastapi-postgres-crud.git
cd fastapi-postgres-crud
```

### 2. Create environment file

```bash
cp .env.example .env
```

`.env.example`:
```env
DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/mydb
```

### 3. Start PostgreSQL with Docker

```bash
docker compose up postgres -d
```

### 4. Create virtual environment & install dependencies

```bash
python -m venv venv
source venv/Scripts/activate   # Windows
# source venv/bin/activate     # Linux/Mac

pip install -r requirements.txt
```

### 5. Run the development server

```bash
uvicorn app.main:app --reload
```

API will be available at: `http://127.0.0.1:8000`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/items` | Get all items |
| `GET` | `/items/{id}` | Get item by ID |
| `POST` | `/items` | Create new item |
| `PUT` | `/items/{id}` | Update item |
| `DELETE` | `/items/{id}` | Delete item |

## Interactive API Docs

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Run with Docker (full stack)

```bash
docker compose up -d
```

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+psycopg://postgres:password@postgres:5432/mydb` |

## License

MIT