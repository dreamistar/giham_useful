import pandas as pd
import numpy as np
import copy
import matplotlib.pyplot as plt

# df_print Ver. 1
# Made by Kihyuk Yoon, UNIST, Service Engineering & Knowledge Discovery

def printing(df, columns, colors, sizes, scale, figsize = (20, 10), SAVE = None, SHOW = True) : 
    
    passing = False 
    for c in columns : 
        if type(c) == str : 
            if len(df[~df[c].isna()]) == 0 : passing = True
        elif type(c) == tuple : 
            for c_ in c : 
                if len(df[~df[c_].isna()]) == 0 : passing = True
    
    if passing : pass
    else : 
        fig, ax = plt.subplots(figsize = figsize)

        ax_list = [ax]
        for i in range(1, len(columns)) : 
            ax_ = ax.twinx()
            rspine = ax_.spines['right']
            rspine.set_position(('axes', 0.95 + i * 0.05 ))
            ax_.set_frame_on(True)
            ax_.patch.set_visible(False)
            ax_list.append(ax_)

        fig.subplots_adjust(right = 0.8)

        index = list(df.index)
        
        columns_ = []
        total_line = None
        for i, c in enumerate(columns) : 
            current_ax = ax_list[i]
            if type(c) != tuple : 
                columns_.append(c)
                
                current = df[c]
                current_std = np.std(current)
                current_min = np.min(current) - current_std * scale[i]
                current_max = np.max(current) + current_std * scale[i]
                current_ax.set_ylim(current_min, current_max)
                current_line = current_ax.plot(index, current, color = colors[i], label = c, marker = 'o', markersize = sizes[i])
                
                if i == 0 : total_line = current_line
                else : total_line += current_line
                    
            elif type(c) == tuple :
                current_min = 1e+1000000
                current_max = -1e+1000000
                for c_ in c : 
                    columns_.append(c_)
                    
                    current = df[c_]
                    _std = np.std(current)
                    _min = np.min(current) - _std * scale[i]
                    _max = np.max(current) + _std * scale[i]
                    if current_min > _min : current_min = _min
                    if current_max < _max : current_max = _max
                current_ax.set_ylim(current_min, current_max)
                
                for j, c_ in enumerate(c) : 
                    current = df[c_]
                    current_line = current_ax.plot(index, current, color = colors[i][j], label = c_, marker = 'o', markersize = sizes[i][j])
                    
                    if i == 0 and j == 0 : total_line = current_line
                    else : total_line += current_line
                
        plt.grid(True)
        plt.legend(total_line, columns_)
        fig.tight_layout()

        if SAVE != None : plt.savefig(SAVE, dpi = 350)
        if SHOW == True : plt.show()
        
    plt.close('all')