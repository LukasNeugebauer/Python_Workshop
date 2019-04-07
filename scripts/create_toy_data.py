'''
Creating some toy data for you to play around with
It's completely artificial data that was "collected" the following experiment:

Participants see pictures of 30 different food items in random order. The timing is jittered, 
so they don't know when the next item will appear.  
They are instructed to hit a button as fast as possible when an item appears. 
Participants also rated how much they liked each item on a scale from 1 to 20. 

We recorded the reaction times and of course the ratings. This allows for some interesting analysis.
'''

import numpy as np;
from scipy import stats;
import os;
import pandas as pd

base_pth = os.path.abspath( '../toy_data' );

#we assume 15 participants. Unfortunately, one is missing in between
#this will of course make everything harder ]:->
subjects = np.delete( np.arange(1,16), 7 );

#we also assume 150 trials which means there is 5 presentations per stimulus.
n_trials = 150;

#reaction times on average are 0.5 seconds
reac = dict();
reac['mean'] = stats.norm(0.4,0.1);

#stds are also noisy
reac['std'] = stats.norm(0.2,0.1);

#also, skewness is not equal
reac['skew'] = stats.norm(3.5,0.5);

#dependence on liking is noisy
reac['dep_like'] = stats.norm(0.2,0.2);


for sub in subjects:
    
    #create a new directory
    tmp_pth = os.path.join( base_pth, 's{:02d}'.format( sub ) );
    if not os.path.exists(tmp_pth):
        os.mkdir( tmp_pth );
    
    #create random likings of food:
    _like = np.random.randint(1,20,(30,1)) + 1; # +1 because 0-based
    like = np.c_[np.arange(1,31), _like].astype(int); # concatenate along columns
    
    #save to food_ratings.csv
    to_pth = os.path.join(tmp_pth,'food_ratings.csv');
    pd.DataFrame(like).to_csv( to_pth, float_format='%d', index = False,header = False);
    
    #create a random sequence
    seq = np.repeat( np.arange(30), 5 ) + 1;
    np.random.shuffle( seq ); #works in-place
    
    #optionally to be used, replace food_id with liking
    like_seq = np.array( [ like[ np.where( like[:,0] == x ),1 ].squeeze() 
                             for x in seq ] );
    to_pth = os.path.join( tmp_pth, 'rating_sequence.csv');
    pd.DataFrame(like_seq).to_csv( to_pth, float_format='%d', index = False, header = False);
    
    #z-transform
    z_like = ( like_seq - like_seq.mean() ) / like_seq.std();

    #raw reaction times
    skew = reac['skew'].rvs();
    mean = reac['mean'].rvs();
    std  = reac['std'].rvs();
    std  = std if std > 0 else 0.02;
    raw_reac = stats.skewnorm(skew,mean,std).rvs(n_trials);
    
    #add dependence on liking
    dep = reac['dep_like'].rvs();
    add_dep = stats.norm( 0.3, 0.1).rvs(n_trials) * dep * z_like;
    dep_reac = raw_reac - add_dep; # more liking, less reacion
    
    #make sure that smallest reaction time is < 0.5
    dep_reac += 0.05 -dep_reac.min();
    
    #combine with sequence
    seq_reac = np.c_[seq, dep_reac];
    
    #write to file:
    to_pth = os.path.join(tmp_pth, 'sequence_RT.csv');
    pd.DataFrame( seq_reac ).to_csv(to_pth, index = False, header = False )
    
