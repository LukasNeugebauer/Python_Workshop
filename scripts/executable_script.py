#here you can define functions, classes, etc. to be used for the script

from argparse import ArgumentParser

def print_power(base,exponent):
    to_print = base ** exponent;
    print(to_print);
    
if __name__ == '__main__':
    
    parser = ArgumentParser();
    
    parser.add_argument( 'base',
                         action = 'store',
                         type = int,
                         help = 'The base to be used');
    
    parser.add_argument( '--e','-exponent',
                         action = 'store',
                         dest = 'exponent',
                         default = 2,
                         type = int ,
                         help = 'The exponent to be used');
    
    args = parser.parse_args();
    
    print_power( args.base, args.exponent );