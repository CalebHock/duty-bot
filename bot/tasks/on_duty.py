import datetime
import discord
import os
import sqlite3


async def on_duty(bot):
    """Assigns the On Duty role to all users who are on duty at the current
    time. The function runs every 5 minutes.
    """
    with sqlite3.connect("database.db") as db:
        # Retrieve the Discord IDs of users who are currently on duty
        cur = db.cursor()
        cur.execute(
            """
            SELECT discord_id
            FROM discord_users
            INNER JOIN schedule
                ON discord_users.name = schedule.name
                    AND discord_users.complex = schedule.complex
            WHERE DATE(?) BETWEEN DATE(start_date) AND DATE(end_date)
            """,
            (datetime.datetime.today().isoformat(),),
        )
        # Convert Discord IDs to integers because Discord does that for some
        # reason
        on_duty = set([int(row[0]) for row in cur.fetchall()])

        guild = bot.get_guild(int(os.getenv("GUILD_ID")))
        on_duty_role = discord.utils.get(
            guild.roles, name=os.getenv("ON_DUTY_ROLE_NAME")
        )

        # Remove the role from anyone who is no longer on duty
        for member in on_duty_role.members:
            if member.id not in on_duty:
                await member.remove_roles(on_duty_role)

        # Add the role to everyone who is on duty (if they already have the
        # role, then nothing happens)
        for discord_id in on_duty:
            member = guild.get_member(discord_id)
            if member is not None:
                await member.add_roles(on_duty_role)
