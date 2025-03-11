"""
Command handlers for the Telegram Bot
"""
import logging
import json
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from bot.admin import is_admin
from bot.storage import load_data, save_data
from bot.keyboards import (
    create_channels_keyboard, 
    create_groups_keyboard,
    create_schedule_keyboard,
    create_autopost_keyboard,
    build_inline_keyboard,
    create_main_menu_keyboard,
    create_channel_management_keyboard,
    create_group_management_keyboard,
    create_schedule_management_keyboard,
    create_autopost_management_keyboard,
    create_admin_management_keyboard
)
from bot.messages import (
    format_channel_list,
    format_group_list,
    format_scheduled_list,
    format_autopost_list
)
from bot.scheduler import (
    schedule_one_time_message, 
    cancel_scheduled_job,
    schedule_recurring_message,
    cancel_autopost
)
import config

logger = logging.getLogger(__name__)

# Command Handlers
@is_admin
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued with inline keyboard menu."""
    from bot.keyboards import create_main_menu_keyboard
    keyboard = create_main_menu_keyboard()
    await update.message.reply_text(
        config.MESSAGES["start"], 
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

@is_admin
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(config.MESSAGES["help"])

@is_admin
async def add_admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a new admin"""
    if not context.args or len(context.args) < 1:
        await update.message.reply_text(
            "لطفاً شناسه عددی کاربر را وارد کنید. مثال:\n"
            "/addadmin 123456789"
        )
        return
    
    try:
        user_id = int(context.args[0])
        from bot.admin import add_admin
        
        if add_admin(user_id):
            await update.message.reply_text(f"✅ کاربر با شناسه {user_id} با موفقیت به عنوان مدیر اضافه شد!")
        else:
            await update.message.reply_text(f"❌ کاربر با شناسه {user_id} قبلاً به عنوان مدیر تنظیم شده است.")
    except ValueError:
        await update.message.reply_text("❌ شناسه کاربر باید یک عدد باشد.")
    except Exception as e:
        logger.error(f"Error adding admin: {e}")
        await update.message.reply_text(config.MESSAGES["error"].format(str(e)))

@is_admin
async def add_channel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a channel to manage"""
    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            "لطفاً شناسه یا یوزرنیم کانال و نام کانال را وارد کنید. مثال:\n"
            "/addchannel -1001234567890 کانال من\n"
            "یا\n"
            "/addchannel @mychannel کانال من"
        )
        return
    
    try:
        channel_identifier = context.args[0]
        channel_name = ' '.join(context.args[1:])
        
        # Load config
        conf = config.init_config()
        
        # Check if it's a username (starts with @)
        if channel_identifier.startswith('@'):
            # For usernames, we'll need to resolve them to get the channel ID
            # Save the username as is for now, we'll try to get the ID when sending messages
            conf["channels"][channel_identifier] = channel_name
        else:
            # Try to convert to integer ID
            try:
                channel_id = int(channel_identifier)
                conf["channels"][str(channel_id)] = channel_name
            except ValueError:
                await update.message.reply_text("شناسه کانال نامعتبر است. باید یک عدد باشد یا با @ شروع شود.")
                return
        
        # Save config
        config.save_config(conf)
        
        await update.message.reply_text(config.MESSAGES["channel_added"])
    except Exception as e:
        logger.error(f"Error adding channel: {e}")
        await update.message.reply_text(config.MESSAGES["error"].format(str(e)))

@is_admin
async def del_channel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove a channel from management"""
    conf = config.init_config()
    
    if not conf["channels"]:
        await update.message.reply_text(config.MESSAGES["no_channels"])
        return
    
    keyboard = create_channels_keyboard(conf["channels"], "del_channel")
    
    await update.message.reply_text(
        "Select a channel to remove:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

@is_admin
async def list_channels(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """List all managed channels"""
    conf = config.init_config()
    
    if not conf["channels"]:
        await update.message.reply_text(config.MESSAGES["no_channels"])
        return
    
    channel_text = format_channel_list(conf["channels"])
    await update.message.reply_text(channel_text)

@is_admin
async def add_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a group to manage"""
    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            "لطفاً شناسه یا یوزرنیم گروه و نام گروه را وارد کنید. مثال:\n"
            "/addgroup -1001234567890 گروه من\n"
            "یا\n"
            "/addgroup @mygroup گروه من"
        )
        return
    
    try:
        group_identifier = context.args[0]
        group_name = ' '.join(context.args[1:])
        
        # Load config
        conf = config.init_config()
        
        # Check if it's a username (starts with @)
        if group_identifier.startswith('@'):
            # For usernames, save as is
            conf["groups"][group_identifier] = group_name
        else:
            # Try to convert to integer ID
            try:
                group_id = int(group_identifier)
                conf["groups"][str(group_id)] = group_name
            except ValueError:
                await update.message.reply_text("شناسه گروه نامعتبر است. باید یک عدد باشد یا با @ شروع شود.")
                return
        
        # Save config
        config.save_config(conf)
        
        await update.message.reply_text(config.MESSAGES["group_added"])
    except Exception as e:
        logger.error(f"Error adding group: {e}")
        await update.message.reply_text(config.MESSAGES["error"].format(str(e)))

@is_admin
async def del_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove a group from management"""
    conf = config.init_config()
    
    if not conf["groups"]:
        await update.message.reply_text(config.MESSAGES["no_groups"])
        return
    
    keyboard = create_groups_keyboard(conf["groups"], "del_group")
    
    await update.message.reply_text(
        "Select a group to remove:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

@is_admin
async def list_groups(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """List all managed groups"""
    conf = config.init_config()
    
    if not conf["groups"]:
        await update.message.reply_text(config.MESSAGES["no_groups"])
        return
    
    group_text = format_group_list(conf["groups"])
    await update.message.reply_text(group_text)

@is_admin
async def send_message_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start the process of sending a message to a channel or group"""
    conf = config.init_config()
    
    # Check if we have any channels or groups
    if not conf["channels"] and not conf["groups"]:
        await update.message.reply_text("You need to add at least one channel or group first.")
        return
    
    # Store the current state in user_data
    context.user_data["sending_message"] = True
    
    # Create combined keyboard with channels and groups
    combined_keyboard = []
    
    # Add channels
    if conf["channels"]:
        channels_keyboard = create_channels_keyboard(conf["channels"], "send_to")
        combined_keyboard.extend(channels_keyboard)
    
    # Add groups
    if conf["groups"]:
        groups_keyboard = create_groups_keyboard(conf["groups"], "send_to")
        combined_keyboard.extend(groups_keyboard)
    
    await update.message.reply_text(
        "Select where to send the message:",
        reply_markup=InlineKeyboardMarkup(combined_keyboard)
    )

@is_admin
async def schedule_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Schedule a message to be sent later"""
    if not context.args:
        await update.message.reply_text(
            "Please specify delay in minutes or exact time (HH:MM). Examples:\n"
            "/schedule 30 (for 30 minutes from now)\n"
            "/schedule 14:30 (for 2:30 PM today)"
        )
        return
    
    try:
        delay_arg = context.args[0]
        
        # Check if it's a time format (HH:MM)
        if ":" in delay_arg:
            # Parse as exact time
            hour, minute = map(int, delay_arg.split(':'))
            now = datetime.now()
            scheduled_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # If the time is already past for today, schedule it for tomorrow
            if scheduled_time < now:
                scheduled_time += timedelta(days=1)
        else:
            # Parse as minutes delay
            minutes = int(delay_arg)
            scheduled_time = datetime.now() + timedelta(minutes=minutes)
        
        # Store scheduling info in user_data
        context.user_data["scheduling"] = {
            "time": scheduled_time,
            "state": "selecting_target"
        }
        
        # Show selection for where to send the message
        conf = config.init_config()
        
        # Check if we have any channels or groups
        if not conf["channels"] and not conf["groups"]:
            await update.message.reply_text("You need to add at least one channel or group first.")
            context.user_data.pop("scheduling", None)
            return
        
        # Create combined keyboard with channels and groups
        combined_keyboard = []
        
        # Add channels
        if conf["channels"]:
            channels_keyboard = create_channels_keyboard(conf["channels"], "schedule_to")
            combined_keyboard.extend(channels_keyboard)
        
        # Add groups
        if conf["groups"]:
            groups_keyboard = create_groups_keyboard(conf["groups"], "schedule_to")
            combined_keyboard.extend(groups_keyboard)
        
        time_str = scheduled_time.strftime("%Y-%m-%d %H:%M:%S")
        await update.message.reply_text(
            f"Message will be scheduled for: {time_str}\n"
            "Select where to send the message:",
            reply_markup=InlineKeyboardMarkup(combined_keyboard)
        )
    except ValueError:
        await update.message.reply_text("Invalid time format. Use minutes (e.g., 30) or HH:MM format (e.g., 14:30).")
    except Exception as e:
        logger.error(f"Error scheduling message: {e}")
        await update.message.reply_text(config.MESSAGES["error"].format(str(e)))

@is_admin
async def list_scheduled(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """List all scheduled messages"""
    data = load_data()
    
    if not data.get("scheduled_messages", []):
        await update.message.reply_text("No scheduled messages.")
        return
    
    scheduled_text = format_scheduled_list(data["scheduled_messages"])
    keyboard = create_schedule_keyboard(data["scheduled_messages"])
    
    await update.message.reply_text(
        scheduled_text,
        reply_markup=InlineKeyboardMarkup(keyboard) if keyboard else None
    )

@is_admin
async def cancel_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Cancel a scheduled message"""
    data = load_data()
    
    if not data.get("scheduled_messages", []):
        await update.message.reply_text("No scheduled messages to cancel.")
        return
    
    keyboard = create_schedule_keyboard(data["scheduled_messages"], "cancel")
    
    await update.message.reply_text(
        "Select a scheduled message to cancel:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

@is_admin
async def set_autopost(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Set up automatic posting at regular intervals"""
    if len(context.args) < 2:
        await update.message.reply_text(
            "Please specify when to post. Examples:\n"
            "/autopost daily 14:30 (every day at 2:30 PM)\n"
            "/autopost weekly 1 14:30 (every Monday at 2:30 PM)\n"
            "Days: 0=Monday, 1=Tuesday, ..., 6=Sunday"
        )
        return
    
    try:
        schedule_type = context.args[0].lower()
        
        if schedule_type == "daily":
            time_str = context.args[1]
            hour, minute = map(int, time_str.split(':'))
            
            context.user_data["autopost"] = {
                "type": "daily",
                "hour": hour,
                "minute": minute,
                "state": "selecting_target"
            }
        elif schedule_type == "weekly":
            day = int(context.args[1])
            time_str = context.args[2]
            hour, minute = map(int, time_str.split(':'))
            
            if day < 0 or day > 6:
                await update.message.reply_text("Day must be between 0 (Monday) and 6 (Sunday)")
                return
            
            context.user_data["autopost"] = {
                "type": "weekly",
                "day": day,
                "hour": hour,
                "minute": minute,
                "state": "selecting_target"
            }
        else:
            await update.message.reply_text("Invalid schedule type. Use 'daily' or 'weekly'.")
            return
        
        # Show selection for where to send the message
        conf = config.init_config()
        
        # Check if we have any channels or groups
        if not conf["channels"] and not conf["groups"]:
            await update.message.reply_text("You need to add at least one channel or group first.")
            context.user_data.pop("autopost", None)
            return
        
        # Create combined keyboard with channels and groups
        combined_keyboard = []
        
        # Add channels
        if conf["channels"]:
            channels_keyboard = create_channels_keyboard(conf["channels"], "autopost_to")
            combined_keyboard.extend(channels_keyboard)
        
        # Add groups
        if conf["groups"]:
            groups_keyboard = create_groups_keyboard(conf["groups"], "autopost_to")
            combined_keyboard.extend(groups_keyboard)
        
        await update.message.reply_text(
            "Select where to send the automatic posts:",
            reply_markup=InlineKeyboardMarkup(combined_keyboard)
        )
    except ValueError:
        await update.message.reply_text("Invalid time format. Use HH:MM format (e.g., 14:30).")
    except Exception as e:
        logger.error(f"Error setting up autopost: {e}")
        await update.message.reply_text(config.MESSAGES["error"].format(str(e)))

@is_admin
async def list_autopost(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """List all automatic posting configurations"""
    data = load_data()
    
    if not data.get("auto_posts", []):
        await update.message.reply_text("No automatic posts configured.")
        return
    
    autopost_text = format_autopost_list(data["auto_posts"])
    keyboard = create_autopost_keyboard(data["auto_posts"])
    
    await update.message.reply_text(
        autopost_text,
        reply_markup=InlineKeyboardMarkup(keyboard) if keyboard else None
    )

@is_admin
async def delete_autopost(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Delete an automatic posting configuration"""
    data = load_data()
    
    if not data.get("auto_posts", []):
        await update.message.reply_text("No automatic posts to delete.")
        return
    
    keyboard = create_autopost_keyboard(data["auto_posts"], "delete")
    
    await update.message.reply_text(
        "Select an automatic post to delete:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

@is_admin
async def set_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Set welcome message for groups"""
    conf = config.init_config()
    
    if not conf["groups"]:
        await update.message.reply_text("You need to add at least one group first.")
        return
    
    if not context.args:
        # Just show the groups to select
        keyboard = create_groups_keyboard(conf["groups"], "set_welcome")
        
        await update.message.reply_text(
            "Select a group to set welcome message for:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        # User is providing a message along with the command
        # Check if we're already in the middle of setting a welcome message
        if "setting_welcome" in context.user_data and "group_id" in context.user_data["setting_welcome"]:
            group_id = context.user_data["setting_welcome"]["group_id"]
            welcome_message = ' '.join(context.args)
            
            # Save the welcome message
            conf["welcome_messages"][str(group_id)] = welcome_message
            config.save_config(conf)
            
            # Clear the state
            context.user_data.pop("setting_welcome", None)
            
            group_name = conf["groups"].get(str(group_id), "Unknown Group")
            await update.message.reply_text(f"Welcome message set for {group_name}!")
        else:
            await update.message.reply_text("Please select a group first.")

@is_admin
async def create_poll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Create a poll with inline buttons"""
    # Start poll creation process
    context.user_data["creating_poll"] = {
        "state": "title",
        "options": []
    }
    
    await update.message.reply_text(
        "Let's create a poll! First, send me the poll question/title."
    )

@is_admin
async def get_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Get members list from a channel or group"""
    conf = config.init_config()
    
    # Check if we have any channels or groups
    if not conf["channels"] and not conf["groups"]:
        await update.message.reply_text("You need to add at least one channel or group first.")
        return
    
    # Create combined keyboard with channels and groups
    combined_keyboard = []
    
    # Add channels
    if conf["channels"]:
        channels_keyboard = create_channels_keyboard(conf["channels"], "get_members")
        combined_keyboard.extend(channels_keyboard)
    
    # Add groups
    if conf["groups"]:
        groups_keyboard = create_groups_keyboard(conf["groups"], "get_members")
        combined_keyboard.extend(groups_keyboard)
    
    await update.message.reply_text(
        "Select a channel or group to get members from:",
        reply_markup=InlineKeyboardMarkup(combined_keyboard)
    )

# Callback Query Handler
@is_admin
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    try:
        data = json.loads(query.data)
        action = data.get("action")
        
        # Main menu actions
        if action == "main_menu":
            from bot.keyboards import create_main_menu_keyboard
            keyboard = create_main_menu_keyboard()
            await query.edit_message_text(
                config.MESSAGES["start"],
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        
        # Poll Management Actions
        elif action == "create_poll":
            from bot.poll_keyboards import create_poll_management_keyboard
            keyboard = create_poll_management_keyboard()
            await query.edit_message_text(
                "📊 مدیریت نظرسنجی - لطفاً یک گزینه را انتخاب کنید:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        elif action == "poll_templates":
            from bot.poll_keyboards import create_poll_templates_keyboard
            keyboard = create_poll_templates_keyboard()
            await query.edit_message_text(
                "📝 قالب‌های نظرسنجی - لطفاً یک قالب را انتخاب کنید:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        elif action == "poll_settings":
            from bot.poll_keyboards import create_poll_settings_keyboard
            keyboard = create_poll_settings_keyboard()
            await query.edit_message_text(
                "⚙️ تنظیمات نظرسنجی - لطفاً گزینه مورد نظر را انتخاب کنید:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        elif action == "back_to_poll_management":
            from bot.poll_keyboards import create_poll_management_keyboard
            keyboard = create_poll_management_keyboard()
            await query.edit_message_text(
                "📊 مدیریت نظرسنجی - لطفاً یک گزینه را انتخاب کنید:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        
        # Welcome Message Actions
        elif action == "welcome_message":
            from bot.welcome_keyboards import create_welcome_management_keyboard
            keyboard = create_welcome_management_keyboard()
            await query.edit_message_text(
                "👋 مدیریت پیام خوش‌آمدگویی - لطفاً یک گزینه را انتخاب کنید:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        elif action == "welcome_templates":
            from bot.welcome_keyboards import create_welcome_templates_keyboard
            keyboard = create_welcome_templates_keyboard()
            await query.edit_message_text(
                "📝 قالب‌های پیام خوش‌آمدگویی - لطفاً یک قالب را انتخاب کنید:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        elif action == "welcome_settings":
            from bot.welcome_keyboards import create_welcome_settings_keyboard
            keyboard = create_welcome_settings_keyboard()
            await query.edit_message_text(
                "⚙️ تنظیمات پیام خوش‌آمدگویی - لطفاً گزینه مورد نظر را انتخاب کنید:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        elif action == "welcome_buttons":
            from bot.welcome_keyboards import create_welcome_buttons_keyboard
            keyboard = create_welcome_buttons_keyboard()
            await query.edit_message_text(
                "🔗 مدیریت دکمه‌های پیام خوش‌آمدگویی - لطفاً گزینه مورد نظر را انتخاب کنید:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        elif action == "back_to_welcome_management":
            from bot.welcome_keyboards import create_welcome_management_keyboard
            keyboard = create_welcome_management_keyboard()
            await query.edit_message_text(
                "👋 مدیریت پیام خوش‌آمدگویی - لطفاً یک گزینه را انتخاب کنید:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        elif action == "channel_management":
            from bot.keyboards import create_channel_management_keyboard
            keyboard = create_channel_management_keyboard()
            await query.edit_message_text(
                "🔄 مدیریت کانال ها - لطفاً یک گزینه را انتخاب کنید:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        elif action == "group_management":
            from bot.keyboards import create_group_management_keyboard
            keyboard = create_group_management_keyboard()
            await query.edit_message_text(
                "👥 مدیریت گروه ها - لطفاً یک گزینه را انتخاب کنید:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        elif action == "schedule_management":
            from bot.keyboards import create_schedule_management_keyboard
            keyboard = create_schedule_management_keyboard()
            await query.edit_message_text(
                "🕒 زمان‌بندی پیام ها - لطفاً یک گزینه را انتخاب کنید:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        elif action == "autopost_management":
            from bot.keyboards import create_autopost_management_keyboard
            keyboard = create_autopost_management_keyboard()
            await query.edit_message_text(
                "🔄 پست خودکار - لطفاً یک گزینه را انتخاب کنید:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        elif action == "admin_management":
            from bot.keyboards import create_admin_management_keyboard
            keyboard = create_admin_management_keyboard()
            await query.edit_message_text(
                "👤 مدیریت ادمین ها - لطفاً یک گزینه را انتخاب کنید:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        elif action == "list_channels":
            conf = config.init_config()
            
            if not conf["channels"]:
                await query.edit_message_text(
                    config.MESSAGES["no_channels"],
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton(
                            "🔙 بازگشت به مدیریت کانال",
                            callback_data=json.dumps({"action": "channel_management"})
                        )
                    ]])
                )
                return
            
            channel_text = format_channel_list(conf["channels"])
            await query.edit_message_text(
                channel_text,
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        "🔙 بازگشت به مدیریت کانال",
                        callback_data=json.dumps({"action": "channel_management"})
                    )
                ]])
            )
        elif action == "add_channel":
            # Set state to add channel
            context.user_data["adding_channel"] = True
            await query.edit_message_text(
                "لطفاً شناسه کانال و نام آن را به فرمت زیر ارسال کنید:\n"
                "-1001234567890 نام کانال",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        "🔙 لغو و بازگشت",
                        callback_data=json.dumps({"action": "channel_management"})
                    )
                ]])
            )
        elif action == "remove_channel":
            conf = config.init_config()
            
            if not conf["channels"]:
                await query.edit_message_text(
                    config.MESSAGES["no_channels"],
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton(
                            "🔙 بازگشت به مدیریت کانال",
                            callback_data=json.dumps({"action": "channel_management"})
                        )
                    ]])
                )
                return
            
            keyboard = create_channels_keyboard(conf["channels"], "del_channel")
            keyboard.append([
                InlineKeyboardButton(
                    "🔙 بازگشت به مدیریت کانال",
                    callback_data=json.dumps({"action": "channel_management"})
                )
            ])
            
            await query.edit_message_text(
                "یک کانال را برای حذف انتخاب کنید:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        elif action == "list_groups":
            conf = config.init_config()
            
            if not conf["groups"]:
                await query.edit_message_text(
                    config.MESSAGES["no_groups"],
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton(
                            "🔙 بازگشت به مدیریت گروه",
                            callback_data=json.dumps({"action": "group_management"})
                        )
                    ]])
                )
                return
            
            group_text = format_group_list(conf["groups"])
            await query.edit_message_text(
                group_text,
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        "🔙 بازگشت به مدیریت گروه",
                        callback_data=json.dumps({"action": "group_management"})
                    )
                ]])
            )
        elif action == "add_group":
            # Set state to add group
            context.user_data["adding_group"] = True
            await query.edit_message_text(
                "لطفاً شناسه گروه و نام آن را به فرمت زیر ارسال کنید:\n"
                "-1001234567890 نام گروه",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        "🔙 لغو و بازگشت",
                        callback_data=json.dumps({"action": "group_management"})
                    )
                ]])
            )
        elif action == "remove_group":
            conf = config.init_config()
            
            if not conf["groups"]:
                await query.edit_message_text(
                    config.MESSAGES["no_groups"],
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton(
                            "🔙 بازگشت به مدیریت گروه",
                            callback_data=json.dumps({"action": "group_management"})
                        )
                    ]])
                )
                return
            
            keyboard = create_groups_keyboard(conf["groups"], "del_group")
            keyboard.append([
                InlineKeyboardButton(
                    "🔙 بازگشت به مدیریت گروه",
                    callback_data=json.dumps({"action": "group_management"})
                )
            ])
            
            await query.edit_message_text(
                "یک گروه را برای حذف انتخاب کنید:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        elif action == "send_message":
            conf = config.init_config()
            
            # Check if we have any channels or groups
            if not conf["channels"] and not conf["groups"]:
                await query.edit_message_text(
                    "ابتدا باید حداقل یک کانال یا گروه اضافه کنید.",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton(
                            "🔙 بازگشت به منوی اصلی",
                            callback_data=json.dumps({"action": "main_menu"})
                        )
                    ]])
                )
                return
            
            # Store the current state in user_data
            context.user_data["sending_message"] = True
            
            # Create combined keyboard with channels and groups
            combined_keyboard = []
            
            # Add channels
            if conf["channels"]:
                channels_keyboard = create_channels_keyboard(conf["channels"], "send_to")
                combined_keyboard.extend(channels_keyboard)
            
            # Add groups
            if conf["groups"]:
                groups_keyboard = create_groups_keyboard(conf["groups"], "send_to")
                combined_keyboard.extend(groups_keyboard)
            
            combined_keyboard.append([
                InlineKeyboardButton(
                    "🔙 بازگشت به منوی اصلی",
                    callback_data=json.dumps({"action": "main_menu"})
                )
            ])
            
            await query.edit_message_text(
                "کانال یا گروه مورد نظر برای ارسال پیام را انتخاب کنید:",
                reply_markup=InlineKeyboardMarkup(combined_keyboard)
            )
        elif action == "new_schedule":
            # Set state for scheduling
            context.user_data["scheduling_setup"] = True
            await query.edit_message_text(
                "لطفاً زمان ارسال پیام را به یکی از فرمت‌های زیر وارد کنید:\n"
                "30 (برای 30 دقیقه بعد)\n"
                "14:30 (برای ساعت 14:30 امروز)",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        "🔙 لغو و بازگشت",
                        callback_data=json.dumps({"action": "schedule_management"})
                    )
                ]])
            )
        elif action == "schedule_list":
            data = load_data()
            
            if not data.get("scheduled_messages", []):
                await query.edit_message_text(
                    "هیچ پیام زمان‌بندی شده‌ای وجود ندارد.",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton(
                            "🔙 بازگشت به مدیریت زمان‌بندی",
                            callback_data=json.dumps({"action": "schedule_management"})
                        )
                    ]])
                )
                return
            
            scheduled_text = format_scheduled_list(data["scheduled_messages"])
            keyboard = create_schedule_keyboard(data["scheduled_messages"])
            keyboard.append([
                InlineKeyboardButton(
                    "🔙 بازگشت به مدیریت زمان‌بندی",
                    callback_data=json.dumps({"action": "schedule_management"})
                )
            ])
            
            await query.edit_message_text(
                scheduled_text,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        elif action == "cancel_schedule":
            data = load_data()
            
            if not data.get("scheduled_messages", []):
                await query.edit_message_text(
                    "هیچ پیام زمان‌بندی شده‌ای برای لغو وجود ندارد.",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton(
                            "🔙 بازگشت به مدیریت زمان‌بندی",
                            callback_data=json.dumps({"action": "schedule_management"})
                        )
                    ]])
                )
                return
            
            keyboard = create_schedule_keyboard(data["scheduled_messages"], "cancel")
            keyboard.append([
                InlineKeyboardButton(
                    "🔙 بازگشت به مدیریت زمان‌بندی",
                    callback_data=json.dumps({"action": "schedule_management"})
                )
            ])
            
            await query.edit_message_text(
                "پیام زمان‌بندی شده‌ای که می‌خواهید لغو کنید را انتخاب کنید:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        elif action == "add_admin":
            # Set state for adding admin
            context.user_data["adding_admin"] = True
            await query.edit_message_text(
                "لطفاً شناسه عددی کاربر جدید را وارد کنید:",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        "🔙 لغو و بازگشت",
                        callback_data=json.dumps({"action": "admin_management"})
                    )
                ]])
            )
        elif action == "list_admins":
            from bot.admin import get_admins
            admins = get_admins()
            
            if not admins:
                admin_text = "هیچ ادمینی تعریف نشده است."
            else:
                admin_text = "لیست ادمین‌ها:\n\n"
                for i, admin_id in enumerate(admins, 1):
                    admin_text += f"{i}. {admin_id}\n"
            
            await query.edit_message_text(
                admin_text,
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        "🔙 بازگشت به مدیریت ادمین",
                        callback_data=json.dumps({"action": "admin_management"})
                    )
                ]])
            )
        
        if action == "del_channel":
            channel_id = data.get("id")
            conf = config.init_config()
            
            if str(channel_id) in conf["channels"]:
                channel_name = conf["channels"][str(channel_id)]
                del conf["channels"][str(channel_id)]
                config.save_config(conf)
                await query.edit_message_text(f"Channel '{channel_name}' has been removed.")
            else:
                await query.edit_message_text("Channel not found.")
        
        elif action == "del_group":
            group_id = data.get("id")
            conf = config.init_config()
            
            if str(group_id) in conf["groups"]:
                group_name = conf["groups"][str(group_id)]
                del conf["groups"][str(group_id)]
                
                # Also remove any welcome messages for this group
                if str(group_id) in conf["welcome_messages"]:
                    del conf["welcome_messages"][str(group_id)]
                
                config.save_config(conf)
                await query.edit_message_text(f"Group '{group_name}' has been removed.")
            else:
                await query.edit_message_text("Group not found.")
        
        elif action == "send_to":
            target_id = data.get("id")
            target_type = data.get("type")  # 'channel' or 'group'
            
            # Store target info in user_data
            context.user_data["sending_to"] = {
                "id": target_id,
                "type": target_type
            }
            
            # Ask for message text
            keyboard = build_inline_keyboard([
                {"text": "Add Inline Buttons", "callback_data": json.dumps({"action": "add_buttons"})}
            ])
            
            conf = config.init_config()
            target_name = (conf["channels"] if target_type == "channel" else conf["groups"]).get(str(target_id), "Unknown")
            
            await query.edit_message_text(
                f"You'll send a message to {target_type} '{target_name}'.\n"
                "Now send me the message text, or click below to add inline buttons.",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        
        elif action == "add_buttons":
            # Start the process of adding buttons
            context.user_data["adding_buttons"] = {
                "buttons": [],
                "state": "text"
            }
            
            await query.edit_message_text(
                "Let's add some inline buttons. Send me the text for the first button."
            )
        
        elif action == "add_button_url":
            # User wants to add a URL button
            button_text = data.get("text")
            
            # Store button text and update state
            if "adding_buttons" not in context.user_data:
                context.user_data["adding_buttons"] = {
                    "buttons": [],
                    "state": "url"
                }
            
            context.user_data["adding_buttons"]["current_text"] = button_text
            context.user_data["adding_buttons"]["state"] = "url"
            
            await query.edit_message_text(
                f"Button text: '{button_text}'\n"
                "Now send me the URL for this button."
            )
        
        elif action == "add_button_callback":
            # User wants to add a callback button
            button_text = data.get("text")
            
            # Store button text and update state
            if "adding_buttons" not in context.user_data:
                context.user_data["adding_buttons"] = {
                    "buttons": [],
                    "state": "callback"
                }
            
            context.user_data["adding_buttons"]["current_text"] = button_text
            context.user_data["adding_buttons"]["state"] = "callback"
            
            await query.edit_message_text(
                f"Button text: '{button_text}'\n"
                "Now send me the callback data for this button."
            )
        
        elif action == "finish_buttons":
            # User is done adding buttons
            buttons = context.user_data.get("adding_buttons", {}).get("buttons", [])
            
            # Clear the state
            button_data = context.user_data.pop("adding_buttons", {})
            
            # If we were in the process of sending a message
            if "sending_to" in context.user_data:
                target_info = context.user_data["sending_to"]
                
                keyboard = []
                for row in buttons:
                    keyboard_row = []
                    for btn in row:
                        if btn["type"] == "url":
                            keyboard_row.append({
                                "text": btn["text"],
                                "url": btn["url"]
                            })
                        elif btn["type"] == "callback":
                            keyboard_row.append({
                                "text": btn["text"],
                                "callback_data": btn["callback_data"]
                            })
                    keyboard.append(keyboard_row)
                
                context.user_data["sending_to"]["keyboard"] = keyboard
                
                conf = config.init_config()
                target_type = target_info["type"]
                target_id = target_info["id"]
                target_name = (conf["channels"] if target_type == "channel" else conf["groups"]).get(str(target_id), "Unknown")
                
                await query.edit_message_text(
                    f"Buttons have been added! Now send me the message text to send to {target_type} '{target_name}'."
                )
            else:
                await query.edit_message_text("Buttons have been added!")
        
        elif action == "add_row":
            # Start a new row of buttons
            if "adding_buttons" in context.user_data:
                button_data = context.user_data["adding_buttons"]
                
                # If we have pending buttons, add them to the list
                if "current_row" in button_data:
                    button_data["buttons"].append(button_data["current_row"])
                    button_data.pop("current_row")
                
                # Update state
                button_data["state"] = "text"
                
                keyboard = build_inline_keyboard([
                    {"text": "Finish Adding Buttons", "callback_data": json.dumps({"action": "finish_buttons"})}
                ])
                
                await query.edit_message_text(
                    "New row started. Send me the text for the next button, or click below to finish.",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
        
        elif action == "schedule_to":
            target_id = data.get("id")
            target_type = data.get("type")  # 'channel' or 'group'
            
            # Store target info in user_data
            if "scheduling" in context.user_data:
                context.user_data["scheduling"]["target"] = {
                    "id": target_id,
                    "type": target_type
                }
                context.user_data["scheduling"]["state"] = "entering_text"
                
                # Ask for message text
                keyboard = build_inline_keyboard([
                    {"text": "Add Inline Buttons", "callback_data": json.dumps({"action": "schedule_add_buttons"})}
                ])
                
                conf = config.init_config()
                target_name = (conf["channels"] if target_type == "channel" else conf["groups"]).get(str(target_id), "Unknown")
                time_str = context.user_data["scheduling"]["time"].strftime("%Y-%m-%d %H:%M:%S")
                
                await query.edit_message_text(
                    f"Message will be sent to {target_type} '{target_name}' at {time_str}.\n"
                    "Now send me the message text, or click below to add inline buttons.",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
        
        elif action == "schedule_add_buttons":
            # Start the process of adding buttons for scheduled message
            context.user_data["adding_buttons"] = {
                "buttons": [],
                "state": "text",
                "for_schedule": True
            }
            
            await query.edit_message_text(
                "Let's add some inline buttons. Send me the text for the first button."
            )
        
        elif action == "cancel_schedule":
            schedule_id = data.get("id")
            
            # Cancel the job
            result = cancel_scheduled_job(schedule_id)
            
            if result:
                await query.edit_message_text("Scheduled message has been cancelled.")
            else:
                await query.edit_message_text("Failed to cancel scheduled message. It may have already been sent or cancelled.")
        
        elif action == "autopost_to":
            target_id = data.get("id")
            target_type = data.get("type")  # 'channel' or 'group'
            
            # Store target info in user_data
            if "autopost" in context.user_data:
                context.user_data["autopost"]["target"] = {
                    "id": target_id,
                    "type": target_type
                }
                context.user_data["autopost"]["state"] = "entering_text"
                
                # Ask for message text
                keyboard = build_inline_keyboard([
                    {"text": "Add Inline Buttons", "callback_data": json.dumps({"action": "autopost_add_buttons"})}
                ])
                
                conf = config.init_config()
                target_name = (conf["channels"] if target_type == "channel" else conf["groups"]).get(str(target_id), "Unknown")
                
                await query.edit_message_text(
                    f"Automatic posts will be sent to {target_type} '{target_name}'.\n"
                    "Now send me the message text, or click below to add inline buttons.",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
        
        elif action == "autopost_add_buttons":
            # Start the process of adding buttons for autopost
            context.user_data["adding_buttons"] = {
                "buttons": [],
                "state": "text",
                "for_autopost": True
            }
            
            await query.edit_message_text(
                "Let's add some inline buttons. Send me the text for the first button."
            )
        
        elif action == "delete_autopost":
            autopost_id = data.get("id")
            
            # Cancel the autopost
            result = cancel_autopost(autopost_id)
            
            if result:
                await query.edit_message_text("Automatic post has been deleted.")
            else:
                await query.edit_message_text("Failed to delete automatic post.")
        
        elif action == "set_welcome":
            group_id = data.get("id")
            conf = config.init_config()
            
            if str(group_id) in conf["groups"]:
                group_name = conf["groups"][str(group_id)]
                
                # Store group ID in user_data
                context.user_data["setting_welcome"] = {
                    "group_id": group_id
                }
                
                # Check if there's already a welcome message
                current_welcome = conf["welcome_messages"].get(str(group_id), "None")
                
                await query.edit_message_text(
                    f"Setting welcome message for group '{group_name}'.\n"
                    f"Current welcome message: {current_welcome}\n\n"
                    "Send me the new welcome message, or /cancel to abort."
                )
            else:
                await query.edit_message_text("Group not found.")
        
        elif action == "get_members":
            chat_id = data.get("id")
            chat_type = data.get("type")  # 'channel' or 'group'
            
            conf = config.init_config()
            chat_name = (conf["channels"] if chat_type == "channel" else conf["groups"]).get(str(chat_id), "Unknown")
            
            try:
                # Get chat members
                chat = await context.bot.get_chat(chat_id)
                member_count = await context.bot.get_chat_member_count(chat_id)
                
                # For privacy and API limitations, we don't get the actual list
                # But we can provide a count and basic info
                chat_info = (
                    f"📊 Chat Information for {chat_type} '{chat_name}'\n\n"
                    f"Title: {chat.title}\n"
                    f"Chat ID: {chat.id}\n"
                    f"Type: {chat.type}\n"
                    f"Member count: {member_count}\n\n"
                    "Due to Telegram API limitations, detailed member lists are "
                    "only available for channels/groups where the bot is an admin "
                    "and the member count is not too large."
                )
                
                await query.edit_message_text(chat_info)
            except Exception as e:
                logger.error(f"Error getting members: {e}")
                await query.edit_message_text(
                    f"Error getting members from {chat_type} '{chat_name}'.\n"
                    "Make sure the bot is an admin in the channel/group and has the necessary permissions."
                )
        
        elif action == "poll_vote":
            # Handle poll vote
            poll_id = data.get("poll_id")
            option_id = data.get("option_id")
            user_id = update.effective_user.id
            
            # Load the poll data
            data = load_data()
            
            for poll in data.get("polls", []):
                if poll["id"] == poll_id:
                    # Record the vote
                    if user_id not in poll["votes"]:
                        poll["votes"][str(user_id)] = option_id
                        poll["options"][option_id]["count"] += 1
                        
                        # Save the updated poll data
                        save_data(data)
                        
                        # Update the poll message with new counts
                        poll_text = f"📊 Poll: {poll['title']}\n\n"
                        for i, option in enumerate(poll["options"]):
                            poll_text += f"{option['text']}: {option['count']} votes\n"
                        
                        # Recreate the keyboard
                        keyboard = []
                        row = []
                        for i, option in enumerate(poll["options"]):
                            row.append({
                                "text": f"{option['text']} ({option['count']})",
                                "callback_data": json.dumps({
                                    "action": "poll_vote",
                                    "poll_id": poll_id,
                                    "option_id": i
                                })
                            })
                            
                            # 2 buttons per row
                            if len(row) == 2:
                                keyboard.append(row)
                                row = []
                        
                        # Add any remaining buttons
                        if row:
                            keyboard.append(row)
                        
                        await query.edit_message_text(
                            poll_text,
                            reply_markup=InlineKeyboardMarkup(keyboard)
                        )
                    else:
                        # User already voted
                        previous_vote = int(poll["votes"][str(user_id)])
                        if previous_vote != option_id:
                            # Changed vote
                            poll["options"][previous_vote]["count"] -= 1
                            poll["options"][option_id]["count"] += 1
                            poll["votes"][str(user_id)] = option_id
                            
                            # Save the updated poll data
                            save_data(data)
                            
                            # Update the poll message with new counts
                            poll_text = f"📊 Poll: {poll['title']}\n\n"
                            for i, option in enumerate(poll["options"]):
                                poll_text += f"{option['text']}: {option['count']} votes\n"
                            
                            # Recreate the keyboard
                            keyboard = []
                            row = []
                            for i, option in enumerate(poll["options"]):
                                row.append({
                                    "text": f"{option['text']} ({option['count']})",
                                    "callback_data": json.dumps({
                                        "action": "poll_vote",
                                        "poll_id": poll_id,
                                        "option_id": i
                                    })
                                })
                                
                                # 2 buttons per row
                                if len(row) == 2:
                                    keyboard.append(row)
                                    row = []
                            
                            # Add any remaining buttons
                            if row:
                                keyboard.append(row)
                            
                            await query.edit_message_text(
                                poll_text,
                                reply_markup=InlineKeyboardMarkup(keyboard)
                            )
                        else:
                            # Same vote as before
                            await query.answer("You've already voted for this option.")
                    
                    return
            
            # Poll not found
            await query.answer("Poll not found or has expired.")
    
    except Exception as e:
        logger.error(f"Error in button callback: {e}")
        await query.edit_message_text(f"An error occurred: {str(e)}")

# Text message handler for various states
@is_admin
async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages based on conversation state"""
    text = update.message.text
    user_data = context.user_data
    
    # Handle adding a channel
    if user_data.get("adding_channel"):
        try:
            # Expected format: "-1001234567890 Channel Name"
            parts = text.split(" ", 1)
            if len(parts) < 2:
                await update.message.reply_text("لطفاً هم شناسه کانال و هم نام آن را وارد کنید.")
                return
            
            channel_id = int(parts[0])
            channel_name = parts[1]
            
            # Load config
            conf = config.init_config()
            
            # Add channel
            conf["channels"][str(channel_id)] = channel_name
            
            # Save config
            config.save_config(conf)
            
            # Clear state
            user_data.pop("adding_channel")
            
            # Show success message with main menu
            keyboard = create_channel_management_keyboard()
            await update.message.reply_text(
                f"✅ کانال «{channel_name}» با موفقیت اضافه شد!",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        except ValueError:
            await update.message.reply_text(
                "شناسه کانال نامعتبر است. باید یک عدد باشد.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        "🔙 بازگشت به مدیریت کانال",
                        callback_data=json.dumps({"action": "channel_management"})
                    )
                ]])
            )
        except Exception as e:
            logger.error(f"Error adding channel: {e}")
            await update.message.reply_text(config.MESSAGES["error"].format(str(e)))
            user_data.pop("adding_channel", None)
    
    # Handle adding a group
    elif user_data.get("adding_group"):
        try:
            # Expected format: "-1001234567890 Group Name"
            parts = text.split(" ", 1)
            if len(parts) < 2:
                await update.message.reply_text("لطفاً هم شناسه گروه و هم نام آن را وارد کنید.")
                return
            
            group_id = int(parts[0])
            group_name = parts[1]
            
            # Load config
            conf = config.init_config()
            
            # Add group
            conf["groups"][str(group_id)] = group_name
            
            # Save config
            config.save_config(conf)
            
            # Clear state
            user_data.pop("adding_group")
            
            # Show success message with main menu
            keyboard = create_group_management_keyboard()
            await update.message.reply_text(
                f"✅ گروه «{group_name}» با موفقیت اضافه شد!",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        except ValueError:
            await update.message.reply_text(
                "شناسه گروه نامعتبر است. باید یک عدد باشد.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        "🔙 بازگشت به مدیریت گروه",
                        callback_data=json.dumps({"action": "group_management"})
                    )
                ]])
            )
        except Exception as e:
            logger.error(f"Error adding group: {e}")
            await update.message.reply_text(config.MESSAGES["error"].format(str(e)))
            user_data.pop("adding_group", None)
    
    # Handle adding an admin
    elif user_data.get("adding_admin"):
        try:
            user_id = int(text)
            from bot.admin import add_admin
            
            if add_admin(user_id):
                await update.message.reply_text(
                    f"✅ کاربر با شناسه {user_id} با موفقیت به عنوان مدیر اضافه شد!",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton(
                            "🔙 بازگشت به مدیریت ادمین",
                            callback_data=json.dumps({"action": "admin_management"})
                        )
                    ]])
                )
            else:
                await update.message.reply_text(
                    f"❌ کاربر با شناسه {user_id} قبلاً به عنوان مدیر تنظیم شده است.",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton(
                            "🔙 بازگشت به مدیریت ادمین",
                            callback_data=json.dumps({"action": "admin_management"})
                        )
                    ]])
                )
            
            # Clear state
            user_data.pop("adding_admin")
        except ValueError:
            await update.message.reply_text(
                "❌ شناسه کاربر باید یک عدد باشد.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        "🔙 بازگشت به مدیریت ادمین",
                        callback_data=json.dumps({"action": "admin_management"})
                    )
                ]])
            )
        except Exception as e:
            logger.error(f"Error adding admin: {e}")
            await update.message.reply_text(config.MESSAGES["error"].format(str(e)))
            user_data.pop("adding_admin", None)
    
    # Handle scheduling setup
    elif user_data.get("scheduling_setup"):
        try:
            # Parse scheduling time
            if ":" in text:
                # Parse as exact time
                hour, minute = map(int, text.split(':'))
                now = datetime.now()
                scheduled_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                
                # If the time is already past for today, schedule it for tomorrow
                if scheduled_time < now:
                    scheduled_time += timedelta(days=1)
            else:
                # Parse as minutes delay
                minutes = int(text)
                scheduled_time = datetime.now() + timedelta(minutes=minutes)
            
            # Store scheduling info in user_data
            user_data["scheduling"] = {
                "time": scheduled_time,
                "state": "selecting_target"
            }
            
            # Clear setup state
            user_data.pop("scheduling_setup")
            
            # Show selection for where to send the message
            conf = config.init_config()
            
            # Check if we have any channels or groups
            if not conf["channels"] and not conf["groups"]:
                await update.message.reply_text(
                    "ابتدا باید حداقل یک کانال یا گروه اضافه کنید.",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton(
                            "🔙 بازگشت به مدیریت زمان‌بندی",
                            callback_data=json.dumps({"action": "schedule_management"})
                        )
                    ]])
                )
                user_data.pop("scheduling", None)
                return
            
            # Create combined keyboard with channels and groups
            combined_keyboard = []
            
            # Add channels
            if conf["channels"]:
                channels_keyboard = create_channels_keyboard(conf["channels"], "schedule_to")
                combined_keyboard.extend(channels_keyboard)
            
            # Add groups
            if conf["groups"]:
                groups_keyboard = create_groups_keyboard(conf["groups"], "schedule_to")
                combined_keyboard.extend(groups_keyboard)
            
            combined_keyboard.append([
                InlineKeyboardButton(
                    "🔙 بازگشت به مدیریت زمان‌بندی",
                    callback_data=json.dumps({"action": "schedule_management"})
                )
            ])
            
            time_str = scheduled_time.strftime("%Y-%m-%d %H:%M:%S")
            await update.message.reply_text(
                f"پیام برای {time_str} زمان‌بندی خواهد شد.\n"
                "لطفاً کانال یا گروه مقصد را انتخاب کنید:",
                reply_markup=InlineKeyboardMarkup(combined_keyboard)
            )
        except ValueError:
            await update.message.reply_text(
                "فرمت زمان نامعتبر است. از دقیقه (مثلاً 30) یا فرمت HH:MM (مثلاً 14:30) استفاده کنید.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        "🔙 بازگشت به مدیریت زمان‌بندی",
                        callback_data=json.dumps({"action": "schedule_management"})
                    )
                ]])
            )
        except Exception as e:
            logger.error(f"Error scheduling message: {e}")
            await update.message.reply_text(config.MESSAGES["error"].format(str(e)))
            user_data.pop("scheduling_setup", None)
    
    # Handle sending message
    elif user_data.get("sending_to"):
        try:
            target = user_data["sending_to"]
            target_id = target["id"]
            target_type = target["type"]  # 'channel' or 'group'
            
            # Send message to target
            await context.bot.send_message(chat_id=target_id, text=text)
            
            # Get target name
            conf = config.init_config()
            if target_type == "channel":
                target_dict = conf["channels"]
            else:
                target_dict = conf["groups"]
            
            target_name = target_dict.get(str(target_id), "Unknown")
            
            # Success message
            await update.message.reply_text(
                f"✅ پیام با موفقیت به {target_type} «{target_name}» ارسال شد!",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        "🔙 بازگشت به منوی اصلی",
                        callback_data=json.dumps({"action": "main_menu"})
                    )
                ]])
            )
            
            # Clear state
            user_data.pop("sending_to", None)
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            await update.message.reply_text(
                config.MESSAGES["error"].format(str(e)),
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        "🔙 بازگشت به منوی اصلی",
                        callback_data=json.dumps({"action": "main_menu"})
                    )
                ]])
            )
            user_data.pop("sending_to", None)
    
    # Handle scheduling message content
    elif user_data.get("scheduling") and user_data["scheduling"].get("state") == "entering_text":
        try:
            scheduling_data = user_data["scheduling"]
            target_id = scheduling_data["target"]["id"]
            target_type = scheduling_data["target"]["type"]
            scheduled_time = scheduling_data["time"]
            
            # Create scheduled message data
            from bot.utils import generate_unique_id
            message_data = {
                "id": generate_unique_id(),
                "text": text,
                "time": scheduled_time.strftime("%Y-%m-%d %H:%M:%S"),
                "target": {
                    "id": target_id,
                    "type": target_type
                }
            }
            
            # Schedule the message
            from bot.storage import add_scheduled_message
            add_scheduled_message(message_data)
            
            # Set up the job in scheduler
            schedule_one_time_message(message_data)
            
            # Get target name
            conf = config.init_config()
            if target_type == "channel":
                target_dict = conf["channels"]
            else:
                target_dict = conf["groups"]
            
            target_name = target_dict.get(str(target_id), "Unknown")
            
            # Success message
            time_str = scheduled_time.strftime("%Y-%m-%d %H:%M:%S")
            await update.message.reply_text(
                f"✅ پیام با موفقیت برای ارسال به {target_type} «{target_name}» در {time_str} زمان‌بندی شد!",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        "🔙 بازگشت به مدیریت زمان‌بندی",
                        callback_data=json.dumps({"action": "schedule_management"})
                    )
                ]])
            )
            
            # Clear state
            user_data.pop("scheduling", None)
        except Exception as e:
            logger.error(f"Error scheduling message: {e}")
            await update.message.reply_text(
                config.MESSAGES["error"].format(str(e)),
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        "🔙 بازگشت به مدیریت زمان‌بندی",
                        callback_data=json.dumps({"action": "schedule_management"})
                    )
                ]])
            )
            user_data.pop("scheduling", None)
    
    # No active state, show main menu
    else:
        keyboard = create_main_menu_keyboard()
        await update.message.reply_text(
            "لطفاً یکی از گزینه‌های منو را انتخاب کنید:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# Message Handlers for conversation states
@is_admin
async def new_chat_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message to new chat members"""
    # Load welcome messages
    conf = config.init_config()
    
    chat_id = str(update.effective_chat.id)
    
    # Check if we have a welcome message for this group
    if chat_id in conf["welcome_messages"]:
        welcome_message = conf["welcome_messages"][chat_id]
        
        # For each new member
        for member in update.message.new_chat_members:
            # Skip if the new member is the bot itself
            if member.id == context.bot.id:
                continue
            
            # Format welcome message with user's information
            formatted_message = welcome_message.replace("{name}", member.first_name)
            formatted_message = formatted_message.replace("{username}", f"@{member.username}" if member.username else member.first_name)
            formatted_message = formatted_message.replace("{chat}", update.effective_chat.title)
            
            # Send welcome message
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=formatted_message,
                parse_mode=ParseMode.HTML
            )
