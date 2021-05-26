#!/usr/bin/env python3

import os
import gsheeter
import myutils
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
# CHANNEL = os.getenv('DISCORD_CHANNEL')

bot = commands.Bot(command_prefix='!')


@bot.command(name='add', help="add notification for selected stock")
async def stat(ctx, stock: str, cond: str, value: int):

    # response = "test {0}".format(ctx.author.mention)
    response = "{} - {} is {} ${}".format("test", stock, cond, value)
    await ctx.send(response)


bot.run(TOKEN)
