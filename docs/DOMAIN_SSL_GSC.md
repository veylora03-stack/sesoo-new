# راهنمای استقرار، دامنه، SSL و سرچ کنسول

## 1. خرید دامنه و سرور
- دامنه `.ir` را از nic.ir یا دامنه `.com` را از رجیسترارهای بین‌المللی تهیه کنید.
- یک سرور مجازی (VPS) با سیستم عامل اوبونتو 22.04 و IP عمومی اجاره کنید.

## 2. تنظیمات DNS
- در پنل مدیریت دامنه، یک رکورد `A` برای `@` و یک رکورد `A` برای `www` بسازید و هر دو را به IP سرور VPS متصل کنید.

## 3. آماده‌سازی سرور
- با استفاده از SSH وارد سرور شوید.
- اسکریپت نصب داکر را اجرا کنید:
  ```bash
  bash deploy/vps-setup.sh
  ```

## 4. کلون و پیکربندی
- مخزن را کلون کنید: `git clone <repo_url>`
- فایل نمونه را کپی کنید: `cp .env.production.example .env.production`
- فایل `.env.production` را ویرایش کنید:
  - `SECRET_KEY` را با یک رشته قوی و تصادفی پر کنید.
  - `SITE_DOMAIN` را روی دامنه خود تنظیم کنید (مثلاً `example.com`).
  - `ALLOWED_HOSTS` را با دامنه و www پر کنید (مثلاً `example.com,www.example.com`).
  - `DB_PASSWORD` را با یک رمز عبور قوی تنظیم کنید.

## 5. راه‌اندازی سرویس‌ها
- دستور زیر را اجرا کنید:
  ```bash
  docker compose up -d --build
  ```
- سپس یک کاربر ادمین بسازید:
  ```bash
  docker compose exec web python manage.py createsuperuser
  ```

## 6. گواهی SSL
- Caddy به‌صورت خودکار گواهی Let's Encrypt را دریافت و تمدید می‌کند.
- حدود 1 دقیقه پس از بالا آمدن سرویس‌ها، SSL فعال شده و سایت روی `https` در دسترس خواهد بود.

## 7. ثبت در گوگل سرچ کنسول (GSC)
- وارد Google Search Console شوید و یک Property جدید بسازید (URL prefix).
- روش `HTML tag` را انتخاب کرده و مقدار meta tag را کپی کنید.
- در پنل ادمین سایت، به بخش **تنظیمات سایت** (Site Settings) بروید و مقدار را در فیلد `google_search_console_verification` قرار دهید.
- در سرچ کنسول روی Verify کلیک کنید.
- در نهایت، نقشه سایت را ثبت کنید: `https://دامنه/sitemap.xml`

## 8. پشتیبان‌گیری (Backup)
- برای بکاپ از دیتابیس:
  ```bash
  docker compose exec -T db pg_dump -U sesoo_user sesoo_db > backup.sql
  ```
- برای بکاپ از فایل‌های مدیا، از volume مربوطه یا دایرکتوری media پشتیبان تهیه کنید.