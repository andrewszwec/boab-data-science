# -*- coding: utf-8 -*-
# from . import helpers
import helpers

"""
load_data
check file extension if csv or xlsx or dat

fix column names (remove capitals, spaces, dots, symbols)

Fix data types to_numeric to_datetime

for each column check number of missing 
if more than 20% missing then remove
if missing records < 20% try impute
impute - KNN, random for labels or mean impute

Binning of contiuous vars

For categoricals make dummy variables

Always drop dummy [-1] for each group of variables

scale and normalise numeric variables

Balance data using smote

train test split

lassoCV, RidgeCV, Neural Net

Perf report

Save models


"""
import os
import pandas as pd 
import re


import os
import pandas as pd 
import re


class Boab(object):
    """
    Class Desc
    """
    def __init__(self, *args, **kwargs):
        self.df = pd.DataFrame([])
        self.time_cols = []
        self.date_cols = []
        return super().__init__(*args, **kwargs)
    
    def __str__(self):
        return str(self.df.head())
        
    def __repr__(self):
        return str(self.df.head())

    def head(self):
        print(self.df.head())
        
    def fix_col_names(self):
        """
        fix column names (remove capitals, spaces, dots, symbols)
        """
        col_names = [] 
        for n in self.df.columns:
            coln = n.lower()
            coln = re.sub("([-_.\(\) ])", '_', coln)
            coln = re.sub("([+: ])", '', coln)
            col_names.append(coln)
        self.df.columns = col_names

    def load_data(self, filename, sep=','):
        """
        load_data
        check file extension if csv or xlsx or dat
        """
        ext = os.path.splitext(filename)[-1].replace('.','')
        if ext == 'csv':
            self.df = pd.read_csv(filename, sep=sep)
            # return self.df
        elif ext == 'xlsx' or ext == '.xls':
            self.df = pd.read_excel(filename)
            # return self.df
        self.fix_col_names()
        
    def __which_time_col(self, cols):
        # Look for date columns
        time_cols = []
        for i, c in enumerate(cols):
            match_obj = re.match("time", c, flags=re.IGNORECASE)
            if match_obj:
                time_cols.append(match_obj.group())
        return time_cols

    def __which_date_col(self, cols):
        # Look for date columns
        date_cols = []
        for i, c in enumerate(cols):
            match_obj = re.match("datetime|date|dte", c, flags=re.IGNORECASE)
            if match_obj:
                date_cols.append(match_obj.group())
        return date_cols
        

    def fix_types(self):
        """
        Fix data types to_numeric, to_datetime
        Look at top 100 rows of each col and decide on a
        data type, if number rows < 100 then use all rows
        """        
 
        def fix_time_cols(self):
            # Fix TIme Columns
            try:
                # fix time cols
                for c in self.time_cols:
                    self.df[c] = pd.to_datetime(self.df[c], format='%H:%M:%S')
            except:
                pass

            # Fix TIme Columns
            try:
                # fix time cols
                for c in self.time_cols:
                    self.df[c] = pd.to_datetime(self.df[c], format='%H.%M.%S')
            except:
                pass
            
        def fix_date_cols(self):
            # fix date cols
            # for cols in date_cols do pd.to_datetime()
            for c in self.date_cols:
                try:
                    self.df[c] = pd.to_datetime(self.df[c])
                except:
                    self.df[c] = pd.to_datetime(self.df[c], format='%d/%m/%y %H.%M.%S')
                    
        
        # Look for date columns
        self.date_cols = self.__which_date_col(self.df.columns)
        
        # fix date cols
        # for cols in date_cols do pd.to_datetime()
        # for c in self.date_cols:
        #     self.df[c] = pd.to_datetime(self.df[c])
        
        # fix date cols
        fix_date_cols(self)
        
        # Look for time columns
        self.time_cols = self.__which_time_col(self.df.columns)
        
        # Remove Date Cols from Time Cols
        self.time_cols = list(set(self.time_cols) - set(self.date_cols))
        
        # Fix time columns
        fix_time_cols(self)
        
        # Infer Objects
        self.df.infer_objects()
        
        return self
    
    def fix_missing(self):
        """
        For each col count the number of missing 
        divided by the number of rows. 
        Check if over 20% missing
        """
        n_rows = self.df.shape[0]
        perc_missing = []
        for c in self.df.columns:
            n_missing = self.df[c].isna().sum()
            perc_missing.append(n_missing/n_rows)
            
        drop_cols = []
        for i, p in enumerate(perc_missing):
            if p > 0.2:
                drop_cols.append(self.df.columns[i])
        
        # Drop the columns
        self.df.drop(drop_cols, axis=1, inplace=True)
                                 
        return self
               
    def french_dec_english(self, colnames):
        """
        Convert 2,6 to 2.6
        """
        for c in colnames:
            self.df[c] = self.df[c].apply(lambda x: str(x).replace(',','.'))
        
        return self
    
    def is_time_componet(self, colname):
        # There is no time component
        if self.df[colname].dt.hour.sum() == 0 and self.df[colname].dt.minute.sum() == 0 and self.df[colname].dt.second.sum() == 0 and self.df[colname].dt.microsecond.sum() == 0:
            return False
        # There IS a time component
        else:
            return True
    
    def make_discrete_datetime_cols(self, verbose=False):
        # Look for date columns
        self.date_cols = self.__which_date_col(self.df.columns)
        # Look for time columns
        self.time_cols = self.__which_time_col(self.df.columns)
        
        if verbose:
            print('Date columns:', self.date_cols, 'Time columns', self.time_cols )
            
        for d in self.date_cols:
            # append col name as prefix
            self.df['_'.join([d, 'day'])] = self.df[d].dt.day
            self.df['_'.join([d, 'month'])] = self.df[d].dt.month
            self.df['_'.join([d, 'year'])] = self.df[d].dt.year
            
            # If there is a time component then extract hour
            if self.is_time_componet(d):
                self.df['_'.join([d, 'hour'])] = self.df[d].dt.hour

        
                                 
############################################################
### API
############################################################
bo = Boab()
bo.load_data('boab-data-science/boab/AirQualityUCI.csv', sep=';')
bo.fix_types()
bo.fix_missing()
bo.french_dec_english(['co_gt_', 'c6h6_gt_', 't', 'rh', 'ah'])
bo.make_discrete_datetime_cols()
bo.df.head()

#
# CODE
#

#Binning:
# def binning(col, cut_points, labels=None):
#   #Define min and max values:
#   minval = col.min()
#   maxval = col.max()

#   #create list by adding min and max to cut_points
#   break_points = [minval] + cut_points + [maxval]

#   #if no labels provided, use default labels 0 ... (n-1)
#   if not labels:
#     labels = range(len(cut_points)+1)

#   #Binning using cut function of pandas
#   colBin = pd.cut(col,bins=break_points,labels=labels,include_lowest=True)
#   return colBin

# #Binning age:
# cut_points = [90,140,190]
# labels = ["low","medium","high","very high"]
# data["LoanAmount_Bin"] = binning(data["LoanAmount"], cut_points, labels)
# print pd.value_counts(data["LoanAmount_Bin"], sort=False)