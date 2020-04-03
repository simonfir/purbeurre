# PurBeurre

PurBeurre is an cli app that help you find healthier alternatives to
the not-so-healthy foods you love.

It uses the Open Food Facts database, only products sold in France are
suported.

# Usage

## Finding an alternative to a product
```
1 - Quel aliment souhaitez-vous remplacer?
2 - Retrouver mes aliments substitués
3 - Quitter
>>> 1

1 - Recherchez par catégorie
2 - Recherchez par produit
>>> 1

Recherchez une catégorie
>>> pâtes à tartiner

1 - Pâtes à tartiner
2 - Pâtes à tartiner aux noisettes
3 - Pâtes à tartuner au chocolat
4 - ...
>>> 2

Catégorie: pâtes à tartiner
Choisissez un produit
1 - Nutella
2 - Pâte choco noisette
3 - ...
>>> 1

Substitut possible pour Nutella (nutriscore E):

Pâte choco noisette (nutriscore D)
description: pâte à tartiner
magasin où l'acheter: auchan, carfour, ...
page openfoodfact: www.openfoodfact.org/15649653
```

## Saving a substitute

```
Substitut possible pour Nutella (nutriscore E):

Pâte choco noisette (nutriscore D)
description: pâte à tartiner
magasin où l'acheter: auchan, carfour, ...
page openfoodfact: www.openfoodfact.org/15649653

1 - Voir un autre substitut
2 - Enregistrer le substitut
>>> 2

Substitut enregistré.
```

## Browse saved substitutes

```
1 - Quel aliment souhaitez-vous remplacer?
2 - Retrouver mes aliments substitués
3 - Quitter
>>> 2

1 - Pâte choco noisette (substitut pour: Nutella)
2 - ...
>>> 1

Pâte choco noisette (nutriscore D)
enregistré comme substitut pour: Nutella (nutriscore E)
description: pâte à tartiner
magasin où l'acheter: auchan, carfour, ...
page openfoodfact: www.openfoodfact.org/15649653
```
