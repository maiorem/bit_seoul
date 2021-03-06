import numpy as np
from sklearn.decomposition import PCA
from sklearn.datasets import load_diabetes

datasets=load_diabetes()
x=datasets.data
y=datasets.target

print(x.shape) #(442, 10)

# pca=PCA(n_components=5) # 축소할 컬럼의 갯수
# x2d=pca.fit_transform(x)
# print(x2d.shape) #(442, 9)

# pca_EVR=pca.explained_variance_ratio_ 
# print(pca_EVR)
# print(sum(pca_EVR))

pca=PCA()
pca.fit(x)
cumsum=np.cumsum(pca.explained_variance_ratio_) #누적된 합 표시
print(cumsum)

d=np.argmax(cumsum >= 0.95) + 1
print(cumsum>=0.95) # [False False False False False False False  True  True  True]
print(d) # 8

import matplotlib.pyplot as plt

plt.plot(cumsum)
plt.grid()
plt.show()