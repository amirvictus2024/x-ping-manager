#!/usr/bin/env python3
"""
Telegram Channel Management Bot
A comprehensive bot for managing Telegram channels with features like scheduling,
inline buttons, and multi-channel support.
"""
import logging
import os
from bot.bot import start_bot

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Check if the token is available in the environment
    token = os.getenv("8069263840:AAF2JTFJl6cfo7z1rU_CegYnCNJH6bLXcg0")
    if not token:
        logger.error("No TELEGRAM_BOT_TOKEN found in environment variables!")
        exit(1)
    
    # Start the bot
    logger.info("Starting Channel Management Bot...")
    start_bot(token)
