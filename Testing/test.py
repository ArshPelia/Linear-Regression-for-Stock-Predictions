import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import KFold, train_test_split, cross_val_score, GridSearchCV
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, make_scorer
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, PolynomialFeatures
from sklearn.ensemble import RandomForestRegressor

# load the data
df = pd.read_pickle('stock_data.pkl')

# create new column for next close price
df['next_close'] = df['close'].shift(-1)

# drop unnecessary columns
df = df.drop(columns=['Name'])
df = df.drop(columns=['date'])

# remove any rows with missing values
df = df[np.isfinite(df).all(1)]

# split data into X and y
X = df[["open", "high", "low", "volume","close"]] # independent variables
y = df["next_close"] # dependent variable

# Normalize the data
scaler = MinMaxScaler()
X = scaler.fit_transform(X)

# Add polynomial features
poly = PolynomialFeatures(degree=2)
X = poly.fit_transform(X)

# Use k-fold cross-validation
k = 5
cv = KFold(n_splits=k, shuffle=True, random_state=42)

# Define the model
model = RandomForestRegressor(random_state=42)

# Define the hyperparameter grid
param_grid = {'n_estimators': [100, 200, 300],
'max_depth': [3, 5, 7],
'min_samples_split': [2, 4],
'min_samples_leaf': [1, 2]}

# Define the scoring metric
scorer = make_scorer(r2_score)

# Use grid search to tune the hyperparameters
grid_search = GridSearchCV(model, param_grid, cv=cv, scoring=scorer)
grid_search.fit(X, y)

# Print the best parameters
print("Best parameters: ", grid_search.best_params_)

# split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Make predictions using the best model
y_pred = grid_search.predict(X_test)

# Evaluate the model
print("Mean squared error: ", mean_squared_error(y_test, y_pred))
print("R-squared: ", r2_score(y_test, y_pred))

# Save the model to a file
joblib.dump(grid_search.best_estimator_, 'forestmodel.joblib')