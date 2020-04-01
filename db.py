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
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return [Category(*r) for r in results]


class Category:

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def products(self):
        """ Get list of products belonging in Category.
        Return list of Product objects"""
        conn = _connect()
        cursor = conn.cursor()
        req = ("SELECT Product.id " 
               "FROM ProductCategory "
               "INNER JOIN Product ON Product.id = ProductCategory.product_id "
               "WHERE ProductCategory.category_id = %s")
        cursor.execute(req, (self.id,))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return [Product(*r) for r in results]


class Product:

    def __init__(self, id):
        self.id = id

    def short_description(self):
        """ Return a short description: product's name and brands"""
        conn = _connect()
        cursor = conn.cursor()
        req = "SELECT product_name, brands FROM Product WHERE id = %s"
        cursor.execute(req, (self.id,))
        name, brands = cursor.fetchone()
        cursor.close()
        conn.close()
        return '{} - {}'.format(name, brands)

    def description(self):
        pass
