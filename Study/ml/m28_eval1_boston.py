from xgboost import XGBClassifier, XGBRegressor
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.metrics import r2_score

#1. 데이터
x, y=load_boston(return_X_y=True)
x_train, x_test, y_train, y_test=train_test_split(x, y, train_size=0.8, random_state=77)

#2. 모델
# model=XGBRegressor(n_estimators=100, learning_rate=0.1)
model=XGBRegressor()

#3. 훈련
model.fit(x_train, y_train, verbose=True, eval_metric='rmse', eval_set=[(x_train, y_train), (x_test, y_test)])

# eva_metrics 대표 params => rmse, mae, logloss, error, auc

#4. 평가
results=model.evals_result()
# print("eval's results :", results)

y_predict=model.predict(x_test)

r2=r2_score(y_test, y_predict)
print("R2 :", r2)

score=model.score(x_test, y_test)
print("score : ", score)