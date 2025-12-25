import os
from dotenv import load_dotenv

load_dotenv()

# Discord settings
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('PREFIX', '!')

# Lavalink settings
LAVALINK_HOST = os.getenv('LAVALINK_HOST', 'lavalink.jirayu.net')
LAVALINK_PORT = int(os.getenv('LAVALINK_PORT', 13592))
LAVALINK_PASSWORD = os.getenv('LAVALINK_PASSWORD', 'youshallnotpass')
LAVALINK_SECURE = os.getenv('LAVALINK_SECURE', 'False').lower() == 'true'

# Bot settings
MAX_QUEUE_SIZE = 100
DEFAULT_VOLUME = 50
TIMEOUT_SECONDS = 300  # 5 minutos de inactividad
