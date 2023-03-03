import numpy as np


n = 100
seeds = range(n)
algorithms = ["GE+GE","GE+PGE"]
def compare(info,best,i,j):
    if info[i] > info[j]:
        best[i] = True
    else:
        best[j] = True

with open('sh/plot_settings.txt','r') as f:
    with open('/home/cxl/Desktop/share/table.txt','w') as f_out:
        for i,line in enumerate( f.readlines() ):
            info = np.zeros(7)
            M,C,W = map(int,line.split(' '))
            for s in seeds:
                path = f'game/results/{M}-{C}-{W}/{algorithms[0]} 5-5/{s}/fitness.txt'
                with open(path,'r') as t:
                    info[0] += float(t.readline())
                path = f'game/results/{M}-{C}-{W}/{algorithms[0]} 5-5/{s}/time.txt'
                with open(path, 'r') as t:
                    info[2] += float(t.readline())
                path = f'game/results/{M}-{C}-{W}/{algorithms[0]} 5-5/{s}/bt_fit_ratio.txt'
                with open(path, 'r') as t:
                    info[1] += float(t.readline())
                if M <= 100:
                    path = f'game/results/{M}-{C}-{W}/{algorithms[1]} 5-5/{s}/fitness.txt'
                    with open(path, 'r') as t:
                        info[3] += float(t.readline())
                    path = f'game/results/{M}-{C}-{W}/{algorithms[1]} 5-5/{s}/time.txt'
                    with open(path, 'r') as t:
                        times = np.array(list(map(float, t.readlines()[:3])))
                        info[5] += times[0]
                        info[6] += times[1] + times[2]
                    path = f'game/results/{M}-{C}-{W}/{algorithms[1]} 5-5/{s}/bt_fit_ratio.txt'
                    with open(path, 'r') as t:
                        info[4] += float(t.readline())

            print(info)

            info /= n
            best = [False for _ in range(7)]
            if info[0] > info[3]:
                best[0] = True
            else:
                best[3] = True
                
            if info[1] > info[4]:
                best[1] = True
            else:
                best[4] = True
            
            info_str = ['' for _ in range(7)]
            info_str[0] = f'{info[0]:.3f}'
            info_str[2] = f'{info[2]:.3f}'
            info_str[1] = f'{100 * info[1]:.1f}\\%'
            if M <= 100:
                info_str[3] = f'{info[3]:.3f}'
                info_str[5] = f'{info[5]:.3f}'
                info_str[4] = f'{100 * info[4]:.1f}\\%'
                info_str[6] = f'{100 * info[6] / info[5]:.1f}\\%'
                if info[2] > info[5]:
                    best[5] = True
                else:
                    best[2] = True
            else:
                info_str[3:7] = ['-' for _ in range(4)]
                best[2] = True
            for index in range(len(info_str)):
                if best[index]:
                    info_str[index] = f'\\textbf{{{info_str[index]}}}'
            f_out.write(f'{i} & {M} & {C} & {W} & {" & ".join(info_str)} \\\\\n')
