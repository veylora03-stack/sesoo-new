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