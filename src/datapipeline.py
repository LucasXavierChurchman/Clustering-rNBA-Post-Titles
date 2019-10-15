import pandas as pd
import numpy as np
import random

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

if __name__ == '__main__':

    file_name = 'posts_2019.csv'
    pipe = pipeline()
    data = pipe.load_csv(file_name)
    n_samp = 1000
    types =  ['highlights', 'gamethread', 'postgamethread', 'news','discussion', 'rostermoves']
    type_samples = []

    for t in types:
        samp = pipe.sample(df = data, post_type = t, n = n_samp)
        type_samples.append(samp)
        
    balanced_df = pd.concat(type_samples)
    pipe.save_csv(balanced_df, 'balanced_types_' + str(n_samp))
        
    # save_name = 'posts_2019_all.csv'
    # pipe.save_csv(data, save_name)

    # def remove_type_tags_in_title(self, df):
    #     '''
    #     Remove type tags from post titles

    #     Returns: Pandas dataframe
    #     '''

    #     df['original_title'] = df['title'].copy()
    #     titles = df['title'].copy()
    #     titles = titles.str.replace(r'GAME THREAD: ', '')
    #     titles = titles.str.replace(r'\[(Game Thread)\] ', "")
    #     titles = titles.str.replace(r'\[(Highlights)\] ', "")
    #     titles = titles.str.replace(r'\[(Highlight)\] ', "")
    #     titles = titles.str.replace(r'\[(Post-Game Thread)\] ', "")
    #     titles = titles.str.replace(r'\[(Post Game Thread)\] ', "")
    #     titles = titles.str.replace(r'\[(POST GAME THREAD)\] ', "")
    #     titles = titles.str.replace(r'\[(Post-game thread)\] ', "")
    #     titles = titles.str.replace(r'\[(Post-game Thread)\] ', "")

    #     df['title'] = titles
    #     # print(  df[['title','original_title','type']]\
    #     #         [df['original_title'].str.find('Highlight') == True].sample(10))

    #     return df
    


        