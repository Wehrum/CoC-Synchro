# bot.py
import os

import discord
from dotenv import load_dotenv
from discord import Intents

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = Intents.default()

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

client.run(TOKEN)






















# from PIL import Image
# from pytesseract import pytesseract

# # Define path to tesseract
# image = Image.open('sample-image/clash.png')

# text = pytesseract.image_to_string(image, lang='clash')
# print("text")

# count = text.count("the")
# print(f"{count}")