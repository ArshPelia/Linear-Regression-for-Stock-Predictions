import pandas as pd, matplotlib.pyplot as plt, numpy as np
from sklearn.model_selection import train_test_split
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder

# df = pd.read_csv('all_stocks_5yr.csv')
# df.to_pickle('stock_data.pkl', protocol=4)

df = pd.read_pickle('stock_data.pkl')
# print(df.columns)
# df['next_close'] = df['close'].shift(-1)
# df = df.dropna()

le = LabelEncoder()
# df = df.loc[df['Name'] == 'AAL']
print(df)

# plt.scatter(df.date, df.close, color = "black")
# plt.title("Stock Price")
# plt.xlabel("Date")
# plt.ylabel("Price")
# plt.show()

# df['Name'] = le.fit_transform(df['Name'])
# df['date'] = pd.to_datetime(df['date'])
# df['date'] = df['date'].values.astype(float)
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

# load the model
model = joblib.load('model.joblib')

stock_open = 50
stock_high = 52
stock_low = 48
stock_volume = 1000000
# stock_close = 51
stock_prediction = model.predict([[stock_open, stock_high, stock_low, stock_volume]])
print("Predicted stock price: ", stock_prediction)

current_stock_price = df.iloc[-1]['close']
if stock_prediction > current_stock_price:
    print("It is a good idea to invest in this stock")
else:
    print("It might be a good idea to wait before investing in this stock")

print('')
print('---------------------------------------')
print('finished')