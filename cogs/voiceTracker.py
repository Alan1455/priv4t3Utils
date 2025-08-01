# -*- coding: utf-8 -*-

# discord
import discord
from discord import app_commands
from discord.ext import commands

# system class
import json
import os
import time

DATA_PATH = "data/voice_activity.json"
JOIN_TIME = {}

class VoiceTracker(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        os.makedirs("data", exist_ok = True)
        self.data = self._load_data()

    def _load_data(self):
        if os.path.exists(DATA_PATH):
            with open(DATA_PATH, "r", encoding = "utf-8") as f:
                return json.load(f)
        return {}

    def _save_data(self):
        with open(DATA_PATH, "w", encoding = "utf-8") as f:
            json.dump(self.data, f, indent = 2)

    @app_commands.command(name = "vc_activity", description = "Check users vc activity")
    async def VCactivity(self, interaction: discord.Interaction):
        now = time.time()

        for uid, join_time in JOIN_TIME.items():
            duration = int(now - join_time)
            self.data[uid] = self.data.get(uid, 0) + duration
            JOIN_TIME[uid] = now

        self._save_data()

        if not self.data:
            await interaction.response.send_message("No data.")
            return

        sorted_users = sorted(self.data.items(), key = lambda x: x[1], reverse = True)
        embed = discord.Embed(
            title = "🎙️ VC活躍排行榜",
            description = "根據語音頻道停留時間排序",
            color = discord.Color.orange()
        )

        def format_duration(seconds: int):
            hours, remainder = divmod(seconds, 3600)
            minutes, secs = divmod(remainder, 60)

            if hours > 0:
                return f"{hours}小時 {minutes}分 {secs}秒"
            elif minutes > 0:
                return f"{minutes}分 {secs}秒"
            else:
                return f"{secs}秒"

        for i, (uid, total_seconds) in enumerate(sorted_users[:10], start = 1):
            member = interaction.guild.get_member(int(uid))
            name = member.display_name if member else f"Unknown({uid})"
            readable = format_duration(total_seconds)
            embed.add_field(name = f"{i}. {name}", value = f"🕓 {readable}", inline = False)

        await interaction.response.send_message("", embed = embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        uid = str(member.id)

        if member.bot:
            return

        if not before.channel and after.channel:
            JOIN_TIME[uid] = time.time()
        elif before.channel and not after.channel:
            if uid in JOIN_TIME:
                duration = int(time.time() - JOIN_TIME[uid])
                self.data[uid] = self.data.get(uid, 0) + duration
                self._save_data()
                del JOIN_TIME[uid]

async def setup(bot: commands.Bot):
    pass

