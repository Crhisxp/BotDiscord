"""
Bot de Música para Discord
Punto de entrada principal
"""
import discord
from discord.ext import commands
import asyncio
from pathlib import Path

from config.settings import config
from utils.logger import logger

class MusicBot(commands.Bot):
    """Clase principal del bot"""
    
    def __init__(self):
        # Configurar intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        
        super().__init__(
            command_prefix=config.COMMAND_PREFIX,
            intents=intents,
            help_command=None  # Usamos nuestro comando de ayuda personalizado
        )
    
    async def setup_hook(self):
        """Carga los cogs al iniciar"""
        logger.info("Cargando extensiones...")
        
        # Cargar todos los cogs
        cogs_path = Path(__file__).parent / 'cogs'
        for cog_file in cogs_path.glob('*.py'):
            if cog_file.name != '__init__.py':
                cog_name = f'cogs.{cog_file.stem}'
                try:
                    await self.load_extension(cog_name)
                    logger.info(f"✓ Cargado: {cog_name}")
                except Exception as e:
                    logger.error(f"✗ Error cargando {cog_name}: {e}")
    
    async def on_ready(self):
        """Evento cuando el bot está listo"""
        logger.info(f'Bot conectado como {self.user}')
        logger.info(f'ID: {self.user.id}')
        logger.info(f'Servidores: {len(self.guilds)}')
        logger.info('Bot listo para usar!')
        
        # Establecer estado
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name="!help para comandos"
            )
        )
    
    async def on_guild_join(self, guild: discord.Guild):
        """Evento cuando el bot se une a un servidor"""
        logger.info(f"Bot agregado al servidor: {guild.name} (ID: {guild.id})")
    
    async def on_guild_remove(self, guild: discord.Guild):
        """Evento cuando el bot es removido de un servidor"""
        logger.info(f"Bot removido del servidor: {guild.name} (ID: {guild.id})")

async def main():
    """Función principal"""
    # Validar configuración
    try:
        config.validate()
    except ValueError as e:
        logger.error(f"Error de configuración: {e}")
        return
    
    # Crear y ejecutar bot
    bot = MusicBot()
    
    try:
        await bot.start(config.DISCORD_TOKEN)
    except KeyboardInterrupt:
        logger.info("Bot detenido por el usuario")
    except Exception as e:
        logger.error(f"Error crítico: {e}")
    finally:
        await bot.close()

if __name__ == '__main__':
    asyncio.run(main())
