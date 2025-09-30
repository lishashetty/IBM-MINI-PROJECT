import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

df = pd.read_csv("dataset.csv")
X = df[['type','brand','material','size','season']]
y = df['price']

categorical_features = ['type','brand','material','size','season']
preprocessor = ColumnTransformer(
    transformers=[('cat', OneHotEncoder(), categorical_features)]
)

model = Pipeline([
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model.fit(X_train, y_train)


joblib.dump(model, 'model.pkl')
print("Model trained and saved!")