"""
Message formatting and display utilities
تنظیم و نمایش پیام‌ها
"""
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def format_channel_list(channels):
    """Format a list of channels for display"""
    if not channels:
        return "هیچ کانالی تنظیم نشده است."
    
    text = "📢 کانال‌های مدیریت شده:\n\n"
    
    for channel_id, channel_name in channels.items():
        text += f"• {channel_name} (شناسه: {channel_id})\n"
    
    return text

def format_group_list(groups):
    """Format a list of groups for display"""
    if not groups:
        return "هیچ گروهی تنظیم نشده است."
    
    text = "👥 گروه‌های مدیریت شده:\n\n"
    
    for group_id, group_name in groups.items():
        text += f"• {group_name} (شناسه: {group_id})\n"
    
    return text

def format_scheduled_list(scheduled_messages):
    """Format a list of scheduled messages for display"""
    if not scheduled_messages:
        return "هیچ پیام زمان‌بندی شده‌ای وجود ندارد."
    
    text = "🕒 پیام‌های زمان‌بندی شده:\n\n"
    
    for msg in scheduled_messages:
        try:
            # Convert the ISO time string to a datetime object
            scheduled_time = datetime.fromisoformat(msg["time"])
            formatted_time = scheduled_time.strftime("%Y-%m-%d %H:%M:%S")
            
            # Get target info
            target_type = msg.get("target", {}).get("type", "unknown")
            target_name = "کانال" if target_type == "channel" else "گروه" if target_type == "group" else "ناشناخته"
            target_id = msg.get("target", {}).get("id", "ناشناخته")
            
            # Format message preview
            if len(msg["text"]) > 50:
                message_preview = msg["text"][:50] + "..."
            else:
                message_preview = msg["text"]
            
            text += f"⏰ زمان: {formatted_time}\n"
            text += f"📨 به: {target_name} (شناسه: {target_id})\n"
            text += f"💬 پیام: {message_preview}\n"
            text += f"🆔 شناسه: {msg['id']}\n\n"
        except Exception as e:
            logger.error(f"Error formatting scheduled message: {e}")
            text += f"خطا در نمایش پیام با شناسه {msg.get('id', 'ناشناخته')}\n\n"
    
    return text

def format_autopost_list(auto_posts):
    """Format a list of automatic posts for display"""
    if not auto_posts:
        return "هیچ پست خودکاری تنظیم نشده است."
    
    text = "🔄 پست‌های خودکار:\n\n"
    
    for post in auto_posts:
        try:
            # Get schedule info
            if post["type"] == "daily":
                schedule_info = f"روزانه در ساعت {post['hour']}:{post['minute']:02d}"
            elif post["type"] == "weekly":
                days = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه", "شنبه", "یکشنبه"]
                day_name = days[post["day"]]
                schedule_info = f"{day_name} در ساعت {post['hour']}:{post['minute']:02d}"
            else:
                schedule_info = "زمان‌بندی نامشخص"
            
            # Get target info
            target_type = post.get("target", {}).get("type", "unknown")
            target_name = "کانال" if target_type == "channel" else "گروه" if target_type == "group" else "ناشناخته"
            target_id = post.get("target", {}).get("id", "ناشناخته")
            
            # Format message preview
            if len(post["text"]) > 50:
                message_preview = post["text"][:50] + "..."
            else:
                message_preview = post["text"]
            
            text += f"🔄 زمان‌بندی: {schedule_info}\n"
            text += f"📨 به: {target_name} (شناسه: {target_id})\n"
            text += f"💬 پیام: {message_preview}\n"
            text += f"🆔 شناسه: {post['id']}\n\n"
        except Exception as e:
            logger.error(f"Error formatting automatic post: {e}")
            text += f"خطا در نمایش پست خودکار با شناسه {post.get('id', 'ناشناخته')}\n\n"
    
    return text

def format_welcome_message(welcome_text, user_name, username, chat_name):
    """Format a welcome message with user information"""
    return (
        welcome_text
        .replace("{name}", user_name)
        .replace("{username}", username)
        .replace("{chat}", chat_name)
    )
