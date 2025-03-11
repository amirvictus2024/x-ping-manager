"""
کیبوردهای مخصوص پیام خوش‌آمدگویی
Welcome message keyboard utilities
"""
import json
import logging
from telegram import InlineKeyboardButton

logger = logging.getLogger(__name__)

def create_welcome_management_keyboard():
    """Create keyboard for welcome message management"""
    keyboard = [
        # Create/Edit Welcome
        [
            InlineKeyboardButton(
                "✏️ ایجاد/ویرایش پیام خوش‌آمد",
                callback_data=json.dumps({"action": "create_edit_welcome"})
            ),
        ],
        # Welcome Settings
        [
            InlineKeyboardButton(
                "⚙️ تنظیمات خوش‌آمدگویی",
                callback_data=json.dumps({"action": "welcome_settings"})
            ),
        ],
        # Welcome Templates
        [
            InlineKeyboardButton(
                "📝 قالب‌های آماده",
                callback_data=json.dumps({"action": "welcome_templates"})
            ),
        ],
        # Media in Welcome
        [
            InlineKeyboardButton(
                "🖼️ تصویر/ویدیو",
                callback_data=json.dumps({"action": "welcome_media"})
            ),
            InlineKeyboardButton(
                "🔗 دکمه‌های لینک دار",
                callback_data=json.dumps({"action": "welcome_buttons"})
            ),
        ],
        # Statistics
        [
            InlineKeyboardButton(
                "📊 آمار عضوگیری",
                callback_data=json.dumps({"action": "welcome_stats"})
            ),
        ],
        # Back Button
        [
            InlineKeyboardButton(
                "🔙 بازگشت به منوی اصلی",
                callback_data=json.dumps({"action": "main_menu"})
            ),
        ],
    ]
    return keyboard

def create_welcome_templates_keyboard():
    """Create keyboard for welcome templates"""
    keyboard = [
        # Simple Welcome
        [
            InlineKeyboardButton(
                "👋 خوش‌آمدگویی ساده",
                callback_data=json.dumps({"action": "welcome_template_simple"})
            ),
        ],
        # Group Rules
        [
            InlineKeyboardButton(
                "📜 قوانین گروه",
                callback_data=json.dumps({"action": "welcome_template_rules"})
            ),
        ],
        # Group Info
        [
            InlineKeyboardButton(
                "ℹ️ اطلاعات گروه",
                callback_data=json.dumps({"action": "welcome_template_info"})
            ),
        ],
        # Interactive Welcome
        [
            InlineKeyboardButton(
                "🎮 خوش‌آمدگویی تعاملی",
                callback_data=json.dumps({"action": "welcome_template_interactive"})
            ),
        ],
        # Professional Welcome
        [
            InlineKeyboardButton(
                "🌟 خوش‌آمدگویی حرفه‌ای",
                callback_data=json.dumps({"action": "welcome_template_professional"})
            ),
        ],
        # Custom Template
        [
            InlineKeyboardButton(
                "✏️ قالب سفارشی",
                callback_data=json.dumps({"action": "welcome_template_custom"})
            ),
        ],
        # Back Button
        [
            InlineKeyboardButton(
                "🔙 بازگشت به مدیریت خوش‌آمدگویی",
                callback_data=json.dumps({"action": "back_to_welcome_management"})
            ),
        ],
    ]
    return keyboard

def create_welcome_settings_keyboard():
    """Create keyboard for welcome message settings"""
    keyboard = [
        # Auto Delete
        [
            InlineKeyboardButton(
                "🗑️ حذف خودکار",
                callback_data=json.dumps({"action": "welcome_setting_auto_delete"})
            ),
        ],
        # User Tags
        [
            InlineKeyboardButton(
                "🏷️ نمایش نام‌کاربری",
                callback_data=json.dumps({"action": "welcome_setting_user_tags"})
            ),
        ],
        # Media Options
        [
            InlineKeyboardButton(
                "🖼️ تنظیمات رسانه",
                callback_data=json.dumps({"action": "welcome_setting_media"})
            ),
        ],
        # Welcome Delay
        [
            InlineKeyboardButton(
                "⏱️ تاخیر پیام خوش‌آمد",
                callback_data=json.dumps({"action": "welcome_setting_delay"})
            ),
        ],
        # Captcha Verification
        [
            InlineKeyboardButton(
                "🔐 تأیید هویت کاربر",
                callback_data=json.dumps({"action": "welcome_setting_captcha"})
            ),
        ],
        # Back Button
        [
            InlineKeyboardButton(
                "🔙 بازگشت به مدیریت خوش‌آمدگویی",
                callback_data=json.dumps({"action": "back_to_welcome_management"})
            ),
        ],
    ]
    return keyboard

def create_welcome_buttons_keyboard():
    """Create keyboard for adding buttons to welcome messages"""
    keyboard = [
        # Add Button
        [
            InlineKeyboardButton(
                "➕ افزودن دکمه",
                callback_data=json.dumps({"action": "welcome_add_button"})
            ),
        ],
        # Button Types
        [
            InlineKeyboardButton(
                "🔗 دکمه لینک",
                callback_data=json.dumps({"action": "welcome_button_url"})
            ),
            InlineKeyboardButton(
                "📱 دکمه داخلی",
                callback_data=json.dumps({"action": "welcome_button_callback"})
            ),
        ],
        # Edit Existing Buttons
        [
            InlineKeyboardButton(
                "✏️ ویرایش دکمه‌ها",
                callback_data=json.dumps({"action": "welcome_edit_buttons"})
            ),
        ],
        # Button Layout
        [
            InlineKeyboardButton(
                "🎨 چیدمان دکمه‌ها",
                callback_data=json.dumps({"action": "welcome_button_layout"})
            ),
        ],
        # Back Button
        [
            InlineKeyboardButton(
                "🔙 بازگشت به مدیریت خوش‌آمدگویی",
                callback_data=json.dumps({"action": "back_to_welcome_management"})
            ),
        ],
    ]
    return keyboard

def create_group_welcome_keyboard(groups, action_prefix="set_welcome"):
    """Create a keyboard to select groups for welcome messages"""
    keyboard = []
    
    for group_id, group_name in groups.items():
        # Check if it's a username (starts with @) or a numeric ID
        if group_id.startswith('@'):
            group_id_value = group_id  # Keep username as string
        else:
            try:
                group_id_value = int(group_id)  # Convert numeric ID to int
            except ValueError:
                group_id_value = group_id  # Keep as string if conversion fails
        
        keyboard.append([
            InlineKeyboardButton(
                f"👥 {group_name}",
                callback_data=json.dumps({
                    "action": action_prefix,
                    "id": group_id_value,
                    "type": "group"
                })
            )
        ])
    
    # Back Button
    keyboard.append([
        InlineKeyboardButton(
            "🔙 بازگشت به مدیریت خوش‌آمدگویی",
            callback_data=json.dumps({"action": "back_to_welcome_management"})
        )
    ])
    
    return keyboard