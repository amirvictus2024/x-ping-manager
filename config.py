"""
Configuration settings for the Telegram Channel Management Bot
"""
import os
import json
from pathlib import Path

# Create data directory if it doesn't exist
data_dir = Path('data')
data_dir.mkdir(exist_ok=True)

# Default configuration
DEFAULT_CONFIG = {
    "admin_ids": [],  # List of admin Telegram IDs
    "channels": {},   # Dictionary of channels {id: name}
    "groups": {},     # Dictionary of groups {id: name}
    "welcome_messages": {},  # {group_id: welcome_message}
    "scheduled_messages": [],  # List of scheduled messages
    "auto_posts": []  # List of auto posts configurations
}

# Path to config file
CONFIG_FILE = data_dir / 'config.json'

def init_config():
    """Initialize configuration file if it doesn't exist"""
    if not CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        return DEFAULT_CONFIG
    
    # Load existing config
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # If file is corrupted, create a new one
        with open(CONFIG_FILE, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        return DEFAULT_CONFIG

def save_config(config):
    """Save configuration to file"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

# Bot settings
COMMAND_PREFIX = "/"
ADMIN_COMMANDS = [
    "start", "help", "addadmin", "addchannel", "delchannel", "channels", 
    "addgroup", "delgroup", "groups", "send", "schedule", 
    "schedulelist", "cancelschedule", "autopost", "autopostlist", 
    "delautopost", "welcome", "poll", "getmembers"
]

# Messages
MESSAGES = {
    "start": "👋 به ربات مدیریت کانال خوش آمدید!\nبرای دیدن دستورات موجود از /help استفاده کنید.",
    "help": "دستورات موجود:\n\n"
            "/addadmin - افزودن مدیر جدید\n"
            "/addchannel - افزودن کانال برای مدیریت\n"
            "نکته: می‌توانید کانال را با نام کاربری (@mychannel) یا شناسه عددی اضافه کنید\n"
            "/delchannel - حذف کانال\n"
            "/channels - نمایش کانال‌های مدیریت شده\n"
            "/addgroup - افزودن گروه برای مدیریت\n"
            "/delgroup - حذف گروه\n"
            "/groups - نمایش گروه‌های مدیریت شده\n"
            "/send - ارسال پیام به کانال/گروه\n"
            "/schedule - زمان‌بندی پیام\n"
            "/schedulelist - نمایش پیام‌های زمان‌بندی شده\n"
            "/cancelschedule - لغو پیام زمان‌بندی شده\n"
            "/autopost - تنظیم ارسال خودکار\n"
            "/autopostlist - نمایش پست‌های خودکار\n"
            "/delautopost - حذف پست خودکار\n"
            "/welcome - تنظیم پیام خوش‌آمدگویی برای گروه‌ها\n"
            "/poll - ایجاد نظرسنجی با دکمه‌های شیشه‌ای\n"
            "/getmembers - دریافت لیست اعضای کانال/گروه",
    "not_admin": "⛔ شما مجوز استفاده از این ربات را ندارید.",
    "channel_added": "✅ کانال با موفقیت اضافه شد!",
    "channel_removed": "✅ کانال با موفقیت حذف شد!",
    "group_added": "✅ گروه با موفقیت اضافه شد!",
    "group_removed": "✅ گروه با موفقیت حذف شد!",
    "no_channels": "هیچ کانالی توسط این ربات مدیریت نمی‌شود.",
    "no_groups": "هیچ گروهی توسط این ربات مدیریت نمی‌شود.",
    "welcome_set": "✅ پیام خوش‌آمدگویی برای این گروه تنظیم شد!",
    "scheduled": "✅ پیام زمان‌بندی شد!",
    "schedule_cancelled": "✅ پیام زمان‌بندی شده لغو شد!",
    "autopost_added": "✅ ارسال خودکار پیام تنظیم شد!",
    "autopost_removed": "✅ پست خودکار حذف شد!",
    "error": "❌ خطایی رخ داده است: {}"
}
