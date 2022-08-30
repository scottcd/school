# ==============================================================================================
#   (05.1) threads with join().py - 
#          Show effect of threading.join() with daemon and non-daemon threads.
# ----------------------------------------------------------------------------------------------
#   adapted from code by Doug Hellman and Vijay Sajip by Phil Pfeiffer
#     sources:  
#         "Python 3 Module of the Week:  threading - Manage Concurrent Operations Within a Process"
#         URL:     https://pymotw.com/3/threading/ 
#                  - last accessed 13 July 2018
#         "Logging Cookbook: Adding Contextual Information to Your Logging Output"
#         URL:     https://docs.python.org/3/howto/logging-cookbook.html#adding-contextual-information-to-your-logging-output
#                  - last accessed 17 July 2018
#   last updated:  August 2022
# ----------------------------------------------------------------------------------------------
#   usage notes:
#   *.  daemon threads continue to execute after the program that creates them ends, 
#         ** so long as the python runtime in which they are launched continues to run **
#       executing this code using a CLI command like 'python threads05.py' won't produce the intended effect:
#         when this terminates, the CLI will terminate the python runtime, with any daemon threads.
#       rather -
#       *. start a python shell, then
#       *. within the shell, execute the code, using a command like exec(open('threads05.py').read())
#       the program should quickly exit, restoring the interactive python prompt -
#          then, at the specified time, the daemon thread should print its name and exit.
# ==============================================================================================

# ++++++++++++++++++++++++++++++++++++++++++++++
# imports
# ++++++++++++++++++++++++++++++++++++++++++++++
#
# collections - 
#    collections.namedtuple - generate named tuples that characterize tests to run
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
import collections
import logging
import random
import threading
import time


# +++++++++++++++++++++++++++++++++++++++++++++
# supporting functions
# +++++++++++++++++++++++++++++++++++++++++++++
#
aborting =   lambda: f'?? Aborting at {time.ctime()}'

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
#
# logging.basicConfig format parameter: formatting string for log messages sent to the logging module
#     levelname - a logging module built-in
#     message - reference to log messages' first parameter
# my_logger - logger to use for thread output
#     max_thread_name_length is determined after threads to create are declared
#
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')
my_logger = CustomLogger(logging.getLogger(__name__), { 'max_thread_name_length': 0 } )

class MyThread(threading.Thread):
    """ sleep for a random time, relative to user-specified min and max waith times """
    def __init__(self, *, name=None, lifetime_range=((10.0, 10.0)), logger=my_logger, is_daemon=False):
        """
        required:      none
        optional:
            name -           name to give to a thread.  None => use Python default name
            is_daemon -      if True, launch thread as a daemon
            lifetime_range - a sequence of numbers- nominally, a pair- whose min and max values denote min and max wait times
            logger -         the object to use for logging
        """
        super().__init__(name=name, daemon=is_daemon)
        self.logger = logger
        try:
            self.sleep_time = random.uniform(min(lifetime_range), max(lifetime_range))
        except:
            self.logger.exception( aborting() )
    #
    def run( self ):
        """thread worker function"""
        try:
            self.logger.info( f'Starting at {time.ctime()} - should exit at {time.ctime(time.time()+self.sleep_time)}' )
            time.sleep(self.sleep_time)
            self.logger.info( f'Exiting at {time.ctime()}' )
        except:
            self.logger.exception( aborting() )


# ===============================================
#    Program Main
# ===============================================
#
try:
    # -------------------------------------------------
    # program thread-dependent operating parameters
    # -------------------------------------------------
    #
    # Thread_test - a type that characterizes the following attributes of a thread to test-run
    #     thread -         thread object proper
    #     wait_time -      how long supporting code should wait on the thread to complete, using threading.join()
    #
    Thread_test = collections.namedtuple('Thread_test', ['thread', 'wait_time'])

    thread_tests = []
    test_name_wait_time_pairs = [ ('indefinite wait', None), ('excessive wait', 15.0), ('inadequate wait', 5.0) ]

	# create two tests for every <name, delay> pair - one for an ordinary thread and one for a daemon thread
	#
    for (i, (core_thread_name, wait_time)) in enumerate(test_name_wait_time_pairs):
       thread_tests += [ Thread_test( MyThread(                 name=f'non-daemon {i+1} - {core_thread_name}' ), wait_time ) ]
       thread_tests += [ Thread_test( MyThread( is_daemon=True, name=f'daemon {i+1} - {core_thread_name}' ),     wait_time ) ]

    # configure logging, part 2 - determine space to leave for columnating thread names, including main (i.e., current) thread
    #
    my_logger.extra['max_thread_name_length'] = max([ len(threading.current_thread().name) ] + [len(test.thread.name) for test in thread_tests])

    # use current time to seed random number generator, making thread sleep times quasi-nondeterministic
    #
    random.seed()

    # create and launch one thread per entry in thread name matrix
    #
    my_logger.info( 'starting main execution' )
    for test in thread_tests:
        test.thread.start()
        test.thread.join(test.wait_time)
        my_logger.info( f'{test.thread.name} is {"" if test.thread.is_alive() else "NOT "}alive at join point\n' )
    my_logger.info( 'exiting' )

except:
    my_logger.exception( aborting() )
