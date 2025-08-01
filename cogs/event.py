# -*- coding: utf-8 -*-

# discord
import discord
from discord import app_commands
from discord.ext import commands

# system class
import json
import aiofiles
import asyncio
import gzip
import shutil
import os
import datetime

LOG_DIR = "logs"

class Event(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.queue = asyncio.Queue()
        self.current_log_path = os.path.join(LOG_DIR, "latest.log")
        os.makedirs(LOG_DIR, exist_ok = True)
        self.task = bot.loop.create_task(self.writer_loop())

    def _should_rotate(self):
        return os.path.exists(self.current_log_path) and os.path.getsize(self.current_log_path) >= 100 * 1024

    def _rotate_and_compress(self):
        timestamp = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours = 8))).strftime("%Y%m%d_%H%M%S")
        archived_path = os.path.join(LOG_DIR, f"{timestamp}.log")
        os.rename(self.current_log_path, archived_path)
        with open(archived_path, 'rb') as f_in:
            with gzip.open(f"{archived_path}.gz", 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove(archived_path)

    async def writer_loop(self):
        while True:
            line = await self.queue.get()
            if self._should_rotate():
                self._rotate_and_compress()

            async with aiofiles.open(self.current_log_path, "a", encoding = "utf-8") as f:
                await f.write(line)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user or message.author.bot:
            return

        try:
            line = f"[{message.created_at}] {message.author}: {message.content}\n"
            await self.queue.put(line)
        except Exception as e:
            print(str(e))

        if not message.guild and message.author != self.bot.user:
            try:
                pass
            except discord.errors.Forbidden:
                pass

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        pass

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = discord.utils.get(member.guild.channels, id = 1398225803027812382)
        if not channel:
            return
        
        info = discord.Embed(title = f"{member} ({member.nick})", description = f"{member.id}", color = 0x3cd7e7)

        joined_at = member.joined_at.strftime("%b %d, %Y, %T")
        created_at = member.created_at.strftime("%b %d, %Y, %T")

        info.add_field(name = "Is bot", value = f"{member.bot}", inline = False)
        info.add_field(name = "Join server", value = f"at {joined_at}", inline = False)
        info.add_field(name = "Create account", value = f"at {created_at}", inline = False)

        info.set_thumbnail(url = member.display_avatar)
        info.set_footer(text = "Dev.", icon_url = "https://cdn.discordapp.com/attachments/1160900391303663667/1392092994471202979/IMG_1584.jpg")

        if member.banner:
            info.set_image(url = member.banner)

        await channel.send(f"{member.mention}", embed = info)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        channel = discord.utils.get(member.guild.channels, id = 1398225803027812382)
        if not channel:
            return
        await channel.send(f"`{member.name}` left the server.")

    @commands.Cog.listener()
    async def on_command_error(self, ctx: discord.Message, error: commands.CommandError):
        if isinstance(error, commands.CommandNotFound):
            return await ctx.channel.send("**Unknown Command.**")
        elif isinstance(error, commands.MissingRequiredArgument):
            return await ctx.channel.send("**Missing Required Argument.**")
        elif isinstance(error, commands.MissingPermissions):
            return await ctx.channel.send("**Missing Permissions.**")
        return print(error)

    @commands.Cog.listener()
    async def on_tree_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
        return print(error)

async def setup(bot: commands.Bot):
    pass

