import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from DataPipeline import pipeline
from matplotlib.pyplot import figure
figure(num=None, figsize=(10, 6), dpi=80, facecolor='w', edgecolor='k')
plt.style.use('seaborn')

class EDA(object):

    def __init__(self):

        self.types_wanted = ['highlights', 
                            'gamethread', 
                            'postgamethread', 
                            'news',
                            'discussion',
                            'rostermoves']

    def summary_stats(self):
        file_name = '~/Galvanize/Projects/data/Capstone2Data/balanced_types_2500.csv'
        df = pd.read_csv(file_name)
        types = self.types_wanted
        
        #All posts
        d1 = {'Avg Title Length (chars)': np.mean((df['title'].apply(len))),
            'Avg Title Length (words)': np.mean((df['title'].str.split().apply(len))),
            'Max Title Length (words)': np.max((df['title'].str.split().apply(len))),
            'Min Title Length (words)': np.min((df['title'].str.split().apply(len))),
            'Std Title Length (chars)': np.std((df['title'].apply(len))),
            'Std Title Length (words)': np.std((df['title'].str.split().apply(len)))}

        all_table = pd.DataFrame(d1, index = [0]).round(2)
        all_table.to_csv('tables/SummaryStatsAll.csv')

        #Posts Per-Type
        n_of_type = []
        avg_len_chars = []
        avg_len_words = []
        max_len_words = []
        min_len_words = []
        std_len_chars = []
        std_len_words = []

        for t in types:
            df_t = df[df['type'] == t]

            n_of_type.append(df_t.shape[0])
            avg_len_chars.append(np.mean((df_t['title'].apply(len))))
            avg_len_words.append(np.mean((df_t['title'].str.split().apply(len))))
            max_len_words.append(np.max((df_t['title'].str.split().apply(len))))
            min_len_words.append(np.min((df_t['title'].str.split().apply(len))))
            std_len_chars.append(np.std((df_t['title'].apply(len))))
            std_len_words.append(np.std((df_t['title'].str.split().apply(len))))

        d2 = {'Type' : types,
            'Number of Posts': n_of_type, 
            'Avg Title Length (chars)': avg_len_chars,
            'Avg Title Length (words)': avg_len_words,
            'Max Title Length (words)': max_len_words,
            'Min Title Length (words)': min_len_words,
            'Std Title Length (chars)': std_len_chars,
            'Std Title Length (words)': std_len_words}
        # print(pd.DataFrame(d2))
        
        per_type_table = pd.DataFrame.from_dict(d2).round(2)
        per_type_table.to_csv('tables/SummaryStatsPerType.csv')
        return  all_table, per_type_table

    def summary_hist(self, table):
        barWidth = 0.13

        bars1 = table['Avg Title Length (words)']
        bars2 = table['Max Title Length (words)']
        bars3 = table['Min Title Length (words)']
        bars4 = table['Std Title Length (words)']

        r1 = np.arange(len(bars1))
        r2 = [x + barWidth for x in r1]
        r3 = [x + barWidth for x in r2]
        r4 = [x + barWidth for x in r3]

        plt.bar(r1, bars1, color= 'red', alpha = 0.69, width=barWidth,  label='Avg Title Length (words)')
        plt.plot(r1, bars1, color='red',linewidth = 1, marker = 'o', mfc = 'black', linestyle = '--')
        plt.bar(r2, bars2, color='orangered', alpha = 0.69, width=barWidth,  label='Max Title Length (words)')
        plt.plot(r2, bars2, color='orangered',linewidth = 1, marker = 'o', mfc = 'black', linestyle = '--')
        plt.bar(r3, bars3, color= 'aqua', alpha = 0.69, width=barWidth,  label='Min Title Length (words)')
        plt.plot(r3, bars3, color= 'aqua',linewidth = 1, marker = 'o', mfc = 'black', linestyle = '--')
        plt.bar(r4, bars4, color='orange', alpha = 0.69, width=barWidth, label='Std Title Length (words)')
        plt.plot(r4, bars4, color='orange',linewidth = 1, marker = 'o', mfc = 'black', linestyle = '--')
        # plt.xlabel('group', fontweight='bold')
        plt.xticks( [r + barWidth for r in range(len(bars1))], table['Type'],
                    rotation = 45)

        plt.title('Summary Statistics of Titles by Type', loc = 'left')
        plt.legend(loc='lower left', bbox_to_anchor= (.5, 1), ncol=2, 
            borderaxespad=0, frameon=False)
        plt.tight_layout()
        # plt.show()
        plt.savefig('plots/BarStats.png')

        plt.clf()

        #Plt post counts
        bars5 = table['Number of Posts']
        r5 = [x+1 - 0.5 for x in range(len(bars5))]
        figure(num=None, figsize=(12, 6), dpi=80, facecolor='w', edgecolor='k')
        barWidth = 0.5
        plt.bar(r5, bars5, color='purple', alpha = 0.69)
        plt.xticks( [r + barWidth for r in range(len(bars5))], table['Type'],
                    rotation = 45)
        plt.title('Posts by Type')
        
        plt.tight_layout()
        plt.savefig('plots/barcounts.png')

if __name__ == '__main__':
    table = pd.read_csv('tables/SummaryStatsPerType.csv')
    eda = EDA()
    all_types, per_type = eda.summary_stats()
    eda.summary_hist(table = per_type)
    
