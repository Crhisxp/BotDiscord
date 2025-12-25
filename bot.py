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

# Cargar opus para audio
if not discord.opus.is_loaded():
    try:
        discord.opus.load_opus('libopus.so.0')
        logger.info("✓ Opus cargado correctamente")
    except Exception as e:
        logger.warning(f"⚠ No se pudo cargar opus automáticamente: {e}")
        logger.info("Intentando cargar opus por defecto...")

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
        
        # Verificar que opus está cargado
        if discord.opus.is_loaded():
            logger.info('✓ Opus está disponible para audio')
        else:
            logger.error('✗ Opus NO está cargado - la reproducción de audio puede fallar')
        
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
