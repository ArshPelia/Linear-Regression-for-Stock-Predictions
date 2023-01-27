import pandas as pd, matplotlib.pyplot as plt, numpy as np
from sklearn.model_selection import train_test_split
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder

# df = pd.read_csv('all_stocks_5yr.csv')
# df.to_pickle('stock_data.pkl', protocol=4)

df = pd.read_pickle('stock_data.pkl')

le = LabelEncoder()
# df = df.loc[df['Name'] == 'AAL']
print(df)

df = df.drop(columns=['Name'])
df = df.drop(columns=['date'])
# X = df.drop(columns=['next_close'])  #'next_price' as the target variable and the 'price' as the input variable.
# y = df['next_close']
df = df[np.isfinite(df).all(1)]
X = df[["open", "high", "low", "volume"]] # independent variables
y = df["close"] # dependent variable
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = LinearRegression()
model.fit(X_train, y_train)

# make predictions
y_pred = model.predict(X_test)

# evaluate the model
print("Mean squared error: ", mean_squared_error(y_test, y_pred)) #is a measure of the average squared difference between the predicted and actual values. 
#It is calculated by taking the average of the squared difference between the predicted and actual values. 
#The smaller the MSE, the better the model is at making predictions.
print("R-squared: ", r2_score(y_test, y_pred)) #measure of how well the model fits the data. It is a value between 0 and 1, where 1 means the model perfectly
 #fits the data and 0 means the model does not fit the data at all. The closer R² is to 1, the better the model is at explaining the variation in the data.

# Save the model to a file
joblib.dump(model, 'model.joblib')
