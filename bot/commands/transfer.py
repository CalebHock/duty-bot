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

def check_date_format(date: str):
    """Parses a string for a date. Returns true if 
    date is any of the following formats:
    MM/DD/YYYY
    MM/DD
    DD

    Arguments:
    date -- the date string
    """
    return re.match('([0-9]){1,2}((\/)([0-9]){1,2}){0,1}((\/)([0-9]){4}){0,1}', date)

@commands.command(name="transfer")
async def transfer(ctx: commands.Context, owner: discord.Member=None, recipient: discord.Member=None, date: str=None):
    """Transfer a duty shift from one user to another

    Arguments:
    ctx -- the context of the command
    owner -- the user who is giving away the duty shift
    recipient -- the user accepting the duty shift 
    date -- the date for which the issuing user is requesting a transfer on
    if date is null, use the upcoming weekends's date
    """
    # Check if required arguments are provided
    if owner is None:
        await ctx.send(":warning: No owner specified")
    elif recipient is None:
        await ctx.send(":warning: No recipient specified.")

    # Check if user has permissions
    elif ctx.author.id != owner.id and not ctx.author.guild_permissions.administrator:
        await ctx.send(":warning: You do not have the valid permissions to execute this command")

    # Check date format / if date exists
    elif date is not None and not check_date_format(date):
        await ctx.send(":warning: Invalid date format (MM/DD/YYYY)")

    else:
        if date == None:
            # If date is not provided with command, set to upcoming friday
            date = datetime.date.today() + datetime.timedelta((4-datetime.date.today().day) % 7)
        else:
            # Format date to a datetime.date object
            date = parse_date(date)

        with sqlite3.connect("database.db") as db:
            cur = db.cursor()
            cur.execute(
                """
                SELECT name, complex
                FROM discord_users
                WHERE discord_id = ?
                """,
                (owner.id,),
            )
            owner_disc = cur.fetchall()

            if not owner_disc:
                await ctx.send(
                    f":warning: {owner.display_name} is not correctly linked. Use !id and !staff to link your account to the schedule."
                )

            cur.execute(
                """
                SELECT name, complex
                FROM discord_users
                WHERE discord_id = ?
                """,
                (recipient.id,),
            )
            recip_disc = cur.fetchall()
            
            if not recip_disc:
                await ctx.send(
                    f":warning: {recipient.display_name} is not correctly linked. Use !id and !staff to link your account to the schedule."
                )

            if owner_disc and recip_disc:
                if owner_disc[0][1] != recip_disc[0][1]:
                    await ctx.send(
                        f":warning: {recipient.display_name} is not from the same complex as {owner.display_name}."
                    )
                
                else:
                    cur.execute(
                        """
                        SELECT *
                        FROM schedule
                        WHERE name = ? AND complex = ? AND DATE(?) BETWEEN DATE(start_date) AND DATE(end_date)
                        """,
                        (owner_disc[0][0], owner_disc[0][1], date.isoformat(),),
                    )
                    if not cur.fetchone():
                        await ctx.send(
                            f":warning: {owner.display_name} is not on duty on {date.month}/{date.day}/{date.year}."
                        )
                    else:
                        cur.execute(
                            """
                            UPDATE schedule
                            SET name = ?
                            WHERE name = ? AND complex = ? AND DATE(?) BETWEEN DATE(start_date) AND DATE(end_date)
                            """,
                            (recip_disc[0][0], owner_disc[0][0], owner_disc[0][1], date.isoformat(),),
                        )
                        await ctx.send(
                            f"{owner.display_name} transferred duty on {date.month}/{date.day}/{date.year} to {recipient.display_name}."
                        )