# =======================================================================================================
#   (03.1) threads with logging module.py - 
#          Show use of the python library's logging module to generate output
# -------------------------------------------------------------------------------------------------------
#   adapted from code by Doug Hellman by Phil Pfeiffer
#     source:  "Python 3 Module of the Week:  threading - Manage Concurrent Operations Within a Process"
#     URL:     https://pymotw.com/3/threading/ - last accessed 13 July 2018
#   last updated:  August 2022
# --------------------------------------------------------------------------------------------------------
#   design notes:
#   *.  given this code's structure, logging.basicConfig() should be run at most once in any Python session.  
#       Attempts to rerun this code appear to have no effect on the format string, due to the logging class's 
#       use of a persistent object to manage all formatting
# ========================================================================================================

# +++++++++++++++++++++++++++++++++++++++++++++
# imports
# +++++++++++++++++++++++++++++++++++++++++++++
#
# logging - 
#    logging.* - generate thread-safe output from threads
# random -
#    random.seed - initialize random library random number generators
#    random.uniform - generate random floats over a uniform distribution
# threading - 
#    threading.current_thread - identify current thread
#    threading.Thread - instantiate a thread
# time - 
#    time.ctime - generate human readable time of day
#    time.sleep - stop thread processing for specified number of seconds
#    time.time -  return current time
# argparse -
#    argparse.add_argument - specify one in a series of arguments to parse
#    argparse.Argument_parser - create a string parser
#    argparse.parse_args - do the parse
#
from ast import parse
import logging
import random
import threading
import time
import argparse


# +++++++++++++++++++++++++++++++++++++++++++++
# supporting functions
# +++++++++++++++++++++++++++++++++++++++++++++
#
err_to_str = lambda err: '' if str(err) is None else ': ' + str(err)
aborting =   lambda err: f'?? Aborting at {time.ctime()}{err_to_str(err)}'

# +++++++++++++++++++++++++++++++++++++++++++++
# supporting classes
# +++++++++++++++++++++++++++++++++++++++++++++
#
# class that embodies a thread that runs for a random period of time.  run() is Thread's default thread body
#
class MyThread(threading.Thread):
    """ sleep for a random time, relative to user-specified min and max waith times """
    def __init__(self, *, name=None, lifetime_range=((0,0)), logger=logging):
        """
        required:      none
        optional:
            name -           name to give to a thread.  None => use Python default name
            lifetime_range - a sequence of numbers- nominally, a pair- whose min and max values denote min and max wait times
            logger -         the object to use for logging
        """
        super().__init__(name=name)
        self.logger = logger
        try:
            self.sleep_time = random.uniform(min(lifetime_range), max(lifetime_range))
        except Exception as err:
            self.logger.exception( aborting( err ) )
            raise
    #
    def run( self ):
        """thread worker function"""
        try:
            self.logger.info( f'Starting at {time.ctime()} - should exit at {time.ctime(time.time()+self.sleep_time)}' )
            time.sleep(self.sleep_time)
            self.logger.info( f'Exiting at {time.ctime()}' )
        except Exception as err:
            self.logger.exception( aborting( err ) )

# +++++++++++++++++++++++++++++++++++++++++++++++
# command line parsing logic
# +++++++++++++++++++++++++++++++++++++++++++++++
#
class thread_spec_list_parser(argparse.Action):
    """ parse a comma-separated list of nonnegative floating point values denoting sleep times """
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(thread_spec_list_parser, self).__init__(option_strings, dest, **kwargs)
    def __call__(self, parser, namespace, values, option_string=None):
        try:
            # (thread_name, (lifetime range min, lifetime range max))
            raw_string = ''.join(values.split())
            # split by ),( to get each list item
            
            raw_string = raw_string.lstrip('(')
            raw_string = raw_string.rstrip(')')
            trimmed = raw_string.split(',(')
            print(trimmed)
            print(trimmed[1].split(','))
            
            ready = []
            ready.append(trimmed[0])
            ready.append(trimmed[1].split(','))

            my_threads = []


            my_threads.append(MyThread( name='worker', lifetime_range=(14.0, 20.0) ))
            #values.


            print(ready)
            setattr(namespace, self.dest, [x for x in ready ] )
        except:
            raise argparse.ArgumentTypeError( f'\ninvalid sleep time list: {values}\ntimes must be a comma-separated llist of floating point values' )

class file_name_parser(argparse.Action):
    """ parse a comma-separated list of nonnegative floating point values denoting sleep times """
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(file_name_parser, self).__init__(option_strings, dest, **kwargs)
    def __call__(self, parser, namespace, value, option_string=None):
        try:
            file_name = value
            setattr(namespace, self.dest, file_name )
        except:
            raise argparse.ArgumentTypeError( f'\ninvalid sleep time list: {value}\ntimes must be a comma-separated llist of floating point values' )


# ================================================
#    Program Main
# ================================================
#
try:
    # -------------------------------------------------
    # program thread-dependent operating parameters
    # -------------------------------------------------
    #

    # set up to acquire arguments from command line
    #
    parser = argparse.ArgumentParser( prog='thread-generator', description='Run user-specified number of threads that sleep, then exit.')
    parser.add_argument( '-ts', '--thread-specs', action=thread_spec_list_parser,     dest='thread_specs',  default=[] )
    parser.add_argument( '-fn', '--file-name',  action=file_name_parser,  dest='file_name',   default='console' )

    parsed_args = parser.parse_args( )

    # threads_to_run - list of threading.Thread objects to run
    #
    if parsed_args.thread_specs:
        threads_to_run = parsed_args.thread_specs[:]
    else:
        threads_to_run = [
            MyThread( name='worker', lifetime_range=(14.0, 20.0) ),
            MyThread( name='worker_by_another_name', lifetime_range=(11.0, 16.0) ),
            MyThread( lifetime_range=(8.0, 13.0) ),
            MyThread( lifetime_range=(5.0, 10.0) )
        ]

    # log_message_format - formatting string for log messages sent to the logging module
    #     levelname - a logging module built-in
    #     threadName - accessed as a non-local
    #     str() expression - calculates maximum thread name length for alignment purposes - filter needed because max(None) is undefined
    #     message - reference to log messages' first parameter
    #
    log_message_format = '[%(levelname)s] (%(threadName)-' 
    log_message_format += str(max([len(thread.name) for thread in threads_to_run + [threading.current_thread()]])) 
    log_message_format += 's) %(message)s'

    # configure logging
    # WARNING - second and subsequent calls to logging.basicConfig() during a single Python session will NOT
    #   update the format string.  See Vijay Sinap's "Logging Cookbook" in the Python docs for details.
    #
    if parsed_args.file_name == 'console':
        logging.basicConfig(level=logging.INFO, format=log_message_format)
    else:
        logging.basicConfig(level=logging.INFO, format=log_message_format, filename=parsed_args.file_name)
    # use current time to seed random number generator, making thread sleep times quasi-nondeterministic
    #
    random.seed()

    # create and launch one thread per entry in thread name matrix
    #
    logging.info( f'starting at {time.ctime()}' )
    for thread in threads_to_run:  thread.start()
    logging.info( f'exiting at {time.ctime()}' )

except Exception as err:
    p = 1
    #logger.exception( aborting( err ) )

