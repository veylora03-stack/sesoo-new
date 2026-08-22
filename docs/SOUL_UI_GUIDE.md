# راهنمای رابط کاربری Soul Sesoo

## پالت رنگی
- **Primary (فیروزه‌ای):** #0891B2
- **Teal (سبزآبی):** #14B8A6
- **Cyan (روشن):** #22D3EE
- **Navy (سرمه‌ای تیره):** #0B1B33
- **Accent (نارنجی/هلویی):** #FB923C / #FDBA74
- **Background:** #F5FBFD
- **Surface:** #FFFFFF

## فونت‌ها
- **متن بدنه:** Vazirmatn
- **عنوان‌های نمایشی:** Lalezar
- **نحوه تعویض فونت:** فایل‌های فونت را در `static/fonts` قرار داده و در `fonts.css` آدرس‌دهی کنید.

## تصاویر و لوگو
- **لوگو:** `static/images/logo-placeholder.svg`
- **فاویکون:** `static/images/favicon.svg`
- **تصویر Hero:** `static/images/hero-illustration.svg` (قابل جایگزینی با عکس واقعی از پنل ادمین)

## کامپوننت‌ها
- **دکمه‌ها:** `.btn`, `.btn-primary` (گرادیانت), `.btn-outline`, `.btn-light`
- **کارت‌ها:** `.card` (با hover lift), `.card-icon` (گرادیانت)
- **عمق بصری:** `.blob` (لایه‌های محو پس‌زمینه), `.glass` (شیشه‌ای), `.wave-divider`
- **ساختار:** `.hero`, `.section`, `.section-alt`, `.container`, `.grid`
- **فرآیند:** `.process`, `.process-step`, `.process-node` (تایم‌لاین)
- **نمونه‌کار:** `.portfolio-card`, `.portfolio-overlay`
- **سوالات:** `.faq-list`, `.faq-item`

## انیمیشن‌ها
- اتریبیوت `data-animate` برای فعال‌سازی reveal پلکانی.
- اتریبیوت `data-delay="100"` برای تاخیر در انیمیشن.
- کلاس `.text-gradient` برای رنگ‌آمیزی گرادیانت متن.
- انیمیشن `floatY` برای المان‌های شناور مثل `.hero-chip`.
- رعایت `prefers-reduced-motion` برای غیرفعال کردن انیمیشن‌ها در صورت درخواست کاربر.

## Responsive
- گریدها در موبایل تک‌ستونه می‌شوند.
- تایم‌لاین فرآیند در موبایل عمودی می‌شود.
- منوی ناوبری در موبایل به صورت Drawer از سمت راست باز می‌شود.