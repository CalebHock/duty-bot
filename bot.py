from dotenv import load_dotenv

load_dotenv()

import os
from bot.dutybot import DutyBot


def main():
    bot = DutyBot()
    bot.run(os.getenv("TOKEN"))


if __name__ == "__main__":
    main()
