# -*- coding: utf-8 -*-

# discord
from discord.ext import commands

# cogs
from .event import Event
from .main import Main
from .help import Help
from .activity import Activity
from .voiceTracker import VoiceTracker
from .music import VoiceChat
from .count import Count
# from .dynamicVC import DynamicVC

__all__ = [
    "Event",
    "Main",
    "Help",
    "Activity",
    "VoiceTracker",
    "VoiceChat",
    "Count",
    # "DynamicVC",
]

async def setup(bot: commands.Bot):
    await bot.add_cog(Event(bot))
    await bot.add_cog(Main(bot))
    await bot.add_cog(Help(bot))
    await bot.add_cog(Activity(bot))
    await bot.add_cog(VoiceTracker(bot))
    await bot.add_cog(VoiceChat(bot))
    await bot.add_cog(Count(bot))
    # await bot.add_cog(DynamicVC(bot))

