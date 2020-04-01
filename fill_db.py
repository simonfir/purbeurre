import json

from requests import request
from mysql.connector import MySQLConnection


PRODUCT_FIELDS = ('product_name',
                  'generic_name',
                  'nutrition_grade_fr',
                  'url',
                  'stores',
                  'brands',
                  'categories',
                  'categories_tags')

DB_CONFIG_FILE = 'db_config.json'


def get_products():
    """Get products using the search function of the
    open food facts API."""
    products = []
    page = 1
    while True:
        url = 'https://fr.openfoodfacts.org/cgi/search.pl'
        params = {
            'action': 'process',
            'page_size': 1000,
            'page': page,
            'json': 'true',
            'fields': ','.join(PRODUCT_FIELDS),

            'tagtype_0': 'states',
            'tag_contains_0': 'contains',
            'tag_0': 'en:checked',
        }
        resp = request('GET', url, params=params)
        to_add = json.loads(resp.text)['products']
        products += to_add
        if len(to_add) < 1000:
            return products
        page += 1


class DataBase:

    def __init__(self):
        with open(DB_CONFIG_FILE) as f:
            self.conn = MySQLConnection(json.load(f))

    def insert_category(self, tag, name):
        """ Insert new category in the table Category if it hasn't
        already been inserted. Return category id"""
        cat_id = self.get_category_id(tag)
        if cat_id is None:
            cursor = self.conn.cursor()
            cursor.execute('INSERT INTO Category(tag, name) VALUES (%s, %s)',
                           (tag, name))
            cat_id = cursor.lastrowid
            cursor.close()
        return cat_id

    def get_category_id(self, tag):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id FROM Category WHERE tag = %s', (tag,))
        cat_id = cursor.fetchone()
        cursor.close()
        return None if cat_id is None else cat_id[0]

    def insert_product(self, product):
        cursor = self.conn.cursor()
        fields = list(product.keys())
        req = 'INSERT INTO Product ({}) VALUES (%({})s)'.format(
            ', '.join(fields),
            ')s, %('.join(fields))
        cursor.execute(req, product)
        last_id = cursor.lastrowid
        cursor.close()
        return last_id

    def insert_product_category(self, product_id, category_id):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO ProductCategory (product_id, category_id)'
                       'VALUES (%s, %s)', (product_id, category_id))
        cursor.close()

    def commit(self):
        self.conn.commit()


def main():
    db = DataBase()
    for prod in get_products():
        try:
            categories = prod.pop('categories').split(',')
            categories_tags = prod.pop('categories_tags')
            product_id = db.insert_product(prod)
            for cat, cat_tag in zip(categories, categories_tags):
                cat = cat.strip()
                category_id = db.insert_category(cat_tag, cat)
                db.insert_product_category(product_id, category_id)
        except Exception as e:
            print(e)
        else:
            db.commit()


if __name__ == '__main__':
    main()