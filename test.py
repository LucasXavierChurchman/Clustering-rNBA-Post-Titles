from textgenrnn import textgenrnn
import random
import pandas as pd 

nugg_comments = pd.read_csv('data/Nuggets.csv')

nugg_comments.body.shape

texts = [comment for comment in nugg_comments.body if type(comment) == str]

texts = random.sample(texts, 100)

textgen = textgenrnn()
textgen.train_on_texts(random.sample(texts,100), num_epochs = 1)
textgen.save('weights/nuggs.hdf5')
textgen.generate()

# textgen = textgenrnn('weights/nuggs.hdf5')