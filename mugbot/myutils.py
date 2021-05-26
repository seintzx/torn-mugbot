#!/usr/bin/env python3

import re
import os
from dotenv import load_dotenv

load_dotenv()
SHEET_1 = os.getenv('SHEET_1')
SHEET_2 = os.getenv('SHEET_2')

USER_1 = os.getenv('USER_1')
USER_2 = os.getenv('USER_2')


def regex(reg, msg):
    return re.search(reg, msg).group(0)


def format_response(stat):
    response = """
    **Total Mugged {}**
    success: {}
    failed: {}
    attack: ${:0,.0f}
    mugged: ${:0,.0f}
    profit: ${:0,.0f}
    """.format( stat[0],
                stat[1],
                stat[2],
                int(stat[3]),
                int(stat[4]),
                int(stat[5]))
    return response


def check_user(ctx):
    if str(ctx.author.id) == USER_1:
        sheet_name = SHEET_1
    elif str(ctx.author.id) == USER_2:
        sheet_name = SHEET_2
    else:  # error
        sheet_name = "error"

    return sheet_name