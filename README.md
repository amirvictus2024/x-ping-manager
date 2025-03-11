# ربات مدیریت کانال تلگرام

ربات پیشرفته مدیریت کانال تلگرام با قابلیت‌های زمان‌بندی، دکمه‌های شیشه‌ای، و پشتیبانی از چند کانال همزمان.

## ویژگی‌ها

- رابط کاربری مبتنی بر دکمه‌های شیشه‌ای (Inline Keyboard)
- مدیریت چند کانال و گروه همزمان
- زمان‌بندی پیام‌ها برای ارسال در آینده
- قابلیت ارسال خودکار (اتوپست) در زمان‌های مشخص
- ایجاد پرسشنامه‌های تعاملی
- پیام خوش‌آمدگویی سفارشی برای گروه‌ها
- سیستم مدیریت ادمین‌ها

## پیش‌نیازها

- پایتون 3.9 یا بالاتر
- کتابخانه‌های مورد نیاز در فایل `_requirements.txt`
- توکن ربات تلگرام از BotFather

## راه‌اندازی

1. نصب کتابخانه‌های مورد نیاز:
   ```bash
   pip install -r _requirements.txt
   ```

2. تنظیم متغیر محیطی `TELEGRAM_BOT_TOKEN` با توکن ربات تلگرام
   ```bash
   export TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN"
   ```

3. اجرای ربات:
   ```bash
   python main.py
   ```

## استفاده از ربات

1. بعد از راه‌اندازی، دستور `/start` را به ربات بفرستید
2. منوی اصلی با دکمه‌های شیشه‌ای نمایش داده می‌شود
3. با انتخاب هر گزینه، عملیات مربوطه انجام می‌شود

## دستورات مدیر

- `/start` - شروع ربات و نمایش منوی اصلی
- `/help` - نمایش راهنما
- `/addadmin` - اضافه کردن مدیر جدید
- و سایر دستورات مربوط به مدیریت کانال‌ها و گروه‌ها

## قابلیت‌های مبتنی بر دکمه‌های شیشه‌ای

تمام قابلیت‌های اصلی ربات از طریق دکمه‌های شیشه‌ای (Inline Keyboard) قابل دسترسی هستند، از جمله:

- مدیریت کانال‌ها و گروه‌ها
- ارسال پیام
- زمان‌بندی پیام‌ها
- تنظیم ارسال خودکار
- مدیریت ادمین‌ها
- و بسیاری قابلیت‌های دیگر