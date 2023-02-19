# =============================================================================================================
#    (01.3) free function as thread, command-line-specified count and names. parser as class.py
#           Show thread creation with a free function, using command-line-specified thread count, 
#           thread names, and sleep times (with default values), parsed by a class method
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

# +++++++++++++++++++++++++++++++++++++++++++++++
# imports
# +++++++++++++++++++++++++++++++++++++++++++++++
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
import threading
import time


# +++++++++++++++++++++++++++++++++++++++++++++++
# parameterizable constants
# +++++++++++++++++++++++++++++++++++++++++++++++
#
DEFAULT_THREAD_COUNT = 5
MAX_THREAD_COUNT = 40        # avoid completely flooding the host system

DEFAULT_THREAD_SLEEP_TIME=0.2     # default sleep time, seconds
MAX_THREAD_SLEEP_TIME = 20        # avoid terribly long timeouts


# +++++++++++++++++++++++++++++++++++++++++++++++
# supporting functions
# +++++++++++++++++++++++++++++++++++++++++++++++
#
err_to_str = lambda err: '' if str(err) is None else ': ' + str(err)
aborting =   lambda name, err: f'?? Aborting {name} at {time.ctime()}{err_to_str(err)}'

# ----------------------------------------------
#  thread code body
# ----------------------------------------------
#
def sample_thread( sleep_time ):
    """ sleep for a caller-specified period of time """
    try:
        print( f'Thread {threading.current_thread().name} started - sleeping for {sleep_time} seconds' )
        time.sleep( sleep_time )
        print( f'Thread {threading.current_thread().name} ending' )
    except Exception as err:
        print( aborting(threading.current_thread().name, err) )


# +++++++++++++++++++++++++++++++++++++++++++++++
# command line parsing logic
# +++++++++++++++++++++++++++++++++++++++++++++++
#
class thread_count_parser(argparse.Action):
    """ parse and validate a count of maximal concurrently active threads  """
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(thread_count_parser, self).__init__(option_strings, dest, **kwargs)
    def __call__(self, parser, namespace, value, option_string=None):
        try:
            raw_thread_count = int(value)
            if raw_thread_count > MAX_THREAD_COUNT:  
                print( f'?? limiting thread count (was {raw_thread_count}) to {MAX_THREAD_COUNT}' )
            if raw_thread_count < 0:                 
                print( f'?? invalid thread count ({raw_thread_count}); changing to 0' )
            setattr(namespace, self.dest, max(0, min(MAX_THREAD_COUNT, raw_thread_count) ) )
        except:
            raise argparse.ArgumentTypeError( f'\ninvalid thread count: {value}\nmust be an integer' )

class thread_name_list_parser(argparse.Action):
    """ 
    parse a comma-separated list of thread names
    special-case thread name semantics;    
        empty name - use Python default name
        None -       use Python default name
    """
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(thread_name_list_parser, self).__init__(option_strings, dest, **kwargs)
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, [ None if thread_name == '' else thread_name for thread_name in values.split(',')] ) 

class sleep_time_list_parser(argparse.Action):
    """ parse a comma-separated list of nonnegative floating point values denoting sleep times """
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(sleep_time_list_parser, self).__init__(option_strings, dest, **kwargs)
    def __call__(self, parser, namespace, values, option_string=None):
        try:
            raw_thread_sleep_times = [ DEFAULT_THREAD_SLEEP_TIME if sleep_time == '' else float(sleep_time) for sleep_time in values.split(',') ]
            for time in raw_thread_sleep_times:
                if time > MAX_THREAD_SLEEP_TIME:  
                    print( f'?? limiting sleep time (was {time}) to {MAX_THREAD_SLEEP_TIME}' )
                if time < 0:                      
                    print( f'?? invalid negative sleep time ({time}); changing to 0' )
            setattr(namespace, self.dest, [ max(0, min(MAX_THREAD_SLEEP_TIME, time)) for time in raw_thread_sleep_times ] )
        except:
            raise argparse.ArgumentTypeError( f'\ninvalid sleep time list: {values}\ntimes must be a comma-separated llist of floating point values' )

class thread_pair_list_parser(argparse.Action):
    """ parse a list of (thread_name, sleep_times) into a list of thread tuple """
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(thread_pair_list_parser, self).__init__(option_strings, dest, **kwargs)
    def __call__(self, parser, namespace, values, option_string=None):
        try:
            raw_string = ''.join(values.split())
            thread_pairs = raw_string.split('),(')
            parsed_list = []
            bad_args = []

            for thread in thread_pairs:
                try:
                    # trim unneeded characters
                    thread = thread.lstrip('(')
                    thread = thread.rstrip(')')
                    args = thread.split(',')
                    
                    # only name, time allowed
                    if len(args) > 2:
                        raise argparse.ArgumentTypeError( f'\ninvalid arguments: {bad_args}\n can only have two args: (name, time)' )

                    parsed_list.append((args[0], float(args[1])))
                    setattr(namespace, self.dest,  [x for x in parsed_list])
                except:
                    bad_args.append(thread)
            
            if bad_args:
                raise argparse.ArgumentTypeError( f'\ninvalid arguments: {bad_args}\n must be in the format (name, time)' )          

        except Exception as err:
            print( aborting(bad_args, err) )
            exit(1)


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
    parser.add_argument( '-tc', '--thread-count', action=thread_count_parser,     dest='thread_count', default=5, )
    parser.add_argument( '-tp', '--thread-pairs',  action=thread_pair_list_parser,  dest='thread_pairs',   default=[] )


    # parse the arguments, filling out the lists of parameters for thread launch
    #
    parsed_args = parser.parse_args( )
    # fill out the lists of parameters for thread launch
    #
    filler = lambda l, item: [ item ] * max( 0, parsed_args.thread_count - len( l ) )
    # parsed_args.thread_names += filler( parsed_args.thread_names, None )
    # parsed_args.sleep_times += filler( parsed_args.sleep_times, DEFAULT_THREAD_SLEEP_TIME )
    parsed_args.thread_pairs += filler(parsed_args.thread_pairs, (None, DEFAULT_THREAD_SLEEP_TIME))

    # finally, launch the threads
    #
   
    for i in range(parsed_args.thread_count):          
       threading.Thread(target=sample_thread, name=parsed_args.thread_pairs[i][0], args=(parsed_args.thread_pairs[i][1],)).start()
    print( f'{my_name} - ending' )

except Exception as err:
    print( aborting(my_name, err) )
