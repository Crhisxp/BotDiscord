import discord
from discord.ext import commands
import yt_dlp
import asyncio
import os

# Configuración de intents
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Configuración de yt-dlp
YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'quiet': True,
    'no_warnings': True,
    'default_search': 'ytsearch',
    'source_address': '0.0.0.0'
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

@bot.event
async def on_ready():
    print(f'{bot.user} está listo!')

@bot.command()
async def join(ctx):
    """Conecta el bot a tu canal de voz"""
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f'✅ Conectado a {channel}')
    else:
        await ctx.send('❌ Debes estar en un canal de voz')

@bot.command()
async def play(ctx, *, search):
    """Reproduce música desde YouTube"""
    voice_client = ctx.guild.voice_client
    
    if not voice_client:
        if ctx.author.voice:
            voice_client = await ctx.author.voice.channel.connect()
        else:
            await ctx.send('❌ Debes estar en un canal de voz')
            return
    
    await ctx.send(f'🔍 Buscando: {search}')
    
    try:
        loop = asyncio.get_event_loop()
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = await loop.run_in_executor(None, lambda: ydl.extract_info(f"ytsearch:{search}", download=False))
            if 'entries' in info:
                info = info['entries'][0]
            
            url = info['url']
            title = info['title']
        
        voice_client.play(discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS))
        await ctx.send(f'🎵 Reproduciendo: {title}')
    except Exception as e:
        await ctx.send(f'❌ Error al reproducir: {str(e)}')

@bot.command()
async def pause(ctx):
    """Pausa la música actual"""
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send('⏸️ Música pausada')
    else:
        await ctx.send('❌ No hay música reproduciéndose')

@bot.command()
async def resume(ctx):
    """Reanuda la música pausada"""
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send('▶️ Música reanudada')
    else:
        await ctx.send('❌ La música no está pausada')

@bot.command()
async def stop(ctx):
    """Detiene la música y desconecta el bot"""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send('⏹️ Desconectado')
    else:
        await ctx.send('❌ No estoy conectado a ningún canal')

@bot.command()
async def skip(ctx):
    """Salta la canción actual"""
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send('⏭️ Canción saltada')
    else:
        await ctx.send('❌ No hay música reproduciéndose')

# Obtener token desde variable de entorno
TOKEN = os.getenv('DISCORD_TOKEN')

if TOKEN is None:
    print("ERROR: No se encontró el token. Asegúrate de configurar DISCORD_TOKEN")
else:
    bot.run(TOKEN)

