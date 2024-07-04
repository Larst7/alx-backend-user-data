#!/usr/bin/env python3
"""Module for filtering data logs"""

import logging
import re
import os
import mysql.connector
from typing import List

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """initializer"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ using filter_datum"""
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super().format(record)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """performs a regex"""
    pattern = r'(' + '|'.join(map(re.escape, fields)) + r')=' +\
        r'[^' + re.escape(separator) + r']+'
    return re.sub(pattern, r'\1=' + redaction, message)


def get_logger() -> logging.Logger:
    """function log getter"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """connector function"""
    db_username = os.getenv('PERSONAL_DATA_DB_USERNAME') or "root"
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')
    db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD') or ""
    db_host = os.getenv('PERSONAL_DATA_DB_HOST') or "localhost"
    connection = mysql.connector.connect(user=db_username,
                                         password=db_password, host=db_host,
                                         database=db_name)
    return connection


def main():
    """connects the database """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    filtered_fields = ['name', 'email', 'phone', 'ssn', 'password']

    logging.basicConfig(format='[HOLBERTON] user_data INFO: %(message)s',
                        level=logging.INFO)

    for row in rows:
        filtered_row = {key: '***' if key in filtered_fields else value
                        for key, value in zip(cursor.column_names, row)}
        logging.info("; ".join([f"{key}={value}" for key, value in
                                filtered_row.items()]))

    cursor.close()
    db.close()


cursor = None


if __name__ == "__main__":
    main()
