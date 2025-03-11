"""
Storage module for saving and loading bot data
"""
import json
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

# Create data directory if it doesn't exist
data_dir = Path('data')
data_dir.mkdir(exist_ok=True)

# File for storing bot data
DATA_FILE = data_dir / 'bot_data.json'

# Default data structure
DEFAULT_DATA = {
    "scheduled_messages": [],
    "auto_posts": [],
    "polls": []
}

def load_data():
    """Load data from storage file"""
    if not DATA_FILE.exists():
        return DEFAULT_DATA
    
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError:
        logger.warning(f"Error decoding JSON from {DATA_FILE}. Using default data.")
        return DEFAULT_DATA
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        return DEFAULT_DATA

def save_data(data):
    """Save data to storage file"""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        logger.error(f"Error saving data: {e}")
        return False

def add_scheduled_message(message_data):
    """Add a scheduled message to storage"""
    data = load_data()
    data["scheduled_messages"].append(message_data)
    return save_data(data)

def remove_scheduled_message(message_id):
    """Remove a scheduled message from storage"""
    data = load_data()
    data["scheduled_messages"] = [msg for msg in data["scheduled_messages"] if msg["id"] != message_id]
    return save_data(data)

def add_auto_post(post_data):
    """Add an automatic post to storage"""
    data = load_data()
    data["auto_posts"].append(post_data)
    return save_data(data)

def remove_auto_post(post_id):
    """Remove an automatic post from storage"""
    data = load_data()
    data["auto_posts"] = [post for post in data["auto_posts"] if post["id"] != post_id]
    return save_data(data)

def add_poll(poll_data):
    """Add a poll to storage"""
    data = load_data()
    data["polls"].append(poll_data)
    return save_data(data)

def get_poll(poll_id):
    """Get a poll by its ID"""
    data = load_data()
    for poll in data["polls"]:
        if poll["id"] == poll_id:
            return poll
    return None

def update_poll(poll_data):
    """Update a poll in storage"""
    data = load_data()
    for i, poll in enumerate(data["polls"]):
        if poll["id"] == poll_data["id"]:
            data["polls"][i] = poll_data
            save_data(data)
            return True
    return False
