# SAE 2-02 : automates finis en Python

SAE « Exploration algorithmique d'un problème » du BUT Informatique 1re année, IUT de Marne-la-Vallée, Université Gustave Eiffel (2025 - 2026).

Implémentation en Python des algorithmes du cours sur les mots, les langages et les automates finis. Le sujet est dans [sae.pdf](sae.pdf).

## Représentation

Un mot est une chaîne de caractères, un langage une liste de mots, et un automate un dictionnaire :

```python
auto = {
    "alphabet": ['a', 'b'],
    "etats": [1, 2, 3, 4],
    "transitions": [[1, 'a', 2], [2, 'a', 2], [2, 'b', 3], [3, 'a', 4]],
    "I": [1],   # états initiaux
    "F": [4],   # états finaux
}
```

## Fonctions réalisées

| Partie | Fonctions |
| --- | --- |
| Mots | `pref`, `suf`, `fact`, `miroir` |
| Langages | `concatene`, `puis`, `tousmots` |
| Automates | `lirelettre`, `liremot`, `accepte`, `langage_accept` |
| Déterminisation | `deterministe`, `determinise`, `renommage` |
| Complémentation | `complet`, `complete`, `complement` |
| Automate produit | `inter`, `difference` |
| Fermeture | `prefixe`, `suffixe`, `facteur`, `miroir_auto` |
| Minimisation | `minimise` (algorithme de Moore, par raffinement de partitions) |

## Lancer

Python 3, aucune bibliothèque à installer.

```
python3 "SAE math.py"
```

Le programme affiche les résultats des tests de chaque partie sur les automates d'exemple définis dans le fichier.
