import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
from utils.logger import setup_logger

# Cargar variables de entorno
load_dotenv()

# Configurar logger
logger = setup_logger()

# Configurar intents
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True

# Crear bot
bot = commands.Bot(
    command_prefix=os.getenv('PREFIX', '!'),
    intents=intents,
    help_command=None
)

@bot.event
async def on_ready():
    """Evento cuando el bot está listo"""
    logger.info(f'Bot conectado como {bot.user.name}')
    logger.info(f'ID: {bot.user.id}')
    logger.info(f'Servidores: {len(bot.guilds)}')
    
    # Establecer estado
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name=f"{os.getenv('PREFIX', '!')}play"
        )
    )
    logger.info('Bot listo para usar!')

@bot.event
async def on_command_error(ctx, error):
    """Manejo global de errores"""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Comando no encontrado. Usa `!help` para ver los comandos disponibles.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Falta un argumento requerido: `{error.param.name}`")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ No tienes permisos para usar este comando.")
    else:
        logger.error(f'Error en comando: {error}')
        await ctx.send(f"❌ Ocurrió un error: {str(error)}")

async def load_extensions():
    """Cargar todas las extensiones (cogs)"""
    extensions = ['cogs.music', 'cogs.general']
    
    for extension in extensions:
        try:
            await bot.load_extension(extension)
            logger.info(f'✓ Cargado: {extension}')
        except Exception as e:
            logger.error(f'✗ Error cargando {extension}: {e}')

async def main():
    """Función principal"""
    async with bot:
        await load_extensions()
        await bot.start(os.getenv('DISCORD_TOKEN'))

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Bot detenido manualmente')
