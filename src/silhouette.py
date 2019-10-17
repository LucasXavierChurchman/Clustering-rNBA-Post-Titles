from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
from src.KmeansTFIDF import tf_idfvectorize, do_Kmeans
from yellowbrick.cluster import SilhouetteVisualizer
import matplotlib.pyplot as plt
from joblib import dump, load
import pandas as pd

plt.style.use('ggplot')

file_name = 'balanced_types_2500.csv'
data_path = '~/Galvanize/Projects/data/Capstone2Data/{}'.format(file_name)

data = pd.read_csv(data_path)
data.sample(frac=1, random_state = 1994) #shuffles data jic
all_text = list(data['title'])

X = tf_idfvectorize(all_text)
# transformer = TfidfTransformer()
# X_dense = transformer.fit_transform(X).todense()

kmeans = load('models/KM-tfidf-n4.joblib')
visualizer = SilhouetteVisualizer(kmeans, colors = 'yellowbrick')

visualizer.fit(X)
visualizer.show()
print(visualizer.silhouette_score_)

