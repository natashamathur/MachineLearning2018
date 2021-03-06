import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

'''
Read in data
'''

def read_data(file, source_type = 'csv'):
    '''
    Reads data from an external source into a pandas data frame.
    
    Inputs:
        file (str): file path and file name
        source_type (str): csv (default), json, excel
    
    Output
        all_data (pandas dataframe): pandas data frame with data
    '''
    if source_type == 'csv':
        all_data = pd.read_csv(file)
    elif source_type == 'json':
        all_data = pd.read_json(file)
    elif source_type == 'excel':
        all_data = pd.read_excel(file)
    
    return all_data
    
'''
Pre Process Data
'''

#updated
def remove_outliers(df, col):
    '''
    Return data frame with outliers removed in selected column

    Inputs:
        df: pandas dataframe of interest
        col: column to remove outliers from

    Output:
        df: pandas dataframe with outliers removed in that column 
    '''
    df = df[((df[col] - df[col].mean()) / df[col].std()).abs() < 3]
    return df

#updated
def specify_range(df, col, min, max):
    ''' 
    Narrow down a data frame based on a range for a given column
    
    Inputs:
        df (data frame): dataframe to narrow down
        col (data frame column name, str): column to find range in
        min, max: minimum and maximum values for range. Can be str or int depending on column type 
    '''
    output_df = df.loc[(df[col] >= min) & (df[col] <= max)]
    return output_df

# updated   
def replace_na(df, var, method='mean'):
    '''
    Replaces all the NA's in a given column with chosen statistical value.
    
    Input:
        df (pandas dataframe): original dataframe
        var (string): column containing NA values
        method (string): the statistical measure to use to find
            replacement values, default set to 'mean'
    '''
    
    val = getattr(df[var], method)()
    df[var].fillna(val, inplace=True)

#updated
def fill_missing(df):
    '''
    Takes a dataframe and replaces all NA's in all columns with the mean.
    
    Input:
        df (pandas dataframe): original dataframe
    '''
    
    na_cols = list(df.loc[:, df.isna().any()].columns)
    for col in na_cols:
        replace_na(df, col) 
        
    return df
    
def na_cols(df):
    '''
    Produces a list of columns in the data frame that have N/A values.
    
    Input:
        df (data frame): data frame of interest
        
    Output:
        list of columns that contain N/A's
    '''
    
    return list(df.loc[:, df.isna().any()].columns)
    
'''
Explore and Chart Data
'''

# updated
def find_top(df, col_of_interest, sort_by='projectid', ascending=False):
    '''
    Find the most common (or least) values in a given column
    
    Inputs:
        df (pandas dataframe): dataframe of interest
        col (str): name of column of interest
        sort_by (pandas series): column to sort dataframe by
        ascending: default to False, will show highest values 
        
    Output:
        output (pandas dataframe): Sorted pandas dataframe
    '''
    grouped = df.groupby(col_of_interest, sort=False).count()
    
    return grouped.sort_values(by=sort_by, ascending=False)

def plot_line_graph(df, var, title, xlabel, ylabel):
    '''
    Plots a line graph based on columns in a pandas data frame
    
    Inputs:
        df (pandas data frame): data frame containing values to be graphed
        var (str): column name of dependent variable
        title (str): title for line graph
        xlabel (str): label for x-axis
        ylabel (str): label for y-axis
    '''
    
    x = list(df.index.values)
    y = list(df[var].values)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(x,y)
    plt.show()
    
# updated
def plot_all_line_graphs(df, x_label='', y_label='', x_vals='df.index.values'):
    '''
    Plots all the line graphs for all the dependent variables off a given independent variable
        
        df (pandas data frame): data frame containing values to be graphed
        xlabel (str): label for x-axis, default to empty label
        ylabel (str): label for y-axis, default to empty label
        x_vals (data frame column): column to be used for x values, default to index
    
    '''
    for col in df.columns:
        plot_line_graph(df, col, ylabel=col)

#updated
def plot_bar_chart(xvals, yvals, xlabel, ylabel, title, width = 0.35, color = 'purple'):
    '''
    Takes in values and labels and plots a bar chart/
    
    Inputs:
        N (int): number of bars
        xvals (tuple): x value categories
        yvals (tuple): y values
        xlabel, ylabel, title (string): labels for x-axis, y-axis, and title
        width (float): width of each bar, defaults to 0.35
        color (string): color of bars, defaults to purple
            color choices: https://matplotlib.org/api/colors_api.html
    '''
    counts = yvals

    ind = np.arange(len(xvals))  # the x locations for the groups
    width = 0.35       # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, counts, width, color=color)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(xvals)
    
    plt.gcf().subplots_adjust(bottom=0.2) # make room for x-axis labels

    plt.show()

# updated
def plot_correlation_heatmap(df):
    '''
    Creates a correlation heat map of a data frame
    
    Input:
        df (pandas dataframe): data frame to be plotted 
    '''
    
    corr = df.corr()
    sns.heatmap(corr, xticklabels=corr.columns.values, yticklabels=corr.columns.values)
    plt.show()

# updated
def plot_pie_chart(vals, labels, colors = ["red", "blue", "green", "violet", "orange"]):
    '''
    Takes in values and labels and plots a pie chart
    
    Inputs:
        vals (list of ints): values to be charted
        labels (list of strings): labels for each section
        colors (list of strings): Colors for each section of graph. Must be the same length as the number of vals.
            color choices: https://matplotlib.org/api/colors_api.html
    '''
    
    if len(colors) < len(vals):
        print("Please insert more colors")
    
    plt.pie(
    vals,
    labels=labels,
    # with no shadows
    shadow=False,
    # with colors
    colors=colors,
    # with one slide exploded out
    #explode=(0, 0, 0, 0, 0.15),
    # with the start angle at 90%
    startangle=90,
    # with the percent listed as a fraction
    autopct='%1.1f%%',
    )

    plt.axis('equal')

    # View the plot
    plt.tight_layout()
    plt.show()
    
# updated
def bar_top(df, col_of_interest, xlabel, ylabel, title, selected_col='projectid', max = 5, width =0.35, color='blue'):
    '''
    Creates a bar chart of the top categories in a given column
    
    Inputs:
        df (pandas dataframe): dataframe of interest
        col_of_interest (str): name of column of interest
        sort_by (pandas series): column to sort dataframe by
        xlabel, ylabel, title (string): labels for x-axis, y-axis, and title
        width (float): width of each bar, defaults to 0.35
        color (string): color of bars, defaults to purple
            color choices: https://matplotlib.org/api/colors_api.html
    '''
    
    top = find_top(df, col_of_interest)
    top = top[selected_col].head(max)
        
    plot_bar_chart(tuple(top.index), tuple(top), xlabel, ylabel, title, width, color)

# updated
def pie_top(df, col_of_interest, selected_col='projectid', labels = '', colors = ["red", "blue", "green", "violet", "orange"]):
    '''
    Creates a pie chart of the top categories in a given column
    
    Inputs:
        df (pandas dataframe): dataframe of interest
        col_of_interest (str): name of column of interest
        selected_col (str): name of column to display
        labels (list of strings): labels for each section
        colors (list of strings): Colors for each section of graph. Must be the same length as the number of vals.
            color choices: https://matplotlib.org/api/colors_api.html
    '''
    
    
    top = find_top(df, col_of_interest)
    top = top[selected_col]
    if labels == '':
        labels = tuple(top.index)
        
    plot_pie_chart(tuple(top), labels, colors)
    
