
import couchdb
from cluster_id import *
from couchdb_job_control import *
import time
import sys
import drmaa
sys.path.append( "../../../experimental-results-python-library/src/")
import experimental_results_python_library as EXL
from experimental_results_python_library.couchdb_utils import *
from experimental_results_python_library.json_utils import *


#-----------------------------------------------------------------------------

def update_job_status( couch_db, job_doc, drmaa_session,
                       max_tries=10, sleep_time=0.1):
    """Updates the status of the job form the SGE DRMAA interface if the
       job is running in this local clsuter.
       This will retyr a given number of times if there are conflicts
       in the couchdb document update.
       Between each try, some time is spent sleeping to wait for the 
       conflicting process to finish."""
    
    # ignore non local cluster jobs
    if not structure_get( "computation.cluster_id", job_doc ) == get_self_cluster_id():
        return
    
    # ignore anything that is not "submitted" status
    if not structure_get( "computation.status", job_doc ) == "submitted":
        return    

    # get the status of the job
    # get the sge_id and check it's status
    sge_id = structure_get( "computation.sge_id", job_doc )
    sge_status = None
    is_done = False
    try:
        sge_status = drmaa_session.jobStatus( str(sge_id) )
    except drmaa.errors.InvalidJobException:
        # invalid job means the job is finished or removed or otherwise
        # not alive anymore, so change status to done
        sge_status = "invalid job"
        is_done = True

    # only update the status if it has changed
    if sge_status != structure_get( "computation.sge_status", job_doc ):
        
        # ok, update ht job status
        if is_done:
            update_couchdb_document( couch_db, 
                                     job_doc,
                                     [ ("computation.sge_status", sge_status),
                                       ("computation.status", "done" )] )
        else:
            update_couchdb_document( couch_db, 
                                     job_doc,
                                     [ ("computation.sge_status", sge_status) ] )

        # print debug
        print "updating job status: " + str(structure_get( "computation.sge_id", job_doc )) + " " + structure_get( "computation.computation_id", job_doc )
        sys.stdout.flush()

        
    # return the status set
    return sge_status

#-----------------------------------------------------------------------------
