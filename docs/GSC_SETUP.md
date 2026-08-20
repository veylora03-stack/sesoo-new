# راهنمای اتصال به Google Search Console

1. **ساخت Property**
   وارد Google Search Console شوید و یک Property جدید بسازید.
2. **انتخاب نوع Property**
   می‌توانید از URL prefix (مثل `https://example.com`) یا Domain استفاده کنید.
3. **دریافت متا تگ**
   در بخش Verification، گزینه HTML tag را انتخاب کرده و کد را کپی کنید.
4. **وارد کردن در پنل ادمین**
   به پنل ادمین تبریز سایت بروید. مدل `SiteSettings` را باز کنید و مقدار کد را در فیلد `google_search_console_verification` قرار دهید و ذخیره کنید.
5. **بررسی فایل‌ها**
   مطمئن شوید که `/robots.txt` و `/sitemap.xml` بدون خطا و با کد 200 در دسترس هستند.
6. **ثبت Sitemap**
   در Search Console، به بخش Sitemaps رفته و آدرس `sitemap.xml` را ثبت کنید.
7. **بررسی Coverage**
   در بخش Pages یا Coverage، وضعیت ایندکس شدن صفحات را بررسی کنید.
8. **درخواست Index**
   برای صفحات اصلی (مثل صفحه اصلی، خدمات، تماس) از ابزار URL Inspection برای درخواست ایندکس دستی استفاده کنید.
9. **بررسی ایندکس نشدن صفحات داخلی**
   مطمئن شوید که صفحات `/admin/` و `/styleguide/` در نتایج گوگل ظاهر نمی‌شوند (به دلیل تنظیمات robots.txt و noindex).