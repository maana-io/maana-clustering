import numpy as np
import pandas as pd
from sklearn.datasets.samples_generator import make_blobs
from sklearn.cluster import KMeans


#X is the samples array (3 features 2 samples)
# [ 
#   [ f1, f2, f3 ]
#   [ f1, f2, f3 ]
# ]
# y is the label for the row's cluster membership
X, y = make_blobs(n_samples=10, centers=3, cluster_std=1, random_state=0, n_features=3)

print(X)

#creates the algorithm
kmeans = KMeans(init='k-means++', n_clusters = 3, random_state=0, max_iter=300 ,n_init=10)
#cluster segements 
y_kmeans = kmeans.fit_predict(X)

print(y_kmeans)