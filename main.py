import os
import asyncio
from datetime import datetime
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener el token con validación
TOKEN = os.getenv('TOKEN')

# Validar que el token existe
if TOKEN is None:
    print("❌ ERROR: No se encontró TOKEN en el archivo .env")
    print("   Asegúrate de que el archivo .env contenga: TOKEN=tu_token_aqui")
    exit(1)

print(f"🔑 Token cargado (primeros 20 chars): {TOKEN[:20]}...")
print(f"📏 Longitud del token: {len(TOKEN)} caracteres")

# Configurar intents
intents = discord.Intents.default()
intents.message_content = True  # Importante para leer mensajes

# Crear bot
bot = commands.Bot(command_prefix='!', intents=intents)

start_time = datetime.now()

@bot.event
async def on_ready():
    print('\n' + '✅' * 30)
    print(f'🤖 Bot conectado como: {bot.user.name}')
    print(f'🆔 ID del bot: {bot.user.id}')
    print(f'📅 Conectado desde: {start_time.strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'📊 Servidores: {len(bot.guilds)}')
    print('🎮 El bot está en línea y listo para la insignia')
    print('⚠️  Mantén este script ejecutándose por al menos 24 horas')
    print('✅' * 30 + '\n')

    # Cambiar estado del bot (opcional)
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="para la insignia de desarrollador"
        )
    )

# Comando simple
@bot.command()
async def ping(ctx):
    """Responde con Pong!"""
    await ctx.send('🏓 Pong!')

# Comando para verificar estado
@bot.command()
async def status(ctx):
    """Muestra el estado del bot"""
    uptime = datetime.now() - start_time
    hours = int(uptime.total_seconds() // 3600)
    minutes = int((uptime.total_seconds() % 3600) // 60)

    await ctx.send(
        f"**Estado del Bot:**\n"
        f"✅ En línea desde hace: {hours}h {minutes}m\n"
        f"🤖 Nombre: {bot.user.name}\n"
        f"📊 Servidores: {len(bot.guilds)}\n"
        f"🎯 Objetivo: Insignia HypeSquad Bravery"
    )

# Tarea en segundo plano para monitoreo
async def background_task():
    await bot.wait_until_ready()
    while not bot.is_closed():
        # Mostrar estado cada 30 minutos
        uptime = datetime.now() - start_time
        hours = int(uptime.total_seconds() // 3600)

        print(f"⏰ [{datetime.now().strftime('%H:%M:%S')}] "
              f"Bot activo por {hours} horas...")

        # Si llevas más de 24 horas, mostrar mensaje especial
        if hours >= 24:
            print("🎉 ¡Llevas 24+ horas! Deberías poder reclamar la insignia.")
            print("   Ve a Discord → Configuración de Usuario → HypeSquad")

        await asyncio.sleep(1800)  # 30 minutos

@bot.event
async def on_connect():
    print("🔗 Conectado al Gateway de Discord...")
    bot.loop.create_task(background_task())

@bot.event
async def on_message(message):
    # También responder a mensajes directos (sin !)
    if message.author == bot.user:
        return

    # Responder a saludos
    if message.content.lower() in ['hola bot', 'hello bot', 'hey bot']:
        await message.channel.send(f'👋 ¡Hola {message.author.mention}!')

    # Procesar comandos normales
    await bot.process_commands(message)

try:
    print("🚀 Iniciando bot para insignia de desarrollador...")
    bot.run(TOKEN)
except KeyboardInterrupt:
    print("\n🛑 Bot detenido manualmente")
    print(f"⏱️  Tiempo total de actividad: {datetime.now() - start_time}")
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")
