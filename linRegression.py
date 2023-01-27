import pandas as pd, matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
# from sklearn.externals import joblib
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# df = pd.read_csv('all_stocks_5yr.csv')
# df.to_pickle('stock_data.pkl', protocol=4)

df = pd.read_pickle('stock_data.pkl')
print(df.columns)
df['next_close'] = df['close'].shift(-1)
df = df.dropna()

df = df.loc[df['Name'] == 'MGM']

# X = df.drop(columns=['next_close'])  #'next_price' as the target variable and the 'price' as the input variable.
# y = df['next_close']
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

def lossfn(m, b, points):
    total_error = 0
    for i in range(len(points)):
        x = points.iloc[i].close
        y = points.iloc[i].next_close
        total_error += (y - (m + x + b) ** 2)
    total_error / float(len(points)) #dif between prediction and outcome

def grad_descent(m_now, b_now, points, L):
    m_gradiant = 0
    b_gradiant = 0

    n = len(points)

    for i in range(n):
        x = points.iloc[i].close
        y = points.iloc[i].next_close

        m_gradiant += -(2/n) * x * (y - (m_now * x + b_now))
        b_gradiant += -(2/n) * (y - (m_now * x + b_now))

    m = m_now - m_gradiant * L
    b = b_now - b_gradiant * L
    return m, b

m = 0
b = 0
L = 0.001
epochs = 200

for i in range(epochs):
    if i % 50 == 0:
        print(f'Epoch: {i}')
    m, b = grad_descent(m , b, df, L)

print(m,b)

plt.scatter(df.close, df.next_close, color = "black")
plt.plot(list(range(10, 50)), [m * x + b for x in range(10,50)], color='red')
plt.show()


# # Save the model to a file
# joblib.dump(model, 'model.joblib')

# # load the model
# loaded_model = joblib.load('model.joblib')

print('')
print('---------------------------------------')
print('finished')