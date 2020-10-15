from bot.commands import identify
from bot.commands import staff
from bot.commands import duty
from bot.commands import transfer
from bot.tasks import on_duty
import discord
import sqlite3
from discord.ext import commands
from discord.ext import tasks
from datetime import datetime


class DutyBot(commands.Bot):
    def __init__(self):
        commands.Bot.__init__(self, command_prefix="!")

        # Register the commands
        self.add_command(identify.identify)
        self.add_command(staff.staff)
        self.add_command(duty.duty)
        self.add_command(transfer.transfer)

        # Setup the database if the tables do not exist yet
        with sqlite3.connect("database.db") as db:
            cur = db.cursor()
            with open("setup.sql", "r") as setup_file:
                cur.executescript(setup_file.read())
            db.commit()

    async def on_ready(self):
        self.on_duty_task.start()

        print("Duty Bot is on call!")

    @tasks.loop(minutes=5.0)
    async def on_duty_task(self):
        await on_duty.on_duty(self)
