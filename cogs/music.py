# -*- coding: utf-8 -*-

# discord
import discord
from discord import app_commands
from discord.ext import commands

class VoiceChat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = "join", description = "Join vc")
    async def play(self, interaction: discord.Interaction):
        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.response.send_message("You must join the voice channel first.", ephemeral = True)
            return

        voice_channel = interaction.user.voice.channel
        try:
            if interaction.guild.voice_client is None:
                vc = await voice_channel.connect()
            else:
                vc: discord.VoiceClient = interaction.guild.voice_client
                if vc.channel != voice_channel:
                    await vc.move_to(voice_channel)
        except Exception as e:
            print(f"{e}")

        await interaction.response.send_message("Already joined vc.")

    @app_commands.command(name = "leave", description = "Leave vc")
    async def leave(self, interaction: discord.Interaction):
        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.response.send_message("You must join the voice channel first.", ephemeral = True)
            return
    
        vc: discord.VoiceClient = interaction.guild.voice_client
        if vc and vc.is_connected():
            await vc.disconnect()
            await interaction.response.send_message("I have left the voice channel.")
        else:
            await interaction.response.send_message("Im not in any voice channels.", ephemeral = True)

async def setup(bot: commands.Bot):
    pass

