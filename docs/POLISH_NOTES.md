# یادداشت‌های فاز 14 Polish - اصلاحات چیدمان و جلوه‌های بصری

## بخش A: اصلاحات چیدمان (Layout QA)

### 1. جلوگیری از اسکرول افقی
- `overflow-x: hidden` روی html و body
- تمام المان‌های تزئینی (blob, particle, hero-chip) دارای `pointer-events: none` و `z-index: 0`
- محتوای اصلی همیشه در `z-index: 1` یا بالاتر

### 2. لایه‌بندی Hero بدون برخورد
- Hero دارای `overflow: hidden` و `isolation: isolate`
- Grid دو ستونه با gap حداقل 48px
- Hero chips فقط در عرض >=1200px به صورت absolute
- در عرض <1200px chips به صورت flex wrap زیر تصویر
- در موبایل (<992px) hero تک‌ستونه با تصویر بعد از متن

### 3. فونت Lalezar بدون بریدگی
- `line-height: 1.5` برای تمام عنوان‌ها
- `padding-bottom: 0.12em` برای جلوگیری از بریدگی دنباله حروف
- `overflow: visible` برای hero-title و section-title

### 4. فاصله‌گذاری منظم
- سیستم فاصله با متغیرهای CSS (--space-xs تا --space-2xl)
- Section padding: 64px دسکتاپ، 48px موبایل
- Grid gap: 24px دسکتاپ، 16px موبایل
- Card padding: 32px/24px دسکتاپ، 24px/16px موبایل
- حذف تمام marginهای منفی که باعث روی هم افتادن می‌شوند

### 5. Trust bar و Marquee بدون سرریز
- Trust bar با `flex-wrap` و `gap` مناسب
- در موبایل به grid دو ستونه تبدیل می‌شود
- Marquee دارای `overflow: hidden` و mask fade دو طرفه

### 6. کارت‌ها و متن‌ها
- `word-wrap: break-word` برای متن‌های بلند
- تصاویر با `width: 100%` و `aspect-ratio: 16/10`
- هیچ عنوان یا متنی absolute نیست

### 7. تایم‌لاین فرآیند
- دسکتاپ: خط افقی با ::before و nodeهای دایره‌ای
- موبایل: عمودی با padding-right برای خط
- هیچ متنی روی خط نمی‌افتد

### 8. CTA و فوتر
- CTA دارای `overflow: hidden` و pattern با z-index پایین‌تر
- Footer grid در موبایل تک‌ستونه با gap مناسب

### 9. فرم‌ها
- تمام input/textarea/select دارای `width: 100%` و `box-sizing: border-box`
- هیچ فرمی از container بیرون نمی‌زند

## بخش B: جلوه‌های بصری (Visual Enhancements)

### 1. بک‌گراند زنده Hero
- **Aurora/Mesh Gradient**: چند radial-gradient متحرک با انیمیشن 25 ثانیه‌ای
- **Dot Grid**: شبکه نقطه‌ای ظریف با فاصله 24px
- **Noise Layer**: بافت noise بسیار ظریف (opacity 0.03) با SVG feTurbulence

### 2. ذرات شناور
- سه ذره دایره‌ای با اندازه‌ها و رنگ‌های مختلف
- انیمیشن float 20 ثانیه‌ای با delay متفاوت
- حرکت در مسیرهای مختلف برای حس طبیعی

### 3. نوار پیشرفت اسکرول
- نوار gradient (primary -> teal) در بالای صفحه
- با اسکرول پر می‌شود
- z-index: 9999 برای همیشه در بالا بودن

### 4. دکمه بازگشت به بالا
- دکمه دایره‌ای در پایین-چپ (RTL)
- بعد از 400px اسکرول نمایان می‌شود
- Smooth scroll به بالا با کلیک
- Hover با translateY و سایه بیشتر

### 5. Micro-interactions
- **دکمه‌ها**: افکت shine sweep روی hover با ::after
- **کارت‌ها**: translateY(-4px) + rotate(0.5deg) + سایه رنگی
- **لینک‌های منو**: underline gradient که از راست باز می‌شود
- **آیکون کارت‌ها**: scale(1.1) روی hover کارت

### 6. جزئیات برند
- **::selection**: رنگ primary-light برای متن انتخاب شده
- **Custom Scrollbar**: باریک (10px) با thumb gradient
- **Focus Visible**: outline 3px cyan برای تمام المان‌های تعاملی

### 7. احترام به حرکت
- تمام انیمیشن‌های جدید داخل `@media (prefers-reduced-motion: no-preference)`
- در صورت فعال بودن prefers-reduced-motion، همه انیمیشن‌ها غیرفعال می‌شوند
- Back to top در حالت reduced-motion بدون smooth scroll کار می‌کند

## نکات فنی

### سازگاری
- کاملاً با تست‌های قبلی سازگار است
- هیچ کلاس یا المنتی که تست‌ها به آن وابسته‌اند حذف نشده
- تمام المان‌های تزئینی pointer-events: none دارند
- هیچ اسکرول افقی‌ای ایجاد نمی‌شود

### Performance
- انیمیشن‌ها با transform و opacity (GPU-accelerated)
- Intersection Observer برای lazy animation
- هیچ کتابخانه خارجی استفاده نشده
- تمام SVGها inline هستند

### Accessibility
- تمام انیمیشن‌ها respects prefers-reduced-motion
- Focus visible واضح برای keyboard navigation
- ARIA labels برای دکمه back-to-top
- Scroll progress دارای aria-hidden="true"

### Responsive
- Hero chips در موبایل از absolute به static تبدیل می‌شوند
- Trust bar در موبایل grid دو ستونه می‌شود
- Process timeline در موبایل عمودی می‌شود
- Footer grid در موبایل تک‌ستونه می‌شود

## فایل‌های تغییر یافته

1. `static/css/polish.css` - لایه جدید با اصلاحات و جلوه‌ها
2. `static/js/premium.js` - افزودن scroll-progress و back-to-top
3. `templates/base.html` - افزودن polish.css، scroll-progress و back-to-top

## نحوه استفاده

پس از اجرای این فاز:
1. تمام صفحات بدون اسکرول افقی و برخورد المان‌ها هستند
2. Hero دارای عمق بصری بیشتر با aurora gradient و ذرات شناور است
3. نوار پیشرفت اسکرول در بالای صفحه دیده می‌شود
4. دکمه بازگشت به بالا بعد از اسکرول ظاهر می‌شود
5. تمام micro-interactions در hover فعال هستند
6. سایت کاملاً accessible و respectful به prefers-reduced-motion است