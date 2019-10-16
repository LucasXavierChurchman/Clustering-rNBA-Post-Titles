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

if __name__ == '__main__':
    
    test_lines = ['[Post Game Thread] The Toronto Raptors (45-17) blowout the Boston Celtics (37-24), 118-95',
                '[Post Game Thread] The Warriors (25-13) blow out the Suns (9-29) 132-109!',
                '[Stein] The Mavericks will acquire Kelly Olynyk and Derrick Jones from the Heat as part of the Jimmy Butler sign-and-trade, league sources say.',
                '[Wojnarowski] Veteran F/C Donatas Motiejunas plans to sign with the Spurs today, league sources tell ESPN. He will meet team on its current trip. Motiejunas has been playing in China for the past two seasons',
                'Jamal Murray vs Andrew Wiggins premature max contract stats',
                'Triple Doubles are the most important stat in basketball',
                'Damian Lillard sends it to OT - NBCSC',
                '[Highlights] Gordon Hayward drops 35 on 14/18 fg, 4/7 3PT, with 5 assists - Full Highlights with Defense"'
                'GAME THREAD: New York Knicks (9-28) @ Denver Nuggets (23-11) - (January 01, 2019)',
                'GAME THREAD: Brooklyn Nets (1-0) @ Philadelphia 76ers (0-1) - (April 15, 2019)'] 

    #need to pop samples from training data       
    file_name = 'balanced_types_1000.csv'
    data_path = '~/Galvanize/Projects/data/Capstone2Data/{}'.format(file_name)

    data = pd.read_csv(data_path)
    data.sample(frac=1, random_state = 1994) #shuffles data
    all_text = list(data['title'])
    
    vectorizer = TfidfVectorizer(preprocessor=preprocessing)
    tfidf = vectorizer.fit_transform(all_text)
    vocab = vectorizer.vocabulary_
    sorted_vocab = dict(sorted((value,key) for (key,value) in vocab.items()), reverse = True)

    kmeans = KMeans(n_clusters=6).fit(tfidf)
    print(kmeans.predict(vectorizer.transform(test_lines)))
    
    
