import pandas as pd
import numpy as np
import random
from multiprocessing import Process, current_process

class pipeline(object):

    more_columns = ['created_utc', 'title', 'subreddit', 'author', 'num_comments', 'score', 
                        'id', 'link_flair_css_class', 'author_flair_css_class']
    few_cols = ['created_utc','title','link_flair_css_class']
         
    def __init__(self):

        self.data_path = '~/Galvanize/Projects/data/Capstone2Data/{}'

    def load_csv(self, file_name, cols = few_cols):
        '''
        Loads data from fixed path and filters for desired columns. Renames link flair columns
        for less future verbosity
        Assumes .csv file in is in self.data_path (aka '~/Galvanize/Projects/data/Capstone2Data/{}')

        returns: Pandas DataFrame
        '''
        path = self.data_path.format(file_name)
        df = pd.read_csv(path, low_memory = False)
        df = df[cols]
        df.rename(columns = {'link_flair_css_class' :'type'}, inplace = True)
        
        self.df = df
        return df

    def save_csv(self, df, save_name):
        '''
        Saves data frame to consistent path
        '''
        path = self.data_path.format(save_name)+'.csv'
        print('Saved to: ', path)
        df.to_csv(path_or_buf = path)

    def sample(self, df, post_type, n = 'all'):
        '''
        Filters out for certain types of posts and sample size and saves to csv

        Returns: Pandas DataFrame
        '''
        df = df[df['type'] == post_type]

        if n == 'all':
            self.save_csv(df, save_name = str(post_type) + '_all.csv')
            return df
        else:
            df = df.sample(int(n), random_state = 1994) #seed for analysis is 1994
            self.save_csv(df, save_name = str(post_type) + '_' + str(n))
            return df

    def eliminate_outliers(self, df):
        '''
        Filters out entries with word length > mean(length)+3*sd(length)
        Some titles were > 200 words in length which is weird because reddit post titles can only be 300 characters max
        Noticed this was messing things up in analysis a lot
        '''
        sd_length = np.std((df['title'].str.split().apply(len)))
        mean_length = np.mean((df['title'].str.split().apply(len)))
        df = df[df['title'].apply(lambda x: len(x.split(' ')) <= mean_length + 3*(sd_length))]
        return df


if __name__ == '__main__':
    
    file_name = '2018_01to2019_08.csv'
    pipe = pipeline()
    data = pipe.load_csv(file_name)

    data = pipe.eliminate_outliers(data)
    # n_samp = 2500
    # types =  ['highlights', 'gamethread', 'postgamethread', 'news','discussion', 'rostermoves']
    # type_samples = []

    # for t in types:
    #     samp = pipe.sample(df = data, post_type = t, n = n_samp)
    #     type_samples.append(samp)
        
    # balanced_df = pd.concat(type_samples)
    # pipe.save_csv(balanced_df, 'balanced_types_' + str(n_samp))

    unbalanced_df = data.sample(15000)
    pipe.save_csv(unbalanced_df, 'unbalanced_types_15000')
        