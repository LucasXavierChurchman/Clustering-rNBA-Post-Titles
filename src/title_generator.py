from textgenrnn import textgenrnn
import random
import pandas as pd 

file_name = '2018_01to2019_08.csv'

reddit_posts = pd.read_csv('~/Galvanize/Projects/data/Capstone2Data/{}'.format(file_name))

reddit_posts = reddit_posts[reddit_posts['link_flair_css_class'] == 'highlights']
docs = [title for title in reddit_posts['title'] if type(title) == str]


docs = random.sample(docs, 1000)

textgen = textgenrnn()
textgen.train_on_texts(docs, num_epochs = 5)
textgen.save('weights/gamethreadweights.hdf5')
textgen.generate()

# textgen = textgenrnn('weights/nuggs.hdf5')