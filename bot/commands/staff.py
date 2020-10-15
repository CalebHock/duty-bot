import bot.util.complexes as complexes
import discord
from discord.ext import commands
import sqlite3


@commands.command(name="staff")
async def staff(ctx: commands.Context, complex_name: str=None):
    """Connects the issuing user to the complex in which they reside.

    Arguments:
    ctx -- the context of the command
    complex_name -- the complex in which the issuing user resides
    """
    if complex_name is None:
        await ctx.send(":warning: No argument provided `!staff [complex]`")

    else:
        # Make staff command not case sensative
        if len(complex_name) == 2:
            complex_name = complex_name.upper()
        else:
            complex_name = complex_name.title()

        complex_name = complexes.get_complex_name(complex_name)
        if complex_name is None:
            complex_names = "\n".join(sorted(complexes.complexes.keys()))
            await ctx.send(
                f":warning: The provided complex does not exist. The complex name must be one of the following:\n```\n{complex_names}```"
            )
            return

        with sqlite3.connect("database.db") as db:
            cur = db.cursor()

            # Remove the author's complex role if they already appear in the
            # database
            author_id = ctx.author.id
            cur.execute(
                """
                SELECT complex
                FROM discord_users
                WHERE discord_id = ?
                """,
                (author_id,),
            )
            row = cur.fetchone()
            if row is not None:
                complex_role = discord.utils.get(ctx.author.guild.roles, name=row[0])
                if complex_role is not None:
                    await ctx.author.remove_roles(complex_role)

            cur.execute(
                """
                INSERT INTO discord_users (discord_id, complex)
                VALUES (?, ?)
                ON CONFLICT (discord_id) DO UPDATE SET complex = ?
                """,
                (
                    author_id,
                    complex_name,
                    complex_name,
                ),
            )
            db.commit()

        complex_role = discord.utils.get(ctx.author.guild.roles, name=complex_name)
        if complex_role is not None:
            await ctx.author.add_roles(complex_role)
        else:
            await ctx.send(
                ":warning: The role for your complex does not exist. Contact the server administrator for assistance."
            )
