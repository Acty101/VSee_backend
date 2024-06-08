#!/usr/bin/python3
"""Script to insert dummy data from CSV to sqlite3 db.
NOTE: Requires that the db is already set up
"""

import sqlite3
import csv
from pathlib import Path


def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


def get_db():
    db_filename = Path(__file__).resolve().parent.parent / Path(
        "var", "backend.sqlite3"
    )
    sqlite_db = sqlite3.connect(str(db_filename))
    sqlite_db.row_factory = dict_factory
    sqlite_db.execute("PRAGMA foreign_keys = ON")
    return sqlite_db


def main():
    """Main function to execute."""
    connection = get_db()
    csv_folder = Path(__file__).resolve().parent / Path("./csv")
    for csv_file in csv_folder.iterdir():
        # csv_file is the relative path to all csv

        # create a dummy company (table users)
        name = csv_file.stem
        username = f"{name}_startup"
        password = "password"
        filename = ""
        is_vc = False
        points = 0
        industry = "Technology"
        summary = "YanC is a company aimed to democratize access to advanced AI technologies and drive innovation across industries."

        # insert into db
        cur = connection.execute(
            "INSERT INTO users (username, name, password, filename, is_vc, points, industry, summary)"
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                username,
                name,
                password,
                filename,
                is_vc,
                points,
                industry,
                summary,
            ),
        )
        # open csv file and input questions to questions table and answers to answers table
        with open(csv_file, "r") as file:
            csv_reader = csv.reader(file, delimiter=",")
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    pass
                else:
                    question = row[0]
                    ans = row[1]
                    cur = connection.execute(
                        "INSERT INTO questions (text, is_vc) VALUES (?, ?)",
                        (question, is_vc),
                    )
                    id = cur.lastrowid
                    connection.execute(
                        "INSERT INTO answers (question_id, text, username) VALUES (?, ?, ?)",
                        (id, ans, username),
                    )
                line_count += 1
            connection.execute(
                "UPDATE users SET points = ? WHERE username = ?",
                (line_count, username),
            )
    # commit and close the db
    connection.commit()
    connection.close()


if __name__ == "__main__":
    main()
