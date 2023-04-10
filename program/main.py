# bot.py
import subprocess
import discord
import time
import vars
from discord import Intents
from discord import app_commands


MY_GUILD = discord.Object(id=vars.GUILD)

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

debug=True

# Used for debugging
@client.tree.command()
async def hello(interaction: discord.Interaction):
    """Says hello!"""
    with open("loader.gif", "rb") as f:
        file = discord.File(f)
    await interaction.response.send_message(f'Loading, {interaction.user.mention}', file=file)
    message = await interaction.original_response()
    time.sleep(2)
    with open("OIP.jpg", "rb") as f:
        file = discord.File(f)
    await interaction.followup.delete_message(message.id)
    await interaction.channel.send(f'Loading, {interaction.user.mention}', file=file)

# Send Clash of Clans Chat Messages
@client.tree.command()
@app_commands.rename(text_to_send='message')
@app_commands.describe(text_to_send='Text to send in CoC chat')
async def relay(interaction: discord.Interaction, text_to_send: str):
    """Sends a message to the Clash of Clans chat."""

    await interaction.response.send_message(f'Sending: "{text_to_send}" to CoC chat!', 
                                            ephemeral=True, 
                                            embed=embed_image(vars.image_loading))
    open_chat()
    type_message(text_to_send)
    
    message = await interaction.original_response()
    
    # Send an enter key event
    command = "adb shell input keyevent KEYCODE_ENTER"
    subprocess.call(["/bin/bash", "-c", command])
    
    await message.edit(content=f'Sent: "{text_to_send}" to CoC chat!',
                       embed=embed_image(vars.image_checkmark))

# Send Clash of Clans Mails
@client.tree.command()
@app_commands.rename(text_to_send='message')
@app_commands.describe(text_to_send='Text to send in CoC clan mail')
async def mail(interaction: discord.Interaction, text_to_send: str):
    """Sends a mail to the Clash of Clans clan mail system."""
    
    await interaction.response.send_message(f'Sending: "{text_to_send}" to CoC clan mail!', 
                                            ephemeral=True, 
                                            embed=embed_image(vars.image_loading))
    
    message = await interaction.original_response()
    open_clan_mail()
    type_message(text_to_send)
    
    # Hit Send
    command = f"adb shell input tap 1180 500"
    subprocess.call(["/bin/bash", "-c", command])
    
    await message.edit(content=f'Sent: "{text_to_send}" to CoC clan mail!', 
                       embed=embed_image(vars.image_checkmark))
    
def embed_image(image):
    embed = discord.Embed()
    embed.set_image(url=image)
    return embed

def open_clan_mail():
    # Open Menu
    command = f"adb shell input tap 76 65"
    if debug is True:
        print(f'Debug: {command}')
    # subprocess.call(["/bin/bash", "-c", command])
    response = adb_command(command)
    if (response != 0):
        print("There was an error")
        return
    time.sleep(1)

    # Open My Clan
    command = f"adb shell input tap 815 72"
    if debug is True:
        print(f'Debug: {command}')
    subprocess.call(["/bin/bash", "-c", command])
    time.sleep(1)
    
    # Open Send Mail
    command = f"adb shell input tap 1272 736"
    if debug is True:
        print(f'Debug: {command}')
    subprocess.call(["/bin/bash", "-c", command])
    time.sleep(1)
    
    # Open the input box
    command = f"adb shell input tap 950 280"
    if debug is True:
        print(f'Debug: {command}')
    subprocess.call(["/bin/bash", "-c", command])
    time.sleep(1)

def open_chat():
    # Open the chat menu
    command = f"adb shell input tap 25 423"
    if debug is True:
        print(f'Debug: {command}')
    subprocess.call(["/bin/bash", "-c", command])
    time.sleep(1)
    
    # Open the input box
    command = f"adb shell input tap 677 1032"
    if debug is True:
        print(f'Debug: {command}')
    subprocess.call(["/bin/bash", "-c", command])
    time.sleep(1)
    
def type_message(message):
    # Escape special characters in the message
    message = vars.escape_special_chars(message)
    
    # Replace spaces with %s
    message = message.replace(" ", "\%s")

    # Execute the command
    command = f'adb shell input text "{message}"'
    if debug is True:
        print(f'Debug: {command}')
    subprocess.call(["/bin/bash", "-c", command])

def adb_command(command):
    print("command was called")
    response = subprocess.call(["/bin/bash", "-c", command])
    if debug is True:
        print(f'Debug: {command}')
    if (response != 0):
        print("test")
        return response
    return response

def get_screenshot():
    command = "adb exec-out screencap -p > screenshots/screen.png"
    adb_command(command)
    
    # convert screen.png -crop 500x500+100+200 screen.png 

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

client.run(vars.TOKEN)




# from PIL import Image
# from pytesseract import pytesseract

# # Define path to tesseract
# image = Image.open('sample-image/clash.png')

# text = pytesseract.image_to_string(image, lang='clash')
# print("text")

# count = text.count("the")
# print(f"{count}")