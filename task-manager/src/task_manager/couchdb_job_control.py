import couchdb
import sge_manager
from cluster_id import *
import os
import os.path
import uuid
import datetime
import sys
sys.path.append( "../../../experimental-results-python-library/src/")
import experimental_results_python_library as EXL
from experimental_results_python_library.couchdb_utils import *
from experimental_results_python_library.json_utils import *



#-----------------------------------------------------------------------------

def process_single_change( couch_db, couchdb_json_change, last_seq_filename ):
    """Process a single change event from the couchdb jobs databse.
       This will take care of the following:
         (1) start up any new sasked for jobs on the current cluster if
             we want to job to be on the current clsuter.
         (2) stop any jobs running on hte current cluster that were 
             asked to stop
         (3) pause/resume jobs on the current clsuter when asked.
        
       The changes are to the actual job documents in the jobs databse
       and the documents themselves include all relevant information to
       perform the actual processing (such as a SGE id and clsuter id).
       We also overwrite the given file with the sequence number of the
       last change processed."""
    
    # skip "deleted" changes
    if "deleted" in couchdb_json_change:
        # overwrite file with last change procesed
        with open( last_seq_filename, 'w' ) as f:
            f.write( couchdb_json_change["seq"] )
        return
        
    # ensure that we have the document with us
    if not "doc" in couchdb_json_change:
        raise Exception( "We need to have the document included in the changesets!, change: " + str(couchdb_json_change) )
    
    # grab the document that change
    job_doc = couchdb_json_change["doc"]
    
    # check if this is a completely new document using it's revision prefix
    rev_number = revision_number_from_revision( couchdb_json_change["changes"][0]["rev"] )
    if structure_get( "computation.status", job_doc ) == "request:new":
        
        # we are a new job, so treat it as such
        process_new_job( couch_db, job_doc )
    else:
        
        # we are a job that has changed,
        # process the changes
        process_job_change( couch_db, job_doc )

    # overwrite file with last change procesed
    with open( last_seq_filename, 'w' ) as f:
        f.write( str(couchdb_json_change["seq"]) )
        
    

#-----------------------------------------------------------------------------

def process_new_job( couch_db, job_doc ):
    """Process a new job document comming into the database.
       This will fill out the fields for the SGE and will submit this
       new job to hte master quere."""
    
    
    # make sure we have a new job here
    if not structure_has( "computation.status", job_doc ) or not structure_get( "computation.status", job_doc ) == "request:new":
        raise Exception( "Unable to process new job, job document malformed or of unknown type: " + str(job_doc) )
    
    
    # check if this is for us (for our clsuter)
    # return and do nothing otherwise
    if not structure_get( "computation.cluster_id", job_doc ) == get_self_cluster_id():
        return
    
    # create a unique folder for this job
    uid = uuid.uuid1()
    unique_job_folder = os.path.abspath( os.path.join( ".", "job-local", str(uid) ) )
    os.makedirs( unique_job_folder )
    
    # get any dependencies and ensure they are all within this cluster
    dependencies = []
    for dep in structure_get( "computation.depends_on", job_doc, default=[] ):
        dep_job = couch_db.get( dep )
        if not structure_get( "computation.cluster_id", dep_job ) == get_self_cluster_id():
            raise Exception( "Cannot handle jobs with dependencies across different clusters! found inconsistency inside: " + str(job_doc) + "  Dependency " + dep + " is: " + str(dep_job) )
        
        # fetch the actual sge job id from the job
        dep_sge_id = structure_get( "computation.sge_id", dep_job)
        if dep_sge_id is None:
            raise Exception( "Cannot have dependent job without an SGE job id! job: %s, Dependency %s:" %  ( str(job_doc), str(dep), str(dep_job) ) )
        dependencies.append( dep_sge_id )

    # Ok, submit the job using SGE
    sge_jid = sge_manager.submit_task( target = structure_get( "computation.script", job_doc ),
                                       depends_on = dependencies,
                                       cwd = unique_job_folder,
                                       priority = structure_get( "computation.priority", job_doc, default="-1023" ) )
    
    # update the job document to say that it has been submited
    # with a given local folder and SGE job id
    job_id = "%s_%s_%s" % ( get_self_cluster_id(), str(sge_jid), str(uid) )
    update_couchdb_document( couch_db,
                             job_doc,
                             [ ( "computation.computation_id", job_id),
                               ( "computation.sge_id", sge_jid ),
                               ( "computation.local_directory", unique_job_folder ),
                               ( "computation.status" , "submitted" ) ],
                             max_retries = 10 )
    

#-----------------------------------------------------------------------------

def process_job_change( couch_db, job_doc):
    """Process a change in a job document. This takes care of anything not 
       a new job.  For example, this handles stopping, pausing, and resuming 
       jobs if they are running within this clsuter."""
    
    # ignore submitted status jobs, nothing to do
    if structure_get( "computation.status", job_doc ) == "submitted":
        return
    
    
    status = structure_get( "computation.status", job_doc )
    
    # nothing to do if it is not a rewuest for stop, pause, or resume
    if not ( status == "request:stop" or status == "request:pause" or status == "request:resume" ):
        return

    # ignore jobs for different clusters
    if not structure_get( "computation.cluster_id", job_doc ) == get_self_cluster_id():
        return

    # stop a job
    if status == "request:stop":
        process_stop_request( couch_db,
                              job_doc )
    else:
        
        # TODO: implement pause-request, and resume-request
        raise Exception( "Not Implemented: processing of job change: " + str(job_doc) )


#-----------------------------------------------------------------------------

def process_stop_request( couch_db, job_doc ):
    """Stops the given job and removesd it from the SGE master queye.
       This will update the status to stopped."""

    # get the sge job id and stop it
    sge_id = structure_get( "computation.sge_id", job_doc )
    sge_manager.stop_job( sge_id )
    
    # update the status to stopped
    update_couchdb_document( couch_db,
                             job_doc,
                             [( "computation.status", "stopped" ),
                              ( "computation.stop_date", str(datetime.datetime.now()))],
                             max_retries = 10)
    

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

