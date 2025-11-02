# -*- coding: utf-8 -*-

# discord
import discord
from discord.ext import commands
from discord import app_commands
from discord.gateway import DiscordWebSocket

# system class
from identify import identify
import asyncio
import os

# miscellaneous
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
import json


with open("./config.json", encoding = "utf-8") as config:
    configData = json.load(config)

TOKEN = configData["TOKEN"]

DiscordWebSocket.identify = identify

colorama_init()
class color:
    HEADER = Fore.MAGENTA
    OKBLUE = Fore.BLUE
    OKGREEN = Fore.GREEN
    WARNING = Fore.YELLOW
    ENDC = Style.RESET_ALL

intents = discord.Intents.all()
intents.message_content = True
intents.members = True
intents.dm_messages = True
intents.emojis = True
intents.presences = True
intents.dm_reactions = True
intents.guild_messages = True
intents.guild_reactions = True
intents.guild_scheduled_events = True
intents.guild_typing = True
intents.moderation = True
intents.integrations = True
intents.voice_states = True
intents.guilds = True
intents.auto_moderation = True
intents.webhooks = True
intents.invites = True

prefix = commands.when_mentioned_or("!")

class T3mpur4Utils(commands.Bot):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(command_prefix = prefix, activity = discord.Activity(type = discord.ActivityType.watching, name = "private"), status = discord.Status.dnd, intents = intents)

    async def setup_hook(self):
        self.tree.copy_global_to(guild = discord.Object(id = 1398225801924837438))
        # await self.tree.sync()
        await self.tree.sync(guild = discord.Object(id = 1398225801924837438))

bot = T3mpur4Utils(intents = intents)

@bot.event
async def on_ready():
    await bot.wait_until_ready()
    print(f"{Fore.RED}Logged in as {color.WARNING}{bot.user} {color.HEADER}(ID: {bot.user.id}){color.ENDC}")
    print(f"{Fore.RED}Supporting {color.WARNING}{str(len(bot.guilds))} {Fore.RED}Servers{color.ENDC}")
bot.remove_command("help")

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f'Loaded {color.WARNING}{filename[:-3]}{color.ENDC}.')
    print('Done.')

async def main():
    async with bot:
        await load_extensions()
        # await bot.load_extension("cogs")
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())

