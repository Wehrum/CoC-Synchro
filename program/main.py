# bot.py
import os
import subprocess
import time
import re
import discord
from dotenv import load_dotenv
from discord import Intents

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = Intents.all()
client = discord.Client(intents=intents)



def escape_special_chars(s):
    return re.sub(r'(?<!\\)([\'"\\()])', r'\\\1', s)

def type_message(message):
    # Escape special characters in the message
    message = escape_special_chars(message)
    
    # Replace spaces with %s
    message = message.replace(" ", "\%s")
    
    # Open the chat menu
    command = f"adb shell input tap 25 423"
    subprocess.call(["/bin/bash", "-c", command])
    
    # Open the input box
    command = f"adb shell input tap 677 1032"
    subprocess.call(["/bin/bash", "-c", command])
    time.sleep(1)

    # Execute the command
    command = f'adb shell input text "{message}"'
    print(command)
    subprocess.call(["/bin/bash", "-c", command])

    # Send an enter key event
    command = "adb shell input keyevent KEYCODE_ENTER"
    subprocess.call(["/bin/bash", "-c", command])




@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    print("Message received")
    await message.channel.send(f'Sending message {message.content} to Clash')
    type_message(message.content)

client.run(TOKEN)






















# from PIL import Image
# from pytesseract import pytesseract

# # Define path to tesseract
# image = Image.open('sample-image/clash.png')

# text = pytesseract.image_to_string(image, lang='clash')
# print("text")

# count = text.count("the")
# print(f"{count}")