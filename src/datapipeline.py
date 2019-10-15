import pandas as pd
import numpy as np

class pipeline(object):

    default_cols = ['created_utc', 
                    'title', 
                    'subreddit', 
                    'author', 
                    'num_comments', 
                    'score', 
                    'id', 
                    'link_flair_css_class', 
                    'author_flair_css_class']
                    
    def __init__(self):

        self.data_path = '~/Galvanize/Projects/data/Capstone2/{}'

    def load_csv(self, file_name, cols = default_cols):
        '''
        Loads data from fixed path and filters for desired columns
        Assumes .csv file in is in self.data_path (aka '~/Galvanize/Projects/data/Capstone2/{}')

        returns: Pandas DataFrame
        '''
        path = self.data_path.format(file_name)
        df = pd.read_csv(path, low_memory = False)
        df = df[cols]
        # df['type'] = df['link_flair_css_class'] 
        df.rename(columns = {'link_flair_css_class' :'type'}, inplace = True)
        return df

    def remove_type_tags_in_title(self, df):
        '''
        Remove type tags from post titles

        Returns: Pandas dataframe
        '''

        df['original_title'] = df['title'].copy()
        titles = df['title'].copy()
        titles = titles.str.replace(r'GAME THREAD: ', '')
        titles = titles.str.replace(r'\[(Game Thread)\] ', "")
        titles = titles.str.replace(r'\[(Highlights)\] ', "")
        titles = titles.str.replace(r'\[(Highlight)\] ', "")
        titles = titles.str.replace(r'\[(Post-Game Thread)\] ', "")
        titles = titles.str.replace(r'\[(Post Game Thread)\] ', "")
        titles = titles.str.replace(r'\[(POST GAME THREAD)\] ', "")
        titles = titles.str.replace(r'\[(Post-game thread)\] ', "")
        titles = titles.str.replace(r'\[(Post-game Thread)\] ', "")

        df['title'] = titles
        # print(  df[['title','original_title','type']]\
        #         [df['original_title'].str.find('Highlight') == True].sample(10))

        return df
    
    def save_csv(self, df, save_name):
        '''
        Saves data frame to consistent path
        '''
        path = self.data_path.format(save_name)
        print('Saving to: ', path)
        df.to_csv(path_or_buf = path)

    def load_postgres(self):
        '''
        placeholder incase needed for later
        '''
        pass
        
if __name__ == '__main__':

    file_name = 'posts_2019.csv'
    pipe = pipeline()
    data = pipe.load_csv(file_name)

    data = pipe.remove_type_tags_in_title(data)

    save_name = 'posts_2019_all_cleaned.csv'
    pipe.save_csv(data, save_name)

    test_data = pipe.load_csv(file_name).sample(1000)
    pipe.save_csv(test_data, 'test_set.csv')