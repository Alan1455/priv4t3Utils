# -*- coding: utf-8 -*-

# discord
import discord
from discord import app_commands
from discord.ext import commands

# os
import asyncio

class DynamicVC(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if member.bot:
            return

        if after.channel and after.channel.id == 1394950826677637251:
            existing = discord.utils.find(
                lambda ch: ch.name.startswith(f"└[{member.name}"),
                after.channel.category.voice_channels
            )
            if existing:
                await member.move_to(existing)
                return

            voiceChat = await after.channel.category.create_voice_channel(name = f"└[{member.name}]的語音")
            await member.move_to(voiceChat)

        if before.channel and before.channel.name.startswith("└["):
            await asyncio.sleep(1)
            if len(before.channel.members) == 0:
                await before.channel.delete()

async def setup(bot: commands.Bot):
    pass

