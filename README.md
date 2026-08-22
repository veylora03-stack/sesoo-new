# تبریز سایت

پلتفرم حرفه‌ای طراحی سایت و سئو برای کسب‌وکارهای تبریز

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ امکانات

### 🎯 برای کاربران
- صفحه اصلی با معرفی خدمات
- صفحه خدمات (طراحی سایت، سئو)
- نمونه‌کارها با فیلتر دسته‌بندی
- وبلاگ با جستجو و دسته‌بندی
- فرم تماس با validation قوی
- سوالات متداول
- درباره ما

### 🔧 برای مدیران
- پنل مدیریت کامل
- مدیریت لیدها با workflow (new → contacted → won/lost)
- ویرایشگر CKEditor با آپلود تصویر
- مدیریت نمونه‌کارها و وبلاگ
- داشبورد آماری
- تنظیمات سئو (sitemap, robots, schema)

### 🛡️ امنیت
- Rate limiting برای فرم‌ها
- Honeypot ضد اسپم
- CSRF/XSS protection
- HSTS و Secure Cookies
- django-axes برای محافظت ادمین

### 🚀 Performance
- Redis caching
- PostgreSQL
- Gunicorn با multiple workers
- Caddy reverse proxy (with auto SSL)
- Health check endpoint
- Automated backups

## 📦 نصب و راه‌اندازی

### پیش‌نیازها
- Python 3.10+
- Docker & Docker Compose
- PostgreSQL 14+
- Redis 6+

### Development (محلی)
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

### Production (استقرار)
```bash
cp .env.production.example .env.production
# .env.production را ویرایش کنید (SECRET_KEY, ALLOWED_HOSTS, DB_PASSWORD)
docker compose up -d
docker compose exec web python manage.py createsuperuser
```

## 🏗️ ساختار پروژه

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

## 🧪 تست

```bash
python manage.py test
```

## 📊 Monitoring

- Health check: `/healthz/`
- Detailed health (staff only): `/healthz/detailed/`
- Sentry integration (optional)

## 🔒 امنیت

- SECRET_KEY: حتماً در production تغییر دهید
- ALLOWED_HOSTS: فقط دامنه‌های معتبر
- DEBUG=False در production
- HTTPS اجباری

## 📝 License

MIT License

## 👥 Contributors

- veylora03-stack

## 🤝 Support

برای support و سوالات:
- Email: info@tabrizsite.com
- Website: https://tabrizsite.com