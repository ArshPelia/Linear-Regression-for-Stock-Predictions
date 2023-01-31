import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, PolynomialFeatures
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, median_absolute_error
import joblib

df = pd.read_pickle('Data/stock_data.pkl')

df['next_close'] = df['close'].shift(-1)
df = df.drop(columns=['Name', 'date'])
df = df[np.isfinite(df).all(1)]

X = df[["open", "high", "low", "volume", "close"]]
y = df["next_close"]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = Ridge(alpha=0.5)
model.fit(X_train, y_train)


# y_pred = model.predict(X_test)
y_pred = model.predict(X_test)

# Plot the actual vs. predicted values
plt.scatter(y_test, y_pred)
plt.xlabel("Actual")
plt.ylabel("Predicted")
plt.title("Actual vs. Predicted")
plt.show()

print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
#measure of how well the model fits the data. It is a value between 0 and 1, where 1 means the model perfectlyfits the data and 0 means the model does not fit the data at all. The closer R² is to 1, the better the model is at explaining the variation in the data.
print("Mean Absolute Error:", mean_absolute_error(y_test, y_pred))
#is the average of the absolute differences between the predicted and actual values. It is a measure of how well the model fits the data. The smaller the MAE, the better the model is at making predictions.
print("Median Absolute Error:", median_absolute_error(y_test, y_pred))
#is the median of the absolute differences between the predicted and actual values. It is a measure of how well the model fits the data. The smaller the MAE, the better the model is at making predictions.
print("R2 Score:", r2_score(y_test, y_pred))

# Save the model to a file
joblib.dump(model, 'model.joblib')
