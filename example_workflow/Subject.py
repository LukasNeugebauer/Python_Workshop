import numpy as np
from scipy import stats
import os
from ipdb import set_trace
from Base_project import Base_project
import pickle
import pandas as pd
import seaborn as sns
from scipy.stats import linregress
from matplotlib import pyplot as plt

class Subject( Base_project):
    
    def __init__(self,subID, run = False):
        super().__init__();
        self.subID = subID;
        if not self.subject_exists(subID):
            raise Exception('No such subject in the directory ' + self.path)
        #loading data while creating the object
        self.load_data();
        self.convert_seq();
        if run:
            self.fit_regression();
        
    #we will have to load the data
    def load_data(self):
        self.load_rating();
        self.load_RT();
        
    def load_rating(self):
        path = self.path_to_data( self.subID, 'food' );
        self.rating = pd.read_csv(path, header = None).values;
    
    def load_RT(self):
        path = self.path_to_data( self.subID, 'RT' );
        dummy = pd.read_csv( path, header = None ).values;
        self.RT = dummy[:,1]; # second column are RTs
        self.seq = dummy[:,0]; # first column is sequence
        
    #we have to convert the sequence of foodIDs into a 
    def convert_seq(self):
        self.rate_seq = np.array( [ self.rating[ self.rating[:,0] == s, 1] for s in self.seq ] );
    
    #we will use a linear regression
    def fit_regression(self):
        savename = self.path_to_data( self.subID, 'food').replace( 'food_ratings.csv', 'linreg_result.pic' );
        #check if you already saved it before, if yes unpickle
        if os.path.exists(savename):
            print('Found pickled version.')
            with open(savename, 'rb') as f:
                out = pickle.load( f );
        #otherwise, run regression and pickle, so next time you just load the result
        else:
            print('Running analysis now.')
            out = linregress( self.rate_seq.squeeze(), self.RT );
            with open(savename,'wb') as f:
                pickle.dump(out, f, -1 );
        #make it a dict and part of the object:
        result_names = ['slope', 'intercept', 'corr', 'p', 'SE' ];
        self.results = dict(zip(result_names,out));    
        #a function that plots reaction times against ratings
    
    def plot(self, show = False, save = True):
        fig = plt.figure(figsize=(16,8));
        ax = fig.add_subplot(111);
        sns.regplot( self.rate_seq, self.RT, ax= ax ) ;
        ax.set_xlabel('Food ratings',fontsize=20);
        ax.set_ylabel('Reaction times',fontsize=20);
        ax.set_xticks(np.arange(1,21) );
        ax.set_title('Regression of reaction times on food ratings, subject {}'.format(self.subID), fontsize= 25)
        if show:
            plt.show()
        if save:
            savename = self.path_to_data(self.subID, 'food').replace( 'food_ratings.csv', 'reg_plot.PNG' );
            if not os.path.exists(savename):
                fig.savefig( savename )