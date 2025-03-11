"""
Admin authentication and permission handling
"""
import logging
import functools
from telegram import Update
from telegram.ext import ContextTypes
import config

logger = logging.getLogger(__name__)

def is_admin(func):
    """Decorator to check if the user is an admin"""
    @functools.wraps(func)
    async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id
        conf = config.init_config()
        
        # First try to set admin with user ID 6712954701 if admin list is empty
        if not conf["admin_ids"]:
            # Set the predefined admin ID
            predefined_admin_id = 6712954701
            conf["admin_ids"].append(predefined_admin_id)
            config.save_config(conf)
            logger.info(f"Added predefined admin {predefined_admin_id}")
            
            # If current user is the predefined admin, inform them
            if user_id == predefined_admin_id:
                await update.message.reply_text(
                    "شما به عنوان مدیر ربات تنظیم شده‌اید."
                )
        
        if user_id in conf["admin_ids"]:
            return await func(update, context, *args, **kwargs)
        else:
            # Log unauthorized access attempt
            logger.warning(f"Unauthorized access attempt by user {user_id}")
            
            # Inform the user
            if update.message:
                await update.message.reply_text(config.MESSAGES["not_admin"])
            elif update.callback_query:
                await update.callback_query.answer(config.MESSAGES["not_admin"])
            
            return None
    
    return wrapped

def add_admin(user_id: int) -> bool:
    """Add a user to the admin list"""
    try:
        conf = config.init_config()
        
        if user_id not in conf["admin_ids"]:
            conf["admin_ids"].append(user_id)
            config.save_config(conf)
            logger.info(f"Added user {user_id} as admin")
            return True
        else:
            logger.info(f"User {user_id} is already an admin")
            return False
    except Exception as e:
        logger.error(f"Error adding admin: {e}")
        return False

def remove_admin(user_id: int) -> bool:
    """Remove a user from the admin list"""
    try:
        conf = config.init_config()
        
        if user_id in conf["admin_ids"]:
            # Don't allow removing the last admin
            if len(conf["admin_ids"]) <= 1:
                logger.warning("Attempted to remove the last admin")
                return False
            
            conf["admin_ids"].remove(user_id)
            config.save_config(conf)
            logger.info(f"Removed user {user_id} from admins")
            return True
        else:
            logger.warning(f"Attempted to remove non-admin user {user_id}")
            return False
    except Exception as e:
        logger.error(f"Error removing admin: {e}")
        return False

def get_admins() -> list:
    """Get the list of admin user IDs"""
    try:
        conf = config.init_config()
        return conf["admin_ids"]
    except Exception as e:
        logger.error(f"Error getting admins: {e}")
        return []
