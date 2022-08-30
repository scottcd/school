# =======================================================================================================================
#   (03.2) threads with logging module, dynamic message configuration.py - 
#          Show use of the python library's logging adapter class to dynamically alter logging module ou
# -----------------------------------------------------------------------------------------------------------------------
#   adapted from code by Doug Hellman and Vijay Sajip by Phil Pfeiffer
#     sources:  
#         "Python 3 Module of the Week:  threading - Manage Concurrent Operations Within a Process"
#         URL:     https://pymotw.com/3/threading/ 
#                  - last accessed 13 July 2018
#         "Logging Cookbook: Adding Contextual Information to Your Logging Output"
#         URL:     https://docs.python.org/3/howto/logging-cookbook.html#adding-contextual-information-to-your-logging-output
#                  - last accessed 17 July 2018
#   last updated:  August 2022
# -----------------------------------------------------------------------------------------------------------------------
#   design notes:
#   *.  this code's use of a LoggingAdapter object allows it to reformat log output on a per-execution basis
#       when executed multiple times in a single Python session.
# =======================================================================================================================

# ++++++++++++++++++++++++++++++++++++++++++++++
# imports
# ++++++++++++++++++++++++++++++++++++++++++++++
#
# logging - 
#    logging.* - generate thread-safe output from threads
#    logging.basicConfig - set the baseline log message prefix - limited to once per session
#    logging.LoggingAdapter - generate an object for dynamically modifying logging output
# random -
#     random.seed - initialize random library random number generators
#     random.uniform - generate random floats over a uniform distribution
# threading - 
#    threading.current_thread - identify current thread
#    threading.Thread - instantiate a thread
# time - 
#    time.ctime - generate human readable time of day
#    time.sleep - stop thread processing for specified number of seconds
#    time.time -  return current time
#
from ast import parse
import logging
import random
import threading
import time
import sys
from datetime import datetime
import argparse

# +++++++++++++++++++++++++++++++++++++++++++++
# supporting functions
# +++++++++++++++++++++++++++++++++++++++++++++
#
aborting =   lambda: f'?? Aborting at {time.ctime()}'
hour =   lambda: '{:02d}'.format(datetime.now().hour)
minute =   lambda: '{:02d}'.format(datetime.now().minute)
second =   lambda: '{:02d}'.format(datetime.now().second)

logger_destination = 'console'

# ++++++++++++++++++++++++++++++++++++++++++++++
# supporting classes and related objects
# ++++++++++++++++++++++++++++++++++++++++++++++
#
#  CustomLogger - supports use of the Logger class's extra dict to help columnate field names in output messages
#
class CustomLogger(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        my_name = threading.current_thread().name
        padding = (self.extra.get('max_thread_name_length', len(my_name)) +1 - len(my_name))*' '
        return f'({my_name}){padding}{msg}', kwargs

# configure logging, part 1
# logging.basicConfig format parameter: formatting string for log messages sent to the logging module
#     levelname - a logging module built-in
#     message - reference to log messages' first parameter
# my_logger - logger to use for thread output
#     max_thread_name_length is determined after threads to create are declared
#


#logging.basicConfig(level=logging.DEBUG, format=f'[%(levelname)s] {hour()}:{minute()}:{second()} %(message)s')
my_logger = CustomLogger(logging.getLogger(__name__), { 'max_thread_name_length': 0 } )

class MyThread(threading.Thread):
    """ sleep for a random time, relative to user-specified min and max waith times """
    def __init__(self, *, name=None, lifetime_range=((0,0)), logger=my_logger):
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
        except:
            self.logger.exception( aborting() )
            raise
    #
    def run( self ):
        """thread worker function"""
        try:
            self.logger.info( f'Starting at {time.ctime()} - should exit at {time.ctime(time.time()+self.sleep_time)}' )
            time.sleep(self.sleep_time)
            self.logger.info( f'Exiting at {time.ctime()}' )
        except:
            self.logger.exception( aborting() )
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
            my_threads = []
            
            raw_string = ''.join(values.split())
            thread_specs = raw_string.split('),(')

            for thread in thread_specs:
                thread = thread.lstrip('(')
                thread = thread.rstrip(')')
                trimmed = thread.split(',(')
                sleep_time = trimmed[1].split(',')
                my_threads.append(MyThread( name=trimmed[0], lifetime_range=(float(sleep_time[0]), float(sleep_time[1])) ))

            setattr(namespace, self.dest, [x for x in my_threads ] )
        except:
            raise argparse.ArgumentTypeError( f'\ninvalid sleep time list: {values}\ntimes must be a comma-separated llist of floating point values' )

class file_name_parser(argparse.Action):
    """ parse a comma-separated list of nonnegative floating point values denoting sleep times """
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(file_name_parser, self).__init__(option_strings, dest, **kwargs)
    def __call__(self, parser, namespace, value, option_string=None):
        try:
            file_name = value
            global logger_destination 
            logger_destination = value
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

    try:
        parsed_args = parser.parse_args( )
    except Exception as e:
        print(e.args[0])
    
    if logger_destination == 'console':
        logging.basicConfig(level=logging.DEBUG, format=f'[%(levelname)s] {hour()}:{minute()}:{second()} %(message)s')
    else:
        logging.basicConfig(level=logging.DEBUG, format=f'[%(levelname)s] {hour()}:{minute()}:{second()} %(message)s', filename=logger_destination)

    # threads_to_run - list of threading.Thread objects to run
    #
    if parsed_args.thread_specs:
        my_logger.info(parsed_args.thread_specs)
        threads_to_run = parsed_args.thread_specs[:]
    else:
        threads_to_run = [
            MyThread( name='worker', lifetime_range=(14.0, 20.0) ),
            MyThread( name='worker_by_another_name', lifetime_range=(11.0, 16.0) ),
            MyThread( lifetime_range=(8.0, 13.0) ),
            MyThread( lifetime_range=(5.0, 10.0) )
        ]

    # configure logging, part 2 - determine space to leave for columnating thread names
    #
    my_logger.extra['max_thread_name_length'] = max([len(thread.name) for thread in threads_to_run + [threading.current_thread()]])

    # use current time to seed random number generator, making thread sleep times quasi-nondeterministic
    #
    random.seed()

    # create and launch one thread per entry in thread name matrix
    #
    my_logger.info( f'starting at {time.ctime()}' )
    for thread in threads_to_run:  thread.start()
    my_logger.info( f'exiting at {time.ctime()}' )

except:
    my_logger.exception( aborting() )

