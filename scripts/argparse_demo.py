"""
This scripts demonstrates how to use the 'argparse' library
to parse command line arguments
"""


# this is how you import the relevant class from the argparse library
from argparse import ArgumentParser


# here we define three functions, all of which take arguments
def say_hello(name):
    print(f"Hey, {name}, how are you?")


def print_temperature(temperature, convert=False):
    if convert:
        temperature = celcius2fahrenheit(temperature)
    print("The temperature is {} {}".format(temperature, "°F" if convert else "°C"))


def celcius2fahrenheit(celcius):
    return celcius * 1.8 + 32


# this is the part that will only be run if the program is the main program
if __name__ == "__main__":

    # first create an instance of the class ArgumentParser
    parser = ArgumentParser()

    # now we add some arguments to the parser. This means we tell it, what to look for
    # either as positional argument:
    parser.add_argument(
        "name",  # this is how we will find it later
        help="Your name",  # this will be shown as help in the command line
        action="store",  # store it in the parser object
    )

    # or by defining how to give the argument.
    parser.add_argument(
        "-t",
        "--temperature",  # how to give the argument, e.g.: -t 32 or --temperature 32
        action="store",  # store it
        dest="temperature",  # this is where we will find it later
        default=20,  # we can use a default if we don't get a value
        type=int,  # this is needed because by default all arguments are strings
        help="Today's temperature, default = 20°C",  # help text
    )

    # we can use this also to switch between two constants
    parser.add_argument(
        "-c",
        "--convert",
        action="store_const",  # store one of two constants
        dest="convert",  # in here
        const=True,  # this is used if we demand -c while calling the script
        default=False,  # this is used otherwise
        help="Indicating wether you want to convert to Fahrenheit",  # help text
    )

    # let the parser do its job and catch the command line arguments
    args = parser.parse_args()

    # now the arguments are stored in args and we can use them:
    say_hello(args.name)
    print_temperature(args.temperature, args.convert)
