# from configparser import ConfigParser

# config_parser = ConfigParser()

    #Trying a Kbins discretizer
# from sklearn.preprocessing import KBinsDiscretizer

# dis = KBinsDiscretizer(n_bins = 5, encode = 'onehot', strategy = 'uniform')

# x_all_disc = dis.fit_transform(x_all)

#print(x_all_binned)
from sklearn.preprocessing import OneHotEncoder
onehot_encoder = OneHotEncoder(sparse=False)

from sklearn.feature_selection import f_classif, SelectKBest 


def PCA(X,num_components):
    from sklearn.decomposition import PCA
    pca = PCA(n_components=num_components, svd_solver='full')
    return pca.fit_transform(X)  
    
def selectKBest(num_features):
    
    return SelectKBest(k = num_features)

def quantile_bin(df,bin_cols,bins):
    """Quality Binning using Pandas for all the columns in the bin_cols list
    bins = [0, .25, .5, .75, 1.]"""

    for key in df:
        if key in bin_cols:
            bins = df[key].quantile(bins)
            df[key]= pd.cut(df[key],bins.values, labels = labels, include_lowest = True)
            
    return df    

def normalize(df,norm_cols):
    """Min Max normalization given dataframe and list of columns to normalize"""
    for key in df:
        if key in norm_cols:
            mn = df[key].min()
            mx = df[key].max()
            diff = mx - mn
            
            df[key] = df[key].apply(lambda x : (x-mn)/diff)
    return df
        
def stdize(df,std_cols):
    """Standardize given dataframe and list of columns to normalize"""

    for key in df:
        if key in std_cols:
            mean = df[key].mean()
            std = df[key].std()
            df[key ] = df[key].apply(lambda x : (x-mean)/std)
    return df

def onehot(y):
    """Return one-hot encoded data from series"""
    import numpy as np
    y_arr = np.array(y)
    return onehot_encoder.fit_transform(y_arr.reshape(-1,1))

def inv_onehot(y_onehot):
    """Return one-hot encoded data from series"""
    import numpy as np
    return onehot_encoder.inverse_transform(y_onehot)