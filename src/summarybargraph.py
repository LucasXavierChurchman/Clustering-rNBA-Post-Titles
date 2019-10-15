import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
figure(num=None, figsize=(12, 6), dpi=80, facecolor='w', edgecolor='k')
plt.style.use('ggplot')

table = pd.read_csv('data/SummaryStatsPerType.csv')

barWidth = 0.13
bars1 = table['Number of Posts']/100
bars2 = table['Avg Title Length (chars)']
bars3 = table['Avg Title Length (words)']
bars4 = table['Std Title Length (chars)']
bars5 = table['Std Title Length (words)']

r1 = np.arange(len(bars1))
r2 = [x + barWidth for x in r1]
r3 = [x + barWidth for x in r2]
r4 = [x + barWidth for x in r3]
r5 = [x + barWidth for x in r4]

plt.bar(r1, bars1, color='purple', alpha = 0.69, width=barWidth, edgecolor='black', linewidth = 2, label='Number of Posts (div 100)')
plt.bar(r2, bars2, color= 'red', alpha = 0.69, width=barWidth, edgecolor='black', linewidth = 2, label='Avg Title Length (chars)')
plt.bar(r3, bars3, color='orangered', alpha = 0.69, width=barWidth, edgecolor='black', linewidth = 2, label='Avg Title Length (words)')
plt.bar(r4, bars4, color= 'aqua', alpha = 0.69, width=barWidth, edgecolor='black', linewidth = 2, label='Std. Dev. Title Length (chars)')
plt.bar(r5, bars5, color='orange', alpha = 0.69, width=barWidth, edgecolor='black', linewidth = 2, label='Std. Dev. Title Length (words)')
# plt.xlabel('group', fontweight='bold')
plt.xticks( [r + barWidth for r in range(len(bars1))], table['Type'],
            rotation = 45)

plt.title('Summary Statistics by Type')
plt.legend()
plt.tight_layout()
plt.savefig('images/bar.png')
