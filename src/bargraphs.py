import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
figure(num=None, figsize=(12, 6), dpi=80, facecolor='w', edgecolor='k')
plt.style.use('ggplot')

table = pd.read_csv('tables/SummaryStatsPerType.csv')

barWidth = 0.13

bars1 = table['Avg Title Length (chars)']
bars2 = table['Avg Title Length (words)']
bars3 = table['Std Title Length (chars)']
bars4 = table['Std Title Length (words)']

r1 = np.arange(len(bars1))
r2 = [x + barWidth for x in r1]
r3 = [x + barWidth for x in r2]
r4 = [x + barWidth for x in r3]

# 
plt.bar(r1, bars1, color= 'red', alpha = 0.69, width=barWidth,  label='Avg Title Length (chars)')
plt.plot(r1, bars1, color='red',linewidth = 1, marker = 'o', mfc = 'black', linestyle = '--')
plt.bar(r2, bars2, color='orangered', alpha = 0.69, width=barWidth,  label='Avg Title Length (words)')
plt.plot(r2, bars2, color='orangered',linewidth = 1, marker = 'o', mfc = 'black', linestyle = '--')
plt.bar(r3, bars3, color= 'aqua', alpha = 0.69, width=barWidth,  label='Std. Dev. Title Length (chars)')
plt.plot(r3, bars3, color= 'aqua',linewidth = 1, marker = 'o', mfc = 'black', linestyle = '--')
plt.bar(r4, bars4, color='orange', alpha = 0.69, width=barWidth, label='Std. Dev. Title Length (words)')
plt.plot(r4, bars4, color='orange',linewidth = 1, marker = 'o', mfc = 'black', linestyle = '--')
# plt.xlabel('group', fontweight='bold')
plt.xticks( [r + barWidth for r in range(len(bars1))], table['Type'],
            rotation = 45)

plt.title('Summary Statistics by Type')
plt.legend()
plt.tight_layout()
# plt.show()
plt.savefig('images/barstats.png')

plt.clf()

#Plt post counts
plt.style.use('ggplot')
bars5 = table['Number of Posts']
r5 = [x+1 - 0.5 for x in range(len(bars5))]
figure(num=None, figsize=(12, 6), dpi=80, facecolor='w', edgecolor='k')
barWidth = 0.5
plt.bar(r5, bars5, color='purple', alpha = 0.69)
plt.xticks( [r + barWidth for r in range(len(bars5))], table['Type'],
            rotation = 45)
plt.title('Posts by Type')
plt.legend()
plt.tight_layout()
plt.savefig('images/barcounts.png')
