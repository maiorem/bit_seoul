#pca로 축소해서 모델을 완성하시오
#1. 0.95 이상
#2. 1 이상
#mnist dnn과 loss / acc 비교

import numpy as np
from sklearn.decomposition import PCA
from tensorflow.keras.datasets import mnist
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

(x_train, y_train), (x_test, y_test) = mnist.load_data()

x=np.append(x_train, x_test, axis=0)
print(x.shape) #(70000, 28, 28)
x=x.reshape(x.shape[0], x.shape[1]*x.shape[2])

#PCA로 컬럼 걸러내기
pca=PCA()
pca.fit(x)
cumsum=np.cumsum(pca.explained_variance_ratio_) #누적된 합 표시
# print(cumsum)

d=np.argmax(cumsum >= 0.95) + 1
# print(cumsum>=0.95) 
print(d) # 154

pca1=PCA(n_components=d)
x=pca1.fit_transform(x)
# print(x.shape) #(70000, 154)

x_train=x[:60000, :]
x_test=x[60000:, :]

# print(x_train.shape)
# print(x_test.shape)
# print(y_train.shape)
# print(y_test.shape)


y_train=to_categorical(y_train)
y_test=to_categorical(y_test)


x_train=x_train.astype('float32')/255.
x_test=x_test.astype('float32')/255.



#2. 모델
model=Sequential()
model.add(Dense(2000, activation='relu', input_shape=(d,)))
model.add(Dense(4000, activation='relu'))
model.add(Dense(3000, activation='relu'))
model.add(Dense(200, activation='relu'))
model.add(Dense(100, activation='relu'))
model.add(Dense(80, activation='relu'))
model.add(Dense(30, activation='relu'))
model.add(Dense(10, activation='softmax')) 

model.summary()

#3. 컴파일, 훈련
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

es=EarlyStopping(monitor='val_loss', patience=50, mode='auto')
model.fit(x_train, y_train, epochs=10000, batch_size=1000, verbose=1, validation_split=0.2, callbacks=[es])

#4. 평가, 예측
loss, accuracy=model.evaluate(x_test, y_test, batch_size=1000)

print('loss : ', loss)
print('accuracy : ', accuracy)


'''
PCA 없는 DNN
loss :  0.0523512804985046
accuracy :  0.9923999979972839
실제값 :  [7 2 1 0 4 1 4 9 5 9]        
예측값 :  [7 2 1 0 4 1 4 9 5 9]

PCA
loss :  0.14254632592201233
accuracy :  0.9839000105857849
'''
