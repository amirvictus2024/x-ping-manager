"""
Scheduler module for handling timed tasks
"""
import logging
import uuid
from datetime import datetime
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.memory import MemoryJobStore
from telegram import InlineKeyboardMarkup
from bot.storage import load_data, save_data
from bot.keyboards import build_inline_keyboard

logger = logging.getLogger(__name__)

# Global scheduler instance
scheduler = None

def setup_scheduler(bot):
    """Initialize and configure the scheduler"""
    global scheduler
    
    if scheduler is None:
        # Create scheduler
        jobstores = {
            'default': MemoryJobStore()
        }
        
        scheduler = BackgroundScheduler(jobstores=jobstores)
        scheduler.start()
        
        # Load and reschedule saved jobs
        load_scheduled_jobs(bot)
    
    return scheduler

def load_scheduled_jobs(bot):
    """Load and schedule saved jobs from storage"""
    data = load_data()
    current_time = datetime.now(pytz.utc)
    
    # Filter out expired scheduled messages
    valid_messages = []
    
    for msg in data.get("scheduled_messages", []):
        scheduled_time = datetime.fromisoformat(msg["time"])
        
        # If the message is still in the future, reschedule it
        if scheduled_time > current_time:
            job_id = msg["id"]
            
            # Create a job to send the message
            scheduler.add_job(
                send_scheduled_message,
                trigger=DateTrigger(run_date=scheduled_time),
                args=[bot, msg],
                id=job_id,
                replace_existing=True
            )
            
            valid_messages.append(msg)
    
    # Update storage with valid messages
    data["scheduled_messages"] = valid_messages
    
    # Reschedule automatic posts
    for autopost in data.get("auto_posts", []):
        job_id = autopost["id"]
        
        if autopost["type"] == "daily":
            # Daily post at specific time
            scheduler.add_job(
                send_auto_post,
                trigger=CronTrigger(hour=autopost["hour"], minute=autopost["minute"]),
                args=[bot, autopost],
                id=job_id,
                replace_existing=True
            )
        elif autopost["type"] == "weekly":
            # Weekly post on specific day at specific time
            scheduler.add_job(
                send_auto_post,
                trigger=CronTrigger(day_of_week=autopost["day"], hour=autopost["hour"], minute=autopost["minute"]),
                args=[bot, autopost],
                id=job_id,
                replace_existing=True
            )
    
    save_data(data)

async def send_scheduled_message(bot, message_data):
    """Send a scheduled message"""
    try:
        target_id = message_data["target"]["id"]
        text = message_data["text"]
        
        # Check if the target ID is a username (starts with @)
        chat_id = target_id
        
        # Check if there are inline buttons
        keyboard = None
        if "keyboard" in message_data and message_data["keyboard"]:
            parsed_keyboard = []
            for row in message_data["keyboard"]:
                keyboard_row = []
                for button in row:
                    keyboard_row.append(button)
                parsed_keyboard.append(keyboard_row)
            keyboard = InlineKeyboardMarkup(build_inline_keyboard(parsed_keyboard))
        
        # Send the message
        await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=keyboard,
            parse_mode='HTML'
        )
        
        # Remove this scheduled message from storage
        data = load_data()
        data["scheduled_messages"] = [msg for msg in data["scheduled_messages"] if msg["id"] != message_data["id"]]
        save_data(data)
        
        logger.info(f"Sent scheduled message {message_data['id']} to {chat_id}")
    except Exception as e:
        logger.error(f"Error sending scheduled message: {e}")

async def send_auto_post(bot, post_data):
    """Send an automatic post"""
    try:
        target_id = post_data["target"]["id"]
        text = post_data["text"]
        
        # Check if the target ID is a username (starts with @)
        chat_id = target_id
        
        # Check if there are inline buttons
        keyboard = None
        if "keyboard" in post_data and post_data["keyboard"]:
            parsed_keyboard = []
            for row in post_data["keyboard"]:
                keyboard_row = []
                for button in row:
                    keyboard_row.append(button)
                parsed_keyboard.append(keyboard_row)
            keyboard = InlineKeyboardMarkup(build_inline_keyboard(parsed_keyboard))
        
        # Send the message
        await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=keyboard,
            parse_mode='HTML'
        )
        
        logger.info(f"Sent automatic post {post_data['id']} to {chat_id}")
    except Exception as e:
        logger.error(f"Error sending automatic post: {e}")

def schedule_one_time_message(message_data):
    """Add a one-time scheduled message to the scheduler"""
    global scheduler
    
    try:
        # Generate a unique ID for this scheduled message
        job_id = str(uuid.uuid4())
        message_data["id"] = job_id
        
        # Convert scheduled_time to datetime object if it's not already
        if isinstance(message_data["time"], str):
            scheduled_time = datetime.fromisoformat(message_data["time"])
        else:
            scheduled_time = message_data["time"]
            message_data["time"] = scheduled_time.isoformat()
        
        # Add job to scheduler
        scheduler.add_job(
            send_scheduled_message,
            trigger=DateTrigger(run_date=scheduled_time),
            args=[scheduler._executors['default']._scheduler._bot, message_data],
            id=job_id,
            replace_existing=True
        )
        
        # Save to storage
        data = load_data()
        data["scheduled_messages"].append(message_data)
        save_data(data)
        
        logger.info(f"Scheduled message {job_id} for {scheduled_time}")
        return job_id
    except Exception as e:
        logger.error(f"Error scheduling message: {e}")
        return None

def cancel_scheduled_job(job_id):
    """Cancel a scheduled message by its ID"""
    global scheduler
    
    try:
        # Remove from scheduler
        scheduler.remove_job(job_id)
        
        # Remove from storage
        data = load_data()
        data["scheduled_messages"] = [msg for msg in data["scheduled_messages"] if msg["id"] != job_id]
        save_data(data)
        
        logger.info(f"Cancelled scheduled message {job_id}")
        return True
    except Exception as e:
        logger.error(f"Error cancelling scheduled message: {e}")
        return False

def schedule_recurring_message(post_data):
    """Add a recurring message to the scheduler"""
    global scheduler
    
    try:
        # Generate a unique ID for this autopost
        job_id = str(uuid.uuid4())
        post_data["id"] = job_id
        
        if post_data["type"] == "daily":
            # Daily post at specific time
            scheduler.add_job(
                send_auto_post,
                trigger=CronTrigger(hour=post_data["hour"], minute=post_data["minute"]),
                args=[scheduler._executors['default']._scheduler._bot, post_data],
                id=job_id,
                replace_existing=True
            )
        elif post_data["type"] == "weekly":
            # Weekly post on specific day at specific time
            scheduler.add_job(
                send_auto_post,
                trigger=CronTrigger(day_of_week=post_data["day"], hour=post_data["hour"], minute=post_data["minute"]),
                args=[scheduler._executors['default']._scheduler._bot, post_data],
                id=job_id,
                replace_existing=True
            )
        
        # Save to storage
        data = load_data()
        data["auto_posts"].append(post_data)
        save_data(data)
        
        logger.info(f"Set up recurring post {job_id}")
        return job_id
    except Exception as e:
        logger.error(f"Error setting up recurring post: {e}")
        return None

def cancel_autopost(job_id):
    """Cancel an automatic post by its ID"""
    global scheduler
    
    try:
        # Remove from scheduler
        scheduler.remove_job(job_id)
        
        # Remove from storage
        data = load_data()
        data["auto_posts"] = [post for post in data["auto_posts"] if post["id"] != job_id]
        save_data(data)
        
        logger.info(f"Cancelled automatic post {job_id}")
        return True
    except Exception as e:
        logger.error(f"Error cancelling automatic post: {e}")
        return False
