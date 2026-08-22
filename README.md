# Sesoo

Django-based web platform for web design services, portfolio showcase, and lead management.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Features

### For Visitors
- Home page with service introduction
- Services pages (web design, SEO)
- Portfolio with category filtering
- Blog with search and categories
- Contact form with strong validation
- FAQ section
- About page

### For Admins
- Full admin panel
- Lead management with workflow (new → contacted → won/lost)
- CKEditor 5 with image upload
- Portfolio and blog management
- SEO settings (sitemap, robots, schema)

### Security
- IP-based rate limiting for forms
- Honeypot anti-spam
- CSRF/XSS protection
- HSTS and Secure Cookies
- django-axes brute-force protection
- Caddy security headers

### Performance
- Redis caching (mandatory in production)
- PostgreSQL (mandatory in production)
- Gunicorn with multiple workers
- Caddy reverse proxy with auto SSL
- Health check endpoint
- Automated backup scripts

## Setup

### Prerequisites
- Python 3.10+
- Docker & Docker Compose
- PostgreSQL 14+
- Redis 6+

### Development (local)
```bash
git clone https://github.com/veylora03-stack/sesoo-new.git
cd sesoo-new
cp .env.example .env
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements/dev.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Production (deployment)
```bash
# 1. Copy env files
cp .env.production.example .env.production
cp .env.production.example .env

# 2. Edit .env.production with real values:
#    SECRET_KEY, ALLOWED_HOSTS, DB_PASSWORD, POSTGRES_PASSWORD, SITE_DOMAIN, REDIS_URL

# 3. Edit .env with the same POSTGRES_PASSWORD and SITE_DOMAIN

# 4. Start the stack
docker compose up -d

# 5. Create admin user
docker compose exec web python manage.py createsuperuser
```

**Important:** Production requires Redis and PostgreSQL. SQLite is not supported.

### Environment Files
- `.env.production` — Django environment variables (loaded by containers via `env_file`)
- `.env` — Docker Compose interpolation variables (`POSTGRES_PASSWORD`, `SITE_DOMAIN`)

Both files must have matching values for `DB_PASSWORD`/`POSTGRES_PASSWORD`.

## Project Structure

```
.
├── apps/              # Django apps
│   ├── core/         # Core models, views, middleware
│   ├── leads/        # Contact form and lead management
│   ├── services/     # Services pages
│   ├── portfolio/    # Portfolio projects
│   ├── blog/         # Blog posts
│   └── pages/        # Static pages
├── config/           # Django settings
├── templates/        # HTML templates
├── static/           # CSS, JS, images
├── deploy/           # Deployment scripts
└── tests/            # Test suite
```

## Testing

```bash
python manage.py test
```

## Monitoring

- Health check: `/healthz/`
- Detailed health (staff only): `/healthz/detailed/`
- Sentry integration (optional)

## Security

- `SECRET_KEY`: Required in production
- `ALLOWED_HOSTS`: Required in production
- `DEBUG=False` in production
- Redis and PostgreSQL are mandatory in production
- HTTPS required (Caddy handles SSL automatically)
- `/test-error/` returns 403 in production

## Backup & Restore

```bash
# Backup (runs daily via cron)
bash deploy/backup.sh

# Restore
bash deploy/restore.sh /path/to/backup.tar.gz
```

## CI/CD

GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every push:
- Django checks
- Migrations
- Test suite (275 tests)
- Docker Compose validation
- Docker image build

## License

MIT License
