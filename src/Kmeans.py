import re
import nltk
from datapipeline import pipeline
import string
from string import punctuation
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import pandas as pd


def preprocessing(line):
    line = line.lower()
    line = re.sub(r"[{}]".format(string.punctuation), " ", line)
    return line

stopword = stopwords.words('english')
snowball_stemmer = SnowballStemmer('english')


if __name__ == '__main__':
    
    # file_name = 'posts_2019.csv'
    test_line = '[Post Game Thread] The Toronto Raptors (45-17) blowout the Boston Celtics (37-24), 118-95'
    file_name = 'test_set.csv'
    data_path = '~/Galvanize/Projects/data/Capstone2/{}'.format(file_name)
    #need to balance classes
    data = pd.read_csv(data_path)
    all_text = list(data['title'])
    
    tfidf_vectorizer = TfidfVectorizer(preprocessor=preprocessing)
    tfidf = tfidf_vectorizer.fit_transform(all_text)

    kmeans = KMeans(n_clusters=6).fit(tfidf)
    tfidf_vectorizer.transform(lines_for_predicting)
    
