from discord.ext import commands
import sqlite3


@commands.command(name="id")
async def identify(ctx: commands.Context, name: str=None):
    """Connects the issuing user to a person in the database.

    Arguments:
    ctx -- the context of the command
    name -- the name of the issuing user
    """
   
    if name is None:
        await ctx.send(":warning: No argument provided `!id [name]`")

    else:
        # The bot cannot change the nickname of an administrator (since an
        # administrator must have more permissions than the bot)
        if not ctx.author.guild_permissions.administrator:
            await ctx.author.edit(nick=name)

        with sqlite3.connect("database.db") as db:
            cur = db.cursor()
            cur.execute(
                """
                INSERT INTO discord_users (discord_id, name)
                VALUES (?, ?)
                ON CONFLICT (discord_id) DO UPDATE SET name = ?
                """,
                (
                    ctx.author.id,
                    name,
                    name,
                ),
            )
            db.commit()
