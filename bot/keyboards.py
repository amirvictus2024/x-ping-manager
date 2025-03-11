"""
Keyboard utility functions for creating inline keyboards
"""
import json
import logging
from telegram import InlineKeyboardButton

logger = logging.getLogger(__name__)

def create_main_menu_keyboard():
    """Create the main menu keyboard with all admin functions"""
    keyboard = [
        # Channel & Group Management Row (grouped together)
        [
            InlineKeyboardButton(
                "📢 مدیریت کانال ها",
                callback_data=json.dumps({"action": "channel_management"})
            ),
            InlineKeyboardButton(
                "👥 مدیریت گروه ها",
                callback_data=json.dumps({"action": "group_management"})
            ),
        ],
        # Message Management Row
        [
            InlineKeyboardButton(
                "📨 ارسال پیام",
                callback_data=json.dumps({"action": "send_message"})
            ),
        ],
        # Scheduling Row
        [
            InlineKeyboardButton(
                "🕒 زمان‌بندی پیام",
                callback_data=json.dumps({"action": "schedule_management"})
            ),
            InlineKeyboardButton(
                "🔄 پست خودکار",
                callback_data=json.dumps({"action": "autopost_management"})
            ),
        ],
        # Interactive Features Row
        [
            InlineKeyboardButton(
                "📊 نظرسنجی",
                callback_data=json.dumps({"action": "create_poll"})
            ),
            InlineKeyboardButton(
                "👋 پیام خوش‌آمد",
                callback_data=json.dumps({"action": "welcome_message"})
            ),
        ],
        # Statistics & Reports Row
        [
            InlineKeyboardButton(
                "📈 آمار و گزارش",
                callback_data=json.dumps({"action": "stats_reports"})
            ),
        ],
        # Admin Row
        [
            InlineKeyboardButton(
                "👤 مدیریت ادمین ها",
                callback_data=json.dumps({"action": "admin_management"})
            ),
            InlineKeyboardButton(
                "⚙️ تنظیمات",
                callback_data=json.dumps({"action": "settings"})
            ),
        ],
    ]
    return keyboard

def create_channel_management_keyboard():
    """Create keyboard for channel management options"""
    keyboard = [
        # Add/Remove Channel Row
        [
            InlineKeyboardButton(
                "➕ افزودن کانال",
                callback_data=json.dumps({"action": "add_channel"})
            ),
            InlineKeyboardButton(
                "➖ حذف کانال",
                callback_data=json.dumps({"action": "remove_channel"})
            ),
        ],
        # List Channels
        [
            InlineKeyboardButton(
                "📋 لیست کانال ها",
                callback_data=json.dumps({"action": "list_channels"})
            ),
        ],
        # Channel Statistics
        [
            InlineKeyboardButton(
                "📊 آمار کانال",
                callback_data=json.dumps({"action": "channel_stats"})
            ),
        ],
        # Advanced Channel Settings
        [
            InlineKeyboardButton(
                "🎨 قالب پست کانال",
                callback_data=json.dumps({"action": "channel_post_template"})
            ),
            InlineKeyboardButton(
                "🔗 پیوند کانال‌ها",
                callback_data=json.dumps({"action": "link_channels"})
            ),
        ],
        # Member Management
        [
            InlineKeyboardButton(
                "👥 مدیریت اعضا",
                callback_data=json.dumps({"action": "channel_members"})
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

def create_group_management_keyboard():
    """Create keyboard for group management options"""
    keyboard = [
        # Add/Remove Group Row
        [
            InlineKeyboardButton(
                "➕ افزودن گروه",
                callback_data=json.dumps({"action": "add_group"})
            ),
            InlineKeyboardButton(
                "➖ حذف گروه",
                callback_data=json.dumps({"action": "remove_group"})
            ),
        ],
        # List Groups
        [
            InlineKeyboardButton(
                "📋 لیست گروه ها",
                callback_data=json.dumps({"action": "list_groups"})
            ),
        ],
        # Group Admin Management
        [
            InlineKeyboardButton(
                "👮 مدیریت ادمین‌های گروه",
                callback_data=json.dumps({"action": "group_admins"})
            ),
        ],
        # Group Rules & Settings
        [
            InlineKeyboardButton(
                "📝 قوانین گروه",
                callback_data=json.dumps({"action": "group_rules"})
            ),
            InlineKeyboardButton(
                "⚙️ تنظیمات گروه",
                callback_data=json.dumps({"action": "group_settings"})
            ),
        ],
        # Member Management & Statistics
        [
            InlineKeyboardButton(
                "👥 مدیریت اعضا",
                callback_data=json.dumps({"action": "group_members"})
            ),
            InlineKeyboardButton(
                "📊 آمار گروه",
                callback_data=json.dumps({"action": "group_stats"})
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

def create_schedule_management_keyboard():
    """Create keyboard for scheduling options"""
    keyboard = [
        # Add New Schedule Row
        [
            InlineKeyboardButton(
                "➕ زمان‌بندی پیام جدید",
                callback_data=json.dumps({"action": "new_schedule"})
            ),
        ],
        # Schedule List & Cancel Row
        [
            InlineKeyboardButton(
                "📋 لیست پیام‌ها",
                callback_data=json.dumps({"action": "schedule_list"})
            ),
            InlineKeyboardButton(
                "➖ لغو زمان‌بندی",
                callback_data=json.dumps({"action": "cancel_schedule"})
            ),
        ],
        # Schedule Types Row
        [
            InlineKeyboardButton(
                "🕒 زمان دقیق",
                callback_data=json.dumps({"action": "schedule_exact_time"})
            ),
            InlineKeyboardButton(
                "⏰ با تاخیر",
                callback_data=json.dumps({"action": "schedule_with_delay"})
            ),
        ],
        # Schedule Templates Row
        [
            InlineKeyboardButton(
                "📝 قالب‌های زمان‌بندی",
                callback_data=json.dumps({"action": "schedule_templates"})
            ),
        ],
        # Schedule Calendar View Row
        [
            InlineKeyboardButton(
                "📅 نمای تقویم",
                callback_data=json.dumps({"action": "schedule_calendar_view"})
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

def create_autopost_management_keyboard():
    """Create keyboard for autopost options"""
    keyboard = [
        # Add New Autopost
        [
            InlineKeyboardButton(
                "➕ تنظیم پست خودکار",
                callback_data=json.dumps({"action": "new_autopost"})
            ),
        ],
        # List & Delete Row
        [
            InlineKeyboardButton(
                "📋 لیست پست‌ها",
                callback_data=json.dumps({"action": "autopost_list"})
            ),
            InlineKeyboardButton(
                "➖ حذف پست خودکار",
                callback_data=json.dumps({"action": "delete_autopost"})
            ),
        ],
        # Autopost Types Row
        [
            InlineKeyboardButton(
                "🔄 روزانه",
                callback_data=json.dumps({"action": "daily_autopost"})
            ),
            InlineKeyboardButton(
                "📅 هفتگی",
                callback_data=json.dumps({"action": "weekly_autopost"})
            ),
        ],
        # Periodic Row
        [
            InlineKeyboardButton(
                "⏱️ ساعتی",
                callback_data=json.dumps({"action": "hourly_autopost"})
            ),
            InlineKeyboardButton(
                "🔍 هوشمند",
                callback_data=json.dumps({"action": "smart_autopost"})
            ),
        ],
        # Autopost Templates
        [
            InlineKeyboardButton(
                "📝 قالب‌های پست خودکار",
                callback_data=json.dumps({"action": "autopost_templates"})
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

def create_admin_management_keyboard():
    """Create keyboard for admin management"""
    keyboard = [
        # Add/Remove Admin Row
        [
            InlineKeyboardButton(
                "➕ افزودن ادمین",
                callback_data=json.dumps({"action": "add_admin"})
            ),
            InlineKeyboardButton(
                "➖ حذف ادمین",
                callback_data=json.dumps({"action": "remove_admin"})
            ),
        ],
        # List Admins
        [
            InlineKeyboardButton(
                "📋 لیست ادمین ها",
                callback_data=json.dumps({"action": "list_admins"})
            ),
        ],
        # Admin Permissions
        [
            InlineKeyboardButton(
                "🔐 سطوح دسترسی",
                callback_data=json.dumps({"action": "admin_permissions"})
            ),
        ],
        # Activity Log
        [
            InlineKeyboardButton(
                "📊 آمار فعالیت‌ها",
                callback_data=json.dumps({"action": "admin_activity_log"})
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

def create_channels_keyboard(channels, action_prefix):
    """Create an inline keyboard with channel buttons"""
    keyboard = []
    
    for channel_id, channel_name in channels.items():
        # Check if it's a username (starts with @) or a numeric ID
        if channel_id.startswith('@'):
            channel_id_value = channel_id  # Keep username as string
        else:
            try:
                channel_id_value = int(channel_id)  # Convert numeric ID to int
            except ValueError:
                channel_id_value = channel_id  # Keep as string if conversion fails
        
        keyboard.append([
            InlineKeyboardButton(
                channel_name,
                callback_data=json.dumps({
                    "action": action_prefix,
                    "id": channel_id_value,
                    "type": "channel"
                })
            )
        ])
    
    return keyboard

def create_groups_keyboard(groups, action_prefix):
    """Create an inline keyboard with group buttons"""
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
                group_name,
                callback_data=json.dumps({
                    "action": action_prefix,
                    "id": group_id_value,
                    "type": "group"
                })
            )
        ])
    
    return keyboard

def create_schedule_keyboard(scheduled_messages, action_prefix="view"):
    """Create an inline keyboard with scheduled message buttons"""
    keyboard = []
    
    for message in scheduled_messages:
        target_type = message.get("target", {}).get("type", "unknown")
        target_id = message.get("target", {}).get("id", "unknown")
        scheduled_time = message.get("time", "unknown")
        
        # Create a display label
        if len(message.get("text", "")) > 20:
            text_preview = message["text"][:20] + "..."
        else:
            text_preview = message["text"]
        
        label = f"{scheduled_time} - {text_preview}"
        
        keyboard.append([
            InlineKeyboardButton(
                label,
                callback_data=json.dumps({
                    "action": f"{action_prefix}_schedule",
                    "id": message["id"]
                })
            )
        ])
    
    return keyboard

def create_autopost_keyboard(auto_posts, action_prefix="view"):
    """Create an inline keyboard with autopost buttons"""
    keyboard = []
    
    for post in auto_posts:
        target_type = post.get("target", {}).get("type", "unknown")
        target_id = post.get("target", {}).get("id", "unknown")
        
        # Create a display label based on the type
        if post["type"] == "daily":
            schedule_info = f"Daily at {post['hour']}:{post['minute']:02d}"
        elif post["type"] == "weekly":
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            day_name = days[post["day"]]
            schedule_info = f"{day_name} at {post['hour']}:{post['minute']:02d}"
        else:
            schedule_info = "Unknown schedule"
        
        # Text preview
        if len(post.get("text", "")) > 20:
            text_preview = post["text"][:20] + "..."
        else:
            text_preview = post["text"]
        
        label = f"{schedule_info} - {text_preview}"
        
        keyboard.append([
            InlineKeyboardButton(
                label,
                callback_data=json.dumps({
                    "action": f"{action_prefix}_autopost",
                    "id": post["id"]
                })
            )
        ])
    
    return keyboard

def build_inline_keyboard(buttons_data):
    """Build an inline keyboard from a list of button data"""
    keyboard = []
    
    for row_data in buttons_data:
        row = []
        
        # If it's already a list of buttons, process the row
        if isinstance(row_data, list):
            for button_data in row_data:
                button = create_button_from_data(button_data)
                if button:
                    row.append(button)
        # Otherwise treat it as a single button
        else:
            button = create_button_from_data(row_data)
            if button:
                row.append(button)
        
        if row:
            keyboard.append(row)
    
    return keyboard

def create_button_from_data(button_data):
    """Create an InlineKeyboardButton from button data"""
    try:
        if "url" in button_data:
            return InlineKeyboardButton(
                text=button_data["text"],
                url=button_data["url"]
            )
        elif "callback_data" in button_data:
            return InlineKeyboardButton(
                text=button_data["text"],
                callback_data=button_data["callback_data"]
            )
        else:
            logger.warning(f"Button is missing url or callback_data: {button_data}")
            return None
    except Exception as e:
        logger.error(f"Error creating button: {e}")
        return None

def create_poll_keyboard(poll_options, poll_id):
    """Create a keyboard for poll options"""
    keyboard = []
    row = []
    
    for i, option in enumerate(poll_options):
        row.append(
            InlineKeyboardButton(
                text=option["text"],
                callback_data=json.dumps({
                    "action": "poll_vote",
                    "poll_id": poll_id,
                    "option_id": i
                })
            )
        )
        
        # 2 buttons per row
        if len(row) == 2:
            keyboard.append(row)
            row = []
    
    # Add any remaining buttons
    if row:
        keyboard.append(row)
    
    return keyboard
