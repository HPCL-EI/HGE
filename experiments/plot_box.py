
import numpy as np
import matplotlib.pyplot as plt
# from matplotlib import font_manager
# import matplotlib
# matplotlib.font_manager._rebuild()
#
# for font in font_manager.fontManager.ttflist:
#     # 查看字体名以及对应的字体文件名
#     print(font.name, '-', font.fname)

import pandas as pd
import seaborn as sns
sns.set(style="ticks")

# Boxplot
seeds = range(100)
algorithms = ["R+R","R+GE",'R+PR','R+PGE',"GE+R","GE+GE",'GE+PR',"GE+PGE"]
# algorithms = ["R+GE","GE+R"]

data = []
for algo in algorithms:
    for s in seeds:
        path = f'game/results/2-10-10/{algo} 5-5/{s}/fitness.txt'
        with open(path,'r') as f:
            data.append([algo.replace('P','').replace('GE+GE','HGE').replace('+','-'),
                               'BT Expansion' if 'P' in algo else 'General',
                               np.clip( float(f.readline()),a_min=0,a_max=1)])

plt.rc('font',family='Arial')

df = pd.DataFrame(data,columns=['Algorithm','Planning','Fitness'])
# df.Algorithm[df.Algorithm=='GE-GE'] = 'HGE'

# df.boxplot()
# plt.grid(linestyle="--", alpha=0.3)
# plt.ylabel('Fitness')
# plt.show()
fig = plt.figure()
ax = fig.add_subplot(111)

sns.boxplot(x="Algorithm", y="Fitness", hue="Planning", data=df, palette="Pastel1",
            width=0.6,linewidth=1.2,saturation=1,showmeans=True)

# ax.spines['bottom'].set_visible(True)
# ax.spines['bottom'].set_linestyle("--")
# ax.spines['bottom'].set_linewidth('0.4')
# ax.spines['bottom'].set_color('black')

# ax.spines['bottom'].set_linewidth('0.4')


for s in ax.spines.values():
    s.set_linewidth('1.0')

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel('')
plt.ylabel('Fitness',fontsize=12)
plt.legend(loc=(0.66,0.04),frameon=True,fontsize='medium')
plt.tight_layout()
# sns.despine(top=True,right=True,left=True,bottom=True)

plt.savefig('/home/cxl/Desktop/share/boxes_results.png', bbox_inches='tight')
plt.show()