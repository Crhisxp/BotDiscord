import discord
from discord.ext import commands
import platform
from datetime import datetime

class General(commands.Cog):
    """Comandos generales del bot"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.start_time = datetime.now()
    
    @commands.command(name='ping')
    async def ping(self, ctx: commands.Context):
        """Muestra la latencia del bot"""
        latency = round(self.bot.latency * 1000)
        
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latencia: **{latency}ms**",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='help', aliases=['ayuda'])
    async def help(self, ctx: commands.Context):
        """Muestra la ayuda del bot"""
        embed = discord.Embed(
            title="🎵 Bot de Música - Ayuda",
            description="Bot de música con soporte para YouTube, Spotify, SoundCloud y más.",
            color=discord.Color.blue()
        )
        
        music_commands = """
        `!play <canción>` - Reproduce una canción
        `!pause` - Pausa/reanuda la reproducción
        `!skip` - Salta a la siguiente canción
        `!stop` - Detiene la música y limpia la cola
        `!queue` - Muestra la cola de reproducción
        `!nowplaying` - Muestra la canción actual
        `!volume <0-100>` - Ajusta el volumen
        `!disconnect` - Desconecta el bot
        """
        
        general_commands = """
        `!ping` - Muestra la latencia
        `!info` - Información del bot
        `!help` - Muestra esta ayuda
        """
        
        embed.add_field(name="🎵 Comandos de Música", value=music_commands, inline=False)
        embed.add_field(name="⚙️ Comandos Generales", value=general_commands, inline=False)
        embed.set_footer(text="Bot creado con Wavelink + Lavalink")
        
        await ctx.send(embed=embed)
    
    @commands.command(name='info')
    async def info(self, ctx: commands.Context):
        """Información del bot"""
        uptime = datetime.now() - self.start_time
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        embed = discord.Embed(
            title="ℹ️ Información del Bot",
            color=discord.Color.blue()
        )
        
        embed.add_field(name="Servidores", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="Usuarios", value=len(self.bot.users), inline=True)
        embed.add_field(name="Uptime", value=f"{hours}h {minutes}m {seconds}s", inline=True)
        embed.add_field(name="Python", value=platform.python_version(), inline=True)
        embed.add_field(name="Discord.py", value=discord.__version__, inline=True)
        embed.add_field(name="Latencia", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))
