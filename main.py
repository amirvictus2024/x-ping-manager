
#!/usr/bin/env python3
"""
Telegram Channel Management Bot
A comprehensive bot for managing Telegram channels with features like scheduling,
inline buttons, and multi-channel support.
"""
import logging
from bot.bot import start_bot

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # توکن ربات تلگرام به صورت مستقیم در فایل
    token = "8069263840:AAF2JTFJl6cfo7z1rU_CegYnCNJH6bLXcg0"  # توکن ربات شما
    
    # Start the bot
    logger.info("Starting Channel Management Bot...")
    start_bot(token)
