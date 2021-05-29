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


@bot.command(name='add', help="add mug event")
async def add(ctx, *, mugLog: str):
    #if ctx.channel == CHANNEL:
    sheet_name = myutils.check_user(ctx)
    if sheet_name != "error":
        gsheeter.update_mug(sheet_name, mugLog)
        response = "mugs updated!"
    else:
        response = "Error, user not recognized!"
    await ctx.send(response)

@bot.command(name='stat', help="show all-time stat")
async def stat(ctx):
    #if ctx.channel == CHANNEL:
    sheet_name = myutils.check_user(ctx)
    if sheet_name != "error":
        stat = gsheeter.get_total_stat(sheet_name)
        response = myutils.format_response(stat)
    else:
        response = "Error, user not recognized!"
    await ctx.send(response)


@bot.command(name='daily', help="display daily stat")
async def daily(ctx, *, date):
    #if ctx.channel == CHANNEL:
    sheet_name = myutils.check_user(ctx)
    if sheet_name != "error":
        stat = gsheeter.get_daily_stat(sheet_name, date)
        response = myutils.format_response(stat)
    else:
        response = "Error, user not recognized!"
    await ctx.send(response)


bot.run(TOKEN)
