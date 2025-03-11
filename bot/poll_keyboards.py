"""
کیبوردهای مخصوص نظرسنجی ها
Poll-specific keyboard utilities
"""
import json
import logging
from telegram import InlineKeyboardButton

logger = logging.getLogger(__name__)

def create_poll_management_keyboard():
    """Create keyboard for poll management"""
    keyboard = [
        # Create New Poll
        [
            InlineKeyboardButton(
                "➕ ایجاد نظرسنجی جدید",
                callback_data=json.dumps({"action": "create_new_poll"})
            ),
        ],
        # Active and Past Polls
        [
            InlineKeyboardButton(
                "🔄 نظرسنجی‌های فعال",
                callback_data=json.dumps({"action": "active_polls"})
            ),
            InlineKeyboardButton(
                "📊 نظرسنجی‌های پایان یافته",
                callback_data=json.dumps({"action": "finished_polls"})
            ),
        ],
        # Poll Templates
        [
            InlineKeyboardButton(
                "📝 قالب‌های آماده",
                callback_data=json.dumps({"action": "poll_templates"})
            ),
        ],
        # Poll Settings
        [
            InlineKeyboardButton(
                "⚙️ تنظیمات نظرسنجی",
                callback_data=json.dumps({"action": "poll_settings"})
            ),
        ],
        # Poll Analytics
        [
            InlineKeyboardButton(
                "📈 تحلیل نظرسنجی‌ها",
                callback_data=json.dumps({"action": "poll_analytics"})
            ),
        ],
        # Back to Main Menu
        [
            InlineKeyboardButton(
                "🔙 بازگشت به منوی اصلی",
                callback_data=json.dumps({"action": "main_menu"})
            ),
        ],
    ]
    return keyboard

def create_poll_templates_keyboard():
    """Create keyboard for poll templates"""
    keyboard = [
        # Yes/No Template
        [
            InlineKeyboardButton(
                "👍 بله/خیر",
                callback_data=json.dumps({"action": "poll_template_yesno"})
            ),
        ],
        # Rating Template
        [
            InlineKeyboardButton(
                "⭐ امتیازدهی (1-5)",
                callback_data=json.dumps({"action": "poll_template_rating"})
            ),
        ],
        # Multiple Choice Template
        [
            InlineKeyboardButton(
                "🔢 چند گزینه‌ای",
                callback_data=json.dumps({"action": "poll_template_multiplechoice"})
            ),
        ],
        # Feedback Template
        [
            InlineKeyboardButton(
                "💬 نظرسنجی بازخورد",
                callback_data=json.dumps({"action": "poll_template_feedback"})
            ),
        ],
        # Custom Template
        [
            InlineKeyboardButton(
                "✏️ قالب سفارشی",
                callback_data=json.dumps({"action": "poll_template_custom"})
            ),
        ],
        # Back Button
        [
            InlineKeyboardButton(
                "🔙 بازگشت به مدیریت نظرسنجی",
                callback_data=json.dumps({"action": "back_to_poll_management"})
            ),
        ],
    ]
    return keyboard

def create_poll_target_keyboard(channels, groups):
    """Create keyboard for selecting poll target"""
    keyboard = []
    
    # Channels section
    if channels:
        keyboard.append([
            InlineKeyboardButton(
                "📢 کانال‌ها",
                callback_data=json.dumps({"action": "poll_target_channels"})
            )
        ])
        
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
                    f"📢 {channel_name}",
                    callback_data=json.dumps({
                        "action": "poll_target_select",
                        "id": channel_id_value,
                        "type": "channel"
                    })
                )
            ])
    
    # Groups section
    if groups:
        keyboard.append([
            InlineKeyboardButton(
                "👥 گروه‌ها",
                callback_data=json.dumps({"action": "poll_target_groups"})
            )
        ])
        
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
                        "action": "poll_target_select",
                        "id": group_id_value,
                        "type": "group"
                    })
                )
            ])
    
    # Back Button
    keyboard.append([
        InlineKeyboardButton(
            "🔙 بازگشت",
            callback_data=json.dumps({"action": "back_to_poll_management"})
        )
    ])
    
    return keyboard

def create_enhanced_poll_keyboard(poll_options, poll_id):
    """Create an enhanced keyboard for poll options with vote counters"""
    keyboard = []
    
    for i, option in enumerate(poll_options):
        vote_count = option.get("votes", 0)
        vote_text = f"{option['text']} ({vote_count} رای)"
        
        keyboard.append([
            InlineKeyboardButton(
                text=vote_text,
                callback_data=json.dumps({
                    "action": "poll_vote",
                    "poll_id": poll_id,
                    "option_id": i
                })
            )
        ])
    
    # Add results and close buttons
    keyboard.append([
        InlineKeyboardButton(
            text="📊 نتایج",
            callback_data=json.dumps({
                "action": "poll_results",
                "poll_id": poll_id
            })
        ),
        InlineKeyboardButton(
            text="🔒 بستن نظرسنجی",
            callback_data=json.dumps({
                "action": "poll_close",
                "poll_id": poll_id
            })
        )
    ])
    
    return keyboard

def create_poll_settings_keyboard():
    """Create keyboard for poll settings"""
    keyboard = [
        # Anonymous Voting
        [
            InlineKeyboardButton(
                "🕶️ رای‌گیری ناشناس",
                callback_data=json.dumps({"action": "poll_setting_anonymous"})
            ),
        ],
        # Multiple Choices
        [
            InlineKeyboardButton(
                "📑 انتخاب چندگانه",
                callback_data=json.dumps({"action": "poll_setting_multiple_choices"})
            ),
        ],
        # Time Limit
        [
            InlineKeyboardButton(
                "⏱️ محدودیت زمانی",
                callback_data=json.dumps({"action": "poll_setting_time_limit"})
            ),
        ],
        # Display Live Results
        [
            InlineKeyboardButton(
                "📈 نمایش نتایج زنده",
                callback_data=json.dumps({"action": "poll_setting_live_results"})
            ),
        ],
        # Back Button
        [
            InlineKeyboardButton(
                "🔙 بازگشت به مدیریت نظرسنجی",
                callback_data=json.dumps({"action": "back_to_poll_management"})
            ),
        ],
    ]
    return keyboard