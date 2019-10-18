from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
import plotly.express as px
from joblib import dump, load
from Analysis import svd_and_kmeans, cv_vectorize, preprocessing
import pandas as pd

path = 'models/KM-nclusters-6.joblib'
model = load(path)

cv = CountVectorizer(preprocessor=preprocessing)
tf = TfidfTransformer()

file_name = 'balanced_types_2500.csv'
data_path = '~/Galvanize/Projects/data/Capstone2Data/{}'.format(file_name)
data = pd.read_csv(data_path)
data = data.sample(frac=1, random_state = 1994) #shuffles data jic
titles = list(data['title'])

X = cv.fit_transform(titles).todense()

pca = PCA(n_components=3).fit(X)
data2D = pca.transform(X)
plt.scatter(data2D[:,0], data2D[:,1], data2D[:,2])
plt.show()
