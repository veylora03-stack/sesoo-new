# Changelog

تمام تغییرات مهم این پروژه در این فایل ثبت می‌شود.

## [Unreleased]

### Added
- Sentry error monitoring (optional)
- Redis caching برای production
- Health check کامل (database + cache)
- Automated backup system
- README حرفه‌ای

### Changed
- Migration به service جدا در Docker
- حذف nginx و استفاده از Caddy

### Fixed
- لینک‌های تکراری CSS
- مسیرهای سخت‌کد static

## [1.0.0] - 2026-08-21

### Added
- MVP کامل: صفحه اصلی، خدمات، نمونه‌کارها، وبلاگ، تماس
- سیستم لید با UTM tracking و validation
- پنل مدیریت با CKEditor
- داشبورد آماری
- سئو کامل (sitemap, robots, schema)
- امنیت (axes, rate limiting, honeypot)
- Docker + Caddy برای استقرار
- 28 فاز توسعه با تست جامع