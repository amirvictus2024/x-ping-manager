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
        # Channel Management Row
        [
            InlineKeyboardButton(
                "🔄 مدیریت کانال ها",
                callback_data=json.dumps({"action": "channel_management"})
            ),
        ],
        # Group Management Row
        [
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
                "🕒 زمان‌بندی پیام ها",
                callback_data=json.dumps({"action": "schedule_management"})
            ),
        ],
        # Auto Post Row
        [
            InlineKeyboardButton(
                "🔄 پست خودکار",
                callback_data=json.dumps({"action": "autopost_management"})
            ),
        ],
        # Other Features Row
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
        # Admin Row
        [
            InlineKeyboardButton(
                "👤 مدیریت ادمین ها",
                callback_data=json.dumps({"action": "admin_management"})
            ),
        ],
    ]
    return keyboard

def create_channel_management_keyboard():
    """Create keyboard for channel management options"""
    keyboard = [
        [
            InlineKeyboardButton(
                "➕ افزودن کانال",
                callback_data=json.dumps({"action": "add_channel"})
            ),
        ],
        [
            InlineKeyboardButton(
                "➖ حذف کانال",
                callback_data=json.dumps({"action": "remove_channel"})
            ),
        ],
        [
            InlineKeyboardButton(
                "📋 لیست کانال ها",
                callback_data=json.dumps({"action": "list_channels"})
            ),
        ],
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
        [
            InlineKeyboardButton(
                "➕ افزودن گروه",
                callback_data=json.dumps({"action": "add_group"})
            ),
        ],
        [
            InlineKeyboardButton(
                "➖ حذف گروه",
                callback_data=json.dumps({"action": "remove_group"})
            ),
        ],
        [
            InlineKeyboardButton(
                "📋 لیست گروه ها",
                callback_data=json.dumps({"action": "list_groups"})
            ),
        ],
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
        [
            InlineKeyboardButton(
                "➕ زمان‌بندی پیام جدید",
                callback_data=json.dumps({"action": "new_schedule"})
            ),
        ],
        [
            InlineKeyboardButton(
                "📋 لیست پیام های زمان‌بندی شده",
                callback_data=json.dumps({"action": "schedule_list"})
            ),
        ],
        [
            InlineKeyboardButton(
                "➖ لغو زمان‌بندی",
                callback_data=json.dumps({"action": "cancel_schedule"})
            ),
        ],
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
        [
            InlineKeyboardButton(
                "➕ تنظیم پست خودکار",
                callback_data=json.dumps({"action": "new_autopost"})
            ),
        ],
        [
            InlineKeyboardButton(
                "📋 لیست پست های خودکار",
                callback_data=json.dumps({"action": "autopost_list"})
            ),
        ],
        [
            InlineKeyboardButton(
                "➖ حذف پست خودکار",
                callback_data=json.dumps({"action": "delete_autopost"})
            ),
        ],
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
        [
            InlineKeyboardButton(
                "➕ افزودن ادمین",
                callback_data=json.dumps({"action": "add_admin"})
            ),
        ],
        [
            InlineKeyboardButton(
                "➖ حذف ادمین",
                callback_data=json.dumps({"action": "remove_admin"})
            ),
        ],
        [
            InlineKeyboardButton(
                "📋 لیست ادمین ها",
                callback_data=json.dumps({"action": "list_admins"})
            ),
        ],
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
