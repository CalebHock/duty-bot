import bot.util.complexes as complexes
import discord
from discord.ext import commands
import sqlite3
import datetime
from collections import OrderedDict
import re

def parse_date(date: str):
    """Parses a string for a date. If a year and/or month is not specified
    in the string, then current year and/or month is used instead.

    Arguments:
    date -- the date string in format month/day/year -> 00/00/0000
    """
    if "/" in date:
        slash1 = date.index("/")
        if "/" in date[slash1 + 1:]:
            slash2 = date[slash1 + 1:].index("/") + slash1 + 1
            # When date is provided in MM/DD/YYYY format
            return datetime.date(int(date[slash2 + 1:]), int(date[0:slash1]), int(date[slash1 + 1:slash2]))
        else:
            # When date is provided in MM/DD format
            return datetime.date(datetime.date.today().year, int(date[0:slash1]), int(date[slash1 + 1:]))
    else:
        # When date is provided in DD format
        return datetime.date(datetime.date.today().year, datetime.date.today().month, int(date))

@commands.command(name="duty")
async def duty(ctx: commands.Context, date: str=None):
    """Displays who is on duty for a specific date, sorted by complex

    Arguments:
    ctx -- the context of the command
    date -- the date for which the issuing user is requesting 
    information on who is on duty for that specific date,
    if date is null, use the upcoming weekends's date
    """
    # Check date format / if date exists
    if date is not None and not re.match('([0-9]){1,2}((\/)([0-9]){1,2}){0,1}((\/)([0-9]){4}){0,1}', date):
        await ctx.send(":warning: Invalid date format (MM/DD/YYYY)")

    else:
        if date == None:
            # If date is not provided with command, set to upcoming friday
            date = datetime.date.today() + datetime.timedelta((4-datetime.date.today().weekday()) % 7)
        else:
            # Format date to a datetime.date object
            date = parse_date(date)

        with sqlite3.connect("database.db") as db:
            # Retrieve the name and complex of users who are on duty 
            # for the provided date
            cur = db.cursor()
            cur.execute(
                """
                SELECT complex, name
                FROM schedule
                WHERE DATE(?) BETWEEN DATE(start_date) AND DATE(end_date)
                """,
                (date.isoformat(),),
            )
            db_query = cur.fetchall()
            dictionary = OrderedDict()

            for staff, *user in db_query:
                if staff in dictionary:
                    dictionary[staff].append(user)
                else:
                    dictionary[staff] = [user]

            on_duty = [(staff, tuple(map(tuple, user))) for staff, user in dictionary.items()]
            on_duty.sort()
            output = ""

            # Format output to be:
            # Complex1: User1, User2, ...
            # Complex2: User1, ...
            for team in on_duty:
                output += team[0]
                output += ": "
                for name in team[1]:
                    output += name[0]
                    output += ", "
                output = output[:-2]
                output += "\n"
            
            if not output:
                await ctx.send(
                    f"There is nobody currently scheduled for duty on {date.month}/{date.day}/{date.year}."
                )
            else:
                await ctx.send(
                    f"RAs on duty: {date.month}/{date.day}/{date.year}\n```\n{output}```"
                )