from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score


def feature_engineering(df):
    # hauteur des cartes
    rank_map = {r: i for i, r in enumerate('23456789TJQKA', 2)}
    df['carte haute'] = df['main'].str[0].map(rank_map)
    df['carte basse'] = df['main'].str[1].map(rank_map)

    # Variables binaires (Booleans -> 0/1)
    df['est une paire'] = df['main'].apply(lambda x: 1 if x[0] == x[1] else 0)
    df['est même signe'] = df['main'].apply(lambda x: 1 if 's' in x else 0)
    df['se suivent'] = df.apply(lambda row: 1 if abs(row['carte haute'] - row['carte basse']) == 1 else 0, axis=1)
    df['main_gagnante'] = (df['benefice bb'] > 0).astype(int)

    return df

numeric_features = ['stack_bb', 'high_card', 'level']
categorical_features = ['position', 'main']


def regression(df, variables_numeriques, variables_categorielles):
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), variables_numeriques),
            ('cat', OneHotEncoder(handle_unknown='ignore'), variables_categorielles)
        ])

    reg_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])

    # Pipeline de régression
    reg_pipeline = Pipeline([
        ('prepro', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])

    X = df[variables_numeriques + variables_categorielles]
    y_reg = df['benefice bb']

    X_train, X_test, y_train, y_test = train_test_split(X, y_reg, test_size=0.2, random_state=42)

    reg_pipeline.fit(X_train, y_train)
    y_pred_reg = reg_pipeline.predict(X_test)

    print(f"R² Score: {r2_score(y_test, y_pred_reg):.4f}")
    print(f"Erreur Moyenne (MAE): {mean_absolute_error(y_test, y_pred_reg):.2f} BB")
