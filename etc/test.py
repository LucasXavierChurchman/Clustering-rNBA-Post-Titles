from textgenrnn import textgenrnn
import random
import pandas as pd 

file_name = 'posts_2019_all.csv'

reddit_posts = pd.read_csv('~/Galvanize/Projects/data/Capstone2/{}'.format(file_name))

docs = [title for title in reddit_posts['title'] if type(title) == str]

docs = random.sample(docs, 1000)

textgen = textgenrnn()
textgen.train_on_texts(docs, num_epochs = 5)
textgen.save('weights/post_titles.hdf5')
# textgen.generate()

# textgen = textgenrnn('weights/nuggs.hdf5')