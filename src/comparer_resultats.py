import matplotlib.pyplot as plt
import pandas as pd

def comparer_bankroll_joueurs(df_tournois, liste_joueurs):
    """
    Compare l'évolution du profit cumulé de plusieurs joueurs.
    df_tournois : DataFrame des résumés de tournois
    liste_joueurs : list de strings (ex: ['Pseudo1', 'Pseudo2'])
    """
    plt.figure(figsize=(14, 7))

    for joueur in liste_joueurs:
        df_j = df_tournois[df_tournois['joueur'] == joueur].sort_values('start_date').copy()

        if len(df_j) == 0:
            print(f"Aucune donnée pour le joueur : {joueur}")
            continue

        # Calcul du profit net et cumulé
        df_j['profit_net'] = df_j['prizepool'] - (df_j['buy_in_rake'] + df_j['buy_in_price'])
        df_j['bankroll_cumulee'] = df_j['profit_net'].cumsum()

        # On utilise l'index de 0 à N pour comparer le volume de jeu
        plt.plot(range(len(df_j)), df_j['bankroll_cumulee'], label=joueur, linewidth=2)

    plt.axhline(0, color='black', linestyle='--', alpha=0.3)
    plt.title("Comparaison de la progression des gains par joueur", fontsize=15)
    plt.xlabel("Nombre de tournois joués", fontsize=12)
    plt.ylabel("Profit Net Cumulé (€)", fontsize=12)
    plt.legend()
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    plt.show()
