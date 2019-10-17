from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import string
import nltk

plt.style.use('seaborn')

stopword = stopwords.words('english')
snowball_stemmer = SnowballStemmer('english')

def preprocessing(line):
    '''
    Custom preprocessing for tf-idf vectorization
    '''
    line = line.lower()
    line = re.sub(r"[{}]".format(string.punctuation), " ", line)
    line = ''.join(c for c in line if not c.isdigit())
    line = nltk.word_tokenize(line)
    line = [snowball_stemmer.stem(word) for word in line]
    # line = [lemmatizer.lemmatize(word) for word in line]
    line = ' '.join(line)
    return line


file_name = 'balanced_types_2500.csv'
data_path = '~/Galvanize/Projects/data/Capstone2Data/{}'.format(file_name)

data = pd.read_csv(data_path)
data = data.sample(frac=1, random_state = 1994) #shuffles data jic
text = list(data['title'])

# Create a TfidfVectorizer: tfidf
tfidf = CountVectorizer(preprocessor=preprocessing) 

# Apply fit_transform to document: csr_mat
tf_idf = tfidf.fit_transform(text)

# Get the words: words
word = tfidf.get_feature_names()

svd = TruncatedSVD(n_components=2000, random_state=1994)

svd.fit(tf_idf)

features = range(svd.n_components)

plt.figure(figsize=(9,4))

plt.plot(np.cumsum(svd.explained_variance_ratio_), alpha=.6)
plt.axhline(y=0.9, color='black', linestyle='dotted')
plt.axhline(y=0.75, color='red', linestyle='dotted')
plt.xlabel('number of components')
plt.ylabel('explained variance')
plt.title('SVD Explained Variance')
plt.tight_layout()
plt.savefig('images/svd_cum_var.png')

# plt.plot(np.cumsum(pca.explained_variance_ratio_))
# plt.xlabel('number of components')
# plt.ylabel('cumulative explained variance');