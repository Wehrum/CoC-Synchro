from dotenv import load_dotenv
import os
import re

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
ENDPOINT = os.getenv('ENDPOINT')
FORM_KEY = os.getenv('FORM_KEY')

image_loading="https://github.com/Wehrum/CoC-Synchro/blob/connor/changes/program/loader.gif?raw=true"
image_checkmark="https://github.com/Wehrum/CoC-Synchro/blob/connor/changes/program/OIP.jpg?raw=true"

def escape_special_chars(s):
    return re.sub(r'(?<!\\)([\'"\\()])', r'\\\1', s)