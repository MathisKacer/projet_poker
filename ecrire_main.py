def notation_main(liste_cartes):
    """
    Transforme le format d'une main en disant seulement si les signes sont les mêmes
    """

    valeur1, signe1 = liste_cartes[0][0], liste_cartes[0][1]
    valeur2, signe2 = liste_cartes[1][0], liste_cartes[1][1]

    # toujours le même ordre de valeurs pour les signes
    rank_order = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10,
                  '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2}

    if rank_order[valeur2] > rank_order[valeur1]:
        valeur1, valeur2 = valeur2, valeur1
        signe1, signe2 = signe2, signe1

    # On détermine si c'est suitée (s) ou dépareillée (o)
    if signe1 == signe2 :
        suffixe = 's'
    else :
        suffixe = 'o'
    return f"{valeur1}{valeur2}{suffixe}"
