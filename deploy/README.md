# راهنمای استقرار تبریز سایت

## مراحل استقرار با Docker

1. **نصب Docker و Docker Compose**
   مطمئن شوید که Docker و Docker Compose روی سرور نصب هستند.

2. **تنظیم متغیرهای محیطی**
   فایل `.env.production.example` را به `.env.production` کپی کنید:
   ```bash
   cp .env.production.example .env.production
   ```

3. **ویرایش `.env.production`**
   مقادیر `SECRET_KEY`، `ALLOWED_HOSTS`، `DB_PASSWORD` و سایر متغیرها را با مقادیر امن و واقعی جایگزین کنید.

4. **ساخت ایمیج‌ها**
   ```bash
   docker compose build
   ```

5. **راه‌اندازی سرویس‌ها**
   ```bash
   docker compose up -d
   ```

6. **ساخت کاربر ادمین**
   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

7. **بررسی سایت**
   آدرس `http://domain/` را در مرورگر باز کنید.

8. **فعال‌سازی SSL**
   برای فعال‌سازی HTTPS، می‌توانید از reverse proxy (مثل Nginx اصلی سرور یا Traefik) یا Certbot استفاده کنید. تنظیمات SSL در فایل `tabrizsite.conf` کامنت شده‌اند.

9. **بکاپ‌گیری**
   به صورت دوره‌ای از دیتابیس (volume `postgres_data`) و فایل‌های media (volume `media_data`) بکاپ تهیه کنید.

10. **چک‌لیست امنیتی**
    قبل از تحویل نهایی، فایل `DEPLOYMENT_CHECKLIST.md` را بررسی کنید.
## Migrations (Phase 31)

- Migration ها حالا به‌صورت خودکار قبل از startup اجرا می‌شوند: سرویس جداگانه `migrate` در docker-compose.yml فقط یک‌بار اجرا می‌شود (`restart: "no"`) و سرویس `web` با `condition: service_completed_successfully` منتظر آن می‌ماند؛ سرویس `db` نیز healthcheck دارد.
- برای اجرای دستی migration در production:
  `./deploy/run-migrations.sh`
## Sentry Error Monitoring

1. برای ساخت اکانت Sentry به [sentry.io](https://sentry.io) مراجعه کنید.
2. یک پروژه جدید Django بسازید و DSN آن را کپی کنید.
3. مقدار `SENTRY_DSN` را در فایل `.env.production` تنظیم کنید.
   اگر این متغیر خالی باشد، Sentry غیرفعال می‌ماند.
