#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' 

    Example Structure for a Feature Processing Class  
    
'''


from __future__ import absolute_import, division, print_function
import os
import numpy as np
import pandas as pd
from sklearn.utils import shuffle

class Feature_Process:
    """
    The goal of this class is to extract and process useful features.
    """
    
    def __init__(self, DF1, DF2, DF3, DF4, model_path=None,
                 update_statistics=False):
        """ Input should be in the form of pandas dataframe """
        self.DF1, self.DF2, self.DF3, self.DF4 = DF1, DF2, DF3, DF4

    @classmethod
    def from_CSV(cls, CSV1, CSV2, CSV3, CSV4, model_path=None,
                 update_statistics=False):
        """ Alternative constructor from str paths to CSVs """
        if (not os.path.exists(CSV1) or not os.path.exists(CSV2) or
            not os.path.exists(CSV3) or not os.path.exists(CSV4)):
            print('file path does not exist!')
            return
        DF1 = pd.read_csv(CSV1)
        DF2 = pd.read_csv(CSV2)
        DF3 = pd.read_csv(CSV3)
        DF4 = pd.read_csv(CSV4)
        return cls(DF1, DF2, DF3, DF4, model_path=None,
                 update_statistics=False)
    
    
    
    """
    
    .
    .
    .
    
    Add other methods here to address specific needs of your data
    (e.g. balancing, feature selection and feature transormation methods)
    
    .
    .
    .
    
    """
    
    
    
    
    @staticmethod
    def df_shuffle(df):
        return shuffle(df)
    
    @staticmethod
    def norm_data(X_in, model_path=None, update_statistics=False):
        """
        Inputs:
            X_in: data (numpy array) to only rescale according to mean
            and variance in <model_path>.json if exists otherwise will
            normalize to X_in matrix
            model_path: path to mean and variance .json files
            update_statistics: are you normalizing this data to train? if so,
            the algorithm will update the mean and variance .jason files
        This function will normalize the data with: zero mean and unit variance
        """
        if update_statistics is True:
            if model_path is None:
                print("did not insert path to normalization json files;"
                      "creating new files in CWD..")
                model_path = os.getcwd()
                data_count = X_in.shape[0]
                data_mean = X_in.mean(axis=0)
                data_std = X_in.std(axis=0, ddof=1)
            else:
                try:
                    old_count = (pd.read_json(
                        path_or_buf=(model_path + '/data_count.json'),
                        orient='columns', typ='series')).as_matrix()
                    old_mean = (pd.read_json(
                        path_or_buf=(model_path + '/data_mean.json'),
                        orient='columns', typ='series')).as_matrix()
                    old_std = (pd.read_json(
                        path_or_buf=(model_path + '/data_std.json'),
                        orient='columns', typ='series')).as_matrix()
                    for i in range(X_in.shape[0]):
                        data_count = old_count + 1
                        data_mean = (old_mean * old_count +
                                     X_in[i, :]) / data_count
                        s2n_1 = np.square(old_std)
                        n_2 = data_count - 2
                        n_1 = data_count - 1
                        n = data_count
                        xn_meanxn_1 = X_in[i, :] - old_mean
                        s2n = ((n_2 / n_1) * s2n_1) + \
                            ((1 / n) * np.square(xn_meanxn_1))
                        data_std = np.sqrt(s2n)
                        old_count = data_count
                        old_mean = data_mean
                        old_std = data_std
                except ValueError:
                    print("did not find the proper normalization json files;"
                          "creating new files..")
                    data_count = X_in.shape[0]
                    data_mean = X_in.mean(axis=0)
                    data_std = X_in.std(axis=0, ddof=1)
            X_norm = (X_in - data_mean) / data_std
            (pd.Series(data_count)).to_json(path_or_buf=(
                model_path + '/data_count.json'), orient='columns')
            (pd.Series(data_mean)).to_json(path_or_buf=(
                model_path + '/data_mean.json'), orient='columns')
            (pd.Series(data_std)).to_json(path_or_buf=(
                model_path + '/data_std.json'), orient='columns')
        else:
            old_mean = (pd.read_json(
                path_or_buf=(model_path + '/data_mean.json'),
                orient='columns', typ='series')).as_matrix()
            old_std = (pd.read_json(
                path_or_buf=(model_path + '/data_std.json'),
                orient='columns', typ='series')).as_matrix()
            X_norm = (X_in - old_mean) / old_std
        return X_norm
    
    @staticmethod
    def df_saveCSV(df, CSVname, path='empty'):
        if path != 'empty':
            fullPath = path + '/' + CSVname + '.csv'
        else:
            fullPath = CSVname + '.csv'
        df.to_csv(fullPath)
        
        
def main():
    return


if __name__ == "__main__":
    main()        
        
        
        