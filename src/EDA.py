import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from datapipeline import pipeline
from matplotlib.pyplot import figure
figure(num=None, figsize=(10, 6), dpi=80, facecolor='w', edgecolor='k')
plt.style.use('ggplot')

class EDA(object):

    def __init__(self):

        file_name = 'posts_2019.csv'
        pipe = pipeline()
        self.df = pipe.load_csv(file_name)
        self.types_wanted = ['highlights', 
                            'gamethread', 
                            'postgamethread', 
                            'news',
                            'discussion',
                            'rostermoves']
    def summary_stats(self):
        df = self.df
        types = self.types_wanted

        #All posts
        d1 = {'Avg Title Length (chars)': np.mean((df['title'].apply(len))),
            'Avg Title Length (words)': np.mean((df['title'].str.split().apply(len))),
            'Std Title Length (chars)': np.std((df['title'].apply(len))),
            'Std Title Length (words)': np.std((df['title'].str.split().apply(len)))}

        all_table = pd.DataFrame(d1, index = [0]).round(2)
        all_table.to_csv('data/SummaryStatsAll.csv')

        #Posts Per-Type
        n_of_type = []
        avg_len_chars = []
        avg_len_words = []
        std_len_chars = []
        std_len_words = []

        for t in types:
            df_t = df[df['type'] == t]
            n_of_type.append(df_t.shape[0])
            avg_len_chars.append(np.mean((df_t['title'].apply(len))))
            avg_len_words.append(np.mean((df_t['title'].str.split().apply(len))))
            std_len_chars.append(np.std((df_t['title'].apply(len))))
            std_len_words.append(np.std((df_t['title'].str.split().apply(len))))

        d2 = {'Type' : types,
            'Number of Posts': n_of_type, 
            'Avg Title Length (chars)': avg_len_chars,
            'Avg Title Length (words)': avg_len_words,
            'Std Title Length (chars)': std_len_chars,
            'Std Title Length (words)': std_len_words}
        
        per_type_table = pd.DataFrame.from_dict(d2).round(2)
        per_type_table.to_csv('data/SummaryStatsPerType.csv')
        return  all_table, per_type_table

    def summary_hist(self, table):
        table = pd.read_csv('data/SummaryStatsPerType.csv')

        barWidth = 0.25
        bars1 = table['Number of Posts']/100
        bars2 = table['Avg Title Length (chars)']
        bars3 = table['Avg Title Length (words)']

        r1 = np.arange(len(bars1))
        r2 = [x + barWidth for x in r1]
        r3 = [x + barWidth for x in r2]

        plt.bar(r1, bars1, color='purple', width=barWidth, edgecolor='white', label='Number of Posts/100')
        plt.bar(r2, bars2, color= 'red', width=barWidth, edgecolor='white', label='Avg Title Length (chars)')
        plt.bar(r3, bars3, color='orange', width=barWidth, edgecolor='white', label='Avg Title Length (words)')

        # plt.xlabel('group', fontweight='bold')
        plt.xticks( [r + barWidth for r in range(len(bars1))], table['Type'],
                    rotation = 45)

        plt.title('Summary Statistics by Type')
        plt.legend()
        plt.tight_layout()
        plt.show()
        plt.savefig('images/bar.png')

if __name__ == '__main__':
    eda = EDA()
    df = eda.df
    all_types, per_type = eda.summary_stats()
    print(per_type)
