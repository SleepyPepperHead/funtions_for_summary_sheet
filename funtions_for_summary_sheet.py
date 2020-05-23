"""
Created on Fri May  8 15:26:51 2020

@author: yuwan

functions for a summary sheet with paths to the files with data.
change all the path below to what you need.
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def divide_save(path, col, prefix=None, subtype=None, refer=None, header=0):
    """divide data by the col and save the divided. Add the divided to the summary sheet"""
    data = pd.read_excel(path, header=header)
    names = set(data[col])
    save_path = 'a path to save'
    for name in names:
        new_df = data[data[col] == name].reset_index(drop=True)
        if prefix:
            name = f'{prefix}_{name}'
        new_df.to_excel(f'{save_path}/{name}.xlsx')
        add_new(name, subtype, refer)
        print(name, ' saved')


def add_new(name: str, subtype=None, refer=None,  method=None):
    summary = pd.read_excel(r'this is the path to your summary sheet file/autosaved.xlsx', index_col=0)
    new_line = {'name': name, 'subtype': subtype,
                'refer': refer, 'method': method,
                'path': f'path_to\\{name}.xlsx'}
    summary = summary.append(new_line, ignore_index=True)
    pd.set_option('display.max_columns', 8)
    print(summary.tail(2))
    if input('do you want to save? y/n').lower() == 'y':
        summary.to_excel('auto-saved.xlsx')
        """
        Add a path the same as above.
        And you can check the new row added and choose whether to save.
        Then you chan choose whether to clean the str-type cells as described 
        in the function: limit_to nan()
        These input statements also add some fun operating
        """
        if input('clean the limit_str? y/n') == 'y':
            limit_to_nan(new_line['path'], index_col=0)
    else:
        print('canceled')


def limit_to_nan(path: str, elements=None, index_col: int = 0) -> None:
    """
    some data below the detective limit are marked by a str type.
    these str type cell prevent us to plot properly.
    this function is to change the str-type cells to NaN.
    put the elements or columns in a List to the argument 'element',
    default is Ti, Al as below. Change them to what you need.
    """
    if elements is None:
        elements = ['Ti', 'Al']
    df = pd.read_excel(path, index_col=index_col)
    for element in elements:
        if element in df.columns:
            for i, cell in enumerate(df[element]):
                if type(cell) == str:
                    df[element].iat[i] = np.nan
        else:
            print(f'{path} has no {element} col')
    df = df.dropna(how='all')
    df.reset_index(drop=True)
    df.to_excel(path)
    print('Done ', path)



def scatter_log(ax, x, y, size, color, marker, label):
    """
    built the fig and ax in advance.
    use this function in a loop.
    this function is to give the plot different groups and labels.
    my example is showed below.
    """
    ax.scatter(x, y, alpha=0.6, s=size, c=color,
               marker=marker, label=label)
    ax.set_xlim(1e-2, 1e3)
    ax.set_ylim(1e0, 1e4)
    ax.set_xlabel('Ti')
    ax.set_ylabel('Al')
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    '''
    Or if you want the legend on the top instead of left, 
    uncomment the following lines and comment the line above
    '''
    # ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
    # ncol=3, mode="expand", borderaxespad=0.)

'''
Example plotting Al verse Ti:
summary = pd.read_excel()

fig, (ax1,ax2) = plt.subplots(2,1,figsize=(9,12))
types = [
    'epithermal', 'porphyry', 'orogenic', 'pegmatite',  
      'granite', 'skarn','IRG','IRG/ORG',
    'Igneous', 'Hydrothermal', 'greisen-type', 
    'carlin', 'pre-ore Qtz', 'post-ore Qtz'
    ]
colors=[
        'deeppink','lime','royalblue','tan',
       'turquoise','darkorange',
        'dimgrey','limegreen','mediumblue','red','gold',
        'darkviolet','k' ,'navy' ,'darkgreen', 'lightsteelblue', 
        'pink', 'greenyellow','darkkhaki','dodgerblue'
        ]
markers = ['o']*7 + ['x']*7
sizes = [20] * 7 + [40] *7
for type, color, marker, size in zip(types,colors,markers,sizes):
    df = summary[summary['type']==type]
    temTi, temAl = [], []
    for path in df.path:
        temdf = pd.read_excel(path)
        temTi.extend(temdf['Ti'])
        temAl.extend(temdf['Al'])
    scatter_log(ax1,temTi,temAl,size,color,marker,label=type)
'''
