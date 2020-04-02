import db


def numbered_choice(items):
    """ Prompt the user to choose an item from a numbered list.
    Return index of choice"""
    # Print numbered list
    for i, choice in enumerate(items):
        print('{} - {}'.format(i + 1, choice))
    # Ask user until answer is valid
    while True:
        answer = input('>>> ')
        if answer.isdigit() and 0 < int(answer) <= len(items):
            break
        else:
            print('Entrée invalide !')
    return int(answer) - 1


def search_category():
    print('Entrez votre recherche')
    search = input('>>> ')
    categories = db.search_categories(search)
    if categories:
        names = [cat.name for cat in categories]
        return categories[numbered_choice(names)]
    else:
        print('Aucun résultats')


def select_product():
    category = search_category()
    if category:
        products = category.products()
        descriptions = [prod.short_description() for prod in products]
        return products[numbered_choice(descriptions)]


if __name__ == '__main__':
    print(select_product().short_description())
