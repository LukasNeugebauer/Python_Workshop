from Subject import Subject
from argparse import ArgumentParser

def run_subject(subID):
    
    s = Subject(subID,run = False);
    s.fit_regression();
    s.plot(save=True,show=False);
    
if __name__ == '__main__':
    
    parser = ArgumentParser();
    parser.add_argument( 'subID',
                         type = int,
                         action= 'store',
                         help = 'ID of subject to be analyzed.'
                         );
    args = parser.parse_args();
    
    run_subject( args.subID );