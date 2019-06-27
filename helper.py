import pandas as pd


def load_data(datafile, ix):
    '''Load the data from a datafile

       ARGUMENTS:
       datafile - the filename of the data
       ix - the name of the index column

       RETURNS:
       data - the data from the file
    '''

    if datafile[-4:] == '.txt':
        data = pd.read_csv(datafile, sep='\t', header=0, index_col=ix)
    else:
        data = pd.read_csv(datafile, header=0, index_col=ix)
        
    return data


def get_quant_vars(data, *args):
    '''
        Returns the variables of a dataset that are of quantitative
        
        ARGUMENTS:
        data - the dataframe
        args - specify additional variables that should not be
            considered quantitative

        RETURNS:
        num_vars - a dataframe containing only quantitative variables
    '''
    
    
    new_data = data.copy()
    quant_vars = new_data.select_dtypes(exclude=['object', 'category'])
    for arg in args:
        quant_vars = quant_vars.drop(arg, axis=1)

    return quant_vars


def get_catg_vars(data, *args):
    '''
        Returns the variables of a dataset that are categorical.
        Specify any additional variables that should also be considered
        categorical.

        ARGUMENTS:
        data - the dataframe
        args - the name of any additional variables that should be 
            considered categorical
        
        RETURNS:
        catg_vars - a dataframe containing only categorical variables
    '''
    
    new_data = data.copy()
    catg_vars = new_data.select_dtypes(include=['object', 'category'])
    for arg in args:
        catg_vars = pd.concat([catg_vars, new_data[arg]], axis=1)
    
    return catg_vars


def conv_to_catg_type(data, catg_vars):
    '''
        Convert the categorical values to data type category

        ARGUMENTS:
        data - the dataframe
        catg_vars - list of the names of the categorical variables

        RETURNS:
        data - modified dataframe where the categorical variables have
            been converted to data type 'category'
    '''

    data[catg_vars] = data[catg_vars].apply(lambda x: x.astype('category'))
    
    return data


def get_null_vars(data):
    '''
        Returns the column names in a dataframe of the columns 
        with null values. The output is separated by categorical 
        and quantitative variables.

        ARGUMENTS:
        data - the input dataframe

        RETURNS:
        A tuple of the names of variables with null values, separated
        by categorical and quantitative variables
    '''
    
    catg_null_vars = []
    quant_null_vars = []
    vars_w_na_data = data.columns[data.isnull().any()].tolist()

    for var in vars_w_na_data:
        if ((data[var].dtype.name == 'category') 
            or (data[var].dtype.name == 'object')):
            catg_null_vars += [var]
        else:
            quant_null_vars += [var]
    
    return catg_null_vars, quant_null_vars


def get_null_ix(data, col_names):
    '''
        Given a list of column names, return the indices of the rows 
        where the null values of those columns are located.

        ARGUMENTS:
        data - the input dataframe
        col_names - a list of the column names for which we want to find
            the indicies of null values

        RETURNS:
        ix_dict - a dictionary whose keys are column names 
            and whose values are a list of the indices of that column's
            null values
    '''
    
    ix_dict = {col: data[data[col].isnull()].index for col in col_names}
    
    return ix_dict