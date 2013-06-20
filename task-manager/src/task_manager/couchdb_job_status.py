
import couchdb
from cluster_id import *
from couchdb_job_control import *
import time
import sys
import drmaa


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
    if not structure_get( "job.cluster_id", job_doc ) == get_self_cluster_id():
        return
    
    # ignore anything that is not "submitted" status
    if not structure_get( "job.status", job_doc ) == "submitted":
        return    

    # print debug
    print "updating job status: " + str(structure_get( "job.sge_id", job_doc )) + " " + structure_get( "job.job_id", job_doc )
    sys.stdout.flush()
            
    # keep trying to update it's status in event of conflicts
    num_tries = 0
    sge_status = None
    while num_tries <  max_tries:
        
        # get the sge_id and check it's status
        sge_id = structure_get( "job.sge_id", job_doc )
        try:
            sge_status = drmaa_session.jobStatus( str(sge_id) )
        except drmaa.errors.InvalidJobException:
            # invalid job means the job is finished or removed or otherwise
            # not alive anymore, so change status to done
            sge_status = "invalid job"
            structure_put( "job.status", "done", job_doc )
        structure_put( "job.sge_status", sge_status, job_doc )
        try :
            couch_db.save( job_doc )
            break
        except couchdb.ResourceConflit:
            print "  * conflict updating job document %s (%s)" % ( str(sge_id), structure_get( "job.job_id", job_doc ) )
            sys.stdout.flush()
            

        # wait some time before retry
        time.sleep( sleep_time )
        
    # return the status set
    return sge_status

#-----------------------------------------------------------------------------
