import pandas as pd
import matplotlib.pyplot as plt


def analyse_stack_bb(df, bins=None, labels=None):
    """
    Analyse les fréquences de fold et all-in préflop selon le stack en BB.
    
    Paramètres
    ----------
    df     : DataFrame produit par parse_folder
    bins   : liste des bornes des tranches (optionnel)
    labels : liste des noms des tranches (optionnel)
    """
    if bins is None:
        bins = [0, 5, 10, 15, 20, 25, 30, 50, float('inf')]
    if labels is None:
        labels = ['0-5', '5-10', '10-15', '15-20', '20-25', '25-30', '30-50', '50+']

    df = df.copy()
    df['stack_bb_range'] = pd.cut(df['stack_bb'], bins=bins, labels=labels)

    stats = df.groupby('stack_bb_range', observed=True).agg(
        nb_mains = ('hand_id', 'count'),
        fold_pf_pct = ('fold_preflop', 'mean'),
        allin_pf_pct = ('allin_preflop', 'mean'),
    ).round(3)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    stats['fold_pf_pct'].mul(100).plot(kind='bar', ax=axes[0], color='steelblue', edgecolor='white')
    axes[0].set_title('Fréquence de fold préflop selon le stack')
    axes[0].set_xlabel('Stack (BB)')
    axes[0].set_ylabel('%')
    axes[0].tick_params(axis='x', rotation=45)

    stats['allin_pf_pct'].mul(100).plot(kind='bar', ax=axes[1], color='coral', edgecolor='white')
    axes[1].set_title("Fréquence d'all-in préflop selon le stack")
    axes[1].set_xlabel('Stack (BB)')
    axes[1].set_ylabel('%')
    axes[1].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.show()

    return stats
