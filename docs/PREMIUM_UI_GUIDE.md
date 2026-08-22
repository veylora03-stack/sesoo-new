# راهنمای رابط کاربری Premium Sesoo

## پالت رنگی
- **Primary (اصلی):** #0891B2 (آبی فیروزه‌ای)
- **Primary Dark:** #0E7490
- **Primary Deep:** #155E75
- **Primary Light:** #E0F7FA
- **Turquoise (تاکیدی روشن):** #22D3EE
- **Secondary (ثانویه / تیره):** #0F172A
- **Accent (طلایی/نارنجی):** #F59E0B
- **Surface:** #F7FBFC

## فونت‌ها
- **متن بدنه:** Vazirmatn (وزن 400 و 700)
- **عنوان‌های نمایشی:** Lalezar (وزن 400)
- **Fallback:** Estedad, Tahoma, Arial, sans-serif

### نحوه اضافه کردن فونت دستی
فایل‌های فونت باید در مسیر `static/fonts/` قرار گیرند:
1. Vazirmatn-Regular.woff2
2. Vazirmatn-Bold.woff2
3. Lalezar-Regular.woff2

## تصاویر و لوگو
- **لوگو:** `static/images/logo-placeholder.svg`
- **فاویکون:** `static/images/favicon.svg`
- **تصویر Hero:** `static/images/hero-illustration.svg` (قابل جایگزینی با عکس واقعی از پنل ادمین)

## کامپوننت‌ها
- **دکمه‌ها:** `.btn`, `.btn-primary`, `.btn-outline`, `.btn-light`, `.btn-sm`, `.btn-lg`
- **کارت‌ها:** `.card`, `.card-icon`, `.card-title`, `.card-text`
- **نشان‌ها:** `.badge`, `.badge-accent`, `.hero-badge`
- **ساختار:** `.hero`, `.section`, `.section-alt`, `.section-dark`, `.section-head`, `.container`, `.grid`
- **ناوبری:** `.site-header`, `.is-scrolled`, `.navbar`, `.site-nav`, `.menu-toggle`, `.top-bar`
- **فوتر:** `.site-footer`, `.footer-grid`, `.footer-bottom`
- **فرم‌ها:** `.input`, `.textarea`, `.select`, `.label`, `.alert-error`
- **سوالات:** `.faq-list`, `.faq-item`, `.faq-question`, `.faq-answer`

## انیمیشن‌ها
برای فعال‌سازی انیمیشن ورودی، از اتریبیوت `data-animate` روی المان‌ها استفاده کنید.
برای تاخیر در انیمیشن، از `data-delay="100"` (به میلی‌ثانیه) استفاده کنید.
اسکریپت `premium.js` به صورت خودکار با `IntersectionObserver` المان‌ها را هنگام ورود به viewport شناسایی کرده و کلاس `is-visible` را اضافه می‌کند.

## Accessibility
- رعایت `prefers-reduced-motion` برای غیرفعال کردن انیمیشن‌ها در صورت درخواست کاربر.
- کنتراست رنگ‌ها بر اساس استانداردهای WCAG.
- پشتیبانی از `focus-visible` برای کیبورد.

## Responsive
- گریدها در موبایل به صورت تک‌ستونه نمایش داده می‌شوند.
- منوی ناوبری در موبایل به صورت Drawer از سمت راست باز می‌شود.
- Top bar در موبایل مخفی می‌شود تا فضا بهینه‌تر شود.