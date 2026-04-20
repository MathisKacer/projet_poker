import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def range(df, metric):
    ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
    matrix = pd.DataFrame(np.nan, index=ranks, columns=ranks)

    nb_distribuees = df.groupby('main').size()

    # Agrégation des stats
    mains_jouees = df[df["fold_preflop"] == False].groupby('main')['benefice bb'].agg(['mean', 'var', 'count']).reset_index()

    for _, row in mains_jouees.iterrows():
        main = row['main']

        if metric == 'freq':
            nb_recue = nb_distribuees[main]
            val = (row['count'] / nb_recue) * 100
        else:
            val = row[metric]

        r1, r2 = main[0], main[1]

        # Cas des Paires (ex: AAo, 88o)
        if r1 == r2:
            matrix.loc[r1, r2] = val
        # Cas des Suitées (ex: AKs) -> au-dessus de la diagonale
        elif main[2] == 's':
            matrix.loc[r1, r2] = val
        # Cas des Non-suitées (ex: AKo) -> en-dessous de la diagonale
        elif main[2] == 'o':
            matrix.loc[r2, r1] = val

    return matrix

def affichage_range(df, metric):
    ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

    config_all = {
        'mean': {'title': 'Moyenne des gains (BB)', 'cmap': 'RdYlGn', 'fmt': '.1f'},
        'var': {'title': 'Variance (Volatilité)', 'cmap': 'YlOrBr', 'fmt': '.1f'},
        'freq': {'title': 'Fréquence de jeu (Proportion en %)', 'cmap': 'Purples', 'fmt': '.2f'}
    }

    conf = config_all[metric]
    matrix = range(df, metric)

    plt.figure(figsize=(12, 10))

    # On dessine la heatmap
    ax = sns.heatmap(matrix, annot=True, fmt=conf['fmt'], cmap=conf['cmap'],
                     cbar_kws={'label': conf['title']}, mask=matrix.isnull())

    # Ajout des noms des mains pour la légende visuelle
    for i, r1 in enumerate(ranks):
        for j, r2 in enumerate(ranks):
            if i == j:
                label = f"{r1}{r2}"
            elif i < j:
                label = f"{r1}{r2}s"
            else:
                label = f"{r2}{r1}o"

            ax.text(j+0.5, i+0.15, label, ha='center', va='center',
                    fontsize=9, color='black', alpha=0.5)

    plt.title(conf['title'], fontsize=15)
    plt.show()
