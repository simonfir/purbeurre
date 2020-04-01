from json import load
from mysql.connector import MySQLConnection


DB_CONFIG_FILE = 'db_config.json'


def _connect():
    """ Connect to the database, return MysSQLConnection"""
    with open(DB_CONFIG_FILE) as f:
        return MySQLConnection(**load(f))


def categories():
    """ Get the list of all categories. Return list of Category obj"""
    conn = _connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM Category")
    ids = cursor.fetchall()
    cursor.close()
    conn.close()
    for i in ids:
        yield Category(*i)


class Category:

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def products(self):
        """ Get list of products belonging in Category.
        Return list of Product objects"""
        pass


class Product:

    def __init__(self, id):
        self.id = id

    def description(self):
        pass
