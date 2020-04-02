from json import load
from mysql.connector import MySQLConnection


DB_CONFIG_FILE = 'db_config.json'


def _connect():
    """ Connect to the database, return MysSQLConnection"""
    with open(DB_CONFIG_FILE) as f:
        return MySQLConnection(**load(f))


def _execute(request, args):
    """ Execute request on the database, Return rows as a tuple"""
    conn = _connect()
    cursor = conn.cursor()
    cursor.execute(request, args)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


def search_categories(search):
    """ Search categories matching search. Return Category object"""
    results = _execute("SELECT id, name FROM Category "
                       "WHERE MATCH (name) AGAINST (%s) ",
                       (search,))
    return [Category(*r) for r in results]


def search_products(search):
    """ Search products matching search. Return Product object"""
    results = _execute("SELECT id FROM Products "
                       "WHERE MATCH (product_name, gerenic_name, brands) "
                       "AGAINST (%s)", (search,))
    return [Product(*r) for r in results]


class Category:

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def products(self):
        """ Get list of products belonging in Category.
        Return list of Product objects"""
        results = _execute("SELECT Product.id "
                           "FROM ProductCategory "
                           "INNER JOIN Product "
                           "ON Product.id = ProductCategory.product_id "
                           "WHERE ProductCategory.category_id = %s",
                           (self.id,))
        return [Product(*r) for r in results]


class Product:

    def __init__(self, id):
        self.id = id

    def short_description(self):
        """ Return a short description: product's name and brands"""
        name, brands = _execute("SELECT product_name, brands "
                                "FROM Product WHERE id = %s",
                                (self.id,))[0]
        return '{} - {}'.format(name, brands)

    def description(self):
        """ Return a long description of the product"""
        values = _execute(
            "SELECT product_name, brands, UPPER(nutrition_grade_fr), "
            "generic_name, stores, url "
            "FROM Product WHERE id = %s",
            (self.id,))[0]
        print("{} - {}\n"
              "Nutriscore : {}\n"
              "Description : {}\n"
              "Où l'acheter : {}\n"
              "Page Open Food Facts : {}\n"
              .format(*values))
