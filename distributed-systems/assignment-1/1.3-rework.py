# =============================================================================================================
#    (01.3) free function as thread, command-line-specified count and names. parser as function.py
#           Show thread creation with a free function, using command-line-specified thread count,
#           thread names, and sleep times (with default values), parsed by a free function.
#
# -------------------------------------------------------------------------------------------------------------
#   adapted from code by Doug Hellman by Phil Pfeiffer
#     source:  "Python 3 Module of the Week:  threading - Manage Concurrent Operations Within a Process"
#     URL:     https://pymotw.com/3/threading/ - last accessed 13 July 2018
#   last updated:  September 2018
# -------------------------------------------------------------------------------------------------------------
#   adapted further by Chandler Scott
#   class:  CSCI-5150-201
#   last updated:  August 2022
# -------------------------------------------------------------------------------------------------------------
#   usage:
#       <program-name> <thread-count> <thread-name-list> <sleep_times>
#       command line arguments:
#           thread-count:  number of threads to launch
#               format:  --thread-count <number>  or   -tc <number>
#           thread-names:  comma-separated list of strings for naming threads
#               format:  --thread-names <list>    or   -tn <list>
#           sleep-times:  comma-separated list of floating point values for time for threads to sleep
#               format:  --sleep-times <list>     or   -st <list>
#        all arguments are optional.  for defaults, see below.
# =============================================================================================================

# ---------------------------------------------
# imports
# ----------------------------------------------
#
# argparse -
#    argparse.add_argument - specify one in a series of arguments to parse
#    argparse.Argument_parser - create a string parser
#    argparse.parse_args - do the parse
# threading -
#    threading.current_thread - identify current thread
#    threading.Thread - instantiate a thread
# time -
#    time.ctime - returns current time of day
#    time.sleep - stop thread processing for specified number of seconds
#
import argparse
from ast import parse
from ctypes import ArgumentError
import threading
import time


# +++++++++++++++++++++++++++++++++++++++++++++++
# parameterizable constants
# +++++++++++++++++++++++++++++++++++++++++++++++
#
DEFAULT_THREAD_COUNT = 5
MAX_THREAD_COUNT = 40       # avoid completely flooding the host system

DEFAULT_THREAD_SLEEP_TIME=0.2       # default sleep time, seconds
MAX_THREAD_SLEEP_TIME = 20          # avoid terribly long timeouts


# +++++++++++++++++++++++++++++++++++++++++++++++
# supporting functions
# +++++++++++++++++++++++++++++++++++++++++++++++

err_to_str = lambda err: '' if str(err) is None else ': ' + str(err)
aborting =   lambda name, err: f'?? Aborting {name} at {time.ctime()}{err_to_str(err)}'

# ----------------------------------------------
#  thread code body
# ----------------------------------------------
#
def sample_thread( sleep_time ):
    """ sleep for a caller-specified period of time """
    err_to_str = lambda err: '' if str(err) is None else ': ' + str(err)
    #
    try: 
        print( f'Thread {threading.current_thread().name} started - sleeping for {sleep_time} seconds' )
        time.sleep( sleep_time )
        print( f'Thread {threading.current_thread().name} ending' )
    except Exception as err:
        print( aborting(threading.current_thread().name, err) )


# ----------------------------------------------
# command line parsing logic
# ----------------------------------------------
#
def thread_count_parser( value ):
    """ parse and validate a count of threads to invoke  """
    try:
        raw_thread_count = int( value )
        if raw_thread_count > MAX_THREAD_COUNT:
            print( f'?? limiting thread count (was {raw_thread_count}) to {MAX_THREAD_COUNT}' )
        if raw_thread_count < 0:
            print( f'?? invalid thread count ({raw_thread_count}); changing to 0' )
        return max(0, min(MAX_THREAD_COUNT, raw_thread_count) )
    except:
        raise argparse.ArgumentTypeError( f'\ninvalid thread count: {value}\nmust be an integer' )

def sleep_time_parser( value ):
    """ parse a comma-separated list of nonnegative floating point values denoting sleep times """
    try:
        raw_sleep_time = DEFAULT_THREAD_SLEEP_TIME if value == '' else float(value)
    
        if raw_sleep_time > MAX_THREAD_SLEEP_TIME:
            print( f'?? limiting sleep time (was {raw_sleep_time}) to {MAX_THREAD_SLEEP_TIME}' )
        if raw_sleep_time < 0:
            print( f'?? invalid negative sleep time ({raw_sleep_time}); changing to 0' )
        return max(0, min(MAX_THREAD_SLEEP_TIME, raw_sleep_time))
    except:
        raise argparse.ArgumentTypeError( f'\ninvalid sleep time list: {value}\n must be a floating point value' )

def split_list( string ):
    """
    parse a (a),(b),(c)... list
    """
    list = string.split('),(')
    
    for i in range(len(list)):
        list[i] = list[i].replace('(', '')
        list[i] = list[i].replace(')', '')
    

    return list

def split_pairs( unpaired_list ):
    """
    parse a comma-separated list of pairs of thread names and sleep times
    """

    return [ x.split(',') for x in unpaired_list ]

def exit_program_with_error (error):
    """"""
    print(error)
    exit(1)


def thread_pair_list_parser( args ):
    """
    parse a parentheses-separated list of thread names & sleep times separated by commas.
    check for clean user input and report discrepancies to the user.
    special-case thread name semantics;
        empty name - use Python default name
        None -       use Python default name
    special-case sleep semantics;
        empty time - use DEFAULT_THREAD_SLEEP_TIME
    """
    # split the list into each pair
    unpaired_list = split_list(args)
    # next, split the pairs
    paired_list = split_pairs(unpaired_list)
    
    if len(paired_list) > MAX_THREAD_COUNT:
        error_message = f"There are more arguments than there are max threads allowed. ({MAX_THREAD_COUNT})"
        exit_program_with_error(error_message)

    parsed_list = []
    type_exceptions = []
    numargs_exceptions = []

    # 3 cases: user gave time & name, user gave name, user gave time; 
    # error cases: user gives too many args, user gives args in wrong orders
    for list in paired_list:       
        try:
            if len(list) > 2:
               raise ArgumentError
            elif len(list) == 2:
                tp_args = (list[0], sleep_time_parser(list[1]))
                parsed_list.append(tp_args)
            else:
                # if len==1, the argument could be time OR a name.
                try:
                    float(list[0])
                    tp_args = (None, sleep_time_parser(list[0]))
                except:
                    tp_args = (list[0], sleep_time_parser(''))
                finally:
                    parsed_list.append(tp_args)
        except ArgumentError:
            numargs_exceptions.append(list)
        except argparse.ArgumentTypeError:
            type_exceptions.append(list)

    error_message = ''
    exit_from_input_error = False
    if len(type_exceptions) > 0:
        error_message += 'The following -tp arguments are not in the correct format. Time was not able to be parsed.\n'
        error_message += str([ex for ex in type_exceptions]) + "\n"
        exit_from_input_error = True
    if len(numargs_exceptions) > 0:
        error_message += 'The following -tp arguments are not in the correct format. Too many arguments were given.\n'
        error_message += str([ex for ex in numargs_exceptions]) + "\n"
        exit_from_input_error = True
    if exit_from_input_error:
        exit_program_with_error(error_message)
        

    return parsed_list

# ================================================
#    Program Main
# ================================================
#
my_name = threading.current_thread().name
#
try:
    print( f'{my_name} - starting' )

    # set up to acquire arguments from command line
    #
    parser = argparse.ArgumentParser( prog='thread-generator', description='Run user-specified number of threads that sleep, then exit.')
    parser.add_argument( '-tc', '--thread-count', type=thread_count_parser,     dest='thread_count',  default=DEFAULT_THREAD_COUNT )
    parser.add_argument( '-tp', '--thread-pairs',  type=thread_pair_list_parser,  dest='thread_pairs',   default=[] )

    # parse the arguments, filling out the lists of parameters for thread launch
    #
    parsed_args = parser.parse_args( )

    # fill out the lists of parameters for thread launch
    #
    filler = lambda l, item: [ item ] * max( 0, parsed_args.thread_count - len( l ) )
    parsed_args.thread_pairs += filler(parsed_args.thread_pairs, (None, DEFAULT_THREAD_SLEEP_TIME))

    # check for more thread pairs than specified thread count
    #
    if len(parsed_args.thread_pairs) > parsed_args.thread_count:
        error_message = f"There are more arguments ({len(parsed_args.thread_pairs)}) than there are max threads allowed. ({parsed_args.thread_count})"
        exit_program_with_error(error_message)

    # finally, launch the threads
    #
    for i in range(parsed_args.thread_count):
        
        threading.Thread(target=sample_thread, name=parsed_args.thread_pairs[i][0], args=(parsed_args.thread_pairs[i][1],)).start()
        print( f'{my_name} - ending' )


except Exception as err:
    print( aborting(my_name, err))