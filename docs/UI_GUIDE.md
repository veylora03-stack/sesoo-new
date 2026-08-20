# راهنمای رابط کاربری (UI Guide) تبریز سایت

## پالت رنگی
- **Primary (اصلی):** #1450A3
- **Primary Dark:** #0F3C7A
- **Primary Light:** #EAF2FD
- **Secondary (ثانویه):** #0B1220
- **Accent (تاکیدی):** #F7A400
- **Background:** #FFFFFF
- **Surface:** #F7F9FC
- **Text:** #111827
- **Muted:** #4B5563
- **Border:** #E5E7EB

## فونت‌ها
- **متن:** Vazirmatn (وزن 400 و 700)
- **عنوان‌های نمایشی:** Lalezar (وزن 400)
- **Fallback:** Estedad, Tahoma, Arial, sans-serif

### نحوه اضافه کردن فونت دستی
فایل‌های فونت باید در مسیر `static/fonts/` قرار گیرند:
1. Vazirmatn-Regular.woff2
2. Vazirmatn-Bold.woff2
3. Lalezar-Regular.woff2

## لوگو و فاویکون
- **لوگو:** `static/images/logo-placeholder.svg` (ابعاد پیشنهادی 180x48)
- **فاویکون:** `static/images/favicon.svg` (ابعاد 32x32)

## کامپوننت‌ها
- **دکمه‌ها:** `.btn`, `.btn-primary`, `.btn-outline`, `.btn-light`
- **کارت‌ها:** `.card`, `.card-icon`, `.card-title`, `.card-text`
- **نشان‌ها:** `.badge`, `.badge-accent`
- **ساختار:** `.hero`, `.section`, `.section-alt`, `.section-head`, `.container`, `.grid`
- **ناوبری:** `.site-header`, `.navbar`, `.site-nav`, `.menu-toggle`
- **فوتر:** `.site-footer`, `.footer-grid`, `.footer-bottom`
- **فرم‌ها:** `.input`, `.textarea`, `.select`, `.label`, `.alert-error`

## انیمیشن‌ها
برای فعال‌سازی انیمیشن ورودی، از اتریبیوت `data-animate` روی المان‌ها استفاده کنید.
اسکریپت `animations.js` به صورت خودکار با `IntersectionObserver` المان‌ها را هنگام ورود به viewport شناسایی کرده و کلاس `is-visible` را اضافه می‌کند.

## Accessibility
- رعایت `prefers-reduced-motion` برای غیرفعال کردن انیمیشن‌ها در صورت درخواست کاربر.
- کنتراست رنگ‌ها بر اساس استانداردهای WCAG.
- پشتیبانی از `focus-visible` برای کیبورد.

## Responsive
- گریدها در موبایل به صورت تک‌ستونه نمایش داده می‌شوند.
- منوی ناوبری در موبایل به صورت Drawer از سمت راست باز می‌شود.