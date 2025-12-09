# Wallet Service - Paystack Integration

A FastAPI-based wallet service with Paystack integration, Google OAuth authentication, and API key management.

## Setup

1. Create virtual environment:
```bash
uv venv
.venv\Scripts\activate
```

2. Install dependencies:
```bash
uv pip install -e ".[dev]"
```

3. Set up environment variables (copy .env.example to .env):
```bash
cp .env.example .env
```

4. Run database migrations:
```bash
alembic upgrade head
```

5. Start the server:
```bash
uvicorn app.main:app --reload
```

## Environment Variables

See `.env.example` for required configuration.

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
