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

    cv = cv_vectorize(titles)
    # SVD_cum_var_plot(all_text)
    # svd(n_components, cv)
    model, labels = svd_and_kmeans(6, 800, cv)
    # test_cluster_sizes(n_components, cv)
    # silhouette_plot(all_text, 'KM-nclusters-6.joblib', cv)
    # cluster_distance_map(all_text, 'KM-nclusters-6.joblib', cv)

    df = pd.DataFrame( {'post_number':range(len(titles)), 'label':labels } )

    for i in [0,1,2,3,4,5]:
        index = list(df[df['label']==i]['post_number'])
        print(i, data['title'].iloc[index].head(5))
        labeled_posts = pd.DataFrame( {'label': [i]*5 , 'title': data['title'].iloc[index].head()})
        labeled_posts.to_csv('tables/labeled_posts_{}.csv'.format(str(i)))
    # vectorizer = TfidfVectorizer(preprocessor=preprocessing)
    # vectorizer.fit_transform(all_text)
    # test_predcluster = kmeans.predict(vectorizer.transform(test_lines))
    # preds = list(zip(test_types, test_predcluster, test_lines))
    # preds = pd.DataFrame.from_records(preds, columns = [ 'post_label', 'pred_cluster', 'title'])  
    # preds.to_csv('tables/test_predictions.csv')

    # test_types = ['highlights', 
    #         'highlights', 
    #         'gamethread', 
    #         'gamethread',
    #         'postgamethread', 
    #         'postgamethread', 
    #         'news',
    #         'news',
    #         'discussion',
    #         'discussion',
    #         'rostermoves',
    #         'rostermoves'
    #         'highlights',
    #         'news']

    # test_lines = ['Kristaps Porzingis Full Highlights 2019.10.14 Mavs vs Thunder - 17 Pts, 13 Rebs! | FreeDawkinsHighlights',
    #         '[Highlight] Oubre puts on a happy face for the Joker',
    #         'GAME THREAD: Minnesota Timberwolves (1-2) @ Indiana Pacers (3-0) - (October 15, 2019)',
    #         'GAME THREAD: Haifa Maccabi Haifa (0-2) @ Minnesota Timberwolves (0-2) - (October 13, 2019)Game Thread',
    #         '[Post Game Thread] The Brooklyn Nets sweep the Los Angeles Lakers in China by a score of 91-77 behind 22 points from Caris Levert',
    #         '[Post Game Thread] The Phoenix Suns defeat the Portland Trail Blazers 134-118, with Booker, Rubio, and Ayton out due to load management',
    #         '[Price] Seth Curry will not return due to a right knee contusion.'
    #         'Lowry, Gasol, Ibaka, Powell and VanVleet are all out tonight. Raptors giving their regulars some rest after the quick turnaround coming back from Japan'
    #         'Some Kobe stats from 2006, his scoring season was more impressive than hardens.',
    #         'Predict your team’s best player’s stat line for the 2019-20 season',
    #         'Some Kobe stats from 2006, his scoring season was more impressive than hardens',
    #         'Do you think Lebron will sign one-year deal to return to Cavs for his final season farewell tour?'
    #         'Journalist gets quickly shut down when she asked James Harden, Russell Westbrook if they would refrain from speaking out on politics/social justice after China debacle',
    #         'Dragan Bender is averaging 13/6/3 in the pre season on 61/54/85. Also 1.5 blocks. He’s looked great so far',
    #         'Jordan is actually a great owner. Its just that he doesnt wanna win rings/make the playoffs. He just wants to make money. And hes damn good at it.',
    #         '[Cunningham] The Minnesota Timberwolves hasnowball_stemmersnowball_stemmerve signed Tyus Battle and Barry Brown Jr, the team announced. Jordan Murphy and Lindell Wigginton have been waived to create the necessary room on the roster.']