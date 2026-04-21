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

def comparer_profit_horaire(df_tournois, liste_joueurs):
    """
    Compare le gain moyen par heure pour une liste de joueurs.
    """
    plt.figure(figsize=(14, 7))

    # Copie pour ne pas modifier le DataFrame original
    df = df_tournois.copy()

    # Conversion en datetime et extraction de l'heure
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['heure'] = df['start_date'].dt.hour

    # Calcul du profit net avec tes variables
    # Profit = Ce qu'on gagne - (Prix du tournoi + Taxe/Rake)
    df['profit_net'] = df['prizepool'] - (df['buy_in_rake'] + df['buy_in_price'])

    # Filtrer pour les joueurs demandés
    df_selection = df[df['joueur'].isin(liste_joueurs)]

    # Calcul de la moyenne par heure et par joueur
    # On utilise pivot_table pour faciliter le traçage
    stats_h = df_selection.groupby(['heure', 'joueur'])['profit_net'].mean().unstack()

    # Remplir les heures vides par 0 pour éviter les trous dans la courbe
    stats_h = stats_h.reindex(range(24)).fillna(0)

    # Tracé
    for joueur in stats_h.columns:
        plt.plot(stats_h.index, stats_h[joueur], marker='o', label=joueur, linewidth=2)

    plt.axhline(0, color='black', linestyle='--', alpha=0.3)
    plt.xticks(range(24))
    plt.title("Rentabilité moyenne par heure et par joueur", fontsize=15)
    plt.xlabel("Heure de la journée (0h - 23h)", fontsize=12)
    plt.ylabel("Gain moyen par tournoi (€)", fontsize=12)
    plt.legend()
    plt.grid(True, axis='y', linestyle=':', alpha=0.7)
    plt.show()
