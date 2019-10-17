from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from src.Kmeans import Kmeans_cv, cv_vectorize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import silhouette_samples, silhouette_score
import pandas as pd

file_name = 'balanced_types_2500.csv'
data_path = '~/Galvanize/Projects/data/Capstone2Data/{}'.format(file_name)

data = pd.read_csv(data_path)
data = data.sample(frac=1, random_state = 1994) #shuffles data jic
all_text = list(data['title'])

vectorized = cv_vectorize(all_text)

range_n_clusters = [2, 3, 4, 5, 6]

dense_vec = vectorized.todense()

for n_clusters in range_n_clusters:
    kmeans = Kmeans_cv(n = n_clusters, v_matrix = vectorized)
    cluster_labels = kmeans.fit_predict(vectorized)

    silhouette_avg = silhouette_score(vectorized, cluster_labels)
    print("For n_clusters =", n_clusters,
          "The average silhouette_score is :", silhouette_avg)

    # Compute the silhouette scores for each sample
    sample_silhouette_values = silhouette_samples(vectorized, cluster_labels)