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

DATA_PATH = "data/activity.json"

class Activity(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        os.makedirs("data", exist_ok = True)
        self.data = self._load_data()

    def _load_data(self):
        if os.path.exists(DATA_PATH):
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save_data(self):
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)
    
    @app_commands.command(name = "activity", description = "Check users activity")
    async def activity(self, interaction: discord.Interaction):
        if not self.data:
            await interaction.response.send_message("No data.")
            return

        sorted_users = sorted(self.data.items(), key=lambda x: x[1], reverse=True)
        embed = discord.Embed(
            title = "📊 活躍排行榜",
            description = "根據訊息總數排序",
            color = discord.Color.blue()
        )

        for i, (uid, count) in enumerate(sorted_users[:10], start = 1):
            user = interaction.guild.get_member(int(uid))
            name = user.display_name if user else f"Unknown({uid})"
            embed.add_field(name = f"{i}. {name}", value = f"📝訊息數: {count}", inline = False)

        await interaction.response.send_message("", embed = embed)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user or message.author.bot:
            return

        uid = str(message.author.id)
        self.data[uid] = self.data.get(uid, 0) + 1
        self._save_data()

async def setup(bot: commands.Bot):
    pass

