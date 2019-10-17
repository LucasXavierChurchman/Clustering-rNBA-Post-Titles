from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from src.Kmeans import Kmeans_tfidf, tfidf_vectorize, cv_vectorize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import silhouette_samples, silhouette_score
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('seaborn')

file_name = 'balanced_types_2500.csv'
data_path = '~/Galvanize/Projects/data/Capstone2Data/{}'.format(file_name)

data = pd.read_csv(data_path)
data = data.sample(frac=1, random_state = 1994) #shuffles data jic
all_text = list(data['title'])

tfidf = tfidf_vectorize(all_text)

range_n_clusters = [2, 3, 4, 5, 6, 7, 8, 9, 10]

dense_vec = tfidf.todense()

for n_clusters in range_n_clusters:
    svd_kmeans, labels = Kmeans_tfidf(n = n_clusters, tfidf = tfidf)

    silhouette_avg = silhouette_score(tfidf, labels, metric =  'cosine')
    print("For n_clusters =", n_clusters,
          "The average silhouette_score is :", silhouette_avg)

    # Compute the silhouette scores for each sample
    sample_silhouette_values = silhouette_samples(tfidf, labels)
    print('\n')