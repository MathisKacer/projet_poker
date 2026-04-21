import matplotlib.pyplot as plt


def winrate_par_position(df):
    """
    Calcule et affiche le winrate moyen en BB par position (BTN, SB, BB).
    """
    stats = df.groupby('position').agg(
        nb_mains = ('hand_id', 'count'),
        winrate_bb = ('benefice bb', 'mean'),
        net_bb_total = ('benefice bb', 'sum'),
    ).round(3)

    print(stats)

    stats['winrate_bb'].plot(
        kind='bar',
        color=['steelblue' if x >= 0 else 'coral' for x in stats['winrate_bb']],
        edgecolor='white',
        figsize=(6, 4)
    )
    plt.axhline(0, color='black', linestyle='--', alpha=0.5)
    plt.title('Winrate moyen par position (BB/main)')
    plt.xlabel('Position')
    plt.ylabel('BB/main')
    plt.tick_params(axis='x', rotation=0)
    plt.tight_layout()
    plt.show()
