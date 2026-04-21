from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor


def feature_engineering(df):
    # hauteur des cartes
    rank_map = {r: i for i, r in enumerate('23456789TJQKA', 2)}
    df['carte haute'] = df['main'].str[0].map(rank_map)
    df['carte basse'] = df['main'].str[1].map(rank_map)

    # Variables binaires (Booleans -> 0/1)
    df['est une paire'] = df['main'].apply(lambda x: 1 if x[0] == x[1] else 0)
    df['est même signe'] = df['main'].apply(lambda x: 1 if 's' in x else 0)
    df['se suivent'] = df.apply(lambda row: 1 if abs(row['carte haute'] - row['carte basse']) == 1 else 0, axis=1)

    return df

numeric_features = ['stack_bb', 'high_card', 'level']
categorical_features = ['position', 'main']

def transfo_colonnes(df, colonnes_numeriques, colonnes_categorielles):

    preprocessor = ColumnTransformer(
        transformers=[
            # StandardScaler : centre et réduit les variables numériques
            ('num', StandardScaler(), colonnes_numeriques),
            # OneHotEncoder : transforme les textes en colonnes 0/1
            ('cat', OneHotEncoder(handle_unknown='ignore'), colonnes_categorielles)
        ])

    # 3. On intègre cela dans un Pipeline (méthode Galiana)
    poker_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])
