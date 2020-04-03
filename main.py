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


def search_product():
    """ Search products using user's key words. Return Product object
    or None"""
    while True:
        print('Chercher un produit, entrez vos mots clés.')
        search = input('>>> ')
        products = db.search_products(search)
        if products:
            descriptions = [prod.short_description() for prod in products]
            return products[numbered_choice(descriptions)]
        else:
            print('Aucun résultats')


def find_substitute():
    """ Help user find a substitute for a product"""
    original = search_product()
    print(original.description())
    for substitute in original.substitutes():
        print('Substitut possible:')
        print(substitute.description())
        choice = numbered_choice(('Enregistrer ce substitut',
                                  'Voir un autre substitut',
                                  'Retour'))
        if choice == 0:
            db.save_substitute(original, substitute)
            print('Substitut sauvegardé')
            break
        elif choice == 2:
            break


def browse_saved_substitutes():
    saved_substitutes = db.get_saved_substitutes()
    names = [sub.short_description() for original, sub in saved_substitutes]
    original, substitute = saved_substitutes[numbered_choice(names)]
    print('Substitut pour ' + original.short_description())
    print(substitute.description())


def main():
    while True:
        choice = numbered_choice(('Quel aliment souhatez-vous remplacer?',
                                  'Retrouver mes aliments substitués',
                                  'Quitter'))
        (find_substitute, browse_saved_substitutes, quit)[choice]()


if __name__ == '__main__':
    main()
