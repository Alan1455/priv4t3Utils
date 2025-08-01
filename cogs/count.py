# -*- coding: utf-8 -*-

# discord
import discord
from discord.ext import commands

# os
import json
import os
from sympy import sympify, N
from sympy.core.sympify import SympifyError

CHANNEL_ID = 1398225802608509079
DATA_FILE = "data/count_data.json"

class Count(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        os.makedirs("data", exist_ok = True)
        self.expected_number = self._load_data()

    def _load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding = "utf-8") as f:
                return json.load(f).get("expected_number", 1)
        return 1

    def _save_data(self):
        with open(DATA_FILE, "w", encoding = "utf-8") as f:
            json.dump({"expected_number": self.expected_number}, f, indent = 2)

    def sympy(self, expr: str) -> float | None:
        try:
            result = sympify(expr)
            numeric = N(result)
            return float(numeric)
        except (SympifyError, TypeError, ValueError):
            return None

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if message.channel.id != CHANNEL_ID:
            return

        expr = message.content.strip()
        result = self.sympy(expr)
        if result is None:
            return

        if round(result) == self.expected_number:
            await message.add_reaction("✅")
            self.expected_number += 1
            self._save_data()
        else:
            await message.add_reaction("❌")
            await message.reply(f"❗ 這不是正確的數字! 下次請從 `{self.expected_number}` 開始")

async def setup(bot: commands.Bot):
    pass

