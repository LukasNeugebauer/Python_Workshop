#Class Base_project to be used by the other class


import numpy as np;
import pandas as pd;
import os;
import re


class Base_project:
    
    project = 'Example_project';
    path = 'C:/Users/neugebauer/Documents/Python_workshop/toy_data/';
    file_map = {'food': 'food_ratings.csv', 'rate': 'rating_sequence', 'RT': 'sequence_RT.csv'};

    #you need one anyway
    def __init__(self):
        self.list_subjects();
    
    #list the available subjects and make them part of the object
    def list_subjects(self):
        regex = re.compile( 's[0-9]{2}' );
        self.subjects = [ sub for sub in os.listdir( self.path ) if regex.search( sub ) ];

    #check for a given subject ID if there is data 
    def subject_exists(self,subID):
        return 's{:02d}'.format(subID) in self.subjects  
    
    def data_exists(*args, **kwargs): # you could also just ask for subID and filetype. if there are many input arguments, this is easier.
        path = self.path_to_data(*args, **kwargs);
        return os.path.exists(path)

    def path_to_data(self, subID, filetype):
        if not filetype in self.file_map.keys():
            raise KeyError( "filetype has to be one of the following: ['food','rate','RT']")
        path = os.path.join( self.path, 's{:02d}'.format(subID), self.file_map[filetype]);
        return path