import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
import seaborn as sns
sns.set(style="ticks")

# Boxplot
seeds = range(100)
# algorithms = ["GE+PGE 10-10","GE+PGE 20-20"]
algorithms = [  "GE+PGE 20-20",
                "GE+PGE 10-10",
                "GE+PGE 5-5",
                'GE+GE 20-20',
                'GE+GE 10-10',
                'GE+GE 5-5',
                "GE+PR 5-5",
                "GE+R 5-5"
                ]

data = []
for algo in algorithms:
    W = 10
    fitness = 0
    rb = 0
    for s in seeds:
        path = f'game/results/2-{W}-10/{algo}/{s}/fitness.txt'
        with open(path,'r') as f:
            fitness += float(f.readline())
        path = f'game/results/2-{W}-10/{algo}/{s}/bt_fit_ratio.txt'
        with open(path, 'r') as t:
            rb += float(t.readline())
    fitness /= len(seeds)
    rb /= len(seeds)
    data.append([algo.replace('+','-'),
               fitness,
               rb])

plt.rc('font',family='Arial')

df = pd.DataFrame(data,columns=['Algorithm','Fitness','rb'])
print(df)
# for a in algorithms:
#     name = a.replace('+','-')
#     rb = df.Fitness[df.Algorithm == name].mean()
#     df.Algorithm[df.Algorithm == name] = f'{name} {rb:.3f}'

# df.boxplot()
# plt.grid(linestyle="--", alpha=0.3)
# plt.ylabel('Fitness')
# plt.show()
# fig = plt.figure()
# ax = fig.add_subplot(111)
#
# sns.lineplot(x="rb", y="Fitness", data=df, palette="Pastel1")
#
# for s in ax.spines.values():
#     s.set_linewidth('1.0')
#
# plt.xticks( fontsize=12)
# plt.yticks(fontsize=12)
# plt.xlabel('')
# plt.ylabel('Fitness',fontsize=12)
# plt.legend(loc=(0.73,0.07),frameon=True,fontsize='medium')
# plt.tight_layout()
# # sns.despine(top=True,right=True,left=True,bottom=True)
#
# plt.savefig('/home/cxl/Desktop/share/boxes_results.png', bbox_inches='tight')
# plt.show()