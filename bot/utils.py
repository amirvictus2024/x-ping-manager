"""
Utility functions for the bot
"""
import logging
import uuid
import json
from datetime import datetime
from telegram import InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from bot.storage import add_poll, save_data, load_data
from bot.keyboards import create_poll_keyboard

logger = logging.getLogger(__name__)

def generate_unique_id():
    """Generate a unique ID string"""
    return str(uuid.uuid4())

async def process_message_text(update: Update, context: ContextTypes.DEFAULT_TYPE, state_key, next_state):
    """Process message text based on the current state"""
    user_data = context.user_data
    message_text = update.message.text
    
    # Store the text and move to the next state
    user_data[state_key]["text"] = message_text
    user_data[state_key]["state"] = next_state
    
    return True

async def process_button_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process button text from user input"""
    user_data = context.user_data
    if "adding_buttons" in user_data:
        button_text = update.message.text
        
        # Store the text
        user_data["adding_buttons"]["current_text"] = button_text
        
        # Show button type options
        keyboard = [
            [
                {"text": "URL Button", "callback_data": json.dumps({"action": "add_button_url", "text": button_text})},
                {"text": "Callback Button", "callback_data": json.dumps({"action": "add_button_callback", "text": button_text})}
            ]
        ]
        
        await update.message.reply_text(
            f"Button text: '{button_text}'\n"
            "What type of button is this?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
        return True
    
    return False

async def process_button_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process button URL from user input"""
    user_data = context.user_data
    if "adding_buttons" in user_data and user_data["adding_buttons"]["state"] == "url":
        button_url = update.message.text
        button_text = user_data["adding_buttons"]["current_text"]
        
        # Add button to the list
        if "current_row" not in user_data["adding_buttons"]:
            user_data["adding_buttons"]["current_row"] = []
        
        user_data["adding_buttons"]["current_row"].append({
            "type": "url",
            "text": button_text,
            "url": button_url
        })
        
        # Show options for next steps
        keyboard = [
            [
                {"text": "Add Another Button (Same Row)", "callback_data": json.dumps({"action": "add_button_same_row"})},
                {"text": "Add Button (New Row)", "callback_data": json.dumps({"action": "add_row"})}
            ],
            [
                {"text": "Finish Adding Buttons", "callback_data": json.dumps({"action": "finish_buttons"})}
            ]
        ]
        
        await update.message.reply_text(
            f"Added URL button: '{button_text}' -> {button_url}\n"
            "What would you like to do next?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
        # Reset state
        user_data["adding_buttons"]["state"] = "next"
        
        return True
    
    return False

async def process_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process button callback data from user input"""
    user_data = context.user_data
    if "adding_buttons" in user_data and user_data["adding_buttons"]["state"] == "callback":
        callback_data = update.message.text
        button_text = user_data["adding_buttons"]["current_text"]
        
        # Add button to the list
        if "current_row" not in user_data["adding_buttons"]:
            user_data["adding_buttons"]["current_row"] = []
        
        user_data["adding_buttons"]["current_row"].append({
            "type": "callback",
            "text": button_text,
            "callback_data": callback_data
        })
        
        # Show options for next steps
        keyboard = [
            [
                {"text": "Add Another Button (Same Row)", "callback_data": json.dumps({"action": "add_button_same_row"})},
                {"text": "Add Button (New Row)", "callback_data": json.dumps({"action": "add_row"})}
            ],
            [
                {"text": "Finish Adding Buttons", "callback_data": json.dumps({"action": "finish_buttons"})}
            ]
        ]
        
        await update.message.reply_text(
            f"Added callback button: '{button_text}' with data: {callback_data}\n"
            "What would you like to do next?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
        # Reset state
        user_data["adding_buttons"]["state"] = "next"
        
        return True
    
    return False

async def process_poll_creation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process poll creation steps"""
    user_data = context.user_data
    message_text = update.message.text
    
    if "creating_poll" in user_data:
        poll_data = user_data["creating_poll"]
        
        if poll_data["state"] == "title":
            # Set poll title
            poll_data["title"] = message_text
            poll_data["state"] = "options"
            
            await update.message.reply_text(
                f"Poll title: '{message_text}'\n"
                "Now send me the first option for your poll."
            )
            return True
        
        elif poll_data["state"] == "options":
            # Add option to the list
            poll_data["options"].append(message_text)
            
            keyboard = [
                [
                    {"text": "Add Another Option", "callback_data": json.dumps({"action": "add_poll_option"})},
                    {"text": "Finish Poll", "callback_data": json.dumps({"action": "finish_poll"})}
                ]
            ]
            
            await update.message.reply_text(
                f"Added option: '{message_text}'\n"
                f"You now have {len(poll_data['options'])} options.\n"
                "Would you like to add another option or finish the poll?",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            
            # If we have enough options already, allow finishing
            if len(poll_data["options"]) >= 2:
                poll_data["state"] = "ready"
            
            return True
        
        elif poll_data["state"] == "target":
            # This shouldn't happen via text message, but just in case
            return True
    
    return False

async def create_and_send_poll(update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id):
    """Create and send a poll to the specified chat"""
    user_data = context.user_data
    
    if "creating_poll" in user_data:
        poll_data = user_data["creating_poll"]
        
        # Generate a unique ID for this poll
        poll_id = generate_unique_id()
        
        # Format options with initial count of 0
        formatted_options = []
        for option_text in poll_data["options"]:
            formatted_options.append({
                "text": option_text,
                "count": 0
            })
        
        # Create poll object
        poll = {
            "id": poll_id,
            "title": poll_data["title"],
            "options": formatted_options,
            "votes": {},
            "created_at": datetime.now().isoformat()
        }
        
        # Create keyboard with poll options
        keyboard = create_poll_keyboard(formatted_options, poll_id)
        
        # Send the poll
        poll_text = f"📊 Poll: {poll['title']}\n\n"
        for option in poll["options"]:
            poll_text += f"{option['text']}: {option['count']} votes\n"
        
        await context.bot.send_message(
            chat_id=chat_id,
            text=poll_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
        # Save the poll
        add_poll(poll)
        
        # Clear the state
        del user_data["creating_poll"]
        
        return True
    
    return False
