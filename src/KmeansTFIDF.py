import re
import nltk
import pandas as pd
import string
from datapipeline import pipeline
from string import punctuation
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn import metrics
from joblib import dump, load


test_types = ['highlights', 
        'highlights', 
        'gamethread', 
        'gamethread',
        'postgamethread', 
        'postgamethread', 
        'news',
        'news',
        'discussion',
        'discussion',
        'rostermoves',
        'rostermoves'
        'highlights',
        'news']

test_lines = ['Kristaps Porzingis Full Highlights 2019.10.14 Mavs vs Thunder - 17 Pts, 13 Rebs! | FreeDawkinsHighlights',
        '[Highlight] Oubre puts on a happy face for the Joker',
        'GAME THREAD: Minnesota Timberwolves (1-2) @ Indiana Pacers (3-0) - (October 15, 2019)',
        'GAME THREAD: Haifa Maccabi Haifa (0-2) @ Minnesota Timberwolves (0-2) - (October 13, 2019)Game Thread',
        '[Post Game Thread] The Brooklyn Nets sweep the Los Angeles Lakers in China by a score of 91-77 behind 22 points from Caris Levert',
        '[Post Game Thread] The Phoenix Suns defeat the Portland Trail Blazers 134-118, with Booker, Rubio, and Ayton out due to load management',
        '[Price] Seth Curry will not return due to a right knee contusion.'
        'Lowry, Gasol, Ibaka, Powell and VanVleet are all out tonight. Raptors giving their regulars some rest after the quick turnaround coming back from Japan'
        'Some Kobe stats from 2006, his scoring season was more impressive than hardens.',
        'Predict your team’s best player’s stat line for the 2019-20 season',
        'Some Kobe stats from 2006, his scoring season was more impressive than hardens',
        'Do you think Lebron will sign one-year deal to return to Cavs for his final season farewell tour?'
        'Journalist gets quickly shut down when she asked James Harden, Russell Westbrook if they would refrain from speaking out on politics/social justice after China debacle',
        'Dragan Bender is averaging 13/6/3 in the pre season on 61/54/85. Also 1.5 blocks. He’s looked great so far',
        'Jordan is actually a great owner. Its just that he doesnt wanna win rings/make the playoffs. He just wants to make money. And hes damn good at it.',
        '[Cunningham] The Minnesota Timberwolves have signed Tyus Battle and Barry Brown Jr, the team announced. Jordan Murphy and Lindell Wigginton have been waived to create the necessary room on the roster.']

stopword = stopwords.words('english')
snowball_stemmer = SnowballStemmer('english')

def preprocessing(line):
    '''
    Custom preprocessing for tf-idf vectorization
    '''
    line = line.lower()
    line = re.sub(r"[{}]".format(string.punctuation), " ", line)
    line = nltk.word_tokenize(line)
    line = [snowball_stemmer.stem(word) for word in line]
    line = ' '.join(line)
    return line

def tf_idfvectorize(text):
    vectorizer = TfidfVectorizer(preprocessor=preprocessing)
    tfidf = vectorizer.fit_transform(text)
    # vocab = vectorizer.vocabulary_
    # sorted_vocab = dict(sorted((value,key) for (key,value) in vocab.items()), reverse = True)
    return tfidf

def do_Kmeans(n, v_matrix):
    kmeans = KMeans(n_clusters=n, random_state=2007).fit(v_matrix)
    dump_path = 'KM-tfidf-n{}.joblib'.format(str(n))
    dump(kmeans, dump_path)
    return kmeans

if __name__ == '__main__':  
    file_name = 'balanced_types_2500.csv'
    data_path = '~/Galvanize/Projects/data/Capstone2Data/{}'.format(file_name)

    data = pd.read_csv(data_path)
    data.sample(frac=1, random_state = 1994) #shuffles data jic
    all_text = list(data['title'])
    
    tf_idf = tf_idfvectorize(all_text)

    kmeans = do_Kmeans(10, tf_idf)
    kmeans = load('KM-tfidf-n10.joblib')
    labels = kmeans.labels_
    silh_score = metrics.silhouette_score(tf_idf, labels, metric='euclidean')
    print(silh_score)
    
    vectorizer = TfidfVectorizer(preprocessor=preprocessing)
    vectorizer.fit_transform(all_text)
    test_predcluster = kmeans.predict(vectorizer.transform(test_lines))
    preds = list(zip(test_types, test_predcluster, test_lines))
    preds = pd.DataFrame.from_records(preds, columns = [ 'post_label', 'pred_cluster', 'title'])  
    preds.to_csv('tables/test_predictions.csv')

