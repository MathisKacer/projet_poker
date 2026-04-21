# Projet Poker — Analyse statistique de parties Winamax

Analyse de données issues d'historiques de parties de poker en ligne (format Winamax), réalisée dans le cadre d'un projet Python à l'ENSAI. Les données proviennent des historiques de jeu des membres du groupe ainsi que de leurs proches.

---

## Objectifs

- Construire une base de données structurée à partir de fichiers d'historiques bruts Winamax
- Produire des statistiques descriptives sur les comportements de jeu
- Analyser l'influence de la position et du stack sur les décisions et les résultats
- Prédire le résultat d'une main à partir de features comportementales (ML)

---

## Structure du projet

```
projet_poker/
│
├── data/                          # Données et scripts de traitement
│   ├── historique/                # Fichiers dézippés depuis S3 (ignorés par Git)
│   ├── mains/                     # Fichiers de mains triés (ignorés par Git)
│   ├── resumes/                   # Fichiers résumés de tournois (ignorés par Git)
│   ├── chargement_txt.py          # Téléchargement et dézippage depuis S3
│   ├── creation_bdd_mains.py      # Parser des fichiers de mains → DataFrame
│   ├── creation_bdd_tournois.py   # Parser des fichiers résumés → DataFrame
│   └── tri_dossier.py             # Tri des fichiers en mains / résumés
│
├── src/                           # Fonctions d'analyse et de visualisation
│   ├── decision_par_position.py   # Analyse fold / all-in selon le stack en BB
│   ├── winrate.py                 # Winrate moyen par position (BTN / SB / BB)
│   ├── ranges.py                  # Visualisation des ranges de mains
│   ├── prediction.py              # Modèle de prédiction (Random Forest)
│   └── ecrire_main.py             # Notation et utilitaires sur les mains
│
├── analyse_poker_final.ipynb      # Notebook de présentation des résultats
├── execution.ipynb                # Notebook de développement
├── requirements.txt               # Dépendances Python
├── .gitignore
├── LICENSE
└── README.md
```

---

## Installation

Cloner le dépôt :

```bash
git clone <url_du_repo>
cd projet_poker
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

---

## Utilisation

Ouvrir `analyse_poker_final.ipynb` et exécuter les cellules dans l'ordre. Le notebook se charge de :

1. Télécharger les données depuis le stockage S3 public (aucune configuration nécessaire)
2. Dézipper et trier les fichiers
3. Parser les historiques et construire les deux DataFrames
4. Afficher les analyses et visualisations

---

## Données

Les données sont stockées sur un bucket S3 public (SSPCloud / Minio) et téléchargées automatiquement à l'exécution du notebook. Elles ne sont pas versionnées dans Git.

- **Source** : historiques Winamax exportés par les membres du groupe et leurs proches
- **Format** : fichiers `.txt` au format Winamax Hand History
- **Tournois** : Expresso et Expresso Nitro (format Sit & Go 3 joueurs, winner-takes-all)

---

## Bases de données produites

| DataFrame | Granularité | Colonnes principales |
|---|---|---|
| `tableau_mains` | 1 ligne = 1 main | position, stack_bb, cartes, fold_preflop, allin_preflop, benefice_bb |
| `tableau_tournois` | 1 ligne = 1 tournoi | buy_in, classement, gain, hero |

---

## Dépendances

| Bibliothèque | Usage |
|---|---|
| `pandas` | Manipulation des données |
| `matplotlib` | Visualisations |
| `seaborn` | Visualisations avancées |
| `numpy` | Calculs numériques |
| `scikit-learn` | Modèle de prédiction (Random Forest) |
| `s3fs` | Accès au stockage S3 |

---
