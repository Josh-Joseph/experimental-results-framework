
import subprocess
import re

#-----------------------------------------------------------------------------

def submit_task( target=None,
                 depends_on=None,
                 priority=-1023,
                 cwd="."):
    """Submit a task top the system to be executed.
       This call will queue the task and return with a task_id to be
       used to query and modify the task when needed.
       
       Arguments:
       target -- a path to an executable to run as teh task.
                 this path must be accessible from all of the cluster nodes
       depends_on -- a list of task_id's which must complete before starting 
                     this task. Can be None, which means no dependency
                     on any other tasks completing.  (defaults to None)
       priority -- a number btween -1023 and 1023,  Higher number is higher
                   priority.  In general, do not use non-negative numbers for
                   priority since system tasks use those.
                   
       Returns: a task_id for the submitted task.
       """
    
    # Ok, we are going to use the command line interface to
    # the sun grid engine.
    # In particular, this assumes that you have set up SGE to have the
    # commands in the path and that you ahve setup your Queues how you 
    # want them and that the default Queues are all the matter :-)

    qsub_output = ""
    if depends_on is not None:
        qsub_output = subprocess.check_output( ['qsub', '-p', str(priority), '-V', '-wd', cwd, '-hold_jid', str(depends_on), target ] );
    else:
        qsub_output = subprocess.check_output( ['qsub', '-p', priority, '-V', '-wd', cwd, target ] );
    
    # parse the result of qsub to get the jobid 
    # and use that as the task id to return
    m = re.match( "Your job (\d+).*", qsub_output )
    return int(m.group(1))
    

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

