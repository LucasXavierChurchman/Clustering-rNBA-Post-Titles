from DataPipeline import pipeline
from string import punctuation
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn import metrics
from joblib import dump, load
from yellowbrick.cluster import SilhouetteVisualizer, InterclusterDistance
import matplotlib.pyplot as plt
plt.style.use('seaborn')
import numpy as np
import re
import time
import nltk
import pandas as pd
import string

def preprocessing(line):
    '''
    Custom preprocessing for vectorization
    '''
    stopword = stopwords.words('english')
    snowball_stemmer = SnowballStemmer('english')
    line = line.lower()
    line = re.sub(r"[{}]".format(string.punctuation), " ", line)
    line = ''.join(c for c in line if not c.isdigit())
    line = nltk.word_tokenize(line)
    line = [snowball_stemmer.stem(word) for word in line]
    # line = [lemmatizer.lemmatize(word) for word in line]
    line = ' '.join(line)
    return line

def cv_vectorize(text):
    start = time.time()
    vectorizer = CountVectorizer(preprocessor=preprocessing)
    cv = vectorizer.fit_transform(text)
    end = time.time()
    print('Time to generate cv = ', end - start)
    return cv

def svd_cum_var_plot(text):
    '''
    Generate a cumulative variance plot for our feature reduction
    '''
    vectorizer = CountVectorizer(preprocessor=preprocessing)
    cv = vectorizer.fit_transform(text)
    feature_names = vectorizer.get_feature_names()
    svd = TruncatedSVD(n_components=2000, random_state=1994)
    svd.fit(cv)
    features = range(svd.n_components)

    print('Original number of features: ',  len(feature_names))

    plt.figure(figsize=(9,4))
    plt.plot(np.cumsum(svd.explained_variance_ratio_), alpha=.6)
    plt.axhline(y=0.9, color='red', linestyle='dotted')
    plt.xlabel('number of components')
    plt.ylabel('explained variance')
    plt.title('SVD Explained Variance')
    plt.tight_layout()
    plt.show()
    plt.savefig('plots/SVDCumulativeVariance.png')
    plt.close()

def svd(n_components, v_mat):
    '''
    Generates SVD model and  saves for future use
    '''
    svd = TruncatedSVD(n_components= n_components, random_state = 1994)
    svd_model = svd.fit(v_mat)
    SVD_dump_path = 'models/SVD-ncomps-{}.joblib'.format(str(n_components))
    dump(svd_model, SVD_dump_path)
    return svd_model

def svd_and_kmeans(n_clusters, n_components, v_mat):
    '''
    Fit the SVD model and fit a Kmeans model with it
    '''
    svd = TruncatedSVD(n_components= n_components, random_state = 1994)
    kmeans = KMeans(n_clusters= n_clusters, random_state=1994)
    pipeline = make_pipeline(svd, kmeans)
    print('n_clusters =', kmeans.n_clusters , 'n_components_svd =', svd.n_components)
    start = time.time()
    kmeans_model = pipeline.fit(v_mat)
    labels = pipeline.predict(v_mat)
    end = time.time()
    print('Time to SVD and fit K-Means = ', end - start)
    KM_dump_path = 'models/KM-nclusters-{}.joblib'.format(str(n_clusters))
    dump(kmeans_model, KM_dump_path)
    return kmeans_model, labels

def test_cluster_sizes(n_components, cv):
    '''
    Runs the Kmeans model for difference cluster sizes and prints silhouette scores
    '''
    range_n_clusters = [2, 3, 4, 5, 6, 7, 8, 9, 10]

    for n_clusters in range_n_clusters:
        _, labels = svd_and_kmeans(n_clusters = n_clusters, n_components = n_components, v_mat = cv)

        silhouette_avg = silhouette_score(cv, labels, metric =  'cosine')
        print("For n_clusters =", n_clusters,
            "The average silhouette_score is :", silhouette_avg)
        # Compute the silhouette scores for each sample
        sample_silhouette_values = silhouette_samples(cv, labels)
        print(sample_silhouette_values)
        print('\n')

def silhouette_plot(text, model, cv):
    '''
    Loads in a saved model and produces a silhouette score plot
    '''
    path = 'models/{}'.format(model)
    pipe = load(path)
    kmeans = pipe.named_steps['kmeans']
    svd = pipe.named_steps['truncatedsvd']
    X = svd.fit_transform(cv)
    visualizer = SilhouetteVisualizer(kmeans, colors='sns_deep')
    visualizer.fit(X)
    visualizer.show(outpath="plots/Silhouette.png")
    plt.close()

def cluster_distance_map(text, model, cv):
    path = 'models/{}'.format(model)
    pipe = load(path)
    kmeans = pipe.named_steps['kmeans']
    svd = pipe.named_steps['truncatedsvd']
    X = svd.fit_transform(cv)
    visualizer = InterclusterDistance(kmeans, embedding = 'mds', )
    visualizer.fit(X)
    visualizer.show(outpath="plots/ClusterMap.png")
    plt.close()

if __name__ == '__main__':  
    file_name = 'balanced_types_2500.csv'
    data_path = '~/Galvanize/Projects/data/Capstone2Data/{}'.format(file_name)
    data = pd.read_csv(data_path)
    data = data.sample(frac=1, random_state = 1994) #shuffles data jic
    titles = list(data['title'])
    n_components = 800

    n_clusters = 6
    cv = cv_vectorize(titles)
    # SVD_cum_var_plot(all_text)
    # svd(n_components, cv)
    model, labels = svd_and_kmeans(n_clusters, 800, cv)
    # test_cluster_sizes(n_components, cv)
    # silhouette_plot(all_text, 'KM-nclusters-6.joblib', cv)
    # cluster_distance_map(all_text, 'KM-nclusters-6.joblib', cv)

    df = pd.DataFrame( {'post_number':range(len(titles)), 'label':labels } )
    df = df.sample(frac = 1, random_state = 1997)

    #Generate labeled posts
    labeled_posts = []
    for i in range(0,n_clusters):
        index = list(df[df['label']==i]['post_number'])
        print(i, data['title'].iloc[index].head(5))
        posts = pd.DataFrame( { 'cluster label': [i]*5 ,
                                'type on reddit': data['type'].iloc[index].head(),
                                'title': data['title'].iloc[index].head()},
                                index = None)
        labeled_posts.append(posts)
    labeled_posts = pd.concat(labeled_posts)
    labeled_posts.to_csv('tables/labeled_posts.csv')