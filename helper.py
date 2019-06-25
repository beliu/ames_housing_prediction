'''These functions process, transform, and visualize data for the
    Kaggle Ames House Price Prediction competition.
'''
import pandas as pd


def load_data(datafile, ix):
    '''Load the data from a datafile

       ARGUMENTS:
       datafile - the filename of the data
       ix - the name of the index column

       RETURN:
       data - the data from the file
    '''

    if datafile[-4:] == '.txt':
        data = pd.read_csv(datafile, sep='\t', header=0, index_col=ix)
    else:
        data = pd.read_csv(datafile, header=0, index_col=ix)
        
    return data


def get_num_vars(data):
    '''
        Returns the variables of a dataset that are of a numeric type
        
        ARGUMENTS:
        data - the dataframe

        RETURN:
        num_vars - a dataframe containing only numeric variables
    '''
    
    new_data = data.copy()
    num_vars = new_data.select_dtypes(exclude=['object', 'category'])
    
    return num_vars


def get_catg_vars(data, *args):
    '''
        Returns the variables of a dataset that are categorical.
        Specify any additional variables that should also be considered
        categorical.

        ARGUMENTS:
        data - the dataframe
        args - the name of any additional variables that should be 
            considered categorical
        
        RETURN:
        catg_vars - a dataframe containing only categorical variables
    '''
    
    new_data = data.copy()
    catg_vars = new_data.select_dtypes(include=['object', 'category'])
    for arg in args:
        catg_vars = pd.concat([catg_vars, new_data[arg]], axis=1)
    

    return catg_vars