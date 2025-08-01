# -*- coding: utf-8 -*-

# discord
import discord
from discord import app_commands
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = "help", description = "help")
    async def help(self, interaction: discord.Interaction):
        options = [
            discord.SelectOption(label = "help", description = "Get help"),
            discord.SelectOption(label = "activity", description = "Display users activity rank"),
            discord.SelectOption(label = "vc activity", description = "Display users vc activity rank"),
            discord.SelectOption(label = "join", description = "Join VC"),
            discord.SelectOption(label = "leave", description = "Leave VC"),
        ]

        select = discord.ui.Select(placeholder = "Choose one", options = options)

        async def select_callback(interaction: discord.Interaction):
            command_details = {
                "help": discord.Embed(title = "Help", description = "Displays the help menu.", color = 0x2fa6d6)
                .add_field(name = "Usage", value = "Simply enter the command.", inline = False)
                .add_field(name = "Example", value = "```/help```", inline = False),

                "activity": discord.Embed(title = "Activity", description = "Display users activity rank.", color = 0x2fa6d6)
                .add_field(name = "Usage", value = "Simply enter the command.", inline = False)
                .add_field(name = "Example", value = "```/activity```", inline = False),

                "vc activity": discord.Embed(title = "VC Activity", description = "Display users vc activity rank.", color = 0x2fa6d6)
                .add_field(name = "Usage", value = "Simply enter the command.", inline = False)
                .add_field(name = "Example", value = "```/vc_activity```", inline = False),

                "join": discord.Embed(title = "Join", description = "Join VC.", color = 0x2fa6d6)
                .add_field(name = "Usage", value = "Simply enter the command.", inline = False)
                .add_field(name = "Example", value = "```/join```", inline = False),

                "leave": discord.Embed(title = "Leave", description = "Leave VC.", color = 0x2fa6d6)
                .add_field(name = "Usage", value = "Simply enter the command.", inline = False)
                .add_field(name = "Example", value = "```/leave```", inline = False),
            }

            selected_command = select.values[0]
            embed = command_details.get(selected_command, discord.Embed(title = "Unknown Command", description = "No details available.", color = 0xff0000))
            embed.set_footer(text = "Dev.", icon_url = "https://cdn.discordapp.com/attachments/1160900391303663667/1392092994471202979/IMG_1584.jpg")
            await interaction.response.send_message(embed = embed, ephemeral = True)

        select.callback = select_callback
        view = discord.ui.View()
        view.add_item(select)

        await interaction.response.send_message("Select a command to get more details:", view = view, ephemeral = True)

async def setup(bot: commands.Bot):
    pass

