import numpy as np
from sklearn.datasets import load_iris
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout, Conv2D, Flatten
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA

dataset=load_iris()
x=dataset.data
y=dataset.target
# print(x)
# print(x.shape, y.shape) #(150, 4) (150,)

scaler=StandardScaler()
scaler.fit(x)
x=scaler.transform(x)


#PCA로 컬럼 걸러내기
pca=PCA()
pca.fit(x)
cumsum=np.cumsum(pca.explained_variance_ratio_) #누적된 합 표시
# print(cumsum)

d=np.argmax(cumsum >= 1) + 1
# print(cumsum>=0.95) 
print(d) # 2 4

pca1=PCA(n_components=d)
x=pca1.fit_transform(x)


x_train, x_test, y_train, y_test=train_test_split(x, y, test_size=0.2)

y_train=to_categorical(y_train) 
y_test=to_categorical(y_test)


# x_train=x_train.reshape(x_train.shape[0], x_train.shape[1],1)
# x_test=x_test.reshape(x_test.shape[0],x_test.shape[1],1)

model=Sequential()
model.add(Dense(80, activation='relu', input_shape=(x.shape[1],)))
model.add(Dense(350, activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(550, activation='relu'))
model.add(Dense(1000, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(480, activation='relu'))
model.add(Dropout(0.4))
model.add(Dense(80, activation='relu'))
model.add(Dense(30))
model.add(Dense(3, activation='softmax'))


model.summary()
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

from tensorflow.keras.callbacks import EarlyStopping, TensorBoard
es=EarlyStopping(monitor='loss', patience=50, mode='auto')
# to_hist=TensorBoard(log_dir='graph', histogram_freq=0, write_graph=True, write_images=True)

model.fit(x_train, y_train, epochs=10000, batch_size=1, validation_split=0.2, callbacks=[es])

#4. 평가, 예측
loss, accuracy=model.evaluate(x_test, y_test, batch_size=1)

print('loss : ', loss)
print('accuracy : ', accuracy)



y_predict=model.predict(x_test)
y_predict=np.argmax(y_predict, axis=1)
y_actually=np.argmax(y_test, axis=1)
print('실제값 : ', y_actually)
print('예측값 : ', y_predict)

'''
PCA X
loss :  1.6466704607009888
accuracy :  0.8999999761581421
실제값 :  [0 0 2 0 2 0 2 1 1 2 1 1 0 2 
2 0 0 1 0 2 0 2 1 1 1 2 1 2 1 1]       
예측값 :  [0 0 2 0 2 0 1 1 1 2 1 1 0 2 
2 0 0 1 0 2 0 2 1 1 2 1 1 2 1 1] 
 
PCA 0.95
loss :  0.10601406544446945
accuracy :  1.0
실제값 :  [1 0 1 0 1 1 2 2 2 1 2 0 1 0 2 2 0 1 1 1 2 0 2 1 2 2 1 0 2 0]
예측값 :  [1 0 1 0 1 1 2 2 2 1 2 0 1 0 2 2 0 1 1 1 2 0 2 1 2 2 1 0 2 0]

PCA 1
loss :  0.17372563481330872
accuracy :  0.9333333373069763
실제값 :  [0 1 0 2 0 1 1 0 1 1 2 0 2 0 2 1 2 0 1 2 1 1 0 2 0 2 2 0 1 1]
예측값 :  [0 1 0 2 0 1 1 0 2 1 2 0 2 0 2 2 2 0 1 2 1 1 0 2 0 2 2 0 1 1]
'''