from json import load
from mysql.connector import MySQLConnection


DB_CONFIG_FILE = 'db_config.json'


def _connect():
    """ Connect to the database, return MysSQLConnection"""
    with open(DB_CONFIG_FILE) as f:
        return MySQLConnection(**load(f))


def _execute(request, args=()):
    """ Execute request on the database, Return rows as a tuple"""
    conn = _connect()
    cursor = conn.cursor()
    cursor.execute(request, args)
    results = cursor.fetchall() if cursor.with_rows else None
    cursor.close()
    conn.commit()
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
    results = _execute("SELECT id FROM Product "
                       "WHERE MATCH (product_name, generic_name, brands) "
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
        name, brands, grade = _execute(
            "SELECT product_name, brands, nutrition_grade_fr"
            "FROM Product WHERE id = %s",
            (self.id,))[0]
        return '{} - {} (Nutriscore: {})'.format(name, brands, grade)

    def description(self):
        """ Return a long description of the product"""
        values = _execute(
            "SELECT product_name, brands, UPPER(nutrition_grade_fr), "
            "generic_name, stores, url "
            "FROM Product WHERE id = %s",
            (self.id,))[0]
        return ("{} - {}\n"
                "Nutriscore : {}\n"
                "Description : {}\n"
                "Où l'acheter : {}\n"
                "Page Open Food Facts : {}"
                .format(*values))

    def substitutes(self):
        """ Get a list of similar products with a better nutrition grade.
        Return Product object."""
        # Here we assume that the more categories two products share,
        # the more similar they are. We use a subrequest on the
        # ProductCategory table to get an intermediate table `Similar`
        # containing the number of categories each product shares with
        # the original product. We can then keep the products with a
        # better nutrition grade and sort them to get the most similar
        # substitutes first.
        results = _execute(
            "SELECT Product.id "
            "FROM ( "
            "  SELECT product_id, COUNT(product_id) AS nb_shared_categories "
            "  FROM ProductCategory "
            "  WHERE category_id IN ( "
            "    SELECT category_id FROM ProductCategory WHERE Product_id = %s) "
            "  GROUP BY product_id"
            "  ) AS Similar "
            "INNER JOIN Product ON Similar.product_id = Product.id "
            "WHERE Product.nutrition_grade_fr < ( "
            "  SELECT nutrition_grade_fr FROM Product WHERE id = %s) "
            "ORDER BY nb_shared_categories DESC, nutrition_grade_fr ",
            (self.id,)*2
        )
        return [Product(*r) for r in results]
