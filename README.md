# Deheus Django API

Multi-tenant CRM API built with Django REST Framework.

## Setup

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Environment Variables

Copy `.env.example` to `.env` and fill in:
```bash
cp .env.example .env
```

## API Endpoints

- **Admin**: `/admin/`
- **Auth**: `/api/auth/login`, `/api/auth/refresh`, `/api/auth/logout`, `/api/auth/forgot-password`, `/api/auth/reset-password`, `/api/auth/me`
- **Health**: `/health/`
- **API root**: `/api/`
- **Swagger docs**: `/api/docs/swagger/`
- **ReDoc**: `/api/docs/redoc/`
- **Schema**: `/api/schema/`

## Deployment

```bash
bash deploy.sh
```

Or push to `joe` or `master` branch to trigger GitHub Actions auto-deploy.
