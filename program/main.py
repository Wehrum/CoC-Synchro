# bot.py
import os
import subprocess
import re
import discord
import time
from dotenv import load_dotenv
from discord import Intents
from discord import app_commands

MY_GUILD = discord.Object(id=349593031579533312)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

intents = discord.Intents.all()
client = MyClient(intents=intents)

@client.tree.command()
async def hello(interaction: discord.Interaction):
    """Says hello!"""
    await interaction.response.send_message(f'Hi, {interaction.user.mention}')

@client.tree.command()
@app_commands.describe(
    first_value='The first value you want to add something to',
    second_value='The value you want to add to the first value',
)
async def add(interaction: discord.Interaction, first_value: int, second_value: int):
    """Adds two numbers together."""
    await interaction.response.send_message(f'{first_value} + {second_value} = {first_value + second_value}')

# The rename decorator allows us to change the display of the parameter on Discord.
# In this example, even though we use `text_to_send` in the code, the client will use `text` instead.
# Note that other decorators will still refer to it as `text_to_send` in the code.
@client.tree.command()
@app_commands.rename(text_to_send='text')
@app_commands.describe(text_to_send='Text to send in CoC chat')
async def relay(interaction: discord.Interaction, text_to_send: str):
    """Sends a message to the Clash of Clans chat."""
    await interaction.response.send_message(f'Sent: "{text_to_send}" to CoC chat')
    open_chat()
    type_message(text_to_send)
    # Send an enter key event
    command = "adb shell input keyevent KEYCODE_ENTER"
    subprocess.call(["/bin/bash", "-c", command])

@client.tree.command()
@app_commands.describe(text_to_send='Text to send in CoC clan mail')
async def mail(interaction: discord.Interaction, text_to_send: str):
    """Sends a mail to the Clash of Clans clan mail system."""
    await interaction.response.send_message(f'Sent: "{text_to_send}" to CoC clan mail')
    open_clan_mail()
    type_message(text_to_send)
    # Hit Send
    command = f"adb shell input tap 1191 152"
    subprocess.call(["/bin/bash", "-c", command])

def escape_special_chars(s):
    return re.sub(r'(?<!\\)([\'"\\()])', r'\\\1', s)

def open_clan_mail():
    # Open Menu
    command = f"adb shell input tap 76 65"
    subprocess.call(["/bin/bash", "-c", command])
    time.sleep(1)

    # Open My Clan
    command = f"adb shell input tap 815 72"
    subprocess.call(["/bin/bash", "-c", command])
    time.sleep(1)
    
    # Open Send Mail
    command = f"adb shell input tap 1272 736"
    subprocess.call(["/bin/bash", "-c", command])
    time.sleep(1)
    
    # Open the input box
    command = f"adb shell input tap 1191 152"
    subprocess.call(["/bin/bash", "-c", command])
    time.sleep(1)

def open_chat():
    # Open the chat menu
    command = f"adb shell input tap 25 423"
    subprocess.call(["/bin/bash", "-c", command])
    
    # Open the input box
    command = f"adb shell input tap 677 1032"
    subprocess.call(["/bin/bash", "-c", command])

def type_message(message):
    # Escape special characters in the message
    message = escape_special_chars(message)
    
    # Replace spaces with %s
    message = message.replace(" ", "\%s")

    # Execute the command
    command = f'adb shell input text "{message}"'
    print(command)
    subprocess.call(["/bin/bash", "-c", command])


# @client.event
# async def on_ready():
#     for guild in client.guilds:
#         if guild.name == GUILD:
#             break

#     print(
#         f'{client.user} is connected to the following guild:\n'
#         f'{guild.name}(id: {guild.id})'
#     )

# @client.command()
# async def relay(ctx, *, message): # Define the relay command
#     if ctx.author == client.user:
#         return
    
#     print("Message received")
#     await ctx.send(f'Sending message: "{message}" to Clash')
#     type_message(message)

client.run(TOKEN)




# from PIL import Image
# from pytesseract import pytesseract

# # Define path to tesseract
# image = Image.open('sample-image/clash.png')

# text = pytesseract.image_to_string(image, lang='clash')
# print("text")

# count = text.count("the")
# print(f"{count}")