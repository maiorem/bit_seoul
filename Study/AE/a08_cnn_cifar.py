import numpy as np
from tensorflow.keras.datasets import cifar10

# (x_train, y_train), (x_test, y_test) = mnist.load_data()
(x_train, _), (x_test, _) = cifar10.load_data()

x_train=x_train.astype('float32')/255.
x_test=x_test.astype('float32')/255.

print(x_train[0])
print(x_test[0])


x_train_noised=x_train + np.random.normal(0, 0.1, size=x_train.shape)
x_test_noised=x_test + np.random.normal(0, 0.1, size=x_test.shape)
x_train_noised=np.clip(x_train_noised, a_min=0, a_max=1)
x_test_noised=np.clip(x_test_noised, a_min=0, a_max=1)



from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Input, Conv2D, Flatten, MaxPooling2D

def autoencoder(hidden_layer_size) :
    model=Sequential()
    model.add(Conv2D(filters=hidden_layer_size, kernel_size=2, padding='same', input_shape=(x_train.shape[1], x_train.shape[2], x_train.shape[3]), activation='relu'))
    model.add(Conv2D(filters=2, kernel_size=2, padding='same', activation='relu'))
    model.add(Flatten())
    model.add(Dense(units=x_train.shape[1]*x_train.shape[2]*x_train.shape[3], activation='sigmoid'))
    return model

model=autoencoder(hidden_layer_size=256)

# model.compile(optimizer='adam', loss='binary_crossentropy')
model.compile(optimizer='adam', loss='mse')

model.fit(x_train_noised, x_train.reshape(x_train.shape[0], x_train.shape[1]*x_train.shape[2]*x_train.shape[3]).astype('float32')/255., epochs=10)
output=model.predict(x_test_noised)

import matplotlib.pyplot as plt
import random

fig, ((ax1, ax2, ax3, ax4, ax5), (ax6, ax7, ax8, ax9, ax10), (ax11, ax12, ax13, ax14, ax15)) = plt.subplots(3, 5, figsize=(20, 7))

# 이미지 다섯 개를 무작위로 고른다
random_images=random.sample(range(output.shape[0]), 5)

# 원본(입력) 이미지를 맨 위에 그린다
for i, ax in enumerate([ax1, ax2, ax3, ax4, ax5]) :
    ax.imshow(x_test[random_images[i]].reshape(x_test.shape[1], x_test.shape[2], x_test.shape[3]), cmap='gray')
    if i==0:
        ax.set_ylabel("INPUT", size=40)
    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])

# 노이즈를 넣은 이미지
for i, ax in enumerate([ax6, ax7, ax8, ax9, ax10]) :
    ax.imshow(x_test_noised[random_images[i]].reshape(x_test.shape[1], x_test.shape[2], x_test.shape[3]), cmap='gray')
    if i==0:
        ax.set_ylabel("NOISE", size=40)
    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])

# 오토인코더가 출력한 이미지를 아래에 그린다
for i, ax in enumerate([ax11, ax12, ax13, ax14, ax15]) :
    ax.imshow(output[random_images[i]].reshape(x_test.shape[1], x_test.shape[2], x_test.shape[3]), cmap='gray')
    if i==0:
        ax.set_ylabel("OUTPUT", size=40)
    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])

plt.tight_layout()
plt.show()