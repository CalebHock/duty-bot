from bot.util import complexes
import datetime
import sqlite3
import sys


def convert_month_to_int(month: str) -> int:
    """Converts a month to an integer, i.e.:
    Jan -> 0
    Feb -> 1
    ...

    Arguments:
    month -- the name of the month
    """
    return dict(
        [
            reversed(el)
            for el in enumerate(
                [
                    "Jan",
                    "Feb",
                    "Mar",
                    "Apr",
                    "May",
                    "Jun",
                    "Jul",
                    "Aug",
                    "Sep",
                    "Oct",
                    "Nov",
                    "Dec",
                ]
            )
        ]
    )[month]


def parse_date(date: str, fallback_month: int) -> tuple:
    """Parses a string for a date. If a month is not specified in the string,
    then fallback_month is used instead.

    Arguments:
    date -- the date string
    fallback_month -- the month to use if the date string does not contain a
    month
    """
    if " " in date:
        tokens = date.split()
        return datetime.date(
            datetime.date.today().year,
            convert_month_to_int(tokens[0]) + 1,
            int(tokens[1]),
        )
    else:
        return datetime.date(datetime.date.today().year, fallback_month, int(date))


def main():
    complex_name = complexes.get_complex_name(sys.argv[2])
    with open(sys.argv[1], "r") as schedule_file:
        with sqlite3.connect("database.db") as db:
            cur = db.cursor()
            with open("setup.sql", "r") as setup_file:
                cur.executescript(setup_file.read())
            for line in schedule_file:
                if "-" in line:
                    dash_index = line.index("-")
                    start_date = parse_date(line[0:dash_index], None)
                    end_date = parse_date(line[dash_index + 1 :], start_date.month)
                else:
                    cur.execute(
                        "INSERT INTO schedule VALUES (?, ?, ?, ?)",
                        (
                            line.strip(),
                            complex_name,
                            start_date.isoformat(),
                            end_date.isoformat(),
                        ),
                    )
            db.commit()


main()
