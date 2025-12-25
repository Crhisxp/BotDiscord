"""
Comandos generales del bot
"""
import discord
from discord.ext import commands
from utils.logger import logger

class General(commands.Cog):
    """Cog para comandos generales"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command(name='ping')
    async def ping(self, ctx: commands.Context):
        """Muestra la latencia del bot"""
        latency = round(self.bot.latency * 1000)
        await ctx.send(f'🏓 Pong! Latencia: **{latency}ms**')
    
    @commands.command(name='help', aliases=['ayuda', 'comandos'])
    async def help_command(self, ctx: commands.Context):
        """Muestra la lista de comandos disponibles"""
        embed = discord.Embed(
            title="🎵 Bot de Música - Comandos",
            description="Lista de comandos disponibles",
            color=discord.Color.blue()
        )
        
        # Comandos de música
        music_commands = """
        `!play <canción>` - Reproduce una canción
        `!pause` - Pausa la música
        `!resume` - Reanuda la música
        `!skip` - Salta la canción actual
        `!stop` - Detiene la reproducción
        `!join` - Conecta el bot al canal de voz
        `!leave` - Desconecta el bot
        `!volume <0-100>` - Ajusta el volumen
        """
        
        embed.add_field(
            name="🎵 Música",
            value=music_commands,
            inline=False
        )
        
        # Comandos generales
        general_commands = """
        `!ping` - Muestra la latencia
        `!help` - Muestra este mensaje
        """
        
        embed.add_field(
            name="⚙️ General",
            value=general_commands,
            inline=False
        )
        
        embed.set_footer(text="Usa ! antes de cada comando")
        
        await ctx.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        """Maneja errores de comandos"""
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('❌ Comando no encontrado. Usa `!help` para ver los comandos disponibles')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'❌ Falta un argumento requerido: `{error.param.name}`')
        else:
            logger.error(f"Error en comando: {error}")
            await ctx.send('❌ Ocurrió un error al ejecutar el comando')

async def setup(bot: commands.Bot):
    """Carga el cog"""
    await bot.add_cog(General(bot))
