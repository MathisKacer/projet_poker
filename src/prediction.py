from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.compose import ColumnTransformer



def feature_engineering(df):
    # hauteur des cartes
    rank_map = {r: i for i, r in enumerate('23456789TJQKA', 2)}
    df['carte haute'] = df['main'].str[0].map(rank_map)
    df['carte basse'] = df['main'].str[1].map(rank_map)

    # Variables binaires (Booleans -> 0/1)
    df['est une paire'] = df['main'].apply(lambda x: 1 if x[0] == x[1] else 0)
    df['est meme signe'] = df['main'].apply(lambda x: 1 if 's' in x else 0)
    df['se suivent'] = df.apply(lambda row: 1 if abs(row['carte haute'] - row['carte basse']) == 1 else 0, axis=1)
    df['main_gagnante'] = (df['benefice bb'] > 0).astype(int)

    return df
