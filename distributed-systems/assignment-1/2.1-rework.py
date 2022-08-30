# ========================================================================================================
#   (02.1) overloaded Thread class, free function thread, random run time.py - 
#          Show overloaded thread class with worker thread as free function and random run time
# --------------------------------------------------------------------------------------------------------
#   adapted from code by Doug Hellman by Phil Pfeiffer
#     source:  "Python 3 Module of the Week:  threading - Manage Concurrent Operations Within a Process"
#     URL:     https://pymotw.com/3/threading/ - last accessed 13 July 2018
#   last updated:  August 2022
# =========================================================================================================

# +++++++++++++++++++++++++++++++++++++++++++++
# imports
# +++++++++++++++++++++++++++++++++++++++++++++
#
# random -
#     random.seed - initialize random library random number generators
#     random.uniform - generate random floats over a uniform distribution
# threading - 
#    threading.current_thread - identify current thread
#    threading.local - declare data item as thread-private
#    threading.Thread - instantiate a thread
# time - 
#    time.ctime - generate human readable time of day
#    time.sleep - stop thread processing for specified number of seconds
#    time.time -  return current time
#
import random
import threading
import time


# +++++++++++++++++++++++++++++++++++++++++++++
# supporting functions
# +++++++++++++++++++++++++++++++++++++++++++++
#
err_to_str = lambda err: '' if str(err) is None else ': ' + str(err)
aborting =   lambda name, err: f'?? Aborting {name} at {time.ctime()}{err_to_str(err)}'
my_name = threading.current_thread().name
sleep_time = lambda lifetime_range: random.uniform( min(lifetime_range), max(lifetime_range) )

# ----------------------------------------------
#  thread code body
# ----------------------------------------------
#
def sample_thread( lifetime_range ):
    """
    sleep for a user-specified duration
    required:
        lifetime_range - a sequence of numbers- nominally, a pair- whose min and max values denote min and max wait times
    """
    #
    # keep sleep time and thread name private to each thread
    #
    #
    try:
        print( f'Starting {my_name} at {time.ctime()} - should exit at {time.ctime(time.time() + sleep_time(lifetime_range))}' )
        time.sleep(sleep_time(lifetime_range) )
        print( f'Exiting {my_name} at {time.ctime()}' )
    except Exception as err:
        print( aborting( my_name, err ) )



# +++++++++++++++++++++++++++++++++++++++++++++
# supporting classes
# +++++++++++++++++++++++++++++++++++++++++++++
#
class MyThread(threading.Thread):
    """ invoke a caller-specified function as this thread's body  """
    def __init__(self, name=None, *, function=None):
        """
        required:      none
        optional:
            name -     name to give to a thread.  None => use Python default name
            function - name of a function to invoke when executed as an object
        """
        super().__init__(name=name, target=function)


# ===============================================
#    Program Main
# ===============================================
#
my_name = threading.current_thread().name
#
try:
    # -------------------------------------------------
    # program thread-dependent operating parameters
    # -------------------------------------------------
    #
    # threads_to_run - list of Thread_attributes objects
    #
    threads_to_run = ( 
        MyThread( name='worker', function=lambda: sample_thread( (14.0, 20.0) ) ),
        MyThread( name='worker_by_another_name', function=lambda: sample_thread( (11.0, 16.0) ) ),
        MyThread( function=lambda: sample_thread( (8.0, 13.0) ) ),
        MyThread( function=lambda: sample_thread( (5.0, 10.0) ) )
    )

    # use current time to seed random number generator, making thread sleep times quasi-nondeterministic
    #
    random.seed()

    # create and launch one thread per entry in thread matrix
    #
    print( f'{my_name} - starting' )
    for thread in threads_to_run:  thread.start()
    print( f'{my_name} - ending' )

except Exception as err:
    print( aborting(my_name, err) )
