import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, roc_auc_score, confusion_matrix
import joblib

df = pd.read_pickle('Data/stock_data.pkl')

df['next_close'] = df['close'].shift(-1)
df = df.drop(columns=['Name', 'date'])
df = df[np.isfinite(df).all(1)]

X = df[["open", "high", "low", "volume", "close"]]
y = df["next_close"]

# scaler = MinMaxScaler()
# X = scaler.fit_transform(X)

# poly = PolynomialFeatures(degree=2)
# X = poly.fit_transform(X)

# k = 5
# cv = KFold(n_splits=k, shuffle=True, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
#is a measure of the average squared difference between the predicted and actual values. The smaller the MSE, the better the model is at making predictions.
print("R-squared:", r2_score(y_test, y_pred)) 
#measure of how well the model fits the data. It is a value between 0 and 1, where 1 means the model perfectlyfits the data and 0 means the model does not fit the data at all. The closer R² is to 1, the better the model is at explaining the variation in the data.



# Save the model to a file
joblib.dump(model, 'model.joblib')
