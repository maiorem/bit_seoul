#와인은 csv로

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import accuracy_score, r2_score
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler, MaxAbsScaler
from xgboost import XGBClassifier, XGBRegressor, plot_importance

wine=pd.read_csv('./data/csv/winequality-white.csv', sep=';', header=0)
y=wine['quality']
x=wine.drop('quality', axis=1)

x_train, x_test, y_train, y_test=train_test_split(x, y, train_size=0.8)

parameters= [
    {'xgbclassifier__n_estimators' : [100,200, 300],
    'xgbclassifier__learning_rate' : [0.1,0.3,0.001,0.01],
    'xgbclassifier__max_depth' : [4,5,6]}, 
    {'xgbclassifier__n_estimators' : [100,200, 300],
    'xgbclassifier__learning_rate' : [0.1, 0.001, 0.01],
    'xgbclassifier__max_depth' : [4,5,6],
    'xgbclassifier__colsample_bytree' :[0.6, 0.9, 1]},
    {'xgbclassifier__n_estimators' : [90, 110],
    'xgbclassifier__learning_rate' : [0.1, 0.001, 0.5],
    'xgbclassifier__max_depth' : [4,5,6],
    'xgbclassifier__colsample_bytree' :[0.6, 0.9, 1],
    'xgbclassifier__colsample_bylevel' :[0.6, 0.7, 0.9]}
] 

#2. 모델
# pipe=Pipeline([("scaler", MinMaxScaler()), ('jin', XGBRegressor())])
pipe=make_pipeline(MinMaxScaler(), XGBClassifier()) 
model=RandomizedSearchCV(pipe, parameters, cv=5) 


#3. 훈련
model.fit(x_train, y_train) 

#4. 평가, 예측
print("최적의 매개변수 : ", model.best_estimator_)
y_predict=model.predict(x_test)
print('최종정답률 : ', accuracy_score(y_test, y_predict))

'''
최적의 매개변수 :  Pipeline(steps=[('minmaxscaler', MinMaxScaler()),
                ('xgbclassifier',
                 XGBClassifier(base_score=0.5, booster='gbtree',
                               colsample_bylevel=0.9, colsample_bynode=1,
                               colsample_bytree=0.6, gamma=0, gpu_id=-1,
                               importance_type='gain',
                               interaction_constraints='', learning_rate=0.5,
                               max_delta_step=0, max_depth=5,
                               min_child_weight=1, missing=nan,
                               monotone_constraints='()', n_estimators=110,
                               n_jobs=0, num_parallel_tree=1,
                               objective='multi:softprob', random_state=0,
                               reg_alpha=0, reg_lambda=1, scale_pos_weight=None,
                               subsample=1, tree_method='exact',
                               validate_parameters=1, verbosity=None))])
최종정답률 :  0.6459183673469387
'''