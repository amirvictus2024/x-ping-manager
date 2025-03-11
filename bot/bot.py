"""
Main bot module with initialization and core functionality
"""
import logging
from telegram.ext import (
    Application, 
    CommandHandler, 
    CallbackQueryHandler,
    MessageHandler, 
    filters
)

from bot.handlers import (
    start, help_command, add_admin_command, add_channel, del_channel, list_channels,
    add_group, del_group, list_groups, send_message_command,
    schedule_message, list_scheduled, cancel_schedule,
    set_autopost, list_autopost, delete_autopost,
    set_welcome, create_poll, get_members,
    button_callback, new_chat_members, handle_text_message
)
from bot.scheduler import setup_scheduler
from bot.storage import load_data
import config

logger = logging.getLogger(__name__)

def start_bot(token):
    """Initialize and start the bot"""
    # Initialize configuration
    config.init_config()
    
    # Load stored data
    data = load_data()
    
    # Create the Application
    application = Application.builder().token(token).build()
    
    # Setup scheduler
    scheduler = setup_scheduler(application.bot)
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("addadmin", add_admin_command))
    
    # Channel management commands
    application.add_handler(CommandHandler("addchannel", add_channel))
    application.add_handler(CommandHandler("delchannel", del_channel))
    application.add_handler(CommandHandler("channels", list_channels))
    
    # Group management commands
    application.add_handler(CommandHandler("addgroup", add_group))
    application.add_handler(CommandHandler("delgroup", del_group))
    application.add_handler(CommandHandler("groups", list_groups))
    
    # Message sending commands
    application.add_handler(CommandHandler("send", send_message_command))
    
    # Scheduling commands
    application.add_handler(CommandHandler("schedule", schedule_message))
    application.add_handler(CommandHandler("schedulelist", list_scheduled))
    application.add_handler(CommandHandler("cancelschedule", cancel_schedule))
    
    # Auto-posting commands
    application.add_handler(CommandHandler("autopost", set_autopost))
    application.add_handler(CommandHandler("autopostlist", list_autopost))
    application.add_handler(CommandHandler("delautopost", delete_autopost))
    
    # Other features
    application.add_handler(CommandHandler("welcome", set_welcome))
    application.add_handler(CommandHandler("poll", create_poll))
    application.add_handler(CommandHandler("getmembers", get_members))
    
    # Callback query handler for inline buttons
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Welcome message handler
    application.add_handler(
        MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_chat_members)
    )
    
    # Text message handler for conversational states
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message)
    )
    
    # Start the Bot
    application.run_polling()
    
    return application
